# # -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api

class rtw_sale_order(models.Model):
    _inherit = "sale.order"
    
    transactions = fields.Many2one('res.partner.transactions',string="Transactions" , compute="_compute_transactions")
    transaction_condition_1 = fields.Text(string="Transaction Terms 1" , compute="_compute_transaction_condition_1")
    transaction_condition_2 = fields.Text(string="Transaction Terms 2" , compute="_compute_transaction_condition_2")
    payment_terms = fields.Text(string="Payment terms" , compute="_compute_payment_terms")
    
    def _compute_transactions(self):
        for so in self:           
            if so.partner_invoice_id:
                partner= self.env['res.partner'].search([('id','=',so.partner_invoice_id.id)])
                for p in partner:
                    if p.transactions:
                        so.transactions = p.transactions
                    else:
                        so.transactions = None
            else:
                so.transactions = None

    def _compute_transaction_condition_1(self):
        for so in self:           
            if so.partner_invoice_id:
                partner= self.env['res.partner'].search([('id','=',so.partner_invoice_id.id)])
                for p in partner:
                    if p.payment_terms_1:
                        so.transaction_condition_1 = p.payment_terms_1
                    else:
                        so.transaction_condition_1 = None
            else:
                so.transaction_condition_1 = None

    def _compute_transaction_condition_2(self):
        for so in self:           
            if so.partner_invoice_id:
                partner= self.env['res.partner'].search([('id','=',so.partner_invoice_id.id)])
                for p in partner:
                    if p.payment_terms_2:
                        so.transaction_condition_2 = p.payment_terms_2
                    else:
                        so.transaction_condition_2 = None
            else:
                so.transaction_condition_2 = None
    @api.depends('partner_invoice_id')
    def _compute_payment_terms(self):
        for so in self:           
            if so.partner_invoice_id:
                partner= self.env['res.partner'].search([('id','=',so.partner_invoice_id.id)])
                for p in partner:
                    if p.accounting_supplement_2:
                        so.payment_terms = p.accounting_supplement_2
                    else:
                        so.payment_terms = None
            else:
                so.payment_terms = None
