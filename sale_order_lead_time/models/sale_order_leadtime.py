# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_order_leadtime(models.Model):
    _inherit = "sale.order"

    leadtime = fields.Datetime(string="リードタイム")

    def update_leadtime(self):
        if self.leadtime:
            for line in self.order_line:
                line.date_planned = self.leadtime
            ## update delivery
            stock_picking = self.env['stock.picking'].search([('sale_id', '=', self.id)])
            for stock in stock_picking:
                if stock.state not in ('done', 'cancel'):
                    stock.write({"scheduled_date": self.leadtime})
                    stock.write({"date_deadline": self.leadtime})



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

