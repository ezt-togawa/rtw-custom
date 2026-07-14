# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class sale_line_recreate(models.Model):
    _name = 'sale.order.line'
    _inherit = ['sale.order.line', 'recreate.mixin']

    has_recreate_mo = fields.Boolean(compute='_compute_has_recreate_mo', string='再作成可能な製造あり')
    is_recreate_needed = fields.Boolean(string='要再作成', default=False)

    @api.depends('product_id', 'state', 'order_id.state')
    def _compute_has_recreate_mo(self):
        """この販売明細に対して、ボタンを表示すべきか判定"""
        for line in self:
            # Configurator製品ではない（config_ok == False）、BOMがない（購買のみで完結する製品）、または見積状態ならスキップ
            line.has_recreate_mo = bool(
                line.config_ok and line.product_id.bom_ids and line.order_id.state in ['sale', 'done']
            )

    def action_sale_line_recreate(self):
        """販売明細側ボタン：仕様変更等を反映するため、既存MOを破棄し完全新規で作り直す"""
        had_failure = False
        for line in self:
            try:
                with self.env.cr.savepoint():
                    line._recreate_single_sale_line()
            except UserError as e:
                # 単体クリック（通常運用）の場合は、これまで通り即座にエラーをポップアップ表示する
                if len(self) == 1:
                    raise
                # 複数明細を一括実行した場合は、1明細の失敗が他の成功分を巻き込まないよう
                # savepointでこの明細分だけ巻き戻し、エラーはチャターに記録して処理を継続する
                had_failure = True
                line.order_id.message_post(
                    body=_(
                        "<strong>【再作成エラー】</strong><br/>"
                        "販売明細「%s」の再作成に失敗しました。<br/>"
                        "理由: %s"
                    ) % (line.product_id.display_name, str(e)),
                    message_type='notification'
                )

        # 単体クリックで失敗した場合は上でraiseするので、ここに到達するのは
        # 「全件成功」または「複数件一括実行で一部失敗」の場合のみ
        if had_failure:
            title = _("再作成: 一部失敗しました")
            message = _("失敗した明細があります。詳細はチャターをご確認ください。")
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

    def _recreate_single_sale_line(self):
        """action_sale_line_recreateの実処理（1明細分）。savepointで囲えるよう独立したメソッドに分離"""
        self.ensure_one()
        line = self

        # 親製造取得（全ステータス）
        parent_mos = line._find_parent_productions_for_sale_line(line)
        all_related_mos = parent_mos

        # 親製造のそれぞれに対して、紐づく「すべての子製造」も検索して合流
        for pm in parent_mos:
            sub_mos = self.env["mrp.production"].search([
                ('sale_reference', '=', pm.sale_reference),
                ('origin', '=', pm.name),
                ('id', '!=', pm.id),
            ])
            all_related_mos |= sub_mos

        # 進行中・完了済みのMOがないか安全チェック（Mixinの共通機能をそのまま利用！）
        line._check_active_related_models(all_related_mos)

        # 未着手の有効なMOを保持しておく（メッセージ用）
        active_mos = parent_mos.filtered(lambda m: m.state != 'cancel')

        # 確定済み（発注済み）の購買が旧製造に紐づいている場合の通知処理
        # ※MO側の再作成（action_mrp_recreate）は同じMOレコードを再確定するだけなので、紐づいたまま残る
        confirmed_purchase_orders = self.env['purchase.order']
        # 確定購買に紐づくpickingは保護対象として控えておき、後で取消されていたら元に戻す
        protected_pickings = self.env['stock.picking']
        for target_mo in all_related_mos:
            confirmed_po_lines = self.env['purchase.order.line'].search([
                ('order_id.origin', '=', target_mo.name),
                ('order_id.state', 'in', ['purchase', 'done'])
            ])
            confirmed_pos = confirmed_po_lines.mapped('order_id')
            confirmed_purchase_orders |= confirmed_pos
            protected_pickings |= confirmed_pos.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel'))

        # 親子製造に対して製造をすべて取消し＆掃除
        # 手動取消の製造があることも考慮して全製造に対して掃除を考慮する
        for target_mo in all_related_mos:
            line._clean_up_related_models(target_mo)
            # MO本体をキャンセル
            target_mo.action_cancel()

        # action_cancel()の副作用で確定購買の入荷Pickingが誤って取消されていた場合は元の状態に戻す
        for pick in protected_pickings:
            if pick.state == 'cancel':
                pick.action_back_to_draft()
                pick.action_confirm()

        # 販売明細に紐づく「出荷明細(stock.move)」をキャンセルして手配残をリセット
        # この処理を実施していないと後続の_action_launch_stock_ruleで処理されない
        active_moves = line.move_ids.filtered(lambda m: m.state != 'cancel')
        if active_moves:
            active_moves._action_cancel()

        # Odoo標準のエンジンをキックし、最新の属性仕様で新しい製造・出荷を再生成！
        # ※sale_sourced_by_line（odoo-custom）の_prepare_procurement_valuesは、
        #   line.date_plannedが残っているとPikingの予定日に利用されてしまうので計算中のみクリアしておく
        original_date_planned = line.date_planned
        line.write({'date_planned': False})
        line._action_launch_stock_rule()
        if original_date_planned:
            line.write({'date_planned': original_date_planned})

        # =========================================================================
        # 既存の「write」メソッドをダミーキックして、各種日付を新MOに伝播させる
        # =========================================================================
        # depo_date等のキーが vals に含まれていないと作動しないロジックがあるため、
        # 明細が持っている現在の日付をそのまま write に渡してトリガーを引く
        trigger_vals = {}
        if hasattr(line, 'depo_date'):
            trigger_vals['depo_date'] = line.depo_date
        if hasattr(line, 'shiratani_date'):
            trigger_vals['shiratani_date'] = line.shiratani_date
        if hasattr(line, 'estimated_shipping_date'):
            trigger_vals['estimated_shipping_date'] = line.estimated_shipping_date

        if trigger_vals:
            # 販売明細の write メソッドを実行させる（class MrpAddSolDateSaleOrder 内のWrite）
            # キャンセルされずに生き残っている「新規作成されたMO」に対して完璧に日付が計算・同期されます！
            line.write(trigger_vals)

        # 再作成が完了したら、用更新フラグをOFFに戻す
        line.is_recreate_needed = False

        # 販売オーダーのチャターにログを残す
        # 確定済み購買（子製造分も含む）が残っている場合は、同じメッセージに追記する（自動付け替えはしない）
        old_mo_names = ", ".join(active_mos.mapped('name')) if active_mos else _("なし")
        log_lines = [
            _("<strong>【製造オーダー新規再作成】</strong>"),
            _("販売明細「%s」の製造オーダーを新規作成しました。") % line.product_id.display_name,
            _("・取消した旧製造：%s") % old_mo_names,
        ]
        if confirmed_purchase_orders:
            # data-oe-id/data-oe-model属性付きリンクにすると、チャター上でクリックして
            # そのまま購買オーダーのフォームを開ける（Odoo標準のメッセージ内リンクの仕組み）
            po_links = ", ".join(
                '<a href="#" data-oe-id="%d" data-oe-model="purchase.order">%s</a>' % (po.id, po.name)
                for po in confirmed_purchase_orders
            )
            log_lines.append(_("・確定済み購買：%s") % po_links)
            log_lines.append(_("※確定済み購買については重複して新購買が出来ている可能性があるためご確認ください。"))
        line.order_id.message_post(body="<br/>".join(log_lines), message_type='notification')

    def write(self, vals):
        """
        保存時、特定のフィールドに変更があったかを監視してフラグを立てる
        監視するトリガー項目：数量、製品バリアント、倉庫(製造工場)
        ※確定済み（sale/done）の受注に対する変更だけを「要再作成」として検知する。
        """
        trigger_fields = {'product_uom_qty', 'product_id', 'warehouse_id'}

        """
        数量変更を検知した場合、裏側で「今は保存ボタンからの自動処理だよ」
        という秘密のチケット（コンテキスト）を持たせて標準の保存処理を呼ぶ
        """
        if 'product_uom_qty' in vals and any(line.order_id.state in ['sale', 'done'] for line in self):
            self = self.with_context(skip_auto_procurement_on_write=True)

        if any(key in vals for key in trigger_fields) and 'is_recreate_needed' not in vals:
            confirmed_lines = self.filtered(lambda line: line.order_id.state in ['sale', 'done'])
            other_lines = self - confirmed_lines
            res = True
            if confirmed_lines:
                res = super(sale_line_recreate, confirmed_lines).write(dict(vals, is_recreate_needed=True)) and res
            if other_lines:
                res = super(sale_line_recreate, other_lines).write(vals) and res
            return res

        return super(sale_line_recreate, self).write(vals)

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        """
        Odoo標準の調達エンジンをフックし、条件付きで自動発番をスキップする
        """
        # 保存ボタン（write）から自動的に呼び出された場合のみ関所を発動
        if self.env.context.get('skip_auto_procurement_on_write'):
            lines_to_procure = self.env['sale.order.line']

            for line in self:
                # 製造対象の明細は、再作成ボタンの手動運用に任せるため自動処理をスキップ！
                if line.config_ok and line.product_id.bom_ids:
                    continue
                # BOMがない通常の商品やconfig_okでも仕入商品は、標準仕様通り追加の出荷準備をさせる
                lines_to_procure |= line

            # もし全明細がスキップ対象（製造品）なら、ここで何もせずに終了
            if not lines_to_procure:
                return True

            # 通常商品が混ざっていた場合のみ、それらだけ標準エンジンに渡す
            return super(sale_line_recreate, lines_to_procure)._action_launch_stock_rule(previous_product_uom_qty=previous_product_uom_qty)

        # 最初の受注確定ボタンや、「再作成ボタン」から手動で呼ばれた時は、コンテキストがないため、通常の調達エンジンが走ります
        return super(sale_line_recreate, self)._action_launch_stock_rule(previous_product_uom_qty=previous_product_uom_qty)
