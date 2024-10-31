from odoo import models, fields, api

class account_move_line(models.Model):
    _inherit = "account.move.line"
    price_unit = fields.Monetary('Unit Price', required=True, digits='Product Price')