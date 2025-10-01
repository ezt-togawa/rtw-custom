# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        # Odooの連絡先=会社の場合、アドレスの種類がブランクの場合あり
        # その場合、Odooは子連絡先で「連絡先」指定しているデータを請求先としてしまう
        # 請求先のアドレスの種類が請求ではない場合は、親（関連会社）があれば親を。親がなければ、顧客（自分自身）を明示的に請求先に指定
        if self.partner_invoice_id and self.partner_invoice_id.type != 'invoice':
            if self.partner_id.parent_id:
                self.partner_invoice_id = self.partner_id.parent_id
            elif not self.partner_id.parent_id:
                self.partner_invoice_id = self.partner_id
            else:
                pass

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if {'waypoint', 'waypoint_2', 'sipping_to', 'shipping_to_text', 'forwarding_address_zip', 'forwarding_address', 'shipping_destination_text'}.intersection(vals):
            # 上記のいずれかのフィールドが更新された場合
            for record in self:
                record.update_stock_picking_info()
        return res

    def update_stock_picking_info(self):
        self.ensure_one()
        stock_picking = self.env['stock.picking'].search([
            ('sale_order_id', '=', self.id),
            ('state', 'not in', ['done', 'cancel'])
        ])
        if stock_picking:
            stock_picking.write({
                "waypoint": self.waypoint,
                "waypoint_2": self.waypoint_2,
                "sipping_to": self.sipping_to,
                "shipping_to_text": self.shipping_to_text,
                "forwarding_address_zip": self.forwarding_address_zip,
                "forwarding_address": self.forwarding_address,
                "shipping_destination_text": self.shipping_destination_text
            })

class StockPicking(models.Model):
    _inherit = "stock.picking"

    waypoint = fields.Many2one(
        comodel_name="res.partner",
        string="デポ１",
        required=False,
        ondelete="set null",
    )
    waypoint_2 = fields.Many2one(
        comodel_name="res.partner",
        string="デポ２",
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
    sales_order_name = fields.Char(string='Sales Order Name', compute="_compute_sale_order_name", store=True)
    shiratani_entry_date = fields.Date("Shiratani entry date", compute='compute_shiretani_entry_date')
    itoshima_shiratani_shipping_notes = fields.Text(string="糸島/白谷配送注記",compute="_compute_itoshima_shiratani_shipping_notes")
    estimated_shipping_date = fields.Date('Estimated shipping date', compute='_compute_date_info')
    warehouse_arrive_date = fields.Date("Warehouse arrive date", compute='_compute_date_info')
    warehouse_arrive_date_2 = fields.Date("Warehouse arrive date", compute='_compute_date_info')

    def _compute_date_info(self):
        for picking in self:
            sale_order = self.env['sale.order'].search([('name', '=', picking.sales_order_name)], limit=1)
            if sale_order:
                picking.estimated_shipping_date = sale_order.estimated_shipping_date
                picking.warehouse_arrive_date = sale_order.warehouse_arrive_date
                picking.warehouse_arrive_date_2 = sale_order.warehouse_arrive_date_2
            else:
                picking.estimated_shipping_date = ''
                picking.warehouse_arrive_date = ''
                picking.warehouse_arrive_date_2 = ''

    def _compute_itoshima_shiratani_shipping_notes(self):
        for picking in self:
            sale_order = self.env['sale.order'].search([('name', '=', picking.sales_order_name)], limit=1)
            if sale_order:
                picking.itoshima_shiratani_shipping_notes = sale_order.itoshima_shiratani_shipping_notes
            else:
                picking.itoshima_shiratani_shipping_notes = ''
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

    def compute_shiretani_entry_date(self):
        for rec in self:
            if rec.id :
                stock_move = self.env['stock.move'].search([('picking_id', '=', rec.id)], limit=1)
                if stock_move:
                    rec.shiratani_entry_date = stock_move.shiratani_date
                else:
                    rec.shiratani_entry_date = False

                