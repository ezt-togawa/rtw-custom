from odoo import models, fields, api

class sale_order_work_day(models.Model):
    _name = 'sale.order.work.day'
    _description = 'Selection Work Day'
    _order = "sequence"
    
    name = fields.Char('作成日数' , required=True)
    sequence = fields.Integer(default=10)