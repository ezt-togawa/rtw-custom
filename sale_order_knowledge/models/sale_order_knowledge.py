# -*- coding: utf-8 -*-

from odoo import models, fields, api

knowledge_supplement_id = 39
knowledge_special_id = 39
class sale_order_knowledge(models.Model):
    _inherit = 'sale.order'
    
    knowledge_supplement_name = fields.Char(string="配送補足",compute="_compute_knowledge_supplement")
    knowledge_special_name = fields.Char(string="別注/特注補足",compute="_compute_knowledge_special_name")

    def _compute_knowledge_supplement(self):
        for so in self:
            knowledge=self.env['document.page'].search([('id','=',knowledge_supplement_id)])
            if knowledge :
                for item in knowledge:
                    so.knowledge_supplement_name = item.name
            else:
                so.knowledge_supplement_name = ""

    def knowledge_supplement(self):
        self.ensure_one()
        action = self.env.ref("sale_order_knowledge.action_page_2")
        form = self.env.ref("sale_order_knowledge.view_wiki_form_2")
        action = action.read()[0]
        action["views"] = [(form.id, "form")]
        action["target"] = "new"
        action["res_id"] = knowledge_supplement_id
        return action
    
    def _compute_knowledge_special_name(self):
        for so in self:
            knowledge=self.env['document.page'].search([('id','=',knowledge_special_id)])
            if knowledge :
                for item in knowledge:
                    so.knowledge_special_name = item.name
            else:
                so.knowledge_special_name = ""

    def knowledge_special(self):
        self.ensure_one()
        action = self.env.ref("sale_order_knowledge.action_page_2")
        form = self.env.ref("sale_order_knowledge.view_wiki_form_2")
        action = action.read()[0]
        action["views"] = [(form.id, "form")]
        action["target"] = "new"
        action["res_id"] = knowledge_special_id

        return action
