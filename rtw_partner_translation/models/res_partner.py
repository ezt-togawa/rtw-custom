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
            zip_node.set('style', 'width:100%;display:inline-block;margin-right:0;')
        for state_node in doc.xpath("//field[@name='state_id']"):
            state_node.set('style', 'width:100%;')
            
        res['arch'] = etree.tostring(doc, encoding='unicode')
        
        return res
    
    def write(self, vals):
        sync_fields = ['street', 'street2', 'zip', 'city']
        
        should_sync = any(field in vals for field in sync_fields)
        
        result = super().write(vals)
        
        if should_sync:
            IrTranslation = self.env['ir.translation']
            current_lang = self.env.context.get('lang', 'en_US')

            for rec in self:
                if rec.child_ids:
                    for field in sync_fields:
                        if field in vals:
                            name_field = f'res.partner,{field}'
                            
                            parent_trans = IrTranslation.search([
                                ('name', '=', name_field),
                                ('res_id', '=', rec.id),
                                ('lang', '=', current_lang)
                            ], limit=1)
                            
                            parent_value = parent_trans.value if parent_trans else (vals[field] or '')
                            
                            for child in rec.child_ids:
                                child_trans = IrTranslation.search([
                                    ('name', '=', name_field),
                                    ('res_id', '=', child.id),
                                    ('lang', '=', current_lang)
                                ], limit=1)
                                
                                if not child_trans:
                                    IrTranslation.create({
                                        'name': name_field,
                                        'res_id': child.id,
                                        'lang': current_lang,
                                        'src': vals[field] or '',
                                        'type': 'model',
                                        'value': parent_value,
                                        'state': 'translated'
                                    })
                                else:
                                    child_trans.write({'value': parent_value})

            self.env['ir.translation'].clear_caches()
        
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
    