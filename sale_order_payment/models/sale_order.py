# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_order_payment(models.Model):
    _inherit = "sale.order"

    payment_status = fields.Char('支払状況',compute='_compute_payment_status',store=True)
    has_not_paid_in_payment_status = fields.Boolean(string='has_not_paid_in_payment_status', compute='_compute_has_status_in_payment_status',store=True)
    has_paid_in_payment_status = fields.Boolean(string='has_paid_in_payment_status', compute='_compute_has_status_in_payment_status',store=True)
    has_partial_in_payment_status = fields.Boolean(string='has_partial_in_payment_status', compute='_compute_has_status_in_payment_status',store=True)
    
    @api.depends('payment_status')
    def _compute_has_status_in_payment_status(self):
        for record in self:
            if record.payment_status:
                has_paid_in_payment_status = False
                has_not_paid_in_payment_status = False
                has_partial_in_payment_status = False
                list_status = record.payment_status.split(',')
                # if self.env.context.get('lang') == 'ja_JP':
                if '未払' in list_status:
                    has_not_paid_in_payment_status = True
                if '支払済' in list_status:
                    has_paid_in_payment_status = True
                if '一部支払済' in list_status:
                    has_partial_in_payment_status = True
                # else:
                #     if 'Not Paid' in list_status:
                #         has_not_paid_in_payment_status = True
                #     if 'Paid' in list_status:
                #         has_paid_in_payment_status = True
                #     if 'Partially Paid' in list_status:
                #         has_partial_in_payment_status = True
                        
                record.has_not_paid_in_payment_status = has_not_paid_in_payment_status
                record.has_paid_in_payment_status = has_paid_in_payment_status
                record.has_partial_in_payment_status = has_partial_in_payment_status 
            else:
                record.has_paid_in_payment_status = False
                record.has_not_paid_in_payment_status = False
                record.has_partial_in_payment_status = False
                
    @api.depends('invoice_ids.payment_state')            
    def _compute_payment_status(self):
        for record in self:
            payment_status = []
            if record.invoice_ids:
                for invoice in record.invoice_ids:
                    status = ''
                    # if self.env.context.get('lang') == 'ja_JP':
                    if invoice.payment_state == 'not_paid':
                        status = '未払'
                    elif invoice.payment_state == 'in_payment':
                        status = '支払中'
                    elif invoice.payment_state == 'paid':
                        status = '支払済'
                    elif invoice.payment_state == 'partial':
                        status = '一部支払済'
                    elif invoice.payment_state == 'reversed':
                        status = '逆'
                    elif invoice.payment_state == 'invoicing_legacy':
                        status = '請求書のAppレガシー'
                    else:
                        status = ''
                    # else:
                    #     if invoice.payment_state == 'not_paid':
                    #         status = 'Not Paid'
                    #     elif invoice.payment_state == 'in_payment':
                    #         status = 'In Payment'
                    #     elif invoice.payment_state == 'paid':
                    #         status = 'Paid'
                    #     elif invoice.payment_state == 'partial':
                    #         status = 'Partially Paid'
                    #     elif invoice.payment_state == 'reversed':
                    #         status = 'Reversed'
                    #     elif invoice.payment_state == 'invoicing_legacy':
                    #         status = 'Invoicing App Legacy'
                    #     else:
                    #         status = ''
                    if status:
                        payment_status.append(status)
                    
                record.payment_status = ','.join(payment_status)
            else:
                record.payment_status = ''
                
class stock_picking_payment(models.Model):
    _inherit = "stock.picking"
    
    payment_status = fields.Char(string="支払状況",related='sale_id.payment_status')
    payment_term_id = fields.Many2one(string="支払条件",related='sale_id.payment_term_id')
    has_not_paid_in_payment_status = fields.Boolean(related='sale_id.has_not_paid_in_payment_status')
    has_paid_in_payment_status = fields.Boolean(related='sale_id.has_paid_in_payment_status')
    has_partial_in_payment_status = fields.Boolean(related='sale_id.has_partial_in_payment_status')
    