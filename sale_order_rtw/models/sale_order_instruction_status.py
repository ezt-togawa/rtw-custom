from odoo import models, fields, api

class sale_order_instruction_status(models.Model):
    _name = 'sale.order.instruction.status'
    _description = 'Select Instruction  Status'
    _order = "sequence"
    
    name = fields.Char('名称' , required=True)
    abbreviation = fields.Char('略称' , required=True)
    sequence = fields.Integer(default=11)