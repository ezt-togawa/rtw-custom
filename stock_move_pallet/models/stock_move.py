# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class StockMoveLine(models.Model):
#     _inherit ='stock.move.line'

#     pallet_id = fields.Many2one('stock.move.pallet', 'パレット')

class StockMove(models.Model):
    _inherit ='stock.move'

    pallet_id = fields.Many2one('stock.move.pallet', 'パレット')
    manu_date_planned_start = fields.Datetime(string="製造開始予定日", compute="_manu_date_planned_start")
    pearl_tone_attr = fields.Char(string="パールトーン", compute="_compute_pearl_tone_attr",store=True)
    is_pearl_tone_attr = fields.Boolean()
    check_sale_id = fields.Char()
    
    @api.depends('production_id.date_planned_start')
    def _manu_date_planned_start(self):
        for rec in self:
            mrp = self.env['mrp.production'].search(
                [('origin', '=', rec.sale_id.name)], limit=1)
            if mrp:
                rec.manu_date_planned_start = mrp.date_planned_start 
            elif rec.picking_id.origin and '/MO/' in rec.picking_id.origin:
                if self.env['mrp.production'].search([('name','=',rec.picking_id.origin)]):
                    rec.manu_date_planned_start = self.env['mrp.production'].search([('name','=',rec.picking_id.origin)]).date_planned_start
                else:
                    rec.manu_date_planned_start = None
            else:
                rec.manu_date_planned_start = None
    @api.depends('product_id', 'product_id.product_template_attribute_value_ids', 'sale_id')
    def _compute_pearl_tone_attr(self):
        pearl_tone_attr_values = {}
        for line in self:
            attribute = ''
            is_pearl_tone_attr = False
            check_sale_id = ''
            if line.product_id and line.product_id.product_template_attribute_value_ids:
                for attr in line.product_id.product_template_attribute_value_ids:
                    name_att = self.env['ir.model.data'].search([('model', '=', 'product.attribute'),('res_id', '=', attr.attribute_id.id)]).name
                    value_att = self.env['ir.model.data'].search([('model', '=', 'product.attribute.value'),('res_id', '=', attr.product_attribute_value_id.id)]).name
                    if name_att and name_att.isdigit() and int(name_att) == 951 and \
                        value_att and value_att.isdigit() and int(value_att) != 951006:
                        attribute = attr.name
                        is_pearl_tone_attr = True
                        check_sale_id = line.sale_id
                        pearl_tone_attr_values[check_sale_id] = (is_pearl_tone_attr, attribute)
            if check_sale_id:
                records = self.env['stock.move'].search([('sale_id', '=', int(check_sale_id))])
                records.write({
                'is_pearl_tone_attr': is_pearl_tone_attr,
                'pearl_tone_attr': attribute
                 })
            if line.id:
                reference = self.env['stock.move'].search([('id', '=', line.id)]).reference
                if '/IN/' in reference:
                    pearl_tone_attr_stock_move = self.env['stock.move'].search([('sale_id', '=', int(line.sale_id))]).mapped('pearl_tone_attr')
                    line.is_pearl_tone_attr = True
                    if any(pearl_tone_attr_stock_move):
                        line.pearl_tone_attr = next((x for x in pearl_tone_attr_stock_move if x), False)
                    else:
                        line.pearl_tone_attr = False
                else:
                    line.is_pearl_tone_attr = pearl_tone_attr_values.get(line.sale_id, (False, ''))[0]
                    line.pearl_tone_attr = pearl_tone_attr_values.get(line.sale_id, (False, ''))[1]
                    line.check_sale_id = line.sale_id
            else:
                line.is_pearl_tone_attr = False
                line.pearl_tone_attr = ''