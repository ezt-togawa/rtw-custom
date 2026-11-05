# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    is_planned_start_holiday = fields.Boolean(compute='_compute_is_planned_start_holiday')

    @api.depends('date_planned_start', 'state')
    def _compute_is_planned_start_holiday(self):
        Holiday = self.env['mrp.holiday']
        days = {record: Holiday.to_local_date(record.date_planned_start) for record in self}
        holidays = Holiday.holidays_among(days.values())
        for record in self:
            record.is_planned_start_holiday = (
                record.state not in ('done', 'cancel') and days[record] in holidays)
