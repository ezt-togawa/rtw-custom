from odoo import models, fields, api

class rtw_sf_partner(models.Model):
    _inherit = "res.partner"
                        
    name_contact = fields.Char(string="Contact", compute="_compute_contact", store=True)

    @api.depends('company_type', 'name','last_name','first_name')
    def _compute_contact(self):
        for res in self:
            name = ''
            if res.exists():
                if res.company_type == 'person':
                    if res.last_name:
                        name += res.last_name + " "
                    if res.first_name:
                        name += res.first_name    
                elif res.company_type == 'company':
                    name = res.name
            res.name_contact = name
            
    def write(self, values): 
        res = super(rtw_sf_partner, self).write(values)
        if len(self) == 1:
            self._update_autocomplete_data(values.get('vat', False))
        mailing_trace = self.env['mailing.trace'].search([('res_id','=',self.id)])
        if mailing_trace:
            mailing_trace._compute_contact()
        return res
