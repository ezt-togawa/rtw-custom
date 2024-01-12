# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_order_remark(models.Model):
    _inherit = "sale.order"

    witness = fields.Char('搬入立会人', default=None)
    witness_phone = fields.Char('立会人連絡先', default=None)

