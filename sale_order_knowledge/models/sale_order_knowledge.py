# -*- coding: utf-8 -*-

from odoo import models, fields, api

class sale_order_knowledge(models.Model):
    _inherit = 'sale.order'

    def knowledge_supplement(self):
        knowledge_id = 38 ## REPLACE WITH ID OF APPROPIATE KNOWLEDGE
        self.ensure_one()
        action = self.env.ref("sale_order_knowledge.action_page_2")
        form = self.env.ref("sale_order_knowledge.view_wiki_form_2")
        action = action.read()[0]
        action["views"] = [(form.id, "form")]
        action["target"] = "new"
        action["res_id"] = knowledge_id

        return action

    def knowledge_special(self):
        knowledge_id = 39 ## REPLACE WITH ID OF APPROPIATE KNOWLEDGE
        self.ensure_one()
        action = self.env.ref("sale_order_knowledge.action_page_2")
        form = self.env.ref("sale_order_knowledge.view_wiki_form_2")
        action = action.read()[0]
        action["views"] = [(form.id, "form")]
        action["target"] = "new"
        action["res_id"] = knowledge_id

        return action
