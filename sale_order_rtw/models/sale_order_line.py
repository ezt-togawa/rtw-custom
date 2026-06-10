# -*- coding: utf-8 -*-

from odoo import models, fields, api
from lxml import etree


class sale_order_line_rtw(models.Model):
    _inherit = "sale.order.line"

    memo = fields.Char('memo')
    item_sale_attach_ids = fields.Many2many("item.attach", string="attach", copy=True)
    item_sale_attach_count = fields.Integer(
        "attach Count", compute="_compute_item_attach_count"
    )

    combined_shipment = fields.Many2one(string='同梱',comodel_name='sale.order.instruction.status')
    is_tax_excluded_product = fields.Boolean(
        string='Tax Excluded Product',
        compute='_compute_is_tax_excluded_product',
        store=True,
        help='Product is in GC001 (税抜定価除外) group'
    )
    
    @api.depends('product_id')
    def _compute_is_tax_excluded_product(self):
        for line in self:
            if line.product_id:
                line.is_tax_excluded_product = line.product_id.is_tax_excluded_price_product()
            else:
                line.is_tax_excluded_product = False

    def _compute_item_attach_count(self):
        for line in self:
            line.item_sale_attach_count = len(line.item_sale_attach_ids)

    def action_get_item_sale_attach_view(self):
        self.ensure_one()
        res = self.env["ir.actions.act_window"]._for_xml_id(
            "sale_order_rtw.action_item_attach"
        )
        res["domain"] = [("sale_line_ids", "in", self.id)]
        res["context"] = {
            # "default_name": "図" + str(self.order_id.image_count+1),
            "default_product_id": self.product_id.id if self.product_id else False,
            "default_sale_line_ids": [(4, self.id)],
        }
        return res

    # 明細行の並び順担保処理（OCAのモジュール前提：sale_order_line_sequence）
    def create(self, vals):
        res = super(sale_order_line_rtw, self).create(vals)
        # visible_sequence はOCAの項目、表示上の順番の番号。sequenceの初期値はOdoo側で9999が設定される
        # 複数行追加後に並び順を変えると、Odoo側でsequenceの+1をして、10000以上の数値なり以降の追加行が間に入るので順番が狂うのを調整する
        # メモやセクションは visible_sequence の対象外のようなので、display_type で判断して除外する
        for line in res:
            order = line.mapped("order_id")
            if order:
                # メモ/セクション数
                filtered_lines = order.order_line.filtered(lambda l: l.sequence < 9999)
                if filtered_lines:
                    order_lines_seq_max = max(filtered_lines, key=lambda l: l.sequence).sequence
                else:
                    order_lines_seq_max = 0
                if not line.display_type and line.sequence >= 9999:
                    # 新規追加時は明細の9999を除く最大Sequenceにプラス1した値をセットする
                    line.sequence = order_lines_seq_max + 1

                # Packあり製品の順番担保処理
                if hasattr(line, 'pack_parent_line_id'):
                    # 自分（本体）を親として持つ、先に作成済みのPack明細をすべて取得
                    child_pack_lines = line.order_id.order_line.filtered(
                        lambda l: l.pack_parent_line_id.id == line.id
                    )

                    if child_pack_lines:
                        # 本体（自分）のシーケンス番号を基準にする
                        base_sequence = line.sequence

                        # 先に作られて上にいってしまっていたPack（子）たちのシーケンスを、下に来るように修正
                        for i, child_line in enumerate(child_pack_lines, start=1):
                            child_line.sequence = base_sequence + i
        return res

    def write(self, vals):
        update_from_configurator = 'config_session_id' in vals
        if update_from_configurator:
            protected_fields = [
                'name',           # 説明
                'call_rate',      # 掛率
                'discount',       # 値引
                'price_unit',     # 単価
                'sale_order_sell_unit_price',  # 販売単価
                'product_size',   # 製品サイズ
            ]
            
            for line in self:
                categ_name = line.product_id.categ_id.name if line.product_id and line.product_id.categ_id else False
                if categ_name == "汎用商品":
                    context_key = f'protected_values_{line.id}'
                    if context_key not in self.env.context:
                        protected_values = {field: line[field] for field in protected_fields}
                        self = self.with_context(**{context_key: protected_values})
        
        result = True
        for line in self:
            vals_for_line = dict(vals)
            
            categ_name = line.product_id.categ_id.name if line.product_id and line.product_id.categ_id else False
            context_key = f'protected_values_{line.id}'
            
            if categ_name == "汎用商品" and context_key in self.env.context:
                protected_values = self.env.context[context_key]
                for field, value in protected_values.items():
                    if field in vals_for_line or field not in vals_for_line:
                        vals_for_line[field] = value
            
            result = super(sale_order_line_rtw, line).write(vals_for_line)
        
        return result

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if not self.env.user.has_group('sale_order_rtw.group_sale_cost_price'):
            arch = etree.fromstring(res['arch'])
            for node in arch.xpath("//field[@name='purchase_price']"):
                node.getparent().remove(node)
            res['arch'] = etree.tostring(arch, encoding='unicode')
        return res

    def _purchase_service_create(self, quantity=False):
        """
        販売明細の自動購買生成時、既存POへの合流をさせない
        """
        # 変更点だけの事前対応：
        # 現在データベース上にある、この仕入先宛の「下書き（draft）」状態のPOをすべて探す
        partner_ids = []
        for line in self:
            suppliers = line.product_id._select_seller(quantity=line.product_uom_qty, uom_id=line.product_uom)
            if suppliers:
                partner_ids.append(suppliers[0].name.id)

        draft_pos = self.env['purchase.order'].search([
            ('partner_id', 'in', partner_ids),
            ('state', '=', 'draft'),
            ('company_id', 'in', self.mapped('company_id').ids)
        ])

        # 【一時退避】標準の search() に既存POが見つからないよう、一瞬だけステータスを 'sent' に偽装する
        # ※データベースの書き込み（SQL）は発生しますが、メモリ上の処理なので一瞬
        if draft_pos:
            draft_pos.write({'state': 'sent'})

        try:
            # 既存のPOが 'sent' になっているため、標準コードは「既存POなし」と判定し、必ず綺麗な別POを新規作成します。
            # 単価（price_unit）や通貨、納期などは、正しい仕入先の情報のまま100%正確に計算されます。
            res = super(sale_order_line_rtw, self)._purchase_service_create(quantity=quantity)
        finally:
            # 変更点事後の補正：
            # 何があっても必ず（エラーが起きても）退避させていた既存POのステータスを元の 'draft' に戻す
            if draft_pos:
                draft_pos.write({'state': 'draft'})

        return res