# -*- coding: utf-8 -*-

from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    update_schedule_date_status = fields.Boolean(readonly=True, default=False)

    def update_scheduled_date(self):
        for picking in self:
            date_p = []
            i = 0
            if picking.move_lines:
                for move in picking.move_lines:
                    if move.sale_line_id:
                        if move.sale_line_id.date_planned:
                            date_p.append(move.sale_line_id.date_planned)
                            i += 1
            if i > 0:
                picking.write({'scheduled_date': max(date_p, default=picking.scheduled_date or fields.Datetime.now()),
                               'update_schedule_date_status': True})

    def write(self, vals):
        # 画面から更新の場合のみ予定日が変更されているか確認する
        print(vals.get('update_schedule_date_status'))
        update_flg = False
        if vals.get('update_schedule_date_status') != True:
            for picking in self:
                if picking.scheduled_date:
                    if picking.scheduled_date != vals.get('scheduled_date'):
                        update_flg = True
        else:
            vals.setdefault('update_schedule_date_status', False)
        # 更新先にする
        result = super(StockPicking, self).write(vals)
        # 更新フラグがTrueの場合、pickingの予定日を更新する
        if update_flg == True:
            for picking in self:
                if picking.move_lines:
                    for move in picking.move_lines:
                        if move.sale_line_id:
                            order_line_id = move.sale_line_id
                            # sale_order_lineの関数呼び出し
                            order_line_id.update_date_planned()
        return result
