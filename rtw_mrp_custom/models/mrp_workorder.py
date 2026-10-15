# -*- coding: utf-8 -*-
from odoo import models


class MrpWorkorderCus(models.Model):
    _inherit = 'mrp.workorder'

    def write(self, values):
        # 製造開始予定日と実作業は切り離す（作業オーダーの予定開始を製造オーダーへ反映しない）
        if 'date_planned_start' in values:
            self = self.with_context(rtw_skip_mo_start_sync=True)
        return super(MrpWorkorderCus, self).write(values)
