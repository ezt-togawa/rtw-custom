# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from dateutil.parser import parse


class MrpPickingCustom(models.Model):
    _inherit = 'stock.picking'
    temp_scheduled_date = fields.Char('temp_scheduled_date', compute='_compute_temp_scheduled_date', default='', store=True)

    @api.depends('scheduled_date')
    def _compute_temp_scheduled_date(self):
        # 配送の出荷予定日に合わせて、製造オーダー側の製造部材入荷予定の日付を更新しておく（カレンダー用）
        for record in self:
            if record.group_id:
                # order_no = record.origin
                parent_mo = record.env["mrp.production"].search([('name', '=', record.group_id[0].name)])
                child_mo = record.env["mrp.production"].search(
                    [('sale_reference', '=', parent_mo.sale_reference), ('origin', '=', parent_mo.name)])
                product_ids = child_mo.mapped('product_id.id')
                stock_picking = self.env["stock.picking"].search([('product_id', 'in', product_ids) ,('location_dest_id', '=', parent_mo.location_src_id.id),('sales_order_name', '=', parent_mo.sale_reference),])
                if stock_picking:
                    arrival_schedule_parent_mo = ''
                    for picking in stock_picking:
                        if picking.scheduled_date:
                            arrival_schedule_parent_mo += str(parent_mo._convert_timezone(picking.scheduled_date)) + "\n"
                    parent_mo.prod_parts_arrival_schedule = arrival_schedule_parent_mo.rstrip('\n') if arrival_schedule_parent_mo else ''
                if child_mo and parent_mo.move_raw_ids:
                    arrival_schedule = ''
                    for move in parent_mo.move_raw_ids:
                        if move.forecast_expected_date:
                            move.recompute()
                            arrival_schedule += str(parent_mo._convert_timezone(move.forecast_expected_date)) + "\n"
                    # parent_mo.prod_parts_arrival_schedule = arrival_schedule.rstrip('\n') if arrival_schedule else ''
                    record.temp_scheduled_date = parent_mo.prod_parts_arrival_schedule
