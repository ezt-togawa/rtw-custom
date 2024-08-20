from odoo import models

class rtw_mrp_production(models.Model):
    _inherit = 'mrp.production'
    
    def create(self, vals):
        res = super(rtw_mrp_production, self).create(vals)        
        for line in res:
            if line.picking_type_id and line.picking_type_id.warehouse_id:
                line.user_id = line.picking_type_id.warehouse_id.user_id or None
        return res 
