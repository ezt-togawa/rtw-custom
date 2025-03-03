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
    _inherit = "purchase.order.line"

    sale_order_ids = fields.Char("sale order", compute='_compute_sale_order')
    sale_order_names = fields.Char("sale order title", compute='_compute_sale_order')
    name_selection = fields.Many2one("product.config.session.custom.value", store=True , string='説明選択' , domain= "[('id' , 'in' , allowed_custom_config)]")
    allowed_custom_config = fields.Many2many( # THIS FIELD STORES THE APPROPRIATE CONFIG
        'product.config.session.custom.value', compute='_compute_allowed_custom_config'
    )
    
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
                
    def _get_so_from_mrp(self , mrp_production , count = 0):
        if count >= 10:
            return False
        if not mrp_production.origin:
            return False
        
        sale_order_id = False
        if '/MO/' in mrp_production.origin:
            mrp = self.env['mrp.production'].search([('name','=',mrp_production.origin)])
            if mrp:
                count += 1
                sale_order_id = self._get_so_from_mrp(mrp, count)
        else:
            sale_order_id = self.env['sale.order'].search([('name','=',mrp_production.origin)])
        return sale_order_id
                
    @api.depends('move_dest_ids.group_id.mrp_production_ids')
    def _compute_sale_order(self):
        for purchase in self:
            purchase.sale_order_ids = False
            move_dest_ids = purchase.move_dest_ids.group_id.mrp_production_ids | purchase.move_ids.move_dest_ids.group_id.mrp_production_ids
            if move_dest_ids:
                order = []
                name = []
                order_ids = []
                for rec in move_dest_ids:
                    if rec.origin:
                        sale_order = self._get_so_from_mrp(rec)
                        if sale_order and not sale_order.id in order_ids:
                            if sale_order.name:
                                order.append(sale_order.name)
                            if sale_order.title:
                                name.append(sale_order.title)
                            order_ids.append(sale_order.id)
                purchase.sale_order_ids = ','.join(order)
                purchase.sale_order_names = ','.join(name)
            else:
                purchase.sale_order_ids = purchase.sale_order_id.name
                purchase.sale_order_names = purchase.sale_order_id.title
