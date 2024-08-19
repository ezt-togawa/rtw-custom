from odoo import models, fields, api

class rtw_stock_warehouse(models.Model):
    _inherit = 'stock.warehouse'
    
    user_id = fields.Many2one(comodel_name="res.users", string="発注担当者")

    @api.onchange('user_id')
    def _onchange_user_id(self):
        warehouse_id = self.id.origin
        mrp_production = self.env['mrp.production'].search([('picking_type_id.warehouse_id', '=', warehouse_id or None)])
        if mrp_production:
            for record in mrp_production:
                record.user_id = self.user_id