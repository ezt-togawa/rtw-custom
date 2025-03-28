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
        if mrp:
            edit = False
            if mrp.shiratani_date != self.shiratani_date:
                mrp.shiratani_date = self.shiratani_date
                edit = True
            if mrp.estimated_shipping_date != self.order_id.estimated_shipping_date:
                mrp.estimated_shipping_date = self.order_id.estimated_shipping_date
                edit = True

            if edit:
                # 販売の白谷到着日が更新された場合、手動設定の製造側の糸島出荷日より優先するため、以下Falseに初期化しておく
                mrp.itoshima_shipping_date_edit = False
                mrp.is_active = False
                mrp._compute_itoshima_shipping_date()

        return record
