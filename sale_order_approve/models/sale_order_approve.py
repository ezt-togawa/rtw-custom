# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class sale_order_approve(models.Model):
    _inherit = "sale.order"

    approve_status = fields.Boolean('Approve', default=0)
    approve_status_check = fields.Text('承認状況 ',compute='_compute_approve_status_check', tracking=True)
    is_over_price = fields.Boolean('Is Over Price' , compute='_compute_is_over_price', store=True)
    is_hide_button = fields.Boolean('Is Hide Button' , compute='_compute_is_hide_button' , store=True)
    approve_button = fields.Char('Approve Button' , compute='_compute_approve_button' , store=True)
    total_price_sale = fields.Float('Total Price Sale')
    approve_user = fields.Char('承認者', store=True)

    def _get_over_price_threshold(self):
        # 承認なしで確認できる金額の上限。変更する場合はここ1箇所だけでOK。
        return 2000000

    def _get_amount_total_in_company_currency(self):
        # 閾値(円)や商品原価(標準は会社通貨=円)と比較するため、
        # 受注が外貨建てでも会社通貨(円)に換算した金額を返す。
        self.ensure_one()
        company = self.company_id or self.env.company
        company_currency = company.currency_id
        if not self.currency_id or self.currency_id == company_currency:
            return self.amount_total
        return self.currency_id._convert(
            self.amount_total, company_currency, company, self.date_order or fields.Date.today()
        )

    def toggle_approve_btn(self):
        admin_sale_id = self.env.ref('sales_team.group_sale_manager')
        for record in self:
            user_group_id = record.user_id.groups_id
            if admin_sale_id in user_group_id:
                record.approve_status = not record.approve_status
                if record.approve_status:
                    self.approve_user = self.env.user.name
                else:
                    self.approve_user = ''
            else:
                raise UserError('販売の管理者のみ承認の実行ができます。')

    @api.onchange('approve_status')
    def _onchange_approve_status(self):
        admin_sale_id = self.env.ref('sales_team.group_sale_manager')
        for record in self:
            user_group_id = record.user_id.groups_id
            if  admin_sale_id in user_group_id:
                record.approve_status = not record.approve_status
        else:
            return
    @api.depends('amount_total', 'currency_id')
    def _compute_is_over_price(self):
        for record in self:
            sale_order_lines = self.env['sale.order.line'].search([('order_id' , '=' , record.id)])
            min_price = 0
            max_price = self._get_over_price_threshold()
            for line in sale_order_lines:
                min_price += line.product_id.standard_price
            amount_total_company = record._get_amount_total_in_company_currency()
            new_is_over_price = amount_total_company > max_price or amount_total_company < min_price
            if new_is_over_price != record.is_over_price:
                # 承認要否の判定自体が変わった時だけ、既存の承認状態をリセットする
                # (単に再計算しただけで手動承認を消してしまわないため)
                record.approve_status = False
                record.approve_user = ''
            record.is_over_price = new_is_over_price
            record.total_price_sale = amount_total_company


    @api.onchange('amount_total', 'currency_id')
    def _onchange_amount_total(self):
        for record in self:
            sale_order_lines = self.env['sale.order.line'].search([('order_id' , '=' , record.id)])
            min_price = 0
            max_price = self._get_over_price_threshold()

            for line in sale_order_lines:
                min_price += line.product_id.standard_price

            amount_total_company = record._get_amount_total_in_company_currency()
            if amount_total_company > max_price or amount_total_company < min_price:
                record.is_over_price = True
                record.approve_status = False
                record.approve_user = ''
            else:
                record.is_over_price = False

    @api.depends('approve_status', 'is_over_price')
    def _compute_is_hide_button(self):
        for record in self:
            if not record.approve_status and record.is_over_price:
                record.is_hide_button = True
            else:
                record.is_hide_button = False
    @api.depends('approve_status', 'is_over_price')
    def _compute_approve_button(self):
        for record in self:
            if record.is_over_price:
                if record.approve_status:
                    record.approve_button = '承認'
                else:
                    record.approve_button = '未承認'
            else:
                record.approve_button = ''   
    def _compute_approve_status_check(self):
        for rec in self:
            rec.approve_status_check = "承認済" if rec.approve_status else "未承認"

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}

        # 承認関連のコピー
        default['approve_status'] = False
        default['is_over_price'] = self.is_over_price
        default['approve_user'] = None
        default['status'] = "draft"

        return super(sale_order_approve, self).copy(default)

# class sale_report_approve(models.Model):
#     _inherit = 'ir.actions.report'
#     def _get_rendering_context(self, docids, data):
#         res = super(sale_report_approve, self)._get_rendering_context(docids, data)
#         if self.model == 'sale.order':
#             sale_order = self.env[self.model].sudo(False).browse(docids)
#             if not sale_order.approve_status and sale_order.is_over_price and sale_order.status != 'draft':
#                 raise UserError('未承認のため印刷できません。')
#         return res
class sale_report_excel(models.AbstractModel):
    _inherit = 'xlsx.export'
    def export_xlsx(self, template, res_model, res_ids):
        res = super(sale_report_excel, self).export_xlsx(template, res_model, res_ids)
        if res_model == 'sale.order':
            sale_order = self.env[res_model].sudo(False).browse(res_ids)
            if not sale_order.approve_status and sale_order.is_over_price:
                raise UserError('未承認のため印刷できません。')
        return res