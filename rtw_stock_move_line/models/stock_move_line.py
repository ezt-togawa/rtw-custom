# -*- coding: utf-8 -*-

from odoo import api, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.depends('product_id', 'picking_type_use_create_lots', 'lot_id.expiration_date')
    def _compute_expiration_date(self):
        super()._compute_expiration_date()
        for move_line in self:
            if (
                not move_line.lot_id.expiration_date
                and move_line.picking_type_use_create_lots
                and move_line.product_id.use_expiration_date
                and not move_line.product_id.expiration_time
            ):
                # 有効期限の日数(expiration_time)が0(未設定)の場合、
                # 標準ロジックは「今日」をデフォルトで入れてしまうため、空欄に戻す。
                move_line.expiration_date = False

    @api.onchange('product_id', 'product_uom_id')
    def _onchange_product_id(self):
        res = super()._onchange_product_id()
        if (
            self.picking_type_use_create_lots
            and self.product_id.use_expiration_date
            and not self.product_id.expiration_time
        ):
            self.expiration_date = False
        return res
