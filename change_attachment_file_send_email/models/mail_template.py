from odoo import fields, models
from datetime import datetime

class MailTemplateCus(models.Model):
    _inherit = 'mail.template'

    current_print = fields.Char(compute="_compute_current_print")
    
    def _compute_current_print(self):
        for mail in self:
            mail.current_print = datetime.now().strftime('%Y-%m-%dT%H%M%S')
            