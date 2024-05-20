# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductConfigSessionCustomValue(models.Model):
    _inherit = "product.config.session.custom.value"

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.attribute_id.name} : {record.value}"
            result.append((record.id, name))
        return result
class rtw_purchase(models.Model):
    _inherit = "purchase.order"

    sale_order_ids = fields.Char("sale order", compute='_compute_sale_order')
    sale_order_names = fields.Char("sale order title")
    operation_type = fields.Many2one('stock.picking.type' , string="オペレーションタイプ", compute='_compute_operation_type')
    destination_note = fields.Text('送り先注記')
    name_selection = fields.Many2one("product.config.session.custom.value", store=True , string='説明選択' , domain= "[('id' , 'in' , allowed_custom_config)]")
    allowed_custom_config = fields.Many2many( # THIS FIELD STORES THE APPROPRIATE CONFIG
        'product.config.session.custom.value', compute='_compute_allowed_custom_config'
    )

    def _compute_operation_type(self):
            operation_type_value = self.order_line.move_dest_ids.group_id.mrp_production_ids | self.order_line.move_ids.move_dest_ids.group_id.mrp_production_ids
            if operation_type_value:
                self.operation_type = operation_type_value[0].picking_type_id
            else:
                self.operation_type = False

    # @api.model
    def action_purchase_form(self):
        self.ensure_one()
        action = self.env.ref("purchase.purchase_form_action")
        form = self.env.ref("purchase.purchase_order_form")
        action = action.read()[0]
        action["views"] = [(form.id, "form")]
        action["target"] = "new"
        action["res_id"] = self.id
        return action

    @api.depends('order_line.move_dest_ids.group_id.mrp_production_ids')
    def _compute_sale_order(self):
        for purchase in self:
            purchase.sale_order_ids = False
            move_dest_ids = purchase.order_line.move_dest_ids.group_id.mrp_production_ids | purchase.order_line.move_ids.move_dest_ids.group_id.mrp_production_ids
            move_ids = purchase.order_line.move_ids.move_dest_ids.group_id.mrp_production_ids
            if move_dest_ids:
                order = []
                name = []
                for rec in move_dest_ids:
                    if rec.origin:
                        order.append(rec.origin)
                    if self.env['sale.order'].search([('name', '=', rec.origin)]).title:
                        name.append(self.env['sale.order'].search([('name', '=', rec.origin)]).title)
                    purchase.sale_order_ids = ','.join(order)
                    purchase.sale_order_names = ','.join(name)
            else:
                purchase.sale_order_ids = False
                purchase.sale_order_names = False
                # sale_order = self.env['sale.order'].search([('name', '=', move_dest_ids)])
                # print(sale_order)
            # move_dest_ids.write({
            #     'name': self.invoice_id.name,
            #     'warranty_request_ids': [(4, self.id, {
            #     })]
            #     })
            
    @api.onchange('name_selection')
    def _onchange_name_selection(self):
        for record in self:
            if record.name_selection:
                record.name = f"{record.name_selection.attribute_id.name} : {record.name_selection.value}"
                record.name_selection = False
    
    @api.depends('move_dest_ids.group_id.mrp_production_ids')
    def _compute_allowed_custom_config(self):
        for purchase in self:
            sale_order_line = False
            search_criteria= []
            move_dest_ids = purchase.move_dest_ids.group_id.mrp_production_ids | purchase.move_ids.move_dest_ids.group_id.mrp_production_ids
            if move_dest_ids:
                search_criteria = [  # limit 10 times
                    ('move_ids', 'in', [move_id.id for move_id in move_dest_ids[0].move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in move_dest_ids[0].move_dest_ids.move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in move_dest_ids[0].move_dest_ids.move_dest_ids.move_dest_ids]),
                    ('move_ids', 'in',
                     [move_id.id for move_id in move_dest_ids[0].move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in
                                        move_dest_ids[0].move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in
                                        move_dest_ids[0].move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in
                                        move_dest_ids[0].move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in
                                        move_dest_ids[0].move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in
                                        move_dest_ids[0].move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in
                                        move_dest_ids[0].move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                ]
            for search in search_criteria:  # find sale_order_line
                if self.env['sale.order.line'].search([search]):
                    sale_order_line = self.env['sale.order.line'].search([search])
                    break
            if sale_order_line and sale_order_line.config_session_id.custom_value_ids:
                purchase.allowed_custom_config = sale_order_line.config_session_id.custom_value_ids
            else:
                purchase.allowed_custom_config = False