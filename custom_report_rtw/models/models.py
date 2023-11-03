# -*- coding: utf-8 -*-

from odoo import fields, models
import math

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    calculate_shiratani_date = fields.Char('Shiratani Date' , compute="_compute_get_sale_order")
    calculate_witness = fields.Char('Witness' , compute="_compute_get_sale_order")
    calculate_witness_phone = fields.Char('Witness Phone' , compute="_compute_get_sale_order")
    pic_name = fields.Char('PIC Name' , compute="_compute_get_sale_order")
    calculate_name = fields.Char('Name' , compute="_compute_get_sale_order")
    calculate_note = fields.Char('Note' , compute="_compute_get_sale_order")
    calculate_estimated_shipping_date = fields.Char('Estimated Shipping Date' , compute="_compute_get_sale_order")
    calculate_payment_term = fields.Char('Payment term' , compute="_compute_get_sale_order")

    def _compute_get_sale_order(self):
        sale_order = self.env['sale.order'].search([('id','=',self.sale_id.id)])
        if sale_order:
            self.calculate_shiratani_date = sale_order.shiratani_entry_date
            self.calculate_witness = sale_order.witness
            self.calculate_witness_phone = sale_order.witness_phone
            self.pic_name = sale_order.user_id.name
            self.calculate_name = sale_order.title
            self.calculate_note = sale_order.note
            self.calculate_estimated_shipping_date = sale_order.estimated_shipping_date
            self.calculate_payment_term = sale_order.payment_term_id.name
        else:
            self.calculate_shiratani_date = ''
            self.calculate_witness = ''
            self.calculate_witness_phone = ''
            self.pic_name = ''
            self.calculate_name = ''
            self.calculate_note = ''
            self.calculate_estimated_shipping_date = ''
            self.calculate_payment_term = ''

class StockMove(models.Model):
  _inherit = 'stock.move'
  calculate_packages = fields.Integer('Packages' , compute="_compute_calculate_packages")
 
  def _compute_calculate_packages(self):
    for move in self:
        if move.product_id.two_legs_scale:
            move.calculate_packages = math.ceil(move.product_uom_qty / move.product_id.two_legs_scale)
        else:
            move.calculate_packages = move.product_uom_qty

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    order_line=fields.One2many(
        "sale.order.line",
        "order_id",
        string="Sale order line",
        copy=True,
        auto_join=True,
        compute="_compute_get_sale_order_line",
    )
    sale_order=fields.One2many(
        "sale.order",
        "name",
        string="Sale order line",
        copy=True,
        auto_join=True,
        compute="_compute_get_sale_order",
    )

    def _compute_get_sale_order(self):
        sale_order = self.env['sale.order'].search([('name','=',self.origin)])
        self.sale_order=sale_order

    def _compute_get_sale_order_line(self):        
        sale_order = self.env['sale.order'].search([('name','=',self.origin)])
        order_lines = self.env["sale.order.line"].search([("order_id", "in", sale_order.ids)])
        
        self.order_line = order_lines
