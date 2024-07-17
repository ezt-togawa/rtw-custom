from odoo import models, fields

class mrp_ship_address(models.Model):
    _name = 'mrp.ship.address'
    _description = 'Selection Ship Address'
    _order = "id"
    
    address = fields.Char('住所', required=True)
    
    def name_get(self):
        result = []
        for record in self:
            name = record.address
            result.append((record.id, name))
        return result