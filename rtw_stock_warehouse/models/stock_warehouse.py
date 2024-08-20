from odoo import models, fields, api

class rtw_stock_warehouse(models.Model):
    _inherit = 'stock.warehouse'
    
    user_id = fields.Many2one(comodel_name="res.users", string="発注担当者")
