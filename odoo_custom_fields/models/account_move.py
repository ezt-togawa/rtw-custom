from odoo import models, fields, api
from datetime import datetime

class AccountMove(models.Model):
    _inherit = 'account.move'

    days_remaining = fields.Integer(string='Days Remaining', compute='_compute_days_remaining')

    @api.depends('invoice_date_due')
    def _compute_days_remaining(self):
        today = datetime.today().date()
        for record in self:
            if record.invoice_date_due:
                days_remaining = (record.invoice_date_due - today).days
                record.days_remaining = days_remaining
            else:
                record.days_remaining = 0
