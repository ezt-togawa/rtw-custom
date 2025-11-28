# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from babel.dates import format_date as babel_format_date
from odoo.tools import format_date
from datetime import datetime
AVAILABLE_PRIORITIES = [
    ('0', 'Low'),
    ('1', 'Normal'),
    ('2', 'High'),
    ('3', 'Very High')
]

class sale_order_rtw(models.Model):
    _inherit = "sale.order"
    _description = 'sale_order_rtw.sale_order_rtw'
    title = fields.Char('title')
    status = fields.Selection([
        ('draft', 'draft'),
        ('done', 'done'),
    ],
        string="status", default='draft', store=True)
    process = fields.Selection([
        ('draft', 'draft'),
        ('manufactured', 'manufactured'),
        ('delivered', 'delivered'),
    ],
        string="process", default='draft')
    date_deadline = fields.Date(string="Date deadline", tracking=True)
    payment_deadline = fields.Date(string="Payment deadline", tracking=True)
    preferred_delivery_date = fields.Date(string="Preferred delivery date", tracking=True)
    time_text = fields.Char(string="Time")
    warehouse_arrive_date = fields.Date(string="デポ１到着日", tracking=True)
    warehouse_arrive_date_2 = fields.Date(string="デポ２到着日", tracking=True)
    preferred_delivery_period = fields.Char(string="Preferred delivery period")
    forwarding_address_zip = fields.Char("forwarding address zip")
    forwarding_address = fields.Text(
        string="forwarding address",
        required=False,
    )
    shiratani_entry_date = fields.Date(string="Shiratani entry Date", tracking=True)
    mo_shiratani_entry_date = fields.Char(string="Mo Shiratani Entry Date ", compute='_compute_mo_shiratani_entry_date')
    mo_warehouse_arrive_date = fields.Char(string="Mo Warehouse Arrive Date ", compute='_compute_mo_warehouse_arrive_date')
    mo_warehouse_arrive_date_2 = fields.Char(string="Mo Warehouse Arrive Date 2", compute='_compute_mo_warehouse_arrive_date_2')
    depo_date = fields.Date(string="Depo Date")
    customer_order_number = fields.Char('Customer Order Number')
    items_under_consideration = fields.Boolean('Items under consideration', default=0)
    waypoint = fields.Many2one(
        comodel_name="res.partner",
        string="デポ１",
        required=False,
        ondelete="set null",
    )
    waypoint_2 = fields.Many2one(
        comodel_name="res.partner",
        string="waypoint_2",
        required=False,
        ondelete="set null",
    )
    sipping_to = fields.Selection([
        ('depo', 'デポ入れまで'),
        ('inst', '搬入設置まで'),
        ('direct', '直送（個人邸）'),
        ('container', 'オランダコンテナ出荷（海外）'),
        ('pick_up', '引取（海外）'),
        ('bring_in', '持込（海外）'),
    ], string="配送")
    shipping_to_text = fields.Char(string="配送ラベル")
    estimated_shipping_date = fields.Date('Estimated shipping date')
    overseas = fields.Boolean(string="海外")
    workday_id = fields.Many2one(comodel_name='sale.order.work.day',string="作成日数")
    # workdays = fields.Selection([
    #     ('発注後約 4週以内', '発注後約 4週以内'),
    #     ('発注後約 5-6週間', '発注後約 5-6週間'),
    #     ('発注後約 6-7週間', '発注後約 6-7週間'),
    #     ('発注後約 7-8週間', '発注後約 7-8週間'),
    #     ('発注後約 8-10週間', '発注後約 8-10週間'),
    #     ('発注後約 10-12週間', '発注後約 10-12週間'),
    #     ('発注後約 12以上', '発注後約 12以上'),
    # ],string="作成日数")
    shipping_destination_text = fields.Text(string="送り先")
    #     value = fields.Integer()
    #     value2 = fields.Float(compute="_value_pc", store=True)
    #     description = fields.Text()
    #
    #     @api.depends('value')
    #     def _value_pc(self):
    #         for record in self:
    #             record.value2 = float(record.value) / 100
    transactions = fields.Many2one('res.partner.transactions',string="Transactions" , compute="_compute_transactions")
    transaction_condition_1 = fields.Text(string="Transaction Terms 1" , compute="_compute_transaction_condition_1")
    transaction_condition_2 = fields.Text(string="Transaction Terms 2" , compute="_compute_transaction_condition_2")
    payment_terms = fields.Selection(AVAILABLE_PRIORITIES, string="取引レベル", compute="_compute_payment_terms")


    days_remaining = fields.Integer(string='Days Remaining', compute='_compute_days_remaining')

    @api.depends('estimated_shipping_date')
    def _compute_days_remaining(self):
        today = datetime.today().date()
        for record in self:
            if record.estimated_shipping_date:
                days_remaining = (record.estimated_shipping_date - today).days
                record.days_remaining = days_remaining
            else:
                record.days_remaining = 999
    
    def _compute_mo_shiratani_entry_date(self):
        for record in self:
            if record.shiratani_entry_date:
                date_to_format = fields.Date.from_string(record.shiratani_entry_date)
                user_lang = self.env.user.lang
                formatted_date = format_date(self.env, date_to_format, lang_code=user_lang)
                day_of_week = babel_format_date(date_to_format, "EEE", locale=user_lang)
                record.mo_shiratani_entry_date = f"{formatted_date} [{day_of_week}]"
            else:
                record.mo_shiratani_entry_date = ''
                
    def _compute_mo_warehouse_arrive_date(self):
        for record in self:
            if record.warehouse_arrive_date:
                date_to_format = fields.Date.from_string(record.warehouse_arrive_date)
                user_lang = self.env.user.lang
                formatted_date = format_date(self.env, date_to_format, lang_code=user_lang)
                day_of_week = babel_format_date(date_to_format, "EEE", locale=user_lang)
                record.mo_warehouse_arrive_date = f"{formatted_date} [{day_of_week}]"
            else:
                record.mo_warehouse_arrive_date = ''
            
    def _compute_mo_warehouse_arrive_date_2(self):
        for record in self:
            if record.warehouse_arrive_date_2:
                date_to_format = fields.Date.from_string(record.warehouse_arrive_date_2)
                user_lang = self.env.user.lang
                formatted_date = format_date(self.env, date_to_format, lang_code=user_lang)
                day_of_week = babel_format_date(date_to_format, "EEE", locale=user_lang)
                record.mo_warehouse_arrive_date_2 = f"{formatted_date} [{day_of_week}]"
            else:
                record.mo_warehouse_arrive_date_2 = ''
    

    def toggle_under_consideration(self):
        for record in self:
            record.items_under_consideration = not record.items_under_consideration

    def accepting_order(self):
        self.status = "done"

    def back_to_draft(self):
        self.status = "draft"

    @api.onchange('sipping_to')
    def sipping_to_text(self):
        if self.sipping_to == "depo":
            self.shipping_to_text = 'デポ入れまで'
        if self.sipping_to == "inst":
            self.shipping_to_text = '搬入設置まで'
    
    @api.onchange('shiratani_entry_date')
    def update_order_lines_shiratani_date(self):
        for order in self:
            order.order_line.update({
                'shiratani_date': order.shiratani_entry_date
            })

    @api.onchange('warehouse_arrive_date')
    def update_order_lines_depo_date(self):
        for order in self:
            order.order_line.update({
                'depo_date': order.warehouse_arrive_date
            })

    @api.onchange('estimated_shipping_date')
    def update_commitment_date(self):
        for record in self:
            record.commitment_date = self.estimated_shipping_date

    def action_confirm(self):
        res = super(sale_order_rtw, self).action_confirm()
        self.state = 'sale'
        return res

    def create(self, vals):
        # 複製した場合に配送日がブランクになるのを回避する、発送予定日と連動させる
        if vals.get('estimated_shipping_date', False) and not vals.get('commitment_date', False):
            vals['commitment_date'] = vals.get('estimated_shipping_date')

        res = super(sale_order_rtw, self).create(vals)
        return res

    def _compute_transactions(self):
        for so in self:           
            if so.partner_invoice_id:
                partner= self.env['res.partner'].search([('id','=',so.partner_invoice_id.id)])
                for p in partner:
                    if p.transactions:
                        so.transactions = p.transactions
                    else:
                        so.transactions = None
            else:
                so.transactions = None

    def _compute_transaction_condition_1(self):
        for so in self:           
            if so.partner_invoice_id:
                partner= self.env['res.partner'].search([('id','=',so.partner_invoice_id.id)])
                for p in partner:
                    if p.payment_terms_1:
                        so.transaction_condition_1 = p.payment_terms_1
                    else:
                        so.transaction_condition_1 = None
            else:
                so.transaction_condition_1 = None

    def _compute_transaction_condition_2(self):
        for so in self:           
            if so.partner_invoice_id:
                partner= self.env['res.partner'].search([('id','=',so.partner_invoice_id.id)])
                for p in partner:
                    if p.payment_terms_2:
                        so.transaction_condition_2 = p.payment_terms_2
                    else:
                        so.transaction_condition_2 = None
            else:
                so.transaction_condition_2 = None
    @api.depends('partner_invoice_id')
    def _compute_payment_terms(self):
        for so in self:           
            if so.partner_invoice_id:
                partner= self.env['res.partner'].search([('id','=',so.partner_invoice_id.id)])
                for p in partner:
                    if p.accounting_supplement_3:
                        so.payment_terms = p.accounting_supplement_3
                    else:
                        so.payment_terms = None
            else:
                so.payment_terms = None

