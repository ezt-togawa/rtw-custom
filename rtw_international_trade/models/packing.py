# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_international_trade_packing(models.Model):
    _name = 'rtw_international_trade.packing'
    _description = 'picking packing'

    name = fields.Char("Name")
    move_line_ids = fields.One2many(
        comodel_name="stock.move.line",
        inverse_name="packing_id",
        string="Move lines")
