# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        
        stock_picking = self.env['stock.picking'].search([('sale_id', '=', self.id)])
        for stock in stock_picking:
            stock.write({
                "waypoint": self.waypoint.id,
                "sipping_to": self.sipping_to,
                "shipping_to_text": self.shipping_to_text,
                "forwarding_address_zip": self.forwarding_address_zip,
                "forwarding_address": self.forwarding_address,
                "shipping_destination_text": self.shipping_destination_text
            })
        return result
    
class StockPicking(models.Model):
    _inherit = "stock.picking"

    waypoint = fields.Many2one(
        comodel_name="res.partner",
        string="デポ",
        required=False,
        ondelete="set null",
    )
    sipping_to = fields.Selection([
        ('depo', 'デポ入れまで'),
        ('inst', '搬入設置まで'),
        ('inst_depo', '搬入設置（デポ入）'),
        ('direct', '直送'),
        ('container', 'オランダコンテナ出荷'),
        ('pick_up', '引取'),
        ('bring_in', '持込'),
    ], string="配送")
    sipping_to_value = fields.Char(compute="_compute_sipping_to_value")
    shipping_to_text = fields.Char(string="配送ラベル")

    forwarding_address_zip = fields.Char("納品設置先郵便番号")
    forwarding_address = fields.Text(
        string="納品設置先",
        required=False,
    )
    
    shipping_destination_text = fields.Text(
        "送り先",
    )
    
    sale_order_id = fields.Many2one('sale.order', compute="_compute_sale_order", string="Sale Order")
    shiratani_entry_date = fields.Date(string="Shiratani entry date", compute="_compute_shiratani_entry_date") 
    warehouse_arrive_date = fields.Date("Warehouse arrive date", related="sale_order_id.warehouse_arrive_date")
    estimated_shipping_date = fields.Date('Estimated shipping date', related="sale_order_id.estimated_shipping_date")
    sales_order_name = fields.Char(string='Sales Order Name', compute="_compute_sale_order_name", store=True)

    def _compute_sale_order(self):
        for picking in self:
            if picking.sale_id:
                picking.sale_order_id = picking.sale_id
            else:
                if picking.origin and picking.origin.startswith("S"):
                    sale_order = self.env['sale.order'].search([('name', '=', picking.origin)], limit=1)
                    picking.sale_order_id = sale_order
                else:
                    picking.sale_order_id = False

    @api.depends('name')
    def _compute_sale_order_name(self):
        for picking in self:
            if picking.sale_id:
                picking.sales_order_name = picking.sale_id.name
            else:
                if picking.origin and picking.origin.startswith("S"):
                    sale_order = self.env['sale.order'].search([('name', '=', picking.origin)], limit=1)
                    picking.sales_order_name = sale_order.name
                elif picking.origin:
                    origin_name = picking.origin
                    if origin_name.startswith("P"):
                        origin_name = self.env['purchase.order'].search([('name', '=', origin_name)]).origin

                    mrp = self.env['mrp.production'].search([('name', '=', origin_name)], limit=1)
                    if mrp:
                        picking.sales_order_name = mrp.sale_reference
                    else:
                        picking.sales_order_name = ''
                else:
                    picking.sales_order_name = ''

    @api.onchange('sipping_to')
    def sipping_to_text(self):
        if self.sipping_to == "depo":
            self.shipping_to_text = 'デポ入れまで'
        if self.sipping_to == "inst":
            self.shipping_to_text = '搬入設置まで'
            
    def _compute_sipping_to_value(self):
        for record in self:
            if record.sipping_to == 'depo':
                record.sipping_to_value = 'デポ入れまで'
            elif record.sipping_to == 'inst':
                record.sipping_to_value = '搬入設置まで'
            elif record.sipping_to == 'inst_depo':
                record.sipping_to_value = '搬入設置（デポ入)'
            elif record.sipping_to == 'direct':
                record.sipping_to_value = '直送'
            elif record.sipping_to == 'container':
                record.sipping_to_value = 'オランダコンテナ出荷'
            elif record.sipping_to == 'pick_up':
                record.sipping_to_value = '引取'
            elif record.sipping_to == 'bring_in':
                record.sipping_to_value = '持込'
            else:
                record.sipping_to_value = ''
    
    def _compute_shiratani_entry_date(self):
        for rec in self:
            if rec.origin and '/MO/' in rec.origin:
                mrp_production = self.env['mrp.production'].search([('name', '=', rec.origin)],limit=1)
                if mrp_production:
                    rec.shiratani_entry_date = mrp_production.shiratani_date
                else:
                    rec.shiratani_entry_date = False    
            elif rec.origin and rec.origin.startswith('S'):
                mrp_production = self.env['mrp.production'].search([('origin', '=', rec.origin)],limit=1)
                if mrp_production:
                    rec.shiratani_entry_date = mrp_production.shiratani_date
                else:
                    rec.shiratani_entry_date = False
            elif rec.origin and rec.origin.startswith('P'):
                purchase_order = self.env['purchase.order'].search([('name', '=', rec.origin)],limit=1)
                if purchase_order:
                    purchase_order_origin = purchase_order.origin
                    if purchase_order_origin and '/MO/' in purchase_order_origin:
                        mrp_production = self.env['mrp.production'].search([('name', '=', purchase_order_origin)],limit=1)
                        if mrp_production:
                            if mrp_production.shiratani_date:
                                rec.shiratani_entry_date = mrp_production.shiratani_date
                            elif mrp_production.itoshima_shipping_date_edit:
                                rec.shiratani_entry_date = mrp_production.itoshima_shipping_date_edit
                            else:
                                rec.shiratani_entry_date = False
                        else:
                            rec.shiratani_entry_date = False    
                    else:
                        rec.shiratani_entry_date = False
                else:
                    rec.shiratani_entry_date = False            
            else:
                rec.shiratani_entry_date = False        