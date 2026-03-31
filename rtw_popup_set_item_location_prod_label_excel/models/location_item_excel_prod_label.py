from odoo import models, fields, api
from odoo.exceptions import ValidationError

class rtw_mrp_location_item_excel_prod_label(models.Model):
    """
        【ラベル位置選択】ボタンの位置情報保持モデル
        システム一意の情報
    """
    _name = 'mrp.location_item_excel_prod_label'
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _description = 'set location item excel prod label'

    @api.model
    def _get_location_item_row(self):
        rec = self.get_singleton()
        return rec.location_item_row or 1

    @api.constrains('location_item_row')
    def _check_location_item_row(self):
        for record in self:
            if record.location_item_row <= 0:
                raise ValidationError("印字スタート位置設定")

    @api.model
    def get_singleton(self):
        rec = self.search([], limit=1)
        if not rec:
            rec = self.create({})
        return rec

    location_item_row = fields.Integer('Location item row',default=_get_location_item_row)
    owner_id = fields.Many2one('res.users', 'OwnerId', default=lambda self: self.env.user)
    