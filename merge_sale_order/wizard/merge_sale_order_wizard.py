# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class MergesaleOrder(models.TransientModel):
    _name = 'merge.sale.order'
    _description = 'Merge sale Order'
    merge_type = \
        fields.Selection([
            ('new_cancel',
                'Create new order and cancel all selected sale orders'),
            ('new_delete',
             'Create new order and delete all selected sale orders'),
            ('merge_cancel',
             'Merge order on existing selected order and cancel others'),
            ('merge_delete',
                'Merge order on existing selected order and delete others')],
            default='new_cancel')
    sale_order_id = fields.Many2one('sale.order', 'Sale Order')

    @api.onchange('merge_type')
    def onchange_merge_type(self):
        res = {}
        for order in self:
            order.sale_order_id = False
            if order.merge_type in ['merge_cancel', 'merge_delete']:
                sale_orders = self.env['sale.order'].browse(
                    self._context.get('active_ids', []))
                res['domain'] = {
                    'sale_order_id':
                    [('id', 'in',
                        [sale.id for sale in sale_orders])]
                }
            return res

    def merge_orders(self):
        sale_orders = self.env['sale.order'].browse(
            self._context.get('active_ids', []))
        existing_po_line = False
        if len(self._context.get('active_ids', [])) < 2:
            raise UserError(
                _('Please select atleast two sale orders to perform '
                    'the Merge Operation.'))
        if any(order.state != 'draft' for order in sale_orders):
            raise UserError(
                _('Please select sale orders which are in RFQ state '
                  'to perform the Merge Operation.'))
        partner = sale_orders[0].partner_id.id
        opportunity = sale_orders[0].opportunity_id.id
        if any(order.partner_id.id != partner for order in sale_orders):
            raise UserError(
                _('Please select sale orders whose Vendors are same to '
                    ' perform the Merge Operation.'))
        if self.merge_type == 'new_cancel':
            po = self.env['sale.order'].with_context({
                'trigger_onchange': True,
                'onchange_fields_to_trigger': [partner]
            }).create({'partner_id': partner, 'opportunity_id': opportunity})
            default = {'order_id': po.id}
            for order in sale_orders:
                for line in order.order_line:
                    existing_po_line = False
                    if po.order_line:
                        for poline in po.order_line:
                            if line.product_id == poline.product_id and\
                                    line.price_unit == poline.price_unit:
                                existing_po_line = poline
                                break
                    if existing_po_line:
                        existing_po_line.product_uom_qty += line.product_uom_qty
                        po_taxes = [
                            tax.id for tax in existing_po_line.tax_id]
                        [po_taxes.append((tax.id))
                         for tax in line.tax_id]
                        existing_po_line.tax_id = \
                            [(6, 0, po_taxes)]
                    else:
                        line.copy(default=default)
            for order in sale_orders:
                order.action_cancel()
        elif self.merge_type == 'new_delete':
            po = self.env['sale.order'].with_context({
                'trigger_onchange': True,
                'onchange_fields_to_trigger': [partner]
            }).create({'partner_id': partner, 'opportunity_id': opportunity})
            default = {'order_id': po.id}
            for order in sale_orders:
                for line in order.order_line:
                    existing_po_line = False
                    if po.order_line:
                        for po_line in po.order_line:
                            if line.product_id == po_line.product_id and \
                                    line.price_unit == po_line.price_unit:
                                existing_po_line = po_line
                                break
                    if existing_po_line:
                        existing_po_line.product_uom_qty += line.product_uom_qty
                        po_taxes = [
                            tax.id for tax in existing_po_line.taxes_id]
                        [po_taxes.append((tax.id))
                         for tax in line.taxes_id]
                        existing_po_line.taxes_id = \
                            [(6, 0, po_taxes)]
                    else:
                        line.copy(default=default)
            for order in sale_orders:
                order.sudo().button_cancel()
                order.sudo().unlink()
        elif self.merge_type == 'merge_cancel':
            default = {'order_id': self.sale_order_id.id}
            po = self.sale_order_id
            for order in sale_orders:
                if order == po:
                    continue
                for line in order.order_line:
                    existing_po_line = False
                    if po.order_line:
                        for po_line in po.order_line:
                            if line.product_id == po_line.product_id and \
                                    line.price_unit == po_line.price_unit:
                                existing_po_line = po_line
                                break
                    if existing_po_line:
                        existing_po_line.product_uom_qty += line.product_uom_qty
                        po_taxes = [
                            tax.id for tax in existing_po_line.taxes_id]
                        [po_taxes.append((tax.id))
                         for tax in line.taxes_id]
                        existing_po_line.taxes_id = \
                            [(6, 0, po_taxes)]
                    else:
                        line.copy(default=default)
            for order in sale_orders:
                if order != po:
                    order.sudo().action_cancel()
        else:
            default = {'order_id': self.sale_order_id.id}
            po = self.sale_order_id
            for order in sale_orders:
                if order == po:
                    continue
                for line in order.order_line:
                    existing_po_line = False
                    if po.order_line:
                        for po_line in po.order_line:
                            if line.product_id == po_line.product_id and \
                                    line.price_unit == po_line.price_unit:
                                existing_po_line = po_line
                                break
                    if existing_po_line:
                        existing_po_line.product_uom_qty += line.product_uom_qty
                        po_taxes = [
                            tax.id for tax in existing_po_line.taxes_id]
                        [po_taxes.append((tax.id))
                         for tax in line.taxes_id]
                        existing_po_line.taxes_id = \
                            [(6, 0, po_taxes)]
                    else:
                        line.copy(default=default)
            for order in sale_orders:
                if order != po:
                    order.sudo().action_cancel()
                    order.sudo().unlink()
