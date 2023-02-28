# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    update_date_planned_status = fields.Boolean(readonly=True, default=False)

    def update_date_planned(self):
        for order_line in self:
            if order_line.move_ids:
                for move in order_line.move_ids:
                    if move.picking_id:
                        if move.picking_id.scheduled_date:
                            order_line.write(
                                {'date_planned': move.picking_id.scheduled_date,
                                 'update_date_planned_status': True})

    def write(self, vals):
        print(vals.get('update_date_planned_status'))
        # 画面から更新の場合のみ明細の予定日が変更されているか確認する
        update_flg = False
        if vals.get('update_date_planned_status') != True:
            for order_line in self:
                if order_line.date_planned:
                    if order_line.date_planned != vals.get('date_planned'):
                        update_flg = True
        else:
            vals.setdefault('update_date_planned_status', False)
        # 更新先にする
        result = super(SaleOrderLine, self).write(vals)
        # 更新フラグがTrueの場合、pickingの予定日を更新する
        if update_flg == True:
            for order_line in self:
                if order_line.move_ids:
                    for move in order_line.move_ids:
                        if move.picking_id:
                            picking_id = move.picking_id
                            # pickingの関数を呼び出し
                            picking_id.update_scheduled_date()
        return result
