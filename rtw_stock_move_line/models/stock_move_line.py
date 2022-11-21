# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_stock_move_line(models.Model):
    _inherit = "stock.move"

    sai = fields.Float(compute="_get_sai", group_operator="sum", store=True)
    depo_date = fields.Date(compute="_get_sale", group_operator="sum", store=True)
    warehouse_id = fields.Many2one(related="sale_line_id.warehouse_id")
    sale_order_no = fields.Char(compute="_get_sale_order_no", store=True)
    production_no = fields.Char(compute="_get_production_no", store=True)
    config_value_ids = fields.Many2many(related="sale_line_id.config_session_id.value_ids")
    state_id = fields.Many2one(related="sale_line_id.order_id.partner_id.state_id")
    destination = fields.Char(compute="_get_destination", store=True)
    shiratani_date = fields.Date(compute="_get_shiratani_date", store=True)
    date_planned = fields.Datetime(compute="_get_date_planned", store=True)
    delivery_confirmation = fields.Boolean(compute="_get_delivery_confirmation", store=True)
    remarks = fields.Char(compute="_get_remarks", store=True)

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

    @api.depends('product_id')
    def _get_sale_order_no(self):
        for rec in self:
            if rec.sale_line_id.order_id.name:
                rec.sale_order_no = rec.sale_line_id.order_id.name
            else:
                rec.sale_order_no = ""

    @api.depends('product_id')
    def _get_production_no(self):
        for rec in self:
            if rec.production_id.name:
                rec.production_no = rec.production_id.name
            else:
                rec.production_no = ""

    @api.depends('product_id')
    def _get_destination(self):
        for rec in self:
            if rec.sale_line_id.order_id.partner_id.city:
                rec.destination = rec.sale_line_id.order_id.partner_id.city
            else:
                rec.destination = ""
            if rec.sale_line_id.order_id.partner_id.street:
                rec.destination = rec.destination + rec.sale_line_id.order_id.partner_id.street
            if rec.sale_line_id.order_id.partner_id.street2:
                rec.destination = rec.destination + rec.sale_line_id.order_id.partner_id.street2

    @api.depends('product_id')
    def _get_shiratani_date(self):
        for rec in self:
            if rec.sale_line_id.shiratani_date:
                rec.shiratani_date = rec.sale_line_id.shiratani_date
            else:
                rec.shiratani_date = False

    @api.depends('product_id')
    def _get_date_planned(self):
        for rec in self:
            if rec.sale_line_id.date_planned:
                rec.date_planned = rec.sale_line_id.date_planned
            else:
                rec.date_planned = False

    @api.depends('product_id')
    def _get_delivery_confirmation(self):
        for rec in self:
            if rec.sale_line_id.order_id.delivery_confirmation:
                rec.delivery_confirmation = rec.sale_line_id.order_id.delivery_confirmation
            else:
                rec.delivery_confirmation = False

    @api.depends('product_id')
    def _get_remarks(self):
        for rec in self:
            if rec.sale_line_id.remarks:
                rec.remarks = rec.sale_line_id.remarks
            else:
                rec.remarks = ""

