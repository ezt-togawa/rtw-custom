# -*- coding: utf-8 -*-
from odoo import models, fields, api


class rtw_sf_partner_task(models.Model):
    _name = "res.partner"
    _inherit = [
        "res.partner",
        "task.thread.mixin"
    ]
    _description = 'task'

    # rtw_task_ids = fields.One2many('task.task')
    channel_ids = fields.Many2many(relation='channel_task_thread_mixin_partner')
    meeting_ids = fields.Many2many(relation='meeting_task_thread_mixin_partner')