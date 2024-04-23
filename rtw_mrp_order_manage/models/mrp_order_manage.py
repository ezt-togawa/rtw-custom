# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_mrp_production_revised_edition(models.Model):
    _inherit = 'mrp.production'

    mrp_order_status = fields.Boolean('Mrp Order Status', default=False)

    def toggle_mrp_order_btn(self):
        for record in self:
            print(record.id)
            record.mrp_order_status = not record.mrp_order_status
