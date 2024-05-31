from odoo import fields, models , api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(translate=True)
    last_name = fields.Char(translate=True)
    first_name = fields.Char(translate=True)
    kana = fields.Char(translate=True)
    site = fields.Char(translate=True)
    city = fields.Char(translate=True)
    zip = fields.Char(translate=True)
    street = fields.Char(translate=True)
    street2 = fields.Char(translate=True)
    parent_name = fields.Char(related='parent_id.display_name', readonly=True, string='Parent name')
    
    def write(self, vals):
        result = super(ResPartner, self).write(vals)
        self.refresh()
        sync_fields = ['street','street2','zip','city']
        langs = ['ja_JP','en_US']
        parent_address = {}
        child_address = {}
        for rec in self:
            if rec.parent_id:
                for lang in langs:
                    for field in sync_fields:
                        parent_key = f'{field}_{lang.lower()}'
                        child_key = f'{field}_{lang.lower()}'
                        parent_address[parent_key] = self.env['ir.translation'].search([('name','=',f'res.partner,{field}'),('res_id','=',rec.parent_id.id),('lang','=',lang)])
                        child_address[child_key] = self.env['ir.translation'].search([('name','=',f'res.partner,{field}'),('res_id','=',rec.id),('lang','=',lang)])
                
            for key,value in child_address.items():
                # CREATE MISSING TRANSLATE
                parent_value = parent_address[key]
                if not value:
                    address_key = key.split('_')[0]
                    if parent_value:
                        for lang in langs:
                            if lang.lower() in key:
                                check_exist_translate = self.env['ir.translation'].search([('name','=',f'res.partner,{address_key}'),('res_id','=',rec.id),('lang','=',lang)])
                                if not check_exist_translate:
                                    value = self.env['ir.translation'].create({
                                        'name':f'res.partner,{address_key}',
                                        'res_id':rec.id,
                                        'lang':lang,
                                        'src': rec[address_key],
                                        'type':'model',
                                        'value':parent_value.value,
                                        'state':'translated'
                                    })        
                # REUPDATE VALUE OF TRANSLATE OF CHILD BY PARENT
                if parent_value and value:
                    value.value = parent_address[key].value
                
        return result
    
class IrTranslation(models.Model):
    _inherit = 'ir.translation'
    
    def update_translation(self,contact,name,lang):
        child_address = self.env['ir.translation'].search([('name','=',name),('res_id','=',contact.id),('lang','=',lang)])
        if not child_address:
            child_address = self.env['ir.translation'].create({
                'name':name,
                'res_id':contact.id,
                'lang':lang,
                'src': self.src,
                'type':self.type,
                'value':self.value,
                'state':'translated'
            })
        else:
            child_address.value = self.value
        if contact.child_ids:
            for child_contact in contact.child_ids:
                self.update_translation(child_contact,name,lang)
            
    def write(self, vals):
        result = super(IrTranslation, self).write(vals)
        self.refresh()
        
        for record in self:
            lang = record.lang
            parent_partner = self.env['res.partner'].search([('id', '=', record.res_id)])
            if parent_partner:
                for contact in parent_partner.child_ids:
                    self.update_translation(contact,self.name,lang)

        return result
    