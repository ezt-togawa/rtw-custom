# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime , timedelta


class rtw_crm(models.Model):
    _inherit = 'crm.lead'

    def _send_mail(self):
        current_date = datetime.now().date()
        tomorrow_date = current_date + timedelta(days=1)
        recipients = ['t_ogawa@enzantrades.co.jp']
        subject = '【RTW-Odoo】入荷情報_' + str(current_date)
        body = str(current_date) + '糸島への部材の入荷情報をご連絡します。' + '<br>' + '出力情報：入荷元／件数／部材名' + '<br>'
        itoshima_warehouse = self.env['stock.warehouse'].search([('name','=','糸島工場')])
        itoshima_operation_type = self.env['stock.picking.type'].search([('warehouse_id','=',itoshima_warehouse.id)])
        for type in itoshima_operation_type:
            if type.name == 'Receipts':
                itoshima_picking_type = type
        itoshima_stock_picking = self.env['stock.picking'].search([('picking_type_id','=',itoshima_picking_type.id)])
        for picking in itoshima_stock_picking:
            itoshima_stock_move = self.env['stock.move'].search([('picking_id','=',picking.id)])
            if itoshima_stock_move:
                for move in itoshima_stock_move:
                    if move.state != 'done' and move.state !='cancelled' and move.state !='draft' and picking.scheduled_date.date() == tomorrow_date:
                        body += picking.partner_id.display_name + '/' + str(move.product_uom_qty) + '/' + move.name + '<br>'

        itoshima_filter_action_id = self.env['ir.actions.act_window'].search([('name','=','Stock Picking Itoshima Filter')]).id if self.env['ir.actions.act_window'].search([('name','=','Stock Picking Itoshima Filter')]) else ''

        body = body + '<br>' + '糸島入荷一覧URL' + '<br>' + f'https://rtw.cloudsv.mydns.jp/web#action={itoshima_filter_action_id}&active_id=1&model=stock.picking&view_type=list&cids=1&menu_id=244' + '<br>' + '<br>' + '※本メールはシステム自動配信です、返信は無効となります。'

        mail = self.env['mail.mail'].sudo().create({
            'email_from': self.env.user.email_formatted,
            'email_to': ','.join(recipients),
            'subject': subject,
            'body_html': body,
        })
        if mail:
            mail.send()
        print(',,,,,,,,,,',mail)
        return mail
