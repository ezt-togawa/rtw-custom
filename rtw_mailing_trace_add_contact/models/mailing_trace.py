# -*- coding: utf-8 -*-
from odoo import models, fields, api

class rtw_mailing_trace(models.Model):
    _inherit = "mailing.trace"
    
    name_contact = fields.Char(string="Contact", compute="_compute_contact", store=True)
    company_info = fields.Char(string="Company Info", compute="_compute_contact", store=True)    
    
    @api.depends('res_id')
    def _compute_contact(self):
        for ml in self:
            name_contact = ''
            company_info = ''
            if ml.model == 'res.partner' and ml.res_id:
                res_partner = self.env['res.partner'].with_context({'lang':self.env.user.lang or 'en_US'}).search([('id','=',ml.res_id)])
                if res_partner.exists():
                    if res_partner.company_type == 'person':
                        if res_partner.last_name:
                            name_contact += res_partner.last_name + " "
                        if res_partner.first_name:
                            name_contact += res_partner.first_name  
                        # if res_partner.parent_id:
                        #     company_info = res_partner.parent_id.name
                    elif res_partner.company_type == 'company':
                        name_contact = res_partner.name
            ml.name_contact = name_contact.rstrip()
            ml.company_info = company_info.rstrip()

    def open_res_partner_form_view(self):
        self.ensure_one()
        res_partner = None 
        if self.model == "res.partner":
            res_partner = self.env['res.partner'].browse(self.res_id)
        action = self.env.ref("contacts.action_contacts")
        form = self.env.ref("base.view_partner_form")
        action = action.read()[0]
        action["views"] = [(form.id, "form")]
        if res_partner.exists():
            action["res_id"] = res_partner.id
        else: 
            action["res_id"] = None
        return action
    