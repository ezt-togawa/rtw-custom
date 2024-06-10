from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "mrp.workorder"
    
    implementation_plan_date = fields.Date('Implementation Plan Date')