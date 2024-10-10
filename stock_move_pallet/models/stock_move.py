# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class StockMoveLine(models.Model):
#     _inherit ='stock.move.line'

#     pallet_id = fields.Many2one('stock.move.pallet', 'パレット')

class StockMove(models.Model):
    _inherit ='stock.move'

    pallet_id = fields.Many2one('stock.move.pallet', 'パレット')
    manu_date_planned_start = fields.Datetime(string="製造開始予定日", compute="_manu_date_planned_start")
    pearl_tone_attr = fields.Char(string="パールトーン", compute="_compute_pearl_tone_attr")
    is_pearl_tone_attr = fields.Boolean()
    
    @api.depends('production_id.date_planned_start')
    def _manu_date_planned_start(self):
        for rec in self:
            mrp = self.env['mrp.production'].search(
                [('origin', '=', rec.sale_id.name)], limit=1)
            if mrp:
                rec.manu_date_planned_start = mrp.date_planned_start 
            else:
                rec.manu_date_planned_start = None
                
    def _compute_pearl_tone_attr(self):
        for line in self:
            attribute = ''
            
            if line.product_id and line.product_id.product_template_attribute_value_ids:
                for attr in line.product_id.product_template_attribute_value_ids:
                    name_att = self.env['ir.model.data'].search([('model', '=', 'product.attribute'),('res_id', '=', attr.attribute_id.id)]).name
                    value_att = self.env['ir.model.data'].search([('model', '=', 'product.attribute.value'),('res_id', '=', attr.product_attribute_value_id.id)]).name
                    
                    if name_att and name_att.isdigit() and int(name_att) == 951 and \
                        value_att and value_att.isdigit() and int(value_att) == 951002:
                        attribute = '有'
                        line.is_pearl_tone_attr = True
                    
            line.pearl_tone_attr = attribute
    