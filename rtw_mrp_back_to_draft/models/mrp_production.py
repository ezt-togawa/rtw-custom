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

    @api.depends(
        'move_raw_ids.state', 'move_raw_ids.quantity_done', 'move_finished_ids.state',
        'workorder_ids', 'workorder_ids.state', 'product_qty', 'qty_producing')
    def _compute_state(self):
      for production in self:
          if production.state == 'draft':
              return
      return super(rtw_mrp_production_back_to_draft,self)._compute_state()
