from odoo import fields, models
from datetime import datetime

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    current_print = fields.Char(compute="_compute_current_print")
    
    def _compute_current_print(self):
        for so in self:
            so.current_print = datetime.now().strftime('%Y-%m-%dT%H%M%S')