# -*- coding: utf-8 -*-

from odoo import models, fields, api

class rtw_popup_set_item_location_move(models.Model):
    _inherit = 'stock.move'
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

class rtw_popup_set_item_location_picking(models.Model):
    _inherit = "stock.picking"
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