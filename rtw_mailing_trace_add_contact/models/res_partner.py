from odoo import models, fields, api

class rtw_sf_partner(models.Model):
    _inherit = "res.partner"
                        
    name_contact = fields.Char(string="Contact", compute="_compute_contact", store=True)

    @api.depends('last_name', 'first_name', 'name', 'company_type')
    def _compute_contact(self):
        for res in self:
            name = ''
            if res.company_type == 'person':
                if res.last_name:
                    name += res.last_name + " "
                if res.first_name:
                    name += res.first_name    
            elif res.company_type == 'company':
                name = res.name
            res.name_contact = name
