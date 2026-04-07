# -*- coding: utf-8 -*-

from odoo import models, fields, api

class rtw_mrp_production(models.Model):
    _inherit = 'mrp.production'

    def create_location_item_excel_prod_label(self):
        # 既存レコードを取得（なければ作る）
        rec = self.env['mrp.location_item_excel_prod_label'].get_singleton()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.location_item_excel_prod_label',
            'view_mode': 'form',
            'res_id': rec.id,  # ← ここがポイント
            'target': 'new',
        }