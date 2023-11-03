from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    chop = fields.Binary("Company Chop Image", attachment=True,)
