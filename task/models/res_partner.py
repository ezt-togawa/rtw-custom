from odoo import models, fields, api


class rtw_sf_partner_task(models.Model):
    _inherit = "res.partner"
    _description = 'task'

    rtw_task_ids = fields.One2many('task.task')
