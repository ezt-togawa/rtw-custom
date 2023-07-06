# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class sale_order_approve(models.Model):
    _inherit = "sale.order"

    approve_status = fields.Boolean('Approve', default=0)
    is_over_price = fields.Boolean('Is Over Price' , compute='_compute_is_over_price', store=True)
    is_hide_button = fields.Boolean('Is Hide Button' , compute='_compute_is_hide_button' , store=True)
    approve_button = fields.Char('Approve Button' , compute='_compute_approve_button' , store=True)

    def toggle_approve_btn(self):
        admin_sale_id = self.env.ref('sales_team.group_sale_manager')
        for record in self:
            user_group_id = record.user_id.groups_id
            if  admin_sale_id in user_group_id:
                record.approve_status = not record.approve_status
            else:
                raise UserError('販売の管理者のみ承認の実行ができます。')

    @api.onchange('amount_total')
    def _onchange_amount_total(self):
        for record in self:
            sale_order_lines = self.env['sale.order.line'].search([('order_id' , '=' , record.id)])
            min_price = 0
            _max_price = int(self.env['ir.config_parameter'].sudo().get_param('sale_order.sale_order_max_price', 1000000))

            for line in sale_order_lines:
                min_price += line.product_id.standard_price

            if  record.amount_total > _max_price or record.amount_total < min_price:
                record.is_over_price = True
                record.approve_status = False
            else:
                record.is_over_price = False

    @api.onchange('approve_status')
    def _onchange_approve_status(self):
        admin_sale_id = self.env.ref('sales_team.group_sale_manager')
        for record in self:
            user_group_id = record.user_id.groups_id
            if  admin_sale_id in user_group_id:
                record.approve_status = not record.approve_status
        else:
            return

    @api.depends('amount_total')
    def _compute_is_over_price(self):
        for record in self:
            sale_order_lines = self.env['sale.order.line'].search([('order_id' , '=' , record.id)])
            min_price = 0
            max_price = 1000000

            for line in sale_order_lines:
                min_price += line.product_id.standard_price

            if  record.amount_total > max_price or record.amount_total < min_price:
                record.is_over_price = True
                record.approve_status = False
            else:
                record.is_over_price = False
                record.approve_status = False

    @api.onchange('amount_total')
    def _onchange_amount_total(self):
        for record in self:
            sale_order_lines = self.env['sale.order.line'].search([('order_id' , '=' , record.id)])
            min_price = 0
            max_price = 1000000

            for line in sale_order_lines:
                min_price += line.product_id.standard_price

            if  record.amount_total > max_price or record.amount_total < min_price:
                record.is_over_price = True
                record.approve_status = False
            else:
                record.is_over_price = False

    @api.depends('approve_status' , 'is_over_price')
    def _compute_is_hide_button(self):
        for record in self:
            if not record.approve_status and record.is_over_price:
                record.is_hide_button = True
            else:
                record.is_hide_button = False

    @api.depends('approve_status' , 'is_over_price')
    def _compute_approve_button(self):
        for record in self:
            if record.is_over_price:
                if record.approve_status:
                    record.approve_button = '承認'
                else:
                    record.approve_button = '未承認'
            else:
                record.approve_button = ''

class sale_report_approve(models.Model):
    _inherit = 'ir.actions.report'

    def _get_rendering_context(self, docids, data):
        res = super(sale_report_approve, self)._get_rendering_context(docids, data)
        sale_order = self.env[self.model].sudo(False).browse(docids)
        if not sale_order.approve_status and sale_order.is_over_price:
            raise UserError('未承認のため印刷できません。')
        return res
