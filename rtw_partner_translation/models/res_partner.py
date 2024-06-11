from odoo import fields, models , api
from lxml import etree

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
    
    @api.model
    def _fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ResPartner, self)._fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        
        doc = etree.fromstring(res['arch'])
        for street_node in doc.xpath("//field[@name='street']"):
            street_node.set('style', 'width:100%;display:inline-block;')
        for street2_node in doc.xpath("//field[@name='street2']"):
            street2_node.set('style', 'width:100%;display:inline-block;')
        for city_node in doc.xpath("//field[@name='city']"):
            city_node.set('style', 'width:100%;display:inline-block;margin-right:0;')
        for zip_node in doc.xpath("//field[@name='zip']"):
            zip_node.set('style', 'width:100%;display:inline-block;')
        for state_node in doc.xpath("//field[@name='state_id']"):
            state_node.set('style', 'width:100%;')
            
        res['arch'] = etree.tostring(doc, encoding='unicode')
        
        return res
    
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
        # self.refresh()
        sync_name = ['res.partner,street','res.partner,street2','res.partner,zip','res.partner,city']
        for record in self:
            if record.name in sync_name:
                lang = record.lang
                parent_partner = self.env['res.partner'].search([('id', '=', record.res_id)])
                if parent_partner:
                    for contact in parent_partner.child_ids:
                        self.update_translation(contact,self.name,lang)

        return result
    