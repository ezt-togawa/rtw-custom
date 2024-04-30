from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(translate=True)
    last_name = fields.Char(translate=True)
    first_name = fields.Char(translate=True)
    kana = fields.Char(translate=True)
    site = fields.Char(translate=True)
    city = fields.Char(translate=True)
    zip = fields.Char(translate=True)
    street = fields.Char(translate=True)
    street2 = fields.Char(translate=True)
    parent_name = fields.Char(related='parent_id.display_name', readonly=True, string='Parent name')
