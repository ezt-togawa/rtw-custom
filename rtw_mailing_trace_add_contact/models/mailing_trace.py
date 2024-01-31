# -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api

class rtw_sf_partner(models.Model):
    _inherit = "mailing.trace"
                        
    name_contact = fields.Char(string="Contact", compute="_compute_contact")

    @api.depends('res_id')
    def _compute_contact(self):
        for ml in self:
            name = ''
            if ml.model == 'res.partner' and ml.res_id:
                res_partner = self.env['res.partner'].browse(ml.res_id)
                if res_partner.company_type == 'person':
                    if res_partner.last_name:
                        name += res_partner.last_name + " "
                    if res_partner.first_name:
                        name += res_partner.first_name    
                elif res_partner.company_type == 'company':
                    name = res_partner.name
            ml.name_contact = name

    def open_res_partner_form_view(self):
        self.ensure_one()
        res_partner = self.env['res.partner'].browse(self.res_id)
        action = self.env.ref("contacts.action_contacts")
        form = self.env.ref("base.view_partner_form")
        action = action.read()[0]
        action["views"] = [(form.id, "form")]
        action["res_id"] = res_partner.id

        return action
