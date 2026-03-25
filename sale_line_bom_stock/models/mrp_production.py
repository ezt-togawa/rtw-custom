# -*- coding: utf-8 -*-
import math
from odoo import models


class MrpProductionRTW(models.Model):
    _inherit = "mrp.production"

    def _update_raw_moves(self, factor):
        self.ensure_one()
        done_qty = sum(
            self.move_finished_ids.filtered(
                lambda m: m.product_id == self.product_id and m.state == 'done'
            ).mapped('product_qty')
        )
        qty_produced = self.product_id.uom_id._compute_quantity(done_qty, self.product_uom_id)
        new_product_qty = qty_produced + factor * (self.product_qty - qty_produced)

        update_info = []
        for move in self.move_raw_ids.filtered(lambda m: m.state not in ('done', 'cancel')):
            old_qty = move.product_uom_qty
            odoo_new_qty = old_qty * factor
            bom_line = move.bom_line_id
            if bom_line:
                new_qty = self._apply_bom_line_qty_rules(bom_line, odoo_new_qty, production_qty=new_product_qty)
            
            else:
                new_qty = odoo_new_qty
            move.write({'product_uom_qty': new_qty})
            move._action_assign()
            update_info.append((move, old_qty, new_qty))
        return update_info

    def _get_move_raw_values(self, product_id, product_uom_qty, product_uom,
                             operation_id=False, bom_line=False):
        result = super()._get_move_raw_values(
            product_id, product_uom_qty, product_uom, operation_id, bom_line
        )
        if bom_line:
            new_qty = self._apply_bom_line_qty_rules(bom_line, product_uom_qty)
        
            result['product_uom_qty'] = new_qty
        return result

    def _apply_bom_line_qty_rules(self, bom_line, odoo_qty, production_qty=None):
    
        minimum_qty = bom_line.minimum_quantity or 0.0
        unit_qty = bom_line.unit_quantity or ''

        has_minimum = minimum_qty > 0
        has_unit = bool(unit_qty)

        if not has_minimum and not has_unit:
        
            return odoo_qty

        if has_unit and not has_minimum:
        
            return odoo_qty

        qty_for_calc = production_qty if production_qty is not None else self.product_qty
        if has_unit and unit_qty == '2':
            computed_qty = math.ceil(qty_for_calc / 2.0) * bom_line.product_qty
        
        elif has_unit and unit_qty == '1':
            computed_qty = qty_for_calc * bom_line.product_qty
        
        else:
            computed_qty = odoo_qty

        if computed_qty < minimum_qty:
        
            return minimum_qty

        return computed_qty

