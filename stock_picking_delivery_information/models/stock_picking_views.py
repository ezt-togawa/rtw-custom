# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime

class StockPicking(models.Model):
    _inherit = "stock.picking"

    sipping_to = fields.Char(
        "配送",
        compute="_compute_delivery_information",
    )

    shipping_to_text = fields.Char(
        "配送ラベル",
        compute="_compute_delivery_information",
    )

    waypoint = fields.Char(
        "デポ",
        compute="_compute_delivery_information",
    )

    forwarding_address_zip = fields.Char(
        "納品設置先郵便番号",
        compute="_compute_delivery_information",
    )

    forwarding_address = fields.Char(
        "納品設置先",
        compute="_compute_delivery_information",
    )
    
    shipping_destination_text = fields.Char(
        "送り先",
        compute="_compute_delivery_information",
    )
    
    sale_order_id = fields.Many2one('sale.order', compute="_compute_sale_order", string="Sale Order")
    shiratani_entry_date = fields.Date("Shiratani entry date", related="sale_order_id.shiratani_entry_date")
    warehouse_arrive_date = fields.Date("Warehouse arrive date", related="sale_order_id.warehouse_arrive_date")
    estimated_shipping_date = fields.Date('Estimated shipping date', related="sale_order_id.estimated_shipping_date")

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

    def _compute_delivery_information(self):
        for record in self:
            sale_order = self.env['sale.order'].search([('id' , '=' , record.sale_id.id)])
            if sale_order:
                record.shipping_to_text = sale_order.shipping_to_text
                record.forwarding_address_zip = sale_order.forwarding_address_zip
                record.forwarding_address = sale_order.forwarding_address
                record.shipping_destination_text = sale_order.shipping_destination_text
                if sale_order.sipping_to == 'depo':
                    record.sipping_to = 'デポ入れまで'
                    record.forwarding_address_zip = ''
                    record.forwarding_address = ''
                elif sale_order.sipping_to == 'inst':
                    record.sipping_to = '搬入設置まで'
                elif sale_order.sipping_to == 'inst_depo':
                    record.sipping_to = '搬入設置（デポ入)'
                elif sale_order.sipping_to == 'direct':
                    record.sipping_to = '直送'
                elif sale_order.sipping_to == 'container':
                    record.sipping_to = 'オランダコンテナ出荷'
                elif sale_order.sipping_to == 'pick_up':
                    record.sipping_to = '引取'
                elif sale_order.sipping_to == 'bring_in':
                    record.sipping_to = '持込'
                else:
                    record.sipping_to = ''

                if sale_order.waypoint:
                    record.waypoint = sale_order.waypoint.name
                else:
                    record.waypoint = ''
            else:
                record.shipping_to_text = ''
                record.forwarding_address_zip = ''
                record.forwarding_address = ''
                record.waypoint = ''
                record.sipping_to = ''
                record.shipping_destination_text = ''
