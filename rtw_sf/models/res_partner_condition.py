# Copyright (C) 2021 Picg

from odoo import api, fields, models


class ShipsShip(models.Model):
    _name = "res.partner.condition"
    _description = "condition"
    _rec_name = "name"

    name = fields.Char(required=True, )
    archive = fields.Boolean()
    color = fields.Integer()
