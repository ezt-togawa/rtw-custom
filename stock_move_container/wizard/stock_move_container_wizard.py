# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ContainerLoading(models.TransientModel):
    _name = 'container.loading'
    _description = 'Container Loading'

    def container_loading(self):
        move_pallets = self.env['stock.move.pallet'].browse(
            self._context.get('active_ids', []))
        # 明細チェック数確認
        if len(self._context.get('active_ids', [])) < 1:
            raise UserError(
                _('Please select at least one detail line to perform '
                  'the Register Operation.'))
        # move_line明細ステータス確認
        # if any(move_pallet.move_line_ids.state != 'assigned' for move_pallet in move_pallets):
        #     raise UserError(
        #         _('Please select details line which are in assigned state '
        #           'to perform the Register Operation.'))
        # 対象データ退避
        pallet_ids = self.env['stock.move.pallet'].browse(self.env.context['active_ids'])
        # picking_ids = self.env['stock.picking'].browse(self.env.context['active_ids'])
        # 名前取得
        new_name = self.env['ir.sequence'].next_by_code('stock.move.container') or 'New'
        # 新しいstock.move.container作成
        vals_container = {
            'name': new_name,
            'pallet_ids': pallet_ids
        }
        new_container = self.env['stock.move.container'].create(vals_container)
        # move_pallet側のcontainer_id更新
        for move_pallet in move_pallets:
            move_pallet.container_id = new_container
