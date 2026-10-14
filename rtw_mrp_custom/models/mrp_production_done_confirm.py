# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MrpProductionDoneConfirm(models.TransientModel):
    """製造の完了処理の確認ダイアログ。標準のダイアログ（即時生産・消費量の警告・バックオーダー）が
    どれも出ないときだけ表示する。"""
    _name = 'mrp.production.done.confirm'
    _description = '製造完了の確認'

    production_ids = fields.Many2many('mrp.production', string='製造オーダー', readonly=True)
    show_productions = fields.Boolean(compute='_compute_show_productions')

    @api.depends('production_ids')
    def _compute_show_productions(self):
        for wizard in self:
            wizard.show_productions = len(wizard.production_ids) > 1

    def action_confirm(self):
        self.ensure_one()
        return self.production_ids.button_mark_done()


class MrpProductionDoneConfirmMixin(models.Model):
    _inherit = 'mrp.production'

    def action_mark_done_with_confirm(self):
        """完了ボタン（フォーム・一覧）用。標準の事前チェックでダイアログやエラーが出る場合は標準の動きにして、
        どれも出ない（=確認なしで即完了してしまう）場合だけ、完了の確認ダイアログを出す。
        button_mark_done自体は変更しないため、システム内部の呼び出しや、標準ダイアログからの再実行には影響しない。"""
        if not self:
            return True
        self._button_mark_done_sanity_checks()
        if not self.env.context.get('button_mark_done_production_ids'):
            self = self.with_context(button_mark_done_production_ids=self.ids)
        res = self._pre_button_mark_done()
        if res is not True:
            return res
        wizard = self.env['mrp.production.done.confirm'].create({'production_ids': [(6, 0, self.ids)]})
        view = self.env.ref('rtw_mrp_custom.view_mrp_production_done_confirm')
        return {
            'name': '製造完了の確認',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mrp.production.done.confirm',
            'res_id': wizard.id,
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
        }
