# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import datetime


class rtw_crm_presence(models.Model):
    _inherit = 'crm.lead'

    presence_ids = fields.One2many(comodel_name="rtw_presence.presence",
                                   inverse_name="crm_id",
                                   string="crm")

    def create_presence(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'rtw_presence.presence',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_crm_id': self.id,
                'default_name': self.name + "（立会）",
                'default_owner_id': self.user_id.ids
            }
        }