# -*- coding: utf-8 -*-

from odoo import models, fields, api

class rtw_mrp_calendar_rename(models.Model):
    _inherit = 'mrp.workorder'

    def name_get(self):
        res = []
        # 製造オーダーの数量をタイトルの後ろに追加
        for wo in self:
            if len(wo.production_id.workorder_ids) == 1:
                res.append((wo.id, "%s - %s - %s - %s" % (wo.production_id.name, wo.product_id.name, wo.name,
                                                          wo.production_id.product_qty)))
            else:
                res.append((wo.id, "%s - %s - %s - %s - %s" % (
                wo.production_id.workorder_ids.ids.index(wo._origin.id) + 1, wo.production_id.name, wo.product_id.name,
                wo.name, wo.production_id.product_qty)))
        return res
