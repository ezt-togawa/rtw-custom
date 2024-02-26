# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
import calendar


class rtw_crm_sales_person(models.Model):
    _inherit = 'crm.lead'

    user_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, tracking=True, default=False)

    @api.onchange('partner_id')
    def _onchange_crm_lead_partner_id(self):
        print('onchange parter id', self.partner_id.user_id)
        if self.partner_id and self.partner_id.user_id:
            self.user_id = self.partner_id.user_id
        else:
            self.user_id = False
            self.team_id = False
            self.email_from = False
            self.phone = False


class sale_order_sales_person(models.Model):
    _inherit = 'sale.order'

    @api.onchange('opportunity_id')
    def _onchange_opportunity_id(self):
        print('onchange parter id', self.opportunity_id.partner_id.user_id)
        if self.opportunity_id:
            if self.opportunity_id.user_id:
                self.user_id = self.opportunity_id.user_id
        else:
            if self.partner_id:
                self.user_id = self.partner_id.user_id
            else:
                self.user_id = False

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Update the following fields when the partner is changed:
        - Pricelist
        - Payment terms
        - Invoice address
        - Delivery address
        - Sales Team
        """
        if not self.partner_id:
            if not self.opportunity_id:
                self.update({'user_id': False})
                return
            self.update({
                'partner_invoice_id': False,
                'partner_shipping_id': False,
                'fiscal_position_id': False,
            })
            return

        self = self.with_company(self.company_id)

        addr = self.partner_id.address_get(['delivery', 'invoice'])
        partner_user = self.partner_id.user_id or self.partner_id.commercial_partner_id.user_id
        values = {
            'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id and self.partner_id.property_payment_term_id.id or False,
            'partner_invoice_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
        }
        user_id = partner_user.id
        if not self.env.context.get('not_self_saleperson'):
            user_id = user_id or self.env.context.get(
                'default_user_id', self.env.uid)
        if user_id and self.user_id.id != user_id and not self.opportunity_id.user_id:
            values['user_id'] = user_id
        elif not self.partner_id:
            self.user_id = False

        if self.env['ir.config_parameter'].sudo().get_param('account.use_invoice_terms') and self.env.company.invoice_terms:
            values['note'] = self.with_context(
                lang=self.partner_id.lang).env.company.invoice_terms
        if not self.env.context.get('not_self_saleperson') or not self.team_id:
            values['team_id'] = self.env['crm.team'].with_context(
                default_team_id=self.partner_id.team_id.id
            )._get_default_team_id(domain=['|', ('company_id', '=', self.company_id.id), ('company_id', '=', False)], user_id=user_id)
        self.update(values)

        # res = super(sale_order_sales_person, self).onchange_partner_id()
        # print('onchange parter id' , self.partner_id.user_id)
        # if self.partner_id.user_id and not self.opportunity_id and not self.user_id:
        #     self.user_id = self.partner_id.user_id
        # elif not self.partner_id:
        #     self.user_id = False
        # else:
        #     return
