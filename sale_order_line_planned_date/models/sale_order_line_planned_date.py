# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
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
                                    self.env.context, is_show_planned_date_ntoice=False)

    @api.depends('order_line')
    def _compute_error_context(self):
        # print('_compute_error_context', self.env.context)
        if self.env.context.get('is_show_planned_date_notice'):
            self.error_context = self.env.context.get(
                'is_show_planned_date_notice')
        else:
            self.error_context = False
        # print('_compute_error_context 2', self.error_context)
    
    def _get_delay_by_rule(self, move, moves):
        delay = 0
        next_move = next((m for m in moves if m.location_id == move.location_dest_id), None)
        if next_move:
            delay += self._get_delay_by_rule(next_move,moves)
        delay += move.rule_id.delay
        return delay

    def action_confirm(self):
        result = super(sale_order, self).action_confirm()
        stock_picking = self.env['stock.picking'].search([('sale_id', '=', self.id), ('state', 'not in', ('cancel', 'draft'))])
        for delivery in stock_picking:
            moves = [move for move in delivery.group_id.stock_move_ids if move.state != 'cancel']
            for move in moves:
                if move.sale_id and move.sale_id.estimated_shipping_date:
                    delay = self._get_delay_by_rule(move, moves)
                    new_date = move.sale_id.estimated_shipping_date - relativedelta(days=delay)
                    move.date = new_date
                    move.picking_id.scheduled_date = new_date
        return result

