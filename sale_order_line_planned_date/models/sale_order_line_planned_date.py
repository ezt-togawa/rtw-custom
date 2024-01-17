# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_order_line_confirm(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('date_planned')
    def _onchange_date_planned(self):
        for record in self:
            if record._origin.date_planned and record.date_planned:
                    if record._origin.date_planned.strftime("%Y-%m-%d %H:%M:%S") > record.date_planned.strftime("%Y-%m-%d %H:%M:%S"):
                        return {
                            'warning': {
                                'title': '確認',
                                'message': '予定日を前倒しました。ご注意ください。',
                        },
                    }
class sale_order(models.Model):
    _inherit = "sale.order"

    error_context = fields.Char(compute='_compute_error_context')

    @api.onchange('order_line')
    def _onchange_order_line(self):
        has_record_meeting_condition = False
        for order in self:
            for line in order.order_line:
                if bool(line.product_id ) != False and line.display_type != "line_note":
                    if line.date_planned and line._origin and line._origin.date_planned :
                        if line.date_planned.strftime("%Y-%m-%d %H:%M:%S") < line._origin.date_planned.strftime("%Y-%m-%d %H:%M:%S"):
                            has_record_meeting_condition = True
                            if has_record_meeting_condition:
                                self.env.context = dict(
                                    self.env.context, is_show_planned_date_notice=True)
                            else:
                                self.env.context = dict(
                                    self.env.context, is_show_planned_date_notice=False)

    @api.depends('order_line')
    def _compute_error_context(self):
        print('_compute_error_context', self.env.context)
        if self.env.context.get('is_show_planned_date_notice'):
            self.error_context = self.env.context.get(
                'is_show_planned_date_notice')
        else:
            self.error_context = False
        print('_compute_error_context 2', self.error_context)

    def write(self, vals):
        result = super(sale_order, self).write(vals)
        self.refresh()
        stock_picking = self.env['stock.picking'].search(
            [('sale_id', '=', self.id)])
        max_schedule_date = ''
        for line in self.order_line:
            if line.date_planned:
                if max_schedule_date == '':
                    max_schedule_date = line.date_planned
                elif line.date_planned > max_schedule_date:
                    max_schedule_date = line.date_planned
        if max_schedule_date:
            for stock in stock_picking:
                if stock.state not in ('done', 'cancel'):
                    stock.write({"scheduled_date": max_schedule_date})
                    stock.write({"date_deadline": max_schedule_date})
        return result

    def action_confirm(self):
        result = super(sale_order, self).action_confirm()
        self.refresh()
        stock_picking = self.env['stock.picking'].search(
            [('sale_id', '=', self.id)])
        max_schedule_date = ''
        for line in self.order_line:
            if line.date_planned:
                if max_schedule_date == '':
                    max_schedule_date = line.date_planned
                elif line.date_planned > max_schedule_date:
                    max_schedule_date = line.date_planned

        if max_schedule_date:
            for stock in stock_picking:
                if stock.state not in ('done', 'cancel'):
                    stock.write({"scheduled_date": max_schedule_date})
                    stock.write({"date_deadline": max_schedule_date})

        return result
