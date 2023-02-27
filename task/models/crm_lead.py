# -*- coding: utf-8 -*-
from odoo import models, fields, api


class rtw_sf_crm_lead(models.Model):
    _name = "crm.lead"
    _inherit = [
        "crm.lead",
        "task.thread.mixin"
    ]

    # rtw_task_ids = fields.One2many('task.task')
    # channel_ids = fields.Many2many(relation='channel_task_thread_mixin_partner')
    # meeting_ids = fields.Many2many(relation='meeting_task_thread_mixin_partner')

    def create_task(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'task.task',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_res_id': self.id,
                'default_what_id': self.id,
                'default_model': self._name,
                'default_owner_id': self.env.user.id,
                'default_client_id': self.id,
            }
        }
