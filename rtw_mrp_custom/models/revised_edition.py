# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_mrp_revised_edition(models.Model):
    _name = 'mrp.revised_edition'
    _description ='revised_edition'
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]
    _description = 'revised edition'
    _rec_name = "name"

    name = fields.Char('Title')
    description = fields.Char('Description')
    mrp_id = fields.Many2one('mrp.production', string="MRP order")
    date = fields.Date(
        required=True,
        tracking=True,
        default=fields.Date.context_today)
    owner_id = fields.Many2one('res.users', 'OwnerId', default=lambda self: self.env.user)
    confirmation = fields.Boolean("confirmation")
