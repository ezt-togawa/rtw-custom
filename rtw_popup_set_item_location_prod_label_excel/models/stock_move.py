# -*- coding: utf-8 -*-

from odoo import models, fields, api

class rtw_mrp_production_revised_edition(models.Model):
    _inherit = 'stock.move'

    location_item_excel_prod_label_ids = fields.One2many(
        comodel_name="mrp.location_item_excel_prod_label",
        inverse_name="mrp_production_id", 
        string="set location item excel prod label")

    def create_location_item_excel_prod_label(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.location_item_excel_prod_label',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',  
            'context': {
                'default_owner_id': self.env.user.id,
            }
        }
    