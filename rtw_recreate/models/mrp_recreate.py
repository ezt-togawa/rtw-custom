# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class mrp_recreate(models.Model):
    _name = 'mrp.production'
    _inherit = ['mrp.production', 'recreate.mixin']

    origin_sale_line_id = fields.Many2one(
        'sale.order.line', string='元の販売明細',
        copy=False, readonly=True, index=True,
    )

    @api.model
    def create(self, values):
        production = super(mrp_recreate, self).create(values)
        if not production.origin_sale_line_id:
            production.origin_sale_line_id = production._resolve_origin_sale_line_id()
        return production

    def _resolve_origin_sale_line_id(self):
        """
        製造と対になる販売明細を特定して保持しておく
        move_dest_idsを辿り、このMOの発生元となった販売明細を特定して保存する
        """
        self.ensure_one()
        moves = self.move_dest_ids
        seen_moves = self.env['stock.move']
        while moves:
            moves = moves - seen_moves
            if not moves:
                break
            seen_moves |= moves
            with_sale_line = moves.filtered('sale_line_id')
            if with_sale_line:
                return with_sale_line[0].sale_line_id
            moves = moves.mapped('move_dest_ids')
        return False

    def action_mrp_recreate(self, from_sale=False):
        """製造オーダー側ボタン：現在の部材リスト（特注構成）から下位調達を再生成"""
        had_failure = False
        for mo in self:
            try:
                with self.env.cr.savepoint():
                    mo._recreate_single_production(from_sale=from_sale)
            except UserError as e:
                # 単体クリック（通常運用）の場合は、これまで通り即座にエラーをポップアップ表示する
                if len(self) == 1:
                    raise
                # 複数MOを一括実行した場合は、1件の失敗が他の成功分を巻き込まないよう
                # savepointでこの1件分だけ巻き戻し、エラーはチャターに記録して処理を継続する
                had_failure = True
                mo.message_post(
                    body=_(
                        "<strong>【再作成エラー】</strong><br/>"
                        "この製造オーダーの再作成に失敗しました。<br/>"
                        "理由: %s"
                    ) % (str(e)),
                    message_type='notification'
                )

        #単体クリックで失敗した場合は上でraiseするので、ここに到達するのは
        # 「全件成功」または「複数件一括実行で一部失敗」の場合のみ
        if had_failure:
            title = _("再作成: 一部失敗しました")
            message = _("失敗したMOがあります。詳細はチャターをご確認ください。")
            notif_type = 'warning'
        else:
            title = _("再作成完了")
            message = _("製造・購買・運送を再作成しました。")
            notif_type = 'success'

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': message,
                'type': notif_type,
                'sticky': had_failure,
                'next': {'type': 'ir.actions.act_window_close'},    # nextで明示的にact_window_closeを指定してリロードさせる
            }
        }

    def _recreate_single_production(self, from_sale=False):
        """action_mrp_recreateの実処理（1MO分）。savepointで囲えるよう独立したメソッドに分離"""
        self.ensure_one()
        mo = self
        original_state = mo.state

        # 連動する子製造（Sub MO）を全ステータスで特定（取消済も含む！）
        all_sub_mos = self.env["mrp.production"].search([
            ('sale_reference', '=', mo.sale_reference),
            ('origin', '=', mo.name),
            ('id', '!=', mo.id),
        ])

        # 役割に応じてレコードセットを分割する
        active_sub_mos = all_sub_mos.filtered(lambda m: m.state != 'cancel')  # メインで再利用・再確定する子製造
        canceled_sub_mos = all_sub_mos.filtered(lambda m: m.state == 'cancel')  # 掃除だけして二度と触らない残骸

        # 親MOと子MOをまとめたレコードセット（これを使うことでコードが劇的にスッキリします）
        all_mos = mo | active_sub_mos

        # 製造の進行チェック
        self._check_active_related_models(all_mos)

        # ==================================================
        # ステップ1：ドラフトに戻る前に、壊されるハズの製造/購買リンクを緊急退避！
        # ==================================================
        saved_mo_links = self._save_parent_child_mo_links(mo, active_sub_mos)
        saved_purchase_links = self._save_confirmed_purchase_links(all_mos)

        # ==================================================
        # ステップ2：親・すべての子製造の「お掃除」を一斉に実行、取消の子製造も掃除対象にしておく
        # ==================================================
        for target_mo in (all_mos | canceled_sub_mos):
            self._clean_up_related_models(target_mo)

        # ==================================================
        # ステップ3：親・子をドラフト戻し（順番考慮）
        # ==================================================
        active_sub_mos.action_return_to_draft()
        mo.action_return_to_draft()

        # 確定前に、ドラフト状態の子製造の数量を同期する（Mixin関数）
        self._sync_sub_mo_quantities_on_draft(mo, saved_mo_links)

        # ==================================================
        # ステップ4：親・子を再確定（順番考慮）
        # ※ここでOdoo標準機能により、最新のBOMと数量に基づいた「新しい未確定PO」が生まれます
        # ==================================================
        mo.action_confirm()
        active_sub_mos.action_confirm()

        # ==================================================
        # ステップ5：親を起点とした重複整理（新しく湧いた不要な子製造を消す、孫製造はない前提）
        # ==================================================
        self._clean_up_duplicate_models(mo)

        # ==================================================
        # 拡張ステップ6：リンク復元、バラバラにされた製造と確定購買との紐づけもどし
        # ※ここで子の数量も親に合わせて自動追従します
        # ==================================================
        self._restore_parent_child_mo_links(mo, saved_mo_links)
        self._restore_confirmed_purchase_links(mo, saved_purchase_links)

        # ==================================================
        # ステップ7：リンク復元（数量変更）によって子製造の下に湧いたゴミPOの掃除
        # ==================================================
        for sub_mo in active_sub_mos:
            self._clean_up_duplicate_models(sub_mo)

        # ==================================================
        # ★追加：販売明細の write トリガーを引いて、日付を再計算させる
        # ==================================================
        so = self.env['sale.order'].search([('name', '=', mo.origin)], limit=1)
        if so:
            # このMOに紐づく販売明細を取得
            target_line = so.get_sale_order_line_from_mrp(mo)

            if target_line:
                trigger_vals = {}
                if hasattr(target_line, 'depo_date'):
                    trigger_vals['depo_date'] = target_line.depo_date
                if hasattr(target_line, 'shiratani_date'):
                    trigger_vals['shiratani_date'] = target_line.shiratani_date
                if hasattr(target_line, 'estimated_shipping_date'):
                    trigger_vals['estimated_shipping_date'] = target_line.estimated_shipping_date

                if trigger_vals:
                    target_line.write(trigger_vals)

        # 元の状態をキープ（親がドラフトだった場合）
        if original_state == 'draft':
            mo.action_return_to_draft()

        # ==================================================
        # チャターへの再作成ログの投稿
        # ==================================================
        # 連動した子製造の名前をカンマ区切りで取得
        if not from_sale:
            sub_mo_names = ", ".join(active_sub_mos.mapped('name')) if active_sub_mos else _("なし")

            # 投稿するメッセージの作成（HTMLタグが使えます）
            log_message = _(
                "<strong>【再作成の実行】</strong><br/>"
                "製造オーダーの再作成処理が実行されました。<br/>"
                "・関連子製造: %s"
            ) % (sub_mo_names)

            # 親MOのチャターにログを投稿（通知は飛ばさず、単なるログとして記録）
            mo.message_post(body=log_message, message_type='notification')

    def write(self, vals):
        res = super(mrp_recreate, self).write(vals)

        # 処理後に、紐づく販売明細のボタン表示判定値のキャッシュをクリア
        for mo in self:
            if mo.order_line:
                mo.order_line.modified(['has_recreate_mo'])

        return res
