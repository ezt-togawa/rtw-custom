# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_international_trade(models.Model):
    _inherit = 'stock.move.line'

    packing_id = fields.Many2one("rtw_international_trade.packing", string="Packing")