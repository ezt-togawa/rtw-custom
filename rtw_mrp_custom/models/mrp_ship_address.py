from odoo import models, fields, api

class mrp_ship_address(models.Model):
    _name = 'mrp.ship.address'
    _description = 'Selection Ship Address'
    _order = 'sequence'
    
    address = fields.Char('住所', required=True)
    sequence = fields.Integer(default=10)
    
    def name_get(self):
        result = []
        for record in self:
            name = record.address
            result.append((record.id, name))
        return result