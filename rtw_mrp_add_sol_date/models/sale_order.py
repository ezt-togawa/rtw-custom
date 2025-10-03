# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class MrpAddSolDateSaleOrder(models.Model):
    _inherit = "sale.order.line"

    def write(self, vals):
        record = super(MrpAddSolDateSaleOrder, self).write(vals)
        mrp = self.env['mrp.production'].search(
            [('sale_reference', '=', self.order_id.name), ('product_id', '=', self.product_id.id), ('state', '!=', 'cancel')],
            limit=1
        )
        # 紐づく製造に情報を連携する（白谷到着日、発送予定日）
        # 日付更新に伴い糸島出荷日と製造開始予定日の更新関数をCallする
        if mrp:
            edit = mrp.is_calc_date(self)
            if edit:
                # 販売の白谷到着日が更新された場合、手動設定の製造側の糸島出荷日より優先するため、以下Falseに初期化しておく
                mrp.itoshima_shipping_date_edit = False
                mrp.arrival_date_itoshima_stock_move = False
                mrp.is_active = False
                mrp.is_calc_planned_start = True
                mrp._compute_itoshima_shipping_date()

                # 紐づく配送の日付を更新する
                move_list = self.env["stock.move"].search([('mrp_production_id', '=', mrp.name)])
                if move_list:
                    move_list.write({'shiratani_date': mrp.shiratani_date})
                    move_list.write({'shiratani_date_delivery': mrp.shiratani_date})
                    move_list.write({'arrival_date_itoshima': mrp.itoshima_shipping_date})

            # ChildMo側の処理
            if edit:
                child_list = self.env["mrp.production"].search([('origin', '=', mrp.name)])
                for cmo in child_list:
                    cmo.shiratani_date = mrp.shiratani_date
                    cmo.estimated_shipping_date = mrp.estimated_shipping_date

                    # 紐づく配送の日付を更新する
                    c_move_list = self.env["stock.move"].search([('mrp_production_id', '=', cmo.name)])
                    if c_move_list:
                        c_move_list.write({'shiratani_date': cmo.shiratani_date})
                        c_move_list.write({'shiratani_date_delivery': cmo.shiratani_date})
                        c_move_list.write({'arrival_date_itoshima': cmo.itoshima_shipping_date})

        return record
