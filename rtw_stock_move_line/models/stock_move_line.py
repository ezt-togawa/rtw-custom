# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_stock_move_line(models.Model):
    _inherit = "stock.move.line"

    sai = fields.Float(compute="_get_sai", group_operator="sum", store=True)
    depo_date = fields.Date(compute="_get_sale", store=True)
    sale_id = fields.Many2one('sale.order', compute="_get_sale_id", group_operator="sum", store=True)
    customer_id = fields.Many2one(related='sale_id.partner_id', string='顧客')
    title = fields.Char(related='sale_id.title', string='案件名')
    spec = fields.Many2many(related="move_id.sale_line_id.product_id.product_template_attribute_value_ids")
    custom = fields.One2many(related="move_id.sale_line_id.config_session_id.custom_value_ids")

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
            if rec.move_id.sale_line_id.depo_date:
                rec.depo_date = rec.move_id.sale_line_id.depo_date
            else:
                rec.depo_date = False

    @api.depends('product_id')
    def _get_sale_id(self):
        for rec in self:
            if rec.move_id.sale_line_id.order_id:
                rec.sale_id = rec.move_id.sale_line_id.order_id
            else:
                rec.sale_id = False


    # def _get_spec(self):
    #     for rec in self:
    #         if rec.move_id.sale_line_id.config_session_id
    #             for
