# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_presence_person(models.Model):
    _name = 'rtw_presence.person'
    _description = 'rtw_presence.person'

    name = fields.Char('name')
    presence_person_ids = fields.One2many(comodel_name="rtw_presence.presence",
                                          inverse_name="presence_person_id",
                                          string="presence")
