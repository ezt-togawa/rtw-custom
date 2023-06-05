# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_mrp_production_back_to_draft(models.Model):
    _inherit = 'mrp.production'

    def back_to_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        if self.state == 'draft':
            self.state = 'confirmed'
        return super(rtw_mrp_production_back_to_draft,self).action_confirm()
