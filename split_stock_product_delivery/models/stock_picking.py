# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def btn_split_delivery(self):
        for record in self:
            # 詳細オペレーションのSplit基準に分割
            if record.move_line_ids_without_package:
                cnt = 0
                for rec in record.move_line_ids_without_package:
                    if rec.split:
                        cnt += 1
                if cnt >= 1:
                    quotation_id = self.copy()
                    if quotation_id:
                        for new_move_line in quotation_id.move_line_ids_without_package:
                            if not new_move_line.split:
                                new_move_line.unlink()
                                move_id = new_move_line.move_id
                                # オペレーション明細もmove_idで削除
                                for new_move in quotation_id.move_ids_without_package:
                                    if new_move.move_id == move_id:
                                        new_move.unlink()
                            else:
                                new_move_line.split = False
                    for move_line in record.move_line_ids_without_package:
                        if move_line.split:
                            self.env['stock.move.line'].browse(move_line.id).unlink()
                            move_id = move_line.move_id
                            # オペレーション明細もmove_idで削除
                            for move in record.move_ids_without_package:
                                if move.move_id == move_id:
                                    self.env['stock.move'].browse(move.id).unlink()
                else:
                    raise ValidationError(_('Please Select Product To Split'))

    # def btn_split_delivery(self):
    #     for record in self:
    #         # 詳細オペレーションのSplit基準に分割
    #         if record.move_line_ids_without_package:
    #             cnt = 0
    #             for rec in record.move_line_ids_without_package:
    #                 if rec.split:
    #                     cnt += 1
    #             if cnt >= 1:
    #                 quotation_id = self.copy()
    #                 if quotation_id:
    #                     for new_move_line in quotation_id.move_line_ids_without_package:
    #                         if not new_move_line.split:
    #                             new_move_line.unlink()
    #                         else:
    #                             new_move_line.split = False
    #                 for move_line in record.move_line_ids_without_package:
    #                     if move_line.split:
    #                         self.env['stock.move.line'].browse(move_line.id).unlink()
    #             else:
    #                 raise ValidationError(_('Please Select Product To Split'))




