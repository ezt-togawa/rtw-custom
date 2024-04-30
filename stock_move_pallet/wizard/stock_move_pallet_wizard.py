# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PalletLoading(models.TransientModel):
    _name = 'pallet.loading'
    _description = 'Pallet Loading'

    @api.model
    def default_get(self, fields):
        res = super(PalletLoading, self).default_get(fields)
        move_line = self.env['stock.move.line'].browse(self.env.context.get('active_id')).exists()
        if move_line:
            res.update(name="%s %s" % (move_line.move_id.sale_line_id.name if move_line.move_id.sale_line_id.name else move_line.move_id.product_id.name, move_line.sale_id.name if move_line.sale_id.name else ''))
        return res

    name = fields.Char('Name', required=True )

    def pallet_loading(self):
        move_lines = self.env['stock.move.line'].browse(
            self._context.get('active_ids', []))
        # 明細チェック数確認
        print(len(self._context.get('active_ids', [])))
        if len(self._context.get('active_ids', [])) < 1:
            raise UserError(
                _('Please select at least one detail line to perform '
                  'the Register Operation.'))
        # 明細ステータス確認
        if any(move_line.state != 'assigned' for move_line in move_lines):
            raise UserError(
                _('Please select details line which are in assigned state '
                  'to perform the Register Operation.'))
        # 対象データ退避
        move_line_ids = self.env['stock.move.line'].browse(self.env.context['active_ids'])
        picking_ids = self.env['stock.picking'].browse(self.env.context['active_ids'])
        # 画面の名前取得
        for rec in self:
            new_name = rec.name
        # 新しいstock.move.pallet作成
        vals_pallet = {
            'name': new_name,
            'move_line_ids': move_line_ids,
            'picking_ids': picking_ids
        }
        new_pallet = self.env['stock.move.pallet'].create(vals_pallet)
        # move_line側のpallet_id更新
        for move_line in move_lines:
            move_line.pallet_id = new_pallet
