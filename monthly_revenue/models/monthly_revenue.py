# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta

class MonthlyRevenue(models.Model):
    _name = 'rtw_crm.monthly.revenue'
    _description = 'Monthly Revenue'

    date = fields.Date(string='年月')
    display_date = fields.Char(string='display 年月',compute="_compute_date")
    total_revenue = fields.Float(string='売上金額合計')

    def _compute_date(self):
        for record in self:
            record.display_date = record.date.strftime('%Y/%m')
