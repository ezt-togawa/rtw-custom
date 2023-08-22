# Copyright 2018-2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
import math

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    so_title = fields.Char(string="title")
    calculate_planned_date = fields.Date(string="planned date" , compute="_compute_calculate_planned_date")

    def _compute_calculate_planned_date(self):
        max_planned_date = ''
        for line in self.order_line:
            if max_planned_date == '':
                max_planned_date = line.date_planned
            elif line.date_planned and line.date_planned > max_planned_date:
                max_planned_date = line.date_planned
        self.calculate_planned_date = max_planned_date

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    show_details = fields.Boolean(
        string="Show details",
        default=True)
    show_subtotal = fields.Boolean(
        string="Show subtotal",
        default=True)
    calculate_packages = fields.Integer(
        string="Calculate packages",
        compute="_compute_calculate_packages"
    )

    def _compute_calculate_packages(self):
        for line in self:
            if line.product_id.two_legs_scale:
                line.calculate_packages = math.ceil(line.product_uom_qty / line.product_id.two_legs_scale)
            else:
                line.calculate_packages = line.product_uom_qty

    def _prepare_invoice_line(self, qty):
        res = super()._prepare_invoice_line(qty)
        res.update(show_details=self.show_details,
                   show_subtotal=self.show_subtotal)
        return res
