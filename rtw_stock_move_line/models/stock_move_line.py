# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_stock_move_line(models.Model):
    _inherit = "stock.move.line"

    sai = fields.Float(compute="_get_sai", group_operator="sum", store=True)
    depo_date = fields.Date(compute="_get_sale", store=True)
    shiratani_date = fields.Date(related='move_id.sale_line_id.shiratani_date')
    date_planned = fields.Datetime(related='move_id.sale_line_id.date_planned')
    sale_id = fields.Many2one('sale.order', compute="_get_sale_id", group_operator="sum", store=True)
    customer_id = fields.Many2one(related='sale_id.partner_id', string='顧客')
    title = fields.Char(related='sale_id.title', string='案件名')
    spec = fields.Many2many(related="move_id.sale_line_id.product_id.product_template_attribute_value_ids")
    custom = fields.One2many(related="move_id.sale_line_id.config_session_id.custom_value_ids")
    # custom = fields.One2many(related="move_id.sale_line_id.config_session_id.custom_value_ids")
    overseas = fields.Boolean(related="move_id.sale_line_id.order_id.overseas", string="海外")
    factory = fields.Many2one(related="move_id.production_id.picking_type_id")
    # mrp_state = fields.Char(compute="_get_state", store=True)
    mrp_state = fields.Selection(related="move_id.state", store=True)
    memo = fields.Char(related='move_id.sale_line_id.memo')
    area = fields.Many2one(related='sale_id.waypoint.state_id', string='エリア')
    forwarding_address = fields.Text(related='sale_id.forwarding_address', string='到着地')
    # @api.depends('product_id')
    # def _get_state(self):
    #     for rec in self:
    #         if rec.move_id.state:
    #             print(rec.move_id.state)
    #             rec.mrp_state = dict(rec.move_id._fields['type'].selection).get(rec.move_id.type)
    #         else:
    #             rec.mrp_state = ""

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
