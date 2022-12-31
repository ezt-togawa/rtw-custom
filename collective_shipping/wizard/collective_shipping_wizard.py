# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class CollectiveShipping(models.TransientModel):
    _name = 'collective.shipping'
    _description = 'Collective Shipping'

    def collective_shipping(self):
        move_lines = self.env['stock.move.line'].browse(
            self._context.get('active_ids', []))
        # 明細チェック数確認
        if len(self._context.get('active_ids', [])) < 2:
            raise UserError(
                _('Please select atleast two details line to perform '
                  'the Merge Operation.'))
        # 明細ステータス確認
        if any(move_line.state != 'assigned' for move_line in move_lines):
            raise UserError(
                _('Please select details line which are in assigned state '
                  'to perform the Merge Operation.'))
        # 明細移動元・移動先確認
        location_id = move_lines[0].location_id.id
        if any(move_line.location_id.id != location_id for move_line in move_lines):
            raise UserError(
                _('Please select details line whose Location are same to '
                  ' perform the Merge Operation.'))
        location_dest_id = move_lines[0].location_dest_id.id
        if any(move_line.location_dest_id.id != location_dest_id for move_line in move_lines):
            raise UserError(
                _('Please select details line whose Location Dest are same to '
                  ' perform the Merge Operation.'))
        picking_type_id = move_lines[0].picking_id.picking_type_id.id
        if any(move_line.picking_id.picking_type_id.id != picking_type_id for move_line in move_lines):
            raise UserError(
                _('Please select details line whose Picking Type are same to '
                  ' perform the Merge Operation.'))
        partner_id = move_lines[0].picking_id.partner_id.id
        if any(move_line.picking_id.partner_id.id != partner_id for move_line in move_lines):
            raise UserError(
                _('Please select details line whose Partner are same to '
                  ' perform the Merge Operation.'))
        company_id = move_lines[0].picking_id.company_id.id
        if any(move_line.picking_id.company_id.id != company_id for move_line in move_lines):
            raise UserError(
                _('Please select details line whose Company are same to '
                  ' perform the Merge Operation.'))
        move_type = move_lines[0].picking_id.move_type
        # 新しいstock.picking作成
        vals_picking = {
            'partner_id': partner_id,
            'location_id': location_id,
            'location_dest_id': location_dest_id,
            'picking_type_id': picking_type_id,
            'move_type': move_type
        }
        new_picking = self.env['stock.picking'].create(vals_picking)
        for move_line in move_lines:
            # 前のpicking_idを退避
            old_picking_id_id = move_line.picking_id.id
            # 対象のstock.moveとstock.move.lineのpicking_idを新しいpicking_idに更新
            move_line.picking_id = new_picking
            move_line.move_id.picking_id = new_picking
            # 対象のpickingを更新
            old_picking_id = self.env['stock.picking'].search([('id', '=', old_picking_id_id)])
            for record in old_picking_id:
                record.write({
                    'state': record.state
                })
        # 新しいpickingを更新 ※stock.moveとstock.move.lineの情報を紐づけるため
        new_picking_id = self.env['stock.picking'].search([('id', '=', new_picking.id)])
        for record in new_picking_id:
            record.write({
                'state': record.state
            })



