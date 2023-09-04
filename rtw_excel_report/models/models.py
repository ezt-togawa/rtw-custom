# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

# class rtw_excel_report(models.Model):
#     _name = 'rtw_excel_report.rtw_excel_report'
#     _description = 'rtw_excel_report.rtw_excel_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()

#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class SaleOrderExcelReport(models.Model):
    _inherit = "sale.order"
    sale_order_amount_total = fields.Char(
        compute="_compute_sale_order_missing_currency",
        string="Amount total",
    )
    sale_order_amount_untaxed = fields.Char(
        compute="_compute_sale_order_missing_currency",
        string="Amount untax",
    )
    sale_order_amount_tax = fields.Char(
        compute="_compute_sale_order_missing_currency",
        string="Amount tax",
    )
    sale_order_fax = fields.Char(
        compute="_compute_sale_order_missing_char",
        string="Fax",
    )
    sale_order_tel = fields.Char(
        compute="_compute_sale_order_missing_char",
        string="Tel",
    )
    sale_order_zip = fields.Char(
        compute="_compute_sale_order_missing_char",
        string="Zip",
    )
    sale_order_current_date = fields.Char(
        compute="_compute_sale_order_current_date",
        string="Current Date",
    )
    sale_order_estimated_shipping_date = fields.Char(
        compute="_compute_sale_order_format_date",
        string="Estimated Shipping Date",
    )
    sale_order_date_order= fields.Char(
        compute="_compute_sale_order_format_date",
        string="Date Order",
    )
    sale_order_validity_date= fields.Char(
        compute="_compute_sale_order_format_date",
        string="Validity Date",
    )
    sale_order_company_name= fields.Char(
        compute="_compute_sale_order_company_name",
        string="Company Name",
    )
    sale_order_total_list_price = fields.Float(
        compute="_compute_sale_order_list_price",
        string="Total List Price",
    )
    sale_order_total_discount = fields.Char(
        compute="_compute_sale_order_total_discount",
        string="Total Discount",
    )

    def _compute_sale_order_missing_currency(self):
        for record in self:
            record.sale_order_amount_total = record.currency_id.symbol + str(record.amount_total if record.amount_total else '')
            record.sale_order_amount_untaxed = record.currency_id.symbol + str(record.amount_untaxed if record.amount_untaxed else '')
            record.sale_order_amount_tax = record.currency_id.symbol + str(record.amount_tax if record.amount_tax else '')

    def _compute_sale_order_missing_char(self):
        for record in self:
            record.sale_order_fax = 'fax.' + str(record.company_id.partner_id.fax if record.company_id.partner_id.fax else '')
            record.sale_order_tel = 'tel.' + str(record.company_id.partner_id.phone if record.company_id.partner_id.phone else '')
            record.sale_order_zip = '〒' + str(record.company_id.partner_id.zip if record.company_id.partner_id.zip else '')

    def _compute_sale_order_current_date(self):
      day = str(datetime.now().day)
      month = str(datetime.now().month)
      year = str(datetime.now().year)
      for record in self:
          record.sale_order_current_date = year + ' 年 ' + month + ' 月 ' + day + ' 日 '

    def _compute_sale_order_format_date(self):
      for record in self:
          shipping_date = record.estimated_shipping_date
          date_order = record.date_order
          validity_date = record.validity_date
          if shipping_date:
            record.sale_order_estimated_shipping_date = str(shipping_date.year) + '年' + str(shipping_date.month) + '月' + str(shipping_date.day) + '日'
          else:
            record.sale_order_estimated_shipping_date = ''
          if date_order:
            record.sale_order_date_order = str(date_order.year) + '年' + str(date_order.month) + '月' + str(date_order.day) + '日'
          else:
            record.sale_order_date_order = ''
          if validity_date:
            record.sale_order_validity_date = str(validity_date.year) + '年' + str(validity_date.month) + '月' + str(validity_date.day) + '日'
          else:
            record.sale_order_validity_date = ''

    def _compute_sale_order_company_name(self):
        for record in self:
            if record.company_id.partner_id.name:
              record.sale_order_company_name = record.company_id.partner_id.name + ' 様'
            else:
              record.sale_order_company_name = ''

    def _compute_sale_order_list_price(self):
        for record in self:
            total_list_price = 0
            sale_order_lines = record.order_line
            for line in sale_order_lines:
                total_list_price += line.product_template_id.list_price
            record.sale_order_total_list_price = total_list_price

    def _compute_sale_order_total_discount(self):
        for record in self:
            total_discount = 0
            sale_order_lines = record.order_line
            for line in sale_order_lines:
                total_discount += (line.price_unit - line.price_reduce) * line.product_uom_qty
            record.sale_order_total_discount = '- ' + str(total_discount)

class SaleOrderLineExcelReport(models.Model):
  _inherit = "sale.order.line"

  sale_order_number_and_size = fields.Char(
        compute="_compute_sale_order_number_and_size",
        string="品番・サイズ",
  )
  sale_order_product_detail = fields.Char(
        compute="_compute_sale_order_product_detail",
        string="仕様・詳細",
  )
  sale_order_sell_unit_price = fields.Float(
        compute="_compute_sale_order_sell_unit_price",
        string="販売単価",
  )
  sale_order_index = fields.Integer(
        compute="_compute_sale_order_index",
        string="index",
  )

  sale_order_name = fields.Char(
        compute="_compute_sale_order_name",
        string="Name",
  )

  def _compute_sale_order_number_and_size(self):
      for line in self:
          product_number_and_size = ''
          if line.product_id.product_no:
            product_number_and_size +=  str(line.product_id.product_no) + '\n'
          if line.product_id.width:
            product_number_and_size += 'W' + str(line.product_id.width) + ' '
          if line.product_id.depth:
            product_number_and_size += 'D' +  str(line.product_id.depth) + ' '
          if line.product_id.height:
            product_number_and_size += 'H' +  str(line.product_id.height) + ' '
          if line.product_id.ah:
            product_number_and_size += 'AH' +  str(line.product_id.ah) + ' '
          line.sale_order_number_and_size = product_number_and_size

  def _compute_sale_order_product_detail(self):
      for line in self:
          product_detail = ''
          product_config_sessions = line.config_session_id.custom_value_ids
          product_template_attribute_values = line.product_id.product_template_attribute_value_ids
          for attr in product_config_sessions:
              product_detail += attr.display_name + ':' + attr.value + '\n'
          for attr in product_template_attribute_values:
              product_detail += attr.display_name + '\n'
          line.sale_order_product_detail = product_detail

  def _compute_sale_order_sell_unit_price(self):
      for line in self:
        if line.discount > 0:
            discount = line.discount / 100
        else:
            discount = 1
        line.sale_order_sell_unit_price = line.product_template_id.list_price * discount

  def _compute_sale_order_index(self):
      index = 0
      for line in self:
        index = index + 1
        line.sale_order_index = index

  def _compute_sale_order_name(self):
      for line in self:
          p_type = ''
          if line.p_type:
            if line.p_type == 'special':
              p_type = '別注'
            elif line.p_type == 'custom':
              p_type = '特注'
          line.sale_order_name = line.name + '\n' + p_type


