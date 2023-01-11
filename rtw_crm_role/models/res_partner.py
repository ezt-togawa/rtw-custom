# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rtw_crm_role_partner(models.Model):
    _inherit = 'res.partner'

    rel_crm = fields.Many2many(
        comodel_name="crm.lead",
        compute="_get_rel_crm")

    def _get_rel_crm(self):
        for rec in self:
            rec.rel_crm = self.env['crm.lead'].search([('role_ids.contact_id', '=', self.id)])
    # role = fields.Selection([
    #     ('1', '意思決定者'),
    #     ('2', '業務担当者'),
    #     ('3', '有力者'),
    #     ('4', '技術担当者'),
    #     ('5', '予算決定者'),
    #     ('6', '予算担当者'),
    #     ('7', '評価者'),
    #     ('8', '発注担当者'),
    #     ('9', '担当役員'),
    #     ('10', '商品選定者'),
    #     ('11', '設計担当者'),
    #     ('12', '主担当'),
    #     ('13', 'その他'),
    # ], default='',
    #     string="Role")
    # role_name = fields.Char(compute="_get_name")
    #
    # @api.depends("name")
    # def _get_name(self):
    #     for rec in self:
    #         if rec.role:
    #             print("in")
    #             rec.name = rec.name + "(" + dict(rec._fields['role'].selection).get(rec.role) + ")"
    #         else:
    #             rec.name = rec.name