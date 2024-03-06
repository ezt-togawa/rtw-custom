from odoo import models, fields, api

class rtw_sf_partner(models.Model):
    _inherit = "res.partner"
                        
    name_contact = fields.Char(string="Contact", compute="_compute_contact", store=True)

    def _compute_contact(self):
        for res in self:
            name = ''
            res_partner = self.env['res.partner'].browse(res.id)
            if res_partner.company_type == 'person':
                if res_partner.last_name:
                    name += res_partner.last_name + " "
                if res_partner.first_name:
                    name += res_partner.first_name    
            elif res_partner.company_type == 'company':
                name = res_partner.name
            res.name_contact = name
