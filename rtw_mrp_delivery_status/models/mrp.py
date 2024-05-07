# -*- coding: utf-8 -*-

from odoo import models, fields, api

class mrp(models.Model):
    _inherit = "mrp.production"

    delivery_status = fields.Boolean('Delivery Status', default=0)
    delivery_status_text = fields.Char('発注' , compute="_compute_delivery_status_text" , store=True)

    def action_set_delivery_status(self):
        for record in self:
            record.delivery_status = not record.delivery_status

    @api.depends('delivery_status')
    def _compute_delivery_status_text(self):
        for record in self:
            record.delivery_status_text = '発注済' if record.delivery_status else '未'
