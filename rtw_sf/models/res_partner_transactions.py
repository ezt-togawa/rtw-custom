# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_sf_partner_transactions(models.Model):
    _name = 'res.partner.transactions'
    _description = 'rtw_sf.transactions'
    _rec_name = "name"

    name = fields.Char('Transactions', translate=True)
