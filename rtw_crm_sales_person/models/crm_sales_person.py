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
        super(sale_order_sales_person, self).onchange_partner_id()
        if not self.partner_id:
            if not self.opportunity_id:
                self.update({'user_id': False})
                return

        if self.user_id and self.opportunity_id.user_id and self.user_id.id != self.opportunity_id.user_id.id:
            values = {'user_id': self.opportunity_id.user_id}
            self.update(values)
