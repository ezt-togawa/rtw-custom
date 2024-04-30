# # -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api

class rtw_sale_order(models.Model):
    _inherit = "sale.order"
    
    transactions = fields.Many2one('res.partner.transactions',string="Transactions" , compute="_compute_transactions")

    def _compute_transactions(self):
        for so in self:           
            if so.partner_id:
                partner= self.env['res.partner'].search([('id','=',so.partner_id.id)])
                for p in partner:
                    if p.transactions:
                        so.transactions = p.transactions
                    else:
                        so.transactions = None
