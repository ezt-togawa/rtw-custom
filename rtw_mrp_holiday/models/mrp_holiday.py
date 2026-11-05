# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import pytz

from odoo import api, fields, models
from odoo.exceptions import ValidationError

HOLIDAY_TZ = pytz.timezone('Asia/Tokyo')


class MrpHoliday(models.Model):
    _name = 'mrp.holiday'
    _description = '製造休日'
    _order = 'date_from desc, id desc'

    name = fields.Char(string='休日名', required=True)
    date_from = fields.Date(string='開始日', required=True, default=fields.Date.context_today)
    date_to = fields.Date(string='終了日', help="1日だけの場合は空欄にします。")

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for holiday in self:
            if holiday.date_to and holiday.date_to < holiday.date_from:
                raise ValidationError("終了日は開始日以降にしてください。")

    @api.model
    def _holiday_dates(self, start, end):
        """start〜end（含む）に含まれる休日の日付(date)の集合"""
        holidays = self.search([
            ('date_from', '<=', end),
            '|', ('date_to', '>=', start),
            '&', ('date_to', '=', False), ('date_from', '>=', start),
        ])
        dates = set()
        for holiday in holidays:
            day = max(holiday.date_from, start)
            last = min(holiday.date_to or holiday.date_from, end)
            while day <= last:
                dates.add(day)
                day += timedelta(days=1)
        return dates

    @api.model
    def get_holiday_dates(self, date_from, date_to):
        """カレンダー表示用。'YYYY-MM-DD' のリストを返す"""
        dates = self._holiday_dates(fields.Date.to_date(date_from), fields.Date.to_date(date_to))
        return sorted(day.strftime('%Y-%m-%d') for day in dates)

    @api.model
    def to_local_date(self, value):
        """日付型はそのまま、日時型は日本時間の日付にする"""
        if not value:
            return False
        if isinstance(value, datetime):
            return pytz.utc.localize(value).astimezone(HOLIDAY_TZ).date()
        return value

    @api.model
    def holidays_among(self, days):
        """days（date または False のリスト）のうち休日のものの集合。日曜は登録がなくても休日"""
        days = [day for day in days if day]
        if not days:
            return set()
        sundays = {day for day in days if day.weekday() == 6}
        return (self._holiday_dates(min(days), max(days)) & set(days)) | sundays
