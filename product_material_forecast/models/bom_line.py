# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, time
from odoo import models, fields, api


class bom_line_forecast(models.Model):
    _inherit = "mrp.bom.line"

    series = fields.Char(related='parent_product_tmpl_id.series', store=True)
    categ_id = fields.Many2one(related='parent_product_tmpl_id.categ_id', store=True)
    virtual_available = fields.Float(related='product_id.virtual_available', store=True)
