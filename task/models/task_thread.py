# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TaskThread(models.AbstractModel):
    _name = 'task.thread.mixin'
    _description = 'Task Thread'

    rtw_task_ids = fields.One2many(comodel_name='task.task',
                                   inverse_name='res_id', string='Tasks', auto_join=True)
    # rtw_task_ids = fields.One2many('task.task')
    # same_vat_partner_id = fields.Many2one('res.partner', string='Partner with same Tax ID',store=False)
    # partner_gid = fields.Integer('Company database ID')

