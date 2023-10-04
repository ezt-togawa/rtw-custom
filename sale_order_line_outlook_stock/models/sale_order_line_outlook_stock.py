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
        bom_ids = self.env['mrp.bom'].search(
            [('product_tmpl_id', '=', self.product_id.product_tmpl_id.id)])
        template_attribute_value_ids = self.product_id.product_template_attribute_value_ids

        if template_attribute_value_ids:
            for value in template_attribute_value_ids:
                list_attribute.append(value.id)

        if bom_ids:
            for bom in bom_ids:
                list_bom_id.append(bom.id)

            action['context'] = {
                'active_id': self.id,
                'search_default_bom_id': list_bom_id,
                'search_default_bom_product_template_attribute_value_ids': list_attribute,
            }
        else:
            action['context'] = {
                'active_id': self.id,
            }
        action["views"] = [(form.id, "tree")]
        action["target"] = "new"

        return action
