from odoo import models, api
from odoo.tools.float_utils import float_is_zero

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.depends('move_ids.state', 'move_ids.product_uom_qty', 'move_ids.product_uom')
    def _compute_qty_received(self):
        ds_lines = self.filtered(lambda l:
            l.qty_received_method == 'stock_moves' and
            any(m.picking_id.picking_type_id.sequence_code == 'DS'
                for m in l.move_ids if m.state == 'done')
        )
        normal_lines = self - ds_lines

        super(PurchaseOrderLine, normal_lines)._compute_qty_received()

        for line in ds_lines:
            ds_moves = line.move_ids.filtered(
                lambda m: m.state == 'done'
                and m.product_id == line.product_id
                and m.picking_id.picking_type_id.sequence_code == 'DS'
            )
            if not ds_moves:
                super(PurchaseOrderLine, line)._compute_qty_received()
                continue

            first_picking = min(
                ds_moves.mapped('picking_id'),
                key=lambda p: p.date_done or p.create_date
            )
            first_moves = ds_moves.filtered(lambda m: m.picking_id == first_picking)

            total = sum(
                move.product_uom._compute_quantity(
                    move.product_uom_qty,
                    line.product_uom,
                    rounding_method='HALF-UP'
                )
                for move in first_moves
            )

            if float_is_zero(line.qty_received - total, precision_rounding=line.product_uom.rounding):
                continue

            line.with_context(tracking_disable=False).write({'qty_received': total})
