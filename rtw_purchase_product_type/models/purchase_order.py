# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_purchase(models.Model):
    _inherit = "purchase.order"

    production_type = fields.Char('製品タイプ' , compute='_compute_production_type')

    def _compute_production_type(self):
            for order in self:
                    list_custom_config = ''
                    purchase_order_line = order.order_line
                    for line in purchase_order_line: #GET CONFIG SESSION BY PURCHASE ORDER LINE
                        sale_order_line = line.sale_line_id
                        if sale_order_line:
                            config_custom_values = self.env['product.config.session.custom.value'].search([('cfg_session_id','=',sale_order_line.config_session_id.id)])
                            list_custom_config = list_custom_config + '<div style="font-weight:bold">'+ sale_order_line.name +'</div>'

                            if sale_order_line.p_type:
                                if sale_order_line.p_type == 'special':
                                        list_custom_config = list_custom_config + '<div>別注</div>'
                                elif sale_order_line.p_type == 'custom':
                                        list_custom_config = list_custom_config + '<div>特注</div>'

                            for custom in config_custom_values:
                                list_custom_config = list_custom_config + '<div>'+ custom.attribute_id.name + ' : ' + custom.value +'</div>'

                    sale_order_lines = self.env['sale.order.line'].search([('move_ids', 'in', order.order_line.move_dest_ids.ids)]) #GET CONFIG SESSION BY MOVE DEST IDS
                    for sale_order_line in sale_order_lines:
                        if sale_order_line:
                            config_custom_values = self.env['product.config.session.custom.value'].search([('cfg_session_id','=',sale_order_line.config_session_id.id)])
                            list_custom_config = list_custom_config + '<div style="font-weight:bold">'+ sale_order_line.name +'</div>'

                            if sale_order_line.p_type:
                                if sale_order_line.p_type == 'special':
                                        list_custom_config = list_custom_config + '<div>別注</div>'
                                elif sale_order_line.p_type == 'custom':
                                        list_custom_config = list_custom_config + '<div>特注</div>'

                            for custom in config_custom_values:
                                list_custom_config = list_custom_config + '<div>'+ custom.attribute_id.name + ' : ' + custom.value +'</div>'

                    self.production_type = list_custom_config
