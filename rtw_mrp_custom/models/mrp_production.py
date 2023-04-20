# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_mrp_production_revised_edition(models.Model):
    _inherit = 'mrp.production'

    revised_edition_ids = fields.One2many(
        comodel_name="mrp.revised_edition",
        inverse_name="mrp_id",
        string="revised edition")

    def create_revised_edition(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.revised_edition',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_mrp_id': self.id,
                'default_owner_id': self.env.user.id,
            }
        }

    def _compute_display_name(self):
        for record in self:
            project_name = ''
            estimated_shipping_date=''
            if record.origin:
                production = self.env['mrp.production'].browse(record.id) #GET PRODUCTION
                sale_order = self.env['sale.order'].search([ #GET SALE_ORDER By order_id
                    ('name','=', production.origin)
                ], limit=1)
                if sale_order and sale_order.title:
                    project_name =f'/{sale_order.title}'
                if sale_order and sale_order.estimated_shipping_date:
                    estimated_shipping_date =f'/{sale_order.estimated_shipping_date}'
                record.display_name = f'{record.origin}{estimated_shipping_date}{project_name}'
            else:
                record.display_name = ''
