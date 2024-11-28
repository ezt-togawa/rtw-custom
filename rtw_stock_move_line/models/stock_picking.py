# -*- coding: utf-8 -*-

from odoo import fields, models, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    primary_shipment = fields.Boolean('一次出荷', default=False)  

    def toggle_primary_shipment(self):
        for record in self:
            record.primary_shipment = not record.primary_shipment 


