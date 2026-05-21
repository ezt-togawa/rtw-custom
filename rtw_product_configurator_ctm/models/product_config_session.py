from odoo import models, fields, api


class rtw_product_config_session(models.Model):
    _inherit = "product.config.session"

    @api.depends('product_tmpl_id')
    def _compute_currency_id(self):
        """
        1. OCAのproduct_configuratorの _compute_currency_id を改修
        2. 見積書画面から開かれている場合は、見積書の通貨で上書きする
        """
        super(rtw_product_config_session, self)._compute_currency_id()

        for session in self:
            # コンテキストからSaleOrderの情報を取得
            target_order_id = session._context.get('default_order_id')

            # 見積書で設定されいる通貨で上書き
            if target_order_id:
                order = session.env['sale.order'].browse(target_order_id)
                if order.exists() and order.currency_id:
                    session.currency_id = order.currency_id.id
