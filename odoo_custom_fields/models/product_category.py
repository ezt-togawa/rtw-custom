from odoo import models, fields, api
from datetime import datetime

class ProductCategroy(models.Model):
    _inherit = 'product.category'
    _rec_name = "name"

    name = fields.Char(translate=True)
