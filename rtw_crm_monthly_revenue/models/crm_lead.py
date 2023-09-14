# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
import calendar

class rtw_crm(models.Model):
    _inherit = 'crm.lead'

    def find_min_max_date_deadline(self):
        min_date = self.env['crm.lead'].search(
            [('opportunity_completion_date', '!=', False)], order='opportunity_completion_date asc', limit=1).opportunity_completion_date
        max_date = self.env['crm.lead'].search(
            [('opportunity_completion_date', '!=', False)], order='opportunity_completion_date desc', limit=1).opportunity_completion_date
        return min_date, max_date


    @api.onchange('expected_revenue','opportunity_completion_date')
    def compute_monthly_revenue(self):
        min_date, max_date = self.find_min_max_date_deadline()
        current_date = min_date
        while current_date <= max_date:
            next_month = current_date.replace(day=1) + timedelta(days=32)
            end_of_month = current_date.replace(day=1)
            leads_in_month = self.env['crm.lead'].search([
                ('opportunity_completion_date', '>=', (current_date.replace(day=1)+ timedelta(days=32) -timedelta(days=365)).replace(day=1)),
                ('opportunity_completion_date', '<', (end_of_month + timedelta(days=32)).replace(day=1) ),
                ('active' ,'=',True),
            ])
            revenue_in_month = sum(leads_in_month.filtered(lambda lead: lead.stage_id.name == '受注成立').mapped('expected_revenue'))
            existed_monthly_record = self.env['rtw_crm.monthly.revenue'].search([('date', '=', current_date.replace(day=1))])
            if existed_monthly_record:
                existed_monthly_record.total_revenue = revenue_in_month
            else:
                self.env['rtw_crm.monthly.revenue'].create({
                    'date': current_date.replace(day=1),
                    'total_revenue': revenue_in_month
                })
            current_date = next_month

    def write(self , vals):
        result = super(rtw_crm,self).write(vals)
        # self.refresh()
        min_date, max_date = self.find_min_max_date_deadline()
        leads = self.search([])
        current_date = min_date
        while current_date <= max_date:
            next_month = current_date.replace(day=1) + timedelta(days=32)
            end_of_month = current_date.replace(day=1)
            leads_in_month = self.env['crm.lead'].search([
                ('opportunity_completion_date', '>=', (current_date.replace(day=1)+ timedelta(days=32) -timedelta(days=365)).replace(day=1)),
                ('opportunity_completion_date', '<', (end_of_month + timedelta(days=32)).replace(day=1)),
                ('active' ,'=',True),
                ('type','=','opportunity')
            ])
            revenue_in_month = sum(leads_in_month.filtered(lambda lead: lead.stage_id.name == '受注成立').mapped('expected_revenue'))
            existed_monthly_record = self.env['rtw_crm.monthly.revenue'].search([('date', '=', current_date.replace(day=1))])
            if existed_monthly_record:
                existed_monthly_record.total_revenue = revenue_in_month
            else:
                self.env['rtw_crm.monthly.revenue'].create({
                    'date': current_date.replace(day=1),
                    'total_revenue': revenue_in_month
                })
            current_date = next_month

        return result

    def init(self):
        super(rtw_crm, self).init()
        self.compute_monthly_revenue()
