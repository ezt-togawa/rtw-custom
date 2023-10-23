# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_order_line_outlook_stock(models.Model):
    _inherit = "sale.order.line"

    def outlook_link(self):
        self.ensure_one()
        action = self.env.ref("mrp_bom_component_menu.mrp_bom_form_action2")
        form = self.env.ref("mrp_bom_component_menu.mrp_bom_line_tree_view")
        action = action.read()[0]
        list_bom_id = []
        list_attribute = []
        list_satisfy_id = []

        bom_ids = self.env['mrp.bom'].search(
            [('product_tmpl_id', '=', self.product_id.product_tmpl_id.id)])
        bom_lines = self.env['mrp.bom.line'].search(
            [('bom_id', 'in', bom_ids.ids)])
        template_attribute_value_ids = self.product_id.product_template_attribute_value_ids
        for template in template_attribute_value_ids:
            list_attribute.append(template.id)
        for bom in bom_lines:
            if not bom.bom_product_template_attribute_value_ids.ids:
                list_satisfy_id.append(bom.id)
            for item in bom.bom_product_template_attribute_value_ids.ids:
                if all(item in template_attribute_value_ids.ids for item in bom.bom_product_template_attribute_value_ids.ids) or not item:
                    list_satisfy_id.append(bom.id)
                    break
        if bom_ids:
            for bom in bom_ids:
                list_bom_id.append(bom.id)
            action['context'] = {
                'active_id': self.id,
                'search_default_bom_id': [list_bom_id],
                'search_default_id': list_satisfy_id,
                'search_default_product_type': 1,
            }

        else:
            action['context'] = {
                'active_id': self.id,
            }

        action["views"] = [(form.id, "tree")]
        action["target"] = "new"

        return action

class mrp_bom_line_outlook_stock(models.Model):
    _inherit = 'mrp.bom.line'

    def bom_lines_link(self):
        self.ensure_one()
        action = self.env.ref("product_configurator.product_configurable_template_action")
        form = self.env.ref(
            "product.product_template_only_form_view")
        action["views"] = [(form.id, "form")]
        action = action.read()[0]
        action["res_id"] = self.product_id.product_tmpl_id.id
        action['context'] = {
            'active_id': self.product_id.product_tmpl_id.id,
        }
        action["target"] = "new"

        return action
