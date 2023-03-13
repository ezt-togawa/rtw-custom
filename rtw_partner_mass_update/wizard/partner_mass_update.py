# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PartnerMassUpdate(models.TransientModel):
    _name = 'partner_mass_update'
    _description = 'partner_mass_update'

    user_id = fields.Many2one('res.users', 'Purchase Order')

    def update_partner(self):
        lines = self.env['res.partner'].browse(
            self._context.get('active_ids', []))
        for line in lines:
            print(line.name)
            print(line.rel_crm)
            for crm in line.rel_crm:
                print('lead:', crm.name)
