# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from dateutil.parser import parse


class MrpPickingCustom(models.Model):
    _inherit = 'stock.picking'

    def write(self, vals):
        res = super(MrpPickingCustom, self).write(vals)
        print('_mrp_arrival_schedule', self.name)
        for record in self:

            # 配送の出荷予定日に合わせて、製造オーダー側の製造部材入荷予定の日付を更新しておく（カレンダー用）
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

        return res
