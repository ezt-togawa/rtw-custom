# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TaskThread(models.AbstractModel):
    _name = 'task.thread.mixin'
    _description = 'Task Thread'

    rtw_task_ids = fields.One2many('task.task' 'res_id', string='Tasks', auto_join=True)
