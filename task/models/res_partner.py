from odoo import models, fields, api


class rtw_sf_partner_task(models.Model):
    _inherit = [
        "res.partner",
        "task.thread.mixin"
    ]
    _description = 'task'

    # rtw_task_ids = fields.One2many('task.task')
    channel_ids = fields.Many2many('mail.channel',
                                   'mail_channel_task_thread_mixin_partner',
                                   'partner_id',
                                   'channel_id',
                                   string='Channels', copy=False)
    meeting_ids = fields.Many2many(relation='mail_channel_task_thread_mixin_partner')