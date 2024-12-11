# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from dateutil.parser import parse


class MrpPickingCustom(models.Model):
    _inherit = 'stock.picking'
    temp_scheduled_date = fields.Char('temp_scheduled_date', compute='_compute_picking_arrival_schedule', default='')

    @api.depends('scheduled_date')
    def _compute_picking_arrival_schedule(self):
        for record in self:

            # 配送の出荷予定日に合わせて、製造オーダー側の製造部材入荷予定の日付を更新しておく（カレンダー用）
            # 新規作成時はchildeMoが取れないので、Mrp側の更新処理にまかせる
            if record.origin:
                order_no = record.origin
                parent_mo = self.env["mrp.production"].search([('name', '=', order_no)])
                child_mo = self.env["mrp.production"].search(
                    [('sale_reference', '=', parent_mo.sale_reference), ('origin', '=', parent_mo.name)])
                if child_mo and parent_mo.move_raw_ids:
                    arrival_schedule = ''
                    for move in parent_mo.move_raw_ids:
                        if move.forecast_expected_date:
                            arrival_schedule += str(parent_mo._convert_timezone(move.forecast_expected_date)) + "\n"

                    parent_mo.prod_parts_arrival_schedule = arrival_schedule.rstrip('\n') if arrival_schedule else ''

                record.temp_scheduled_date = parent_mo.prod_parts_arrival_schedule
            else:
                record.temp_scheduled_date = ''