class mrp_order_rtw(models.Model):
    _inherit = "mrp.production"
    

    mo_estimated_shipping_date = fields.Char(string="Estimated Shipping Date", compute='_compute_mo_estimated_shipping_date')
    mo_shiratani_date = fields.Char(string="Shiratani Date", compute='_compute_mo_shiratani_date')
    

    def _compute_mo_estimated_shipping_date(self):
        for record in self:
            if record.estimated_shipping_date:
                date_to_format = fields.Date.from_string(record.estimated_shipping_date)
                user_lang = self.env.user.lang
                formatted_date = format_date(self.env, date_to_format, lang_code=user_lang)
                day_of_week = babel_format_date(date_to_format, "EEE", locale=user_lang)
                record.mo_estimated_shipping_date = f"{formatted_date} [{day_of_week}]"
            else:
                record.mo_estimated_shipping_date = ''


    def _compute_mo_shiratani_date(self):
        for record in self:
            if record.shiratani_date:
                date_to_format = fields.Date.from_string(record.shiratani_date)
                user_lang = self.env.user.lang
                formatted_date = format_date(self.env, date_to_format, lang_code=user_lang)
                day_of_week = babel_format_date(date_to_format, "EEE", locale=user_lang)
                record.mo_shiratani_date = f"{formatted_date} [{day_of_week}]"
            else:
                record.mo_shiratani_date = ''
    
    