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

    def _compute_delivery_information(self):
        for record in self:
            sale_order = self.env['sale.order'].search([('id' , '=' , record.sale_id.id)])
            if sale_order:
                record.shipping_to_text = sale_order.shipping_to_text
                record.forwarding_address_zip = sale_order.forwarding_address_zip
                record.forwarding_address = sale_order.forwarding_address
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
