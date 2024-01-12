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

    def _prepare_add_missing_fields(self, values):
        res = super(sale_order_line_custom_date,
                    self)._prepare_add_missing_fields(values)
        sale_order = self.env['sale.order'].search(
            [('id', '=', values['order_id'])])
        if sale_order:
            res['shiratani_date'] = sale_order.shiratani_entry_date
            res['depo_date'] = sale_order.warehouse_arrive_date
        return res
