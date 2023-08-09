# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_order_remark(models.Model):
    _inherit = "sale.order"

    remark = fields.Text('共通備考', default=None)

class mrp_remark(models.Model):
    _inherit = "mrp.production"

    remark = fields.Text('共通備考' , default=None , compute='_compute_remark', inverse='_inverse_remark')


    def _compute_remark(self):
        for record in self:
            sale_order = self.env['sale.order'].search([('name', '=', record.origin)])
            if sale_order:
                record.remark = sale_order.remark

    def _inverse_remark(self):
        for record in self:
            sale_order = self.env['sale.order'].search([('name', '=', record.origin)])
            if sale_order:
                sale_order.write({'remark': record.remark})
