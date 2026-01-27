# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime , timedelta

class sale_order_leadtime(models.Model):
    _inherit = "sale.order"

    leadtime = fields.Date(string="製造リードタイム", compute="_compute_leadtime", store=True)
    scheduled_order_date = fields.Date(string="発注予定日",default=fields.Date.context_today)

    def _compute_additional_time(self, product, product_qty):
        supplier_info = self.env['product.supplierinfo'].search([
            ('product_tmpl_id', '=', product.product_tmpl_id.id)
        ])
        bom_ids = self.env['mrp.bom'].search([
            ('product_tmpl_id', '=', product.product_tmpl_id.id)
        ])

        product_routes = product.route_ids
        supplier_delay = 0
        total_delivery_lead_time = 0
        bom_lead_time_list = []
        template_attribute_value_ids = product.product_template_attribute_value_ids

        if bom_ids and product.qty_available < product_qty:
            for bom in bom_ids:
                for bom_line in bom.bom_line_ids:
                    if (
                        not bom_line.bom_product_template_attribute_value_ids.ids
                        or all(
                            v in template_attribute_value_ids.ids
                            for v in bom_line.bom_product_template_attribute_value_ids.ids
                        )
                    ) and bom_line.product_id.product_tmpl_id.type == 'product':

                        amount_consumed = bom_line.available_quantity - (
                            product_qty * bom_line.product_qty
                        )

                        if amount_consumed < 0:
                            bom_total_lead_time = 0
                            bom_supplier_delay = 0

                            for route in bom_line.product_id.route_ids:
                                bom_total_lead_time += route.delivery_lead_time or 0

                            supplier_infos = self.env['product.supplierinfo'].search([
                                ('product_tmpl_id', '=', bom_line.product_id.product_tmpl_id.id)
                            ])
                            for s in supplier_infos:
                                bom_supplier_delay = max(bom_supplier_delay, s.delay or 0)

                            bom_total = (
                                bom_total_lead_time
                                + bom_supplier_delay
                                + bom_line.product_id.product_tmpl_id.produce_delay
                            )
                            bom_lead_time_list.append(bom_total)

        if bom_lead_time_list:
            supplier_delay = max(bom_lead_time_list)

        for route in product_routes:
            total_delivery_lead_time += route.delivery_lead_time or 0

        for supplier in supplier_info:
            supplier_delay = max(supplier_delay, supplier.delay or 0)

        return supplier_delay + total_delivery_lead_time + product.product_tmpl_id.produce_delay

    @api.depends('order_line.date_planned')
    def _compute_leadtime(self):
        for order in self:
            max_schedule_date = False
            for line in order.order_line:
                if line.date_planned:
                    if not max_schedule_date:
                        max_schedule_date = line.date_planned
                    elif line.date_planned > max_schedule_date:
                        max_schedule_date = line.date_planned
            order.leadtime = max_schedule_date

    def update_leadtime(self):
        for order in self:
            base_date = order.scheduled_order_date or fields.Date.context_today(self)
            base_datetime = datetime.combine(base_date, datetime.min.time())

            for line in order.order_line:
                if not line.product_id:
                    continue

                additional_time = self._compute_additional_time(
                    line.product_id,
                    line.product_uom_qty
                )

                days = int(additional_time)
                hours = (additional_time - days) * 24

                line.date_planned = base_datetime + timedelta(
                    days=days,
                    hours=hours
                )

        if self.leadtime:
            # for line in self.order_line:
            #     line.date_planned = self.leadtime
            ## update delivery
            stock_picking = self.env['stock.picking'].search([('sale_id', '=', self.id)])
            for stock in stock_picking:
                if stock.state not in ('done', 'cancel'):
                    stock.write({"scheduled_date": self.leadtime})
                    stock.write({"date_deadline": self.leadtime})

