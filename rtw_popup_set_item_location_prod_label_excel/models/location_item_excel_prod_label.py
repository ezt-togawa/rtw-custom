from odoo import models, fields, api
from odoo.exceptions import ValidationError

class rtw_mrp_location_item_excel_prod_label(models.Model):
    _name = 'mrp.location_item_excel_prod_label'
    _description ='location_item_excel_prod_label'
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    _description = 'set location item excel prod label'

    @api.model
    def _get_location_item_row(self):
        last_record = self.env["mrp.location_item_excel_prod_label"].search([], order="create_date desc", limit=1)
        if last_record:
            return last_record.location_item_row
        return 1
    
    @api.constrains('location_item_row')
    def _check_location_item_row(self):
        for record in self:
            if record.location_item_row <= 0:
                raise ValidationError("印字スタート位置設定")
    
    location_item_row = fields.Integer('Location item row',default=_get_location_item_row)
    mrp_production_id = fields.Many2one('mrp.production', string="MRP order")
    owner_id = fields.Many2one('res.users', 'OwnerId', default=lambda self: self.env.user)
    