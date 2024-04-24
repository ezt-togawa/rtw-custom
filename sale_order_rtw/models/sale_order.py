# -*- coding: utf-8 -*-

from odoo import models, fields, api


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
    preferred_delivery_date = fields.Date(string="Preferred delivery date", tracking=True)
    warehouse_arrive_date = fields.Date(string="Warehouse arrive date", tracking=True)
    preferred_delivery_period = fields.Char(string="Preferred delivery period")
    forwarding_address_zip = fields.Char("forwarding address zip")
    forwarding_address = fields.Text(
        string="forwarding address",
        required=False,
    )
    shiratani_entry_date = fields.Date(string="Shiratani entry Date", tracking=True)
    depo_date = fields.Date(string="Depo Date")
    customer_order_number = fields.Char('Customer Order Number')
    items_under_consideration = fields.Boolean('Items under consideration', default=0)
    waypoint = fields.Many2one(
        comodel_name="res.partner",
        string="waypoint",
        required=False,
        ondelete="set null",
    )
    sipping_to = fields.Selection([
        ('depo', 'デポ入れまで'),
        ('inst', '搬入設置まで'),
        ('inst_depo', '搬入設置（デポ入）'),
        ('direct', '直送'),
        ('container', 'オランダコンテナ出荷'),
        ('pick_up', '引取'),
        ('bring_in', '持込'),
    ], string="配送")
    shipping_to_text = fields.Char(string="配送ラベル")
    estimated_shipping_date = fields.Date('Estimated shipping date')
    overseas = fields.Boolean(string="海外")
    workdays = fields.Selection([
        ('発注後約 4週以内', '発注後約 4週以内'),
        ('発注後約 5-6週間', '発注後約 5-6週間'),
        ('発注後約 6-7週間', '発注後約 6-7週間'),
        ('発注後約 7-8週間', '発注後約 7-8週間'),
        ('発注後約 8-10週間', '発注後約 8-10週間'),
        ('発注後約 10-12週間', '発注後約 10-12週間'),
        ('発注後約 12以上', '発注後約 12以上'),
    ],string="作成日数")
    shipping_destination_text = fields.Text(string="送り先")
    #     value = fields.Integer()
    #     value2 = fields.Float(compute="_value_pc", store=True)
    #     description = fields.Text()
    #
    #     @api.depends('value')
    #     def _value_pc(self):
    #         for record in self:
    #             record.value2 = float(record.value) / 100

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
