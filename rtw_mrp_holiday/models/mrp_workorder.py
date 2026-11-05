# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    is_plan_date_holiday = fields.Boolean(compute='_compute_is_plan_date_holiday')
    holiday_mark = fields.Char(string='休日', compute='_compute_is_plan_date_holiday')

    @api.depends('implementation_plan_date', 'date_planned_start', 'state')
    def _compute_is_plan_date_holiday(self):
        Holiday = self.env['mrp.holiday']
        days = {
            record: (Holiday.to_local_date(record.implementation_plan_date),
                     Holiday.to_local_date(record.date_planned_start))
            for record in self
        }
        holidays = Holiday.holidays_among([day for pair in days.values() for day in pair])
        for record in self:
            is_holiday = record.state not in ('done', 'cancel') and any(day in holidays for day in days[record])
            record.is_plan_date_holiday = is_holiday
            record.holiday_mark = '休' if is_holiday else False
