# -*- coding: utf-8 -*-
from odoo import models


class MrpWorkorderCus(models.Model):
    _inherit = 'mrp.workorder'

    def write(self, values):
        # 製造開始予定日と実作業は切り離す（作業オーダーの予定開始を製造オーダーへ反映しない）
        if 'date_planned_start' in values:
            self = self.with_context(rtw_skip_mo_start_sync=True)
        return super(MrpWorkorderCus, self).write(values)

    def _set_qty_producing(self):
        if self.env.context.get('rtw_workorder_start'):
            return
        return super(MrpWorkorderCus, self)._set_qty_producing()

    def button_start(self):
        # 開始しても製造オーダーの完成数量・消費数量を自動入力しない（製造オーダーを「進行中」にしないため）
        return super(MrpWorkorderCus, self.with_context(rtw_workorder_start=True)).button_start()
