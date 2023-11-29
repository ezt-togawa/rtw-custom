# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_order_line_custom_date(models.Model):
    _inherit = "sale.order.line"

    depo_date = fields.Date("Depo Date", tracking=True)
    shiratani_date = fields.Date("Shiratani Date", tracking=True)
    p_type = fields.Selection([
        ('special', '別注'),
        ('custom', '特注'),
    ],string = "製品タイプ")

    @api.onchange('product_id')
    def date_default(self):
        for l in self:
            if l.order_id.shiratani_entry_date :
                l.shiratani_date=l.order_id.shiratani_entry_date
            else:
                l.shiratani_date=False

            if l.order_id.warehouse_arrive_date :
                l.depo_date=l.order_id.warehouse_arrive_date
            else:
                l.depo_date=False
