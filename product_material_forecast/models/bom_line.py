# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, time
from odoo import models, fields, api


class bom_line_forecast(models.Model):
    _inherit = "mrp.bom.line"

    series = fields.Char(related='parent_product_tmpl_id.series', store=True)
    categ_id = fields.Many2one(related='parent_product_tmpl_id.categ_id', store=True)
    virtual_available = fields.Float(related='product_id.virtual_available', store=True)
    key_component = fields.Boolean(string="重要在庫", related='product_id.product_tmpl_id.key_component',store=True)
    available_quantity = fields.Float(string='利用可能な数量',compute='_compute_available_quantity')
    
    def _compute_available_quantity(self):
        for record in self:
            stock_quant = self.env['stock.quant'].search([('product_id','=',record.product_id.id),('on_hand','=',True)])
            available_quantity = 0
            for quant in stock_quant:
                available_quantity += quant.available_quantity
            record.available_quantity = available_quantity
    