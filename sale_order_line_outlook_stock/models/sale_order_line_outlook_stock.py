# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_order_line_outlook_stock(models.Model):
    _inherit = "sale.order.line"

    def outlook_link(self):
        print('self', self)
        self.ensure_one()
        action = self.env.ref("mrp_bom_component_menu.mrp_bom_form_action2")
        form = self.env.ref("mrp_bom_component_menu.mrp_bom_line_tree_view")
        action = action.read()[0]
        list_satisfy_id = []

        bom_lines = self.env['mrp.bom.line'].search(
            [('bom_id', '=', self.bom_id.id)])
        template_attribute_value_ids = self.product_id.product_template_attribute_value_ids

        for bom in bom_lines:
            if (not bom.bom_product_template_attribute_value_ids.ids or all(item in template_attribute_value_ids.ids for item in bom.bom_product_template_attribute_value_ids.ids)) and bom.product_id.product_tmpl_id.type == 'product' and bom.id not in list_satisfy_id:
                list_satisfy_id.append(bom.id)

        action['context'] = {
            'active_id': self.id,
            'search_default_id': list_satisfy_id if list_satisfy_id else None,
            'search_default_bom_id': self.bom_id.id,
            'search_default_product_type': 1,
        }
        action["views"] = [(form.id, "tree")]
        action["target"] = "new"

        return action

class mrp_bom_line_outlook_stock(models.Model):
    _inherit = 'mrp.bom.line'

    def bom_lines_link(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            'stock.stock_replenishment_product_product_action')
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        menu_id = self.env['ir.ui.menu'].search([('name','=','Configurator'),('parent_id','=',False)])
        client_action = {
            'type': 'ir.actions.act_url',
            'name': "Product Forecasted",
            'target': 'new',
            'url': base_url+f'/web#action={action["id"]}&active_id={self.product_id.id}&cids=1&menu_id={menu_id}&active_model=product.product',
        }

        return client_action
