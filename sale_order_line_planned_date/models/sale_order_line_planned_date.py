# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_order_line_confirm(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('date_planned')
    def _onchange_date_planned(self):
        for record in self:
            print(record.date_planned)
            print(record._origin.date_planned)
            if record._origin.date_planned and record.date_planned:
                if record._origin.date_planned > record.date_planned:
                    return {
                        'warning': {
                            'title': '確認',
                            'message': '予定を前倒します。よろしいですか？',

                    },
                }

class sale_order(models.Model):
    _inherit ="sale.order"

    def write(self , vals):
        result = super(sale_order,self).write(vals)
        self.refresh()
        stock_picking = self.env['stock.picking'].search([('sale_id' ,'=' ,self.id)])
        max_schedule_date = ''
        for line in self.order_line:
            if line.date_planned:
                if max_schedule_date == '':
                    max_schedule_date = line.date_planned
                elif line.date_planned > max_schedule_date:
                    max_schedule_date = line.date_planned

        if max_schedule_date:
            stock_picking.scheduled_date = max_schedule_date

        return result
