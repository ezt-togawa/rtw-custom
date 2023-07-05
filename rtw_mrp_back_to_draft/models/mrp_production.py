# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_mrp_production_back_to_draft(models.Model):
    _inherit = 'mrp.production'

    def back_to_draft(self):
        self.state = 'draft'
        for move in self.move_raw_ids:
            move.state = 'draft'

    def action_confirm(self):
        for production in self:
            if production.state == 'draft':
                production.state = 'confirmed'
            return super(rtw_mrp_production_back_to_draft,self).action_confirm()

    def action_cancel(self):
        for production in self:
            if production.state == 'draft':
                production.state = 'cancel'
            return super(rtw_mrp_production_back_to_draft,self).action_cancel()
