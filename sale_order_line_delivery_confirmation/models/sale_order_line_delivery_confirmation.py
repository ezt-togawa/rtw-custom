# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class sale_order_line_delivery_confirmation(models.Model):
    _inherit = "sale.order.line"

    delivery_confirmation = fields.Boolean(string='納期確認')

class rtw_crm(models.Model):
    _inherit = 'crm.lead'

    def _send_delivery_confirmation_mail(self):
        current_date = datetime.now().date()
        recipients = ['t_ogawa@enzantrades.co.jp']
        subject = '【RTW-Odoo】製品の納期予定の未確認情報_' + str(current_date)
        body = str(current_date) + '納期が未確認の製品をご連絡します。' + \
            '<br>' + '出力情報：受注番号／納期／Title／商品名' + '<br>'
        sale_orders = self.env['sale.order'].search(
            [('delivery_state', '=', 'unprocessed')])
        sale_line_in_week_one = []
        sale_line_in_week_two = []
        sale_line_in_week_three = []
        for sale in sale_orders:
            for order_line in sale.order_line:
                if order_line.date_planned:
                    if not order_line.delivery_confirmation and order_line.date_planned >= datetime.now() and order_line.date_planned <= (datetime.now() + timedelta(days=7)):  # Planned date in 7 days
                        sale_line_in_week_one.append(
                            (sale.name + ' / ' + str(order_line.date_planned.date()) + ' / ' + str(sale.title) + ' / ' + order_line.product_id.name))
                    # Planned date in 7 days - 14days
                    elif not order_line.delivery_confirmation and order_line.date_planned > (datetime.now() + timedelta(days=7)) and order_line.date_planned <= (datetime.now() + timedelta(days=14)):
                        sale_line_in_week_two.append(
                            (sale.name + ' / ' + str(order_line.date_planned.date()) + ' / ' + str(sale.title) + ' / ' + order_line.product_id.name))
                    # Planned date in 14 days - 21 days
                    elif not order_line.delivery_confirmation and order_line.date_planned > (datetime.now() + timedelta(days=14)) and order_line.date_planned <= (datetime.now() + timedelta(days=21)):
                        sale_line_in_week_three.append(
                            (sale.name + ' / ' + str(order_line.date_planned.date()) + ' / ' + str(sale.title) + ' / ' + order_line.product_id.name))

        body += '<br><b><1週間以内></b>'
        if sale_line_in_week_one:
            for sale_line in sale_line_in_week_one:
                body += '<br>' + sale_line

        body += '<br><b><1週前～2週前></b>'
        if sale_line_in_week_two:
            for sale_line in sale_line_in_week_two:
                body += '<br>' + sale_line

        body += '<br><b><2週前～3週前></b>'
        if sale_line_in_week_three:
            for sale_line in sale_line_in_week_three:
                body += '<br>' + sale_line

        body = body + '<br>'+'※本メールはシステム自動配信です、返信は無効となります。'

        mail = self.env['mail.mail'].sudo().create({
            'email_from': self.env.user.email_formatted,
            'email_to': ','.join(recipients),
            'subject': subject,
            'body_html': body,
        })
        if mail:
            mail.send()
        print(',,,,,,,,,,', mail)
        return mail
