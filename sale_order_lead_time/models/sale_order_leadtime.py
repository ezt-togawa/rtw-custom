# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_order_leadtime(models.Model):
    _inherit = "sale.order"

    leadtime = fields.Datetime(string="リードタイム")

    def update_leadtime(self):
        max_order_line = self.order_line.search([('date_planned' , '!=' , False),('order_id','=',self.id)], order='date_planned desc', limit=1)
        if max_order_line:
            self.leadtime = max_order_line.date_planned


    @api.onchange('order_line')
    def _onchange_order_line_leadtime(self):
        max_schedule_date = ''
        for line in self.order_line:
            if line.date_planned:
                if max_schedule_date == '':
                    max_schedule_date = line.date_planned
                elif line.date_planned > max_schedule_date:
                    max_schedule_date = line.date_planned
        if max_schedule_date:
            self.leadtime = max_schedule_date

