# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_mrp_production_back_to_draft(models.Model):
    _inherit = 'mrp.production'

    def back_to_draft(self):
        self.state = 'draft'
