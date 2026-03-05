from odoo import models, api, fields

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def _gather(self, product_id, location_id, lot_id=None, package_id=None, owner_id=None, strict=False):
        # 製造オーダー利用可能確認時の在庫引当処理、First Expiry First Out (FEFO)指定で破棄日の指定がある場合のみ
        # 在庫を探す
        quants = super(StockQuant, self)._gather(
            product_id, location_id, lot_id=lot_id,
            package_id=package_id, owner_id=owner_id, strict=strict
        )

        # 自動引当（特定のロット指定なし）の場合のみ制限をかける
        if not lot_id and product_id.tracking != 'none':
            now = fields.Datetime.now()

            # 破棄日removal_dateで除外する
            quants = quants.filtered(lambda q: not q.lot_id.removal_date or q.lot_id.removal_date >= now)

        return quants