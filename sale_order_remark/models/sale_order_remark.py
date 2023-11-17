# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_order_remark(models.Model):
    _inherit = "sale.order"

    remark = fields.Text('共通備考', default=None)
    special_note = fields.Text('伝票用特記事項' , default=None)

class mrp_remark(models.Model):
    _inherit = "mrp.production"

    remark = fields.Text('共通備考' , default=None , compute='_compute_remark', inverse='_inverse_remark')
    special_note = fields.Text('伝票用特記事項' , default=None , compute='_compute_special_note', inverse='_inverse_special_note')

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

    def _compute_special_note(self):
        for record in self:
            sale_order = self.env['sale.order'].search([('name', '=', record.origin)])
            if sale_order:
                record.special_note = sale_order.special_note

    def _inverse_special_note(self):
        for record in self:
            sale_order = self.env['sale.order'].search([('name', '=', record.origin)])
            if sale_order:
                sale_order.write({'special_note': record.special_note})
