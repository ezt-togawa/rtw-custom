# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_stock_move_line(models.Model):
    _inherit = "stock.move"

    sai = fields.Float(compute="_get_sai", group_operator="sum", store=True)
    depo_date = fields.Date(compute="_get_sale", group_operator="sum", store=True)

    @api.depends('product_id')
    def _get_sai(self):
        for rec in self:
            if rec.product_id.sai:
                rec.sai = rec.product_id.sai
            else:
                rec.sai = 0

    @api.depends('product_id')
    def _get_sale(self):
        for rec in self:
            if rec.sale_line_id.depo_date:
                rec.depo_date = rec.sale_line_id.depo_date
            else:
                rec.depo_date = False