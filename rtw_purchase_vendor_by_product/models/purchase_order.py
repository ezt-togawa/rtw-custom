# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_purchase(models.Model):
    _inherit = "purchase.order"

    @api.onchange('order_line')
    def onchange_order_line(self):
        supplier_id = False
        for line in self:
            if line.order_line:
                if line.order_line[0].product_id.seller_ids:
                    supplier_id = line.order_line[0].product_id.seller_ids[0].name.id
        if self.order_line:
            if not self.partner_id:
                self.partner_id = supplier_id
            return {'domain': {'partner_id': [('id', '=', supplier_id), '|', ('company_id', '=', False), ('company_id', '=', line.company_id)]}}
        else:
            return {'domain': {'partner_id': ['|', ('company_id', '=', False), ('company_id', '=', line.company_id)]}}
