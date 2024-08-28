# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
import math

class rtw_stock_move(models.Model):
    _inherit = "stock.move"

    sai = fields.Float(compute="_get_sai", group_operator="sum", store=True)
    depo_date = fields.Date(compute="_get_sale", group_operator="sum", store=True)
    shiratani_date = fields.Date(compute="_get_shiratani_date",store=True)
    date_planned = fields.Datetime(
        related='sale_line_id.date_planned', store=True)
    sale_id = fields.Many2one(
        'sale.order', compute="_get_sale_id", group_operator="sum", store=True)
    
    customer_id = fields.Many2one(related='sale_id.partner_id', string='顧客')
    title = fields.Char(related='sale_id.title', string='案件名')
    spec = fields.Many2many(
        related="sale_line_id.product_id.product_template_attribute_value_ids")
    custom = fields.One2many(
        related="sale_line_id.config_session_id.custom_value_ids")
    # 
    overseas = fields.Boolean(
        related="sale_id.overseas", string="海外")
    factory = fields.Many2one(related="production_id.picking_type_id")
    memo = fields.Char(related='sale_line_id.memo')
    area = fields.Many2one(
        related='picking_id.waypoint.state_id', string='エリア',store=True)
    forwarding_address = fields.Text(
        related='picking_id.forwarding_address', string='到着地',store=True)
    shipping_to = fields.Selection(
        string="配送", related='picking_id.sipping_to',store=True)
    # shizai_date = fields.Date(string="資材出荷目安1", compute="_get_shizai_date")
    warehouse_arrive_date = fields.Date(
        compute="_get_warehouse_arrive_date" , store=True)
    mrp_production_id = fields.Char(
        string="製造オーダー", compute="_get_mrp_production_id", store=True)
    product_package_quantity = fields.Float(string="個口数")
    invoice_number = fields.Char(string="送り状番号")

    @api.model_create_multi
    def create(self, vals_list):
        mls = super().create(vals_list)
        for move in mls:
            if move.product_id and move.product_id.two_legs_scale:
                move.product_package_quantity = move.product_id.two_legs_scale
            else:
                move.product_package_quantity = 0
        return mls

    # @api.depends('date_planned')
    # def _get_shizai_date(self):
    #     for rec in self:
    #         if rec.date_planned:
    #             rec.shizai_date = rec.date_planned + \
    #                 datetime.timedelta(days=-20)
    #         else:
    #             rec.shizai_date = False

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

    @api.depends('sale_line_id.depo_date','sale_line_id.depo_date','sale_line_id','sale_id','sale_id.warehouse_arrive_date')
    def _get_warehouse_arrive_date(self):
        for rec in self:
            if rec.sale_line_id.depo_date:
                rec.warehouse_arrive_date = rec.sale_line_id.depo_date
            elif rec.sale_id:
                rec.warehouse_arrive_date = rec.sale_id.warehouse_arrive_date
            else:
                rec.warehouse_arrive_date = False

    @api.depends('sale_line_id', 'picking_id')
    def _get_sale_id(self):
        for rec in self:
            if rec.sale_line_id.order_id:
                rec.sale_id = rec.sale_line_id.order_id
            elif rec.picking_id:
                rec.sale_id = rec.picking_id.sale_id
            else:
                rec.sale_id = False

    @api.depends('production_id', 'picking_id')
    def _get_mrp_production_id(self):
        for rec in self:
            if rec.production_id:
                rec.mrp_production_id = rec.production_id.name
            else:
                mrp = self.env['mrp.production'].search(
                    [('origin', '=', rec.picking_id.sale_id.name), ('product_id', '=', rec.product_id.id)], limit=1)
                if mrp:
                    rec.mrp_production_id = mrp.name
                else:
                    rec.mrp_production_id = None

    @api.depends('sale_line_id.shiratani_date','sale_id','sale_id.shiratani_entry_date')
    def _get_shiratani_date(self):
        for rec in self:
            if rec.sale_line_id.shiratani_date:
                rec.shiratani_date = rec.sale_line_id.shiratani_date
            elif rec.sale_id:
                rec.shiratani_date = rec.sale_id.shiratani_entry_date
            else:
                rec.shiratani_date = False
                