# -*- coding: utf-8 -*-

from odoo import models, fields, api


class stock_move_rtw(models.Model):
    _inherit = "stock.move"

    depo_date = fields.Date(related="sale_line_id.depo_date")
    shiratani_date = fields.Date(related="sale_line_id.shiratani_date")
