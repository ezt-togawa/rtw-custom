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
    shizai_date = fields.Date(string="資材出荷目安1", compute="_get_shizai_date")
    warehouse_arrive_date = fields.Date(
        compute="_get_warehouse_arrive_date" , store=True)
    mrp_production_id = fields.Char(
        string="製造オーダー", compute="_get_mrp_production_id", store=True)
    product_package_quantity = fields.Integer(string="個口数")
    invoice_number = fields.Char(string="送り状番号")
    manu_date_planned_start = fields.Datetime(string="製造開始予定日", compute="_get_mrp_production_id", store=True)
    pearl_tone_attr = fields.Char(string="パールトーン", compute="_compute_pearl_tone_attr")
    is_pearl_tone_attr = fields.Boolean()

    @api.model_create_multi
    def create(self, vals_list):
        mls = super().create(vals_list)
        for move in mls:
            if move.product_id.product_tmpl_id.two_legs_scale > 0:
                move.product_package_quantity = math.ceil(move.product_qty /move.product_id.product_tmpl_id.two_legs_scale)
            else:
                move.product_package_quantity = 0
        return mls

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
                    rec.manu_date_planned_start = mrp.date_planned_start or None
                else:
                    rec.mrp_production_id = None
                    rec.manu_date_planned_start = None

    @api.depends('sale_line_id.shiratani_date','sale_id','sale_id.shiratani_entry_date')
    def _get_shiratani_date(self):
        for rec in self:
            if rec.sale_line_id.shiratani_date:
                rec.shiratani_date = rec.sale_line_id.shiratani_date
            elif rec.sale_id:
                rec.shiratani_date = rec.sale_id.shiratani_entry_date
            else:
                rec.shiratani_date = False
                    
    def _compute_pearl_tone_attr(self):
        for line in self:
            attribute = ''
            
            if line.product_id and line.product_id.product_template_attribute_value_ids:
                for attr in line.product_id.product_template_attribute_value_ids:
                    name_att = self.env['ir.model.data'].search([('model', '=', 'product.attribute'),('res_id', '=', attr.attribute_id.id)]).name
                    value_att = self.env['ir.model.data'].search([('model', '=', 'product.attribute.value'),('res_id', '=', attr.product_attribute_value_id.id)]).name
                    
                    if name_att and name_att.isdigit() and int(name_att) == 951 and \
                        value_att and value_att.isdigit() and int(value_att) == 951002:
                        attribute = '有'
                        line.is_pearl_tone_attr = True
                    
            line.pearl_tone_attr = attribute
            