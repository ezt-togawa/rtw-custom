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
            # record.display_name = record.name
            product_no = ''
            date_planned = ''
            sale_order_no = ''
            if record.sale_reference:
                sale_order = self.env['sale.order'].search([ #GET SALE_ORDER By order_id
                    ('name','=', record.sale_reference)
                ], limit=1)
                if record.product_id.product_no:
                    product_no = f'/{record.product_id.product_no}'
                if sale_order:
                    if sale_order.estimated_shipping_date:
                        date_planned = '/' + str(sale_order.estimated_shipping_date)
                    # if self.env['sale.order.line'].search([('order_id','=',sale_order.id),('product_id','=',record.product_id.id)], order='date_planned desc', limit=1):
                    #     date_planned = '/' + self.env['sale.order.line'].search([('order_id','=',sale_order.id),('product_id','=',record.product_id.id)], order='date_planned desc', limit=1).date_planned.strftime('%Y-%m-%d')
                    record.display_name = f'{record.sale_reference}{product_no}{date_planned}'
            else:
                if record.product_id.product_no:
                    product_no = f'/{record.product_id.product_no}'
                record.display_name = f'{record.name}{product_no}'
