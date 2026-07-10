# -*- coding: utf-8 -*-

from odoo import models, api, _, fields
from odoo.exceptions import UserError


class recreate_mixin(models.AbstractModel):
    _name = 'recreate.mixin'
    _description = '再作成共通ロジック'

    def _check_active_related_models(self, productions):
        """製造オーダーの進捗チェック"""
        active_mos = productions.filtered(lambda m: m.state in ['progress', 'to_close', 'done'] or m.mrp_order_status)
        if active_mos:
            raise UserError(
                _("発注済や進行中、完了済みの製造オーダー (%s) があるため再作成できません。手動で取消や未発注にさせてから実行してください。") % ", ".join(
                    active_mos.mapped('name')))

    def _clean_up_related_models(self, mo):
        """
        購買・運送・配送クリアの共通処理
        - mo: 起点となる親製造オーダー
        """
        # 製造オーダーに紐づく配送（Move）を直接検索
        related_moves = self.env['stock.move'].search([
            ('origin', '=', mo.name)
        ])

        # 製造オーダー起点での運送（Picking）のお掃除
        mo_pickings = related_moves.mapped('picking_id').filtered(lambda p: p.state not in ['done', 'cancel'])
        if mo_pickings:
            # 運送（Picking）自体も、完了・取消以外ならキャンセル（または条件が許せば削除）
            for pick in mo_pickings:
                pick.action_cancel()

        # 未確定の購買（下書き・送信済PO）のお掃除
        draft_pos_lines = self.env['purchase.order.line'].search([
            ('order_id.origin', '=', mo.name),
            ('order_id.state', 'in', ['draft', 'sent'])
        ])
        purchase_orders = draft_pos_lines.mapped('order_id')

        for po in purchase_orders:
            pickings = self.env['stock.picking'].search([
                '|',
                ('group_id.name', '=', po.name),
                ('origin', '=', po.name),
                ('state', 'not in', ['done', 'cancel'])
            ])

            if pickings:
                pickings.mapped('move_ids').filtered(lambda m: m.state != 'done')._action_cancel()

            po_live_moves = po.order_line.mapped('move_ids').filtered(lambda m: m.state not in ['done', 'cancel'])
            if po_live_moves:
                po_live_moves._action_cancel()

            po.button_cancel()
            po.unlink()
            for pick in pickings:
                if not pick.move_ids:
                    pick.unlink()

    def _save_confirmed_purchase_links(self, mos):
        """
        製造と確定購買が結ばれている情報を退避する
        """
        saved_links = []
        for mo in mos:
            # この製造オーダーの名前を起点に、すでに確定している購買明細を検索
            confirmed_po_lines = self.env['purchase.order.line'].search([
                ('order_id.origin', '=', mo.name),
                ('order_id.state', 'in', ['purchase', 'done'])
            ])

            for po_line in confirmed_po_lines:
                # 購買明細が裏で持っている、入荷側（製造側）への在庫移動（Move）を特定
                po_moves = po_line.move_ids.filtered(lambda m: m.state != 'cancel')
                for po_move in po_moves:
                    # この確定購買のMoveが、製造側のどの製品（Product）の、どの完成品/部材移動と結ばれていたかを記憶
                    # (OdooのMTOは move_dest_ids や move_orig_ids で双方向につながっています)
                    for dest_move in po_move.move_dest_ids:
                        saved_links.append({
                            'mo_name': mo.name,
                            'product_id': po_line.product_id.id,
                            'po_move_id': po_move.id,
                            'mo_move_id': dest_move.id
                        })
        return saved_links

    def _save_parent_child_mo_links(self, mo, sub_mos):
        """再作成前に、親製造の部材と、各子製造の完成品Moveのリンクを退避する"""
        mo_links = []
        parent_raw_moves = mo.move_raw_ids.filtered(lambda m: m.state != 'cancel')

        for sub_mo in sub_mos:
            sub_finished_moves = sub_mo.move_finished_ids.filtered(lambda m: m.state != 'cancel')
            for sf_move in sub_finished_moves:
                # Odoo14標準のMTO親子関係（親の元の移動元が子製造の完成品Moveであること）に条件をクリーン化
                connected_parent_moves = parent_raw_moves.filtered(
                    lambda pm: sf_move.id in pm.move_orig_ids.ids
                )

                # Moveの鎖がすでに不安定な場合のセーフティネット（プロダクトID一致）
                if not connected_parent_moves:
                    connected_parent_moves = parent_raw_moves.filtered(
                        lambda pm: pm.product_id.id == sf_move.product_id.id)

                for pm_move in connected_parent_moves:
                    # 使わなくなった古いグループ退避データを綺麗に撤廃し、最小限に集約！
                    mo_links.append({
                        'sub_mo_id': sub_mo.id,
                        'product_id': sf_move.product_id.id,
                        'sub_move_id': sf_move.id
                    })
        return mo_links

    def _restore_confirmed_purchase_links(self, mo, saved_links):
        """
        再確定後に、製造とバラバラになった確定購買とのリンクを再設定する
         引数 saved_links：_save_confirmed_purchase_linksで保持した情報
        """
        # 親MOおよび、生き残った古い子製造をすべて集める
        all_mos = mo | self.env['mrp.production'].search([
            ('origin', '=', mo.name),
            ('state', 'not in', ['draft', 'cancel']),
            ('id', '!=', mo.id)
        ])

        for link in saved_links:
            # 退避しておいた情報をもとに、生き残った製造オーダーの中から該当する部材のMove（新しいMove）を探し出す
            target_mo = all_mos.filtered(lambda m: m.name == link['mo_name'])
            if not target_mo:
                continue

            # 製造側の該当する製品の在庫移動（Move）を特定
            # (部材としての移動、または完成品としての移動から探します)
            mo_moves = (target_mo.move_raw_ids | target_mo.move_finished_ids).filtered(
                lambda m: m.product_id.id == link['product_id'] and m.state != 'cancel'
            )

            # 発注済みの購買側のMoveオブジェクトを取得
            po_move = self.env['stock.move'].browse(link['po_move_id'])

            if mo_moves and po_move.exists():
                for m_move in mo_moves:
                    # 製造側のMoveと確定購買側のMoveを、Odooの結合配列コマンドを使ってガチッと手動リンク！
                    m_move.write({'move_orig_ids': [(4, po_move.id, 0)]})
                    po_move.write({'move_dest_ids': [(4, m_move.id, 0)]})

                # 購買側のMoveが所属している入荷伝票（Picking）を特定
                pick = po_move.picking_id

                # もしOdooの連動によって、この入荷伝票が「cancel」に落とされていたら
                if pick and pick.state == 'cancel':
                    # ドラフトに戻す
                    pick.action_back_to_draft()

                    # 手動の「処理準備（Mark as To Do）」ボタンの標準処理を呼び出す
                    pick.action_confirm()

    def _restore_parent_child_mo_links(self, mo, mo_links):
        """再確定後、切れた古い子製造のリンクと調達グループを完璧に復元する"""
        # 親の最新の部材Move
        parent_raw_moves = mo.move_raw_ids.filtered(lambda m: m.state != 'cancel')

        for link in mo_links:
            sub_move = self.env['stock.move'].browse(link['sub_move_id'])
            target_parent_move = parent_raw_moves.filtered(
                lambda m: m.product_uom_qty > 0 and m.product_id.id == link['product_id'])

            if sub_move.exists() and target_parent_move:
                # 自動生成された新しいゴミリンクの解除 ＆ 本物子製造のMoveとの再結合
                for pm_move in target_parent_move:
                    pm_move.write({'move_orig_ids': [(5, 0, 0)]})
                    pm_move.write({'move_orig_ids': [(4, sub_move.id, 0)]})
                    sub_move.write({'move_dest_ids': [(4, pm_move.id, 0)]})

                    # 親の新しい部材Moveに対して「子製造」セットする（製造のドラフト化にともない消えてしまうことがありそうなので）
                    pm_move.write({
                        'created_production_id': link['sub_mo_id']
                    })

    def _clean_up_duplicate_models(self, mo):
        """
        確定購買がある場合の「重複した購買を削除」＆「sale_order_ids復元」
        合わせて重複した子製造も整理する
        - mo: 起点となる親製造オーダー（※親MO再確定の直後にCallされる前提）
        """
        # 親の構成から削除、または数量0になった子製造を一旦取消にする
        # 現在の親製造が「本当に必要としている部材のプロダクトIDリスト」(数量が0より大きいもの)
        active_product_ids = mo.move_raw_ids.filtered(lambda m: m.product_uom_qty > 0).mapped('product_id.id')

        # この親製造に紐づいている子製造（完了・取消・下書き 以外）を検索
        all_current_sub_mos = self.env['mrp.production'].search([
            ('origin', '=', mo.name),
            ('state', 'not in', ['draft', 'cancel']),
            ('id', '!=', mo.id)
        ])

        for sub_mo in all_current_sub_mos:
            # もし子製造のプロダクトが、現在の親の必要部材リストに入っていなければ「不要」と判断
            if sub_mo.product_id.id not in active_product_ids:
                # 紐づく未確定の購買や運送（Picking）、配送（Move）を根こそぎクリア
                self._clean_up_related_models(sub_mo)
                # 子製造本体は「一旦取消」までにする（削除はしない）
                sub_mo.action_cancel()

        # 新しく重複してできてしまった「確認済(confirmed)の子製造」とその下位調達を完全消去
        # この親製造（origin = mo.name）に紐づく、現在「confirmed」の子製造をすべて検索
        all_sub_mos = self.env['mrp.production'].search([
            ('origin', '=', mo.name),
            ('state', '=', 'confirmed'),
            ('id', '!=', mo.id)
        ], order='id asc')  # IDが古い順（作成順）に並べる

        # 製品（Product）ごとにグループ分け
        product_mo_map = {}
        for sub_mo in all_sub_mos:
            if sub_mo.product_id.id not in product_mo_map:
                product_mo_map[sub_mo.product_id.id] = []
            product_mo_map[sub_mo.product_id.id].append(sub_mo)

        garbage_mo_names = []
        # 同じ製品の子製造が2つ以上あれば、後からできた新しい方をクリア
        for product_id, mos in product_mo_map.items():
            if len(mos) > 1:
                # mos[0] は確定購買と繋がっている「古い本物」なので残す
                # mos[1:] は再確定で新しくできてしまった「重複したゴミ」
                for duplicate_mo in mos[1:]:
                    garbage_mo_names.append(duplicate_mo.name)

                    # 新しくできた重複子製造紐づく情報のクリア
                    self._clean_up_related_models(duplicate_mo)

                    # チャターにログメッセージを出さないように設定＆重複製造の本体を消去
                    duplicate_mo.action_cancel()
                    duplicate_mo.unlink()

            # すべての削除MOの破棄処理が完全に完了し、Odooが例外ログを出し尽くしたこのタイミングで、
            # 溜めておいた削除MO名が含まれる例外活動（Picking側もMO側もすべて）を一網打尽にする！
            if garbage_mo_names:
                # 検索ドメインを「いずれかのゴミMO名が含まれるもの」という形に動的生成
                name_domains = ['|' for _ in range(len(garbage_mo_names) * 2 - 1)]
                for name in garbage_mo_names:
                    name_domains.extend([('summary', 'like', name), ('note', 'like', name)])

                target_garbage_activities = self.env['mail.activity'].search([('activity_type_id.name', 'like', '例外')] + name_domains)
                if target_garbage_activities:
                    target_garbage_activities.unlink()

        # 親MO画面の sale_reference から、大元の販売オーダ（SO）を逆引きする準備
        so_record = False
        if mo.sale_reference:
            so_record = self.env['sale.order'].search([('name', '=', mo.sale_reference)], limit=1)

        # この製造オーダー単体（mo.name）から新しくできてしまった下書きPO明細を検索
        new_draft_po_lines = self.env['purchase.order.line'].search([
            ('order_id.origin', '=', mo.name),
            ('order_id.state', '=', 'draft')
        ])

        for po_line in new_draft_po_lines:
            # すでに過去の発注確定済（purchase/done）の購買が「全く同じ製造起点」で存在するかチェック
            already_confirmed_line = self.env['purchase.order.line'].search([
                ('product_id', '=', po_line.product_id.id),
                ('order_id.origin', '=', mo.name),
                ('order_id.state', 'in', ['purchase', 'done'])
            ], limit=1)

            if already_confirmed_line:
                confirmed_po = already_confirmed_line.order_id

                # sale_order_ids の再設定
                if not confirmed_po.sale_order_ids and so_record:
                    confirmed_po.write({
                        'sale_order_ids': mo.sale_reference
                    })

                # 重複した下書きを削除
                po_id = po_line.order_id
                po_line.unlink()
                if not po_id.order_line:
                    po_id.button_cancel()
                    po_id.unlink()

    def _find_parent_productions_for_sale_line(self, line):
        """
        販売明細から実際に生成された親製造オーダーを特定する（掃除・取消の対象を探すため）。
        origin_sale_line_id（MO作成時、まだMoveの連鎖が新鮮なうちに確定・保存した紐づき）で検索する。
        - line: 対象の販売明細（sale.order.line）
        """
        real_line_id = line._origin.id or line.id

        return self.env['mrp.production'].search([
            ('origin_sale_line_id', '=', real_line_id),
        ])

    def _sync_sub_mo_quantities_on_draft(self, mo, mo_links):
        """確定前（ドラフト状態）に、子製造の本体数量を親の要求数に同期する。
        これにより、再確定時にOdooが正しい数量で下書きPOを自動生成してくれます。
        """
        parent_raw_moves = mo.move_raw_ids.filtered(lambda m: m.state != 'cancel')

        for link in mo_links:
            target_parent_move = parent_raw_moves.filtered(
                lambda m: m.product_uom_qty > 0 and m.product_id.id == link['product_id'])

            if target_parent_move:
                new_required_qty = target_parent_move[0].product_uom_qty
                sub_mo = self.env['mrp.production'].browse(link['sub_mo_id'])

                if sub_mo.exists() and sub_mo.product_qty != new_required_qty:
                    # ゼロ除算エラー防止
                    if sub_mo.product_qty > 0:
                        # 1. 変更比率（factor）を計算し、カスタム関数を明示的にCall（構成品を最新化！）
                        factor = new_required_qty / sub_mo.product_qty
                        sub_mo._update_raw_moves(factor)

                    # 2. 子製造本体の数量をアップデート
                    sub_mo.write({'product_qty': new_required_qty})