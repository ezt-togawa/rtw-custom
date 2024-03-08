# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class rtw_stock_move_line(models.Model):
    _inherit = "stock.move.line"

    sai = fields.Float(compute="_get_sai", group_operator="sum", store=True)
    depo_date = fields.Date(compute="_get_sale", store=True)
    shiratani_date = fields.Date(compute="_get_shiratani_date")
    date_planned = fields.Datetime(
        related='move_id.sale_line_id.date_planned', store=True)
    sale_id = fields.Many2one(
        'sale.order', compute="_get_sale_id", group_operator="sum", store=True)
    customer_id = fields.Many2one(related='sale_id.partner_id', string='顧客')
    title = fields.Char(related='sale_id.title', string='案件名')
    spec = fields.Many2many(
        related="move_id.sale_line_id.product_id.product_template_attribute_value_ids")
    custom = fields.One2many(
        related="move_id.sale_line_id.config_session_id.custom_value_ids")
    # custom = fields.One2many(related="move_id.sale_line_id.config_session_id.custom_value_ids")
    overseas = fields.Boolean(
        related="move_id.sale_line_id.order_id.overseas", string="海外")
    factory = fields.Many2one(related="move_id.production_id.picking_type_id")
    # mrp_state = fields.Char(compute="_get_state", store=True)
    mrp_state = fields.Selection(related="move_id.state", store=True)
    memo = fields.Char(related='move_id.sale_line_id.memo')
    area = fields.Many2one(
        related='sale_id.waypoint.state_id', string='エリア', store=True)
    forwarding_address = fields.Text(
        related='sale_id.forwarding_address', string='到着地' , store=True)
    shipping_to = fields.Selection(
        string="配送", related='sale_id.sipping_to', store=True)
    shizai_date = fields.Date(string="資材出荷目安", compute="_get_shizai_date")
    warehouse_arrive_date = fields.Date(
        compute="_get_warehouse_arrive_date")
    mrp_production_id = fields.Char(
        string="製造オーダー", compute="_get_mrp_production_id", store=True)
    # @api.depends('product_id')
    # def _get_state(self):
    #     for rec in self:
    #         if rec.move_id.state:
    #             print(rec.move_id.state)
    #             rec.mrp_state = dict(rec.move_id._fields['type'].selection).get(rec.move_id.type)
    #         else:
    #             rec.mrp_state = ""

    @api.depends('date_planned')
    def _get_shizai_date(self):
        for rec in self:
            if rec.date_planned:
                rec.shizai_date = rec.date_planned + \
                    datetime.timedelta(days=-20)
            else:
                rec.shizai_date = False

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

    @api.depends('move_id','sale_id')
    def _get_warehouse_arrive_date(self):
        for rec in self:
            if rec.move_id.sale_line_id.depo_date:
                rec.warehouse_arrive_date = rec.move_id.sale_line_id.depo_date
            elif rec.sale_id:
                rec.warehouse_arrive_date = rec.sale_id.warehouse_arrive_date
            else:
                rec.warehouse_arrive_date = False

    @api.depends('move_id', 'picking_id')
    def _get_sale_id(self):
        for rec in self:
            if rec.move_id.sale_line_id.order_id:
                rec.sale_id = rec.move_id.sale_line_id.order_id
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

    @api.depends('product_id')
    def _get_shiratani_date(self):
        for rec in self:
            if rec.move_id.sale_line_id.shiratani_date:
                rec.shiratani_date = rec.move_id.sale_line_id.shiratani_date
            elif rec.sale_id:
                rec.shiratani_date = rec.sale_id.shiratani_entry_date
            else:
                rec.shiratani_date = False

    # def _get_spec(self):
    #     for rec in self:
    #         if rec.move_id.sale_line_id.config_session_id
    #             for
