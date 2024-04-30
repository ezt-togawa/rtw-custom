# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sale_order_line_outlook_stock(models.Model):
    _inherit = "sale.order.line"

    def outlook_link(self):
        self.ensure_one()
        # redirect to product forecasted
        if not self.product_id.product_tmpl_id.config_ok and self.product_id.product_tmpl_id.type == 'product':
            action = self.env["ir.actions.actions"]._for_xml_id(
                'stock.stock_replenishment_product_product_action')
            base_url = self.env['ir.config_parameter'].get_param(
                'web.base.url')
            menu_id = self.env['ir.ui.menu'].search(
                [('name', '=', 'Configurator'), ('parent_id', '=', False)]).id
            client_action = {
                'type': 'ir.actions.act_url',
                'name': "Product Forecasted",
                'target': 'new',
                'url': base_url+f'/web#action={action["id"]}&active_id={self.product_id.product_tmpl_id.id}&cids=1&menu_id={menu_id}&active_model=product.template',
            }
            return client_action

        action = self.env.ref("mrp_bom_component_menu.mrp_bom_form_action2")
        form = self.env.ref("mrp_bom_component_menu.mrp_bom_line_tree_view")
        action = action.read()[0]
        list_bom_id = [self.bom_id.id] if self.bom_id else []
        list_satisfy_id = []
        list_satisfy_child_id = []

        bom_lines = self.env['mrp.bom.line'].search(
            [('bom_id', '=', self.bom_id.id)])
        template_attribute_value_ids = self.product_id.product_template_attribute_value_ids

        for bom in bom_lines:
            if (not bom.bom_product_template_attribute_value_ids.ids or all(item in template_attribute_value_ids.ids for item in bom.bom_product_template_attribute_value_ids.ids)) and bom.product_id.product_tmpl_id.type == 'product' and bom.id not in list_satisfy_id:
                list_satisfy_id.append(bom.id)
                list_child_bom = self.env['mrp.bom'].search(
                    [('product_tmpl_id', '=', bom.product_id.product_tmpl_id.id)])
                if list_child_bom:
                    for child_bom in list_child_bom:
                        child_bom_lines = self.env['mrp.bom.line'].search(
                            [('bom_id', '=', child_bom.id)])
                        print('child', child_bom.product_id.product_tmpl_id.config_ok)
                        list_bom_id.append(child_bom.id)
                        for child_bom_line in child_bom_lines:
                            if (not child_bom_line.bom_product_template_attribute_value_ids.ids or all(item in template_attribute_value_ids.ids for item in child_bom_lines.bom_product_template_attribute_value_ids.ids)) and child_bom_line.product_id.product_tmpl_id.type == 'product' and child_bom_line.id not in list_satisfy_id:
                                list_satisfy_child_id.append(child_bom_line.id)

        list_satisfy_id.extend(list_satisfy_child_id)
        if not self.product_id.product_tmpl_id.config_ok and not self.product_id.product_tmpl_id.type == 'product':
            action['domain'] = [('id', '=', False)]
            action['context'] = {
                'active_id': self.id,
            }
        else:
            action['context'] = {
                'active_id': self.id,
                'search_default_product_type': 1,
                'search_default_bom_id': [list_bom_id],
                'search_default_id': list_satisfy_id if list_satisfy_id else None,
            }
            if list_bom_id:
                action['context']['search_default_bom_id'] = [list_bom_id]

        action["views"] = [(form.id, "tree")]
        action["target"] = "new"
        return action


class mrp_bom_line_outlook_stock(models.Model):
    _inherit = 'mrp.bom.line'

    priority_sort = fields.Float(
        'priority', compute="_compute_priority", store=True)

    def _compute_priority(self):
        for line in self:
            if line.bom_id.product_tmpl_id.config_ok:
                line.priority_sort = 0
            else:
                line.priority_sort = 1

    def bom_lines_link(self):
        self.ensure_one()

        action = self.env["ir.actions.actions"]._for_xml_id(
            'stock.stock_replenishment_product_product_action')
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        menu_id = self.env['ir.ui.menu'].search(
            [('name', '=', 'Configurator'), ('parent_id', '=', False)]).id
        client_action = {
            'type': 'ir.actions.act_url',
            'name': "Product Forecasted",
            'target': 'new',
            'url': base_url+f'/web#action={action["id"]}&active_id={self.product_id.product_tmpl_id.id}&cids=1&menu_id={menu_id}&active_model=product.template',
        }

        return client_action
