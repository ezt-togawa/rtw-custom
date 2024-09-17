from odoo import fields, models
import math
from datetime import datetime
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    calculate_shiratani_date = fields.Char('Shiratani Date' , compute="_compute_get_sale_order")
    calculate_witness = fields.Char('Witness' , compute="_compute_get_sale_order")
    calculate_witness_phone = fields.Char('Witness Phone' , compute="_compute_get_sale_order")
    pic_name = fields.Char('PIC Name' , compute="_compute_get_sale_order")
    calculate_name = fields.Char('Name' , compute="_compute_get_sale_order")
    calculate_note = fields.Char('Note' , compute="_compute_get_sale_order")
    calculate_estimated_shipping_date = fields.Char('Estimated Shipping Date' , compute="_compute_get_sale_order")
    calculate_payment_term = fields.Char('Payment term' , compute="_compute_get_sale_order")
    sale_orders=fields.One2many(
        "sale.order",
        "origin",
        string="Sale order",
        compute="_compute_get_sale_order",
    )
    current_print = fields.Char(compute="_compute_current_print")

    def _compute_current_print(self):
        for so in self:
            so.current_print = datetime.now().strftime('%Y-%m-%dT%H%M%S')
            
    def _compute_get_sale_order(self):
        sale_order = self.env['sale.order'].search([('id','=',self.sale_id.id)])
        if not sale_order:
            sale_order = self.env['sale.order'].search([('name','=',self.origin)])
                    
        if sale_order:
            self.calculate_shiratani_date = sale_order.shiratani_entry_date
            self.calculate_witness = sale_order.witness
            self.calculate_witness_phone = sale_order.witness_phone
            self.pic_name = sale_order.user_id.name
            self.calculate_name = sale_order.title
            self.calculate_note = sale_order.note
            self.calculate_estimated_shipping_date = sale_order.estimated_shipping_date
            self.calculate_payment_term = sale_order.payment_term_id.name
            self.sale_orders = sale_order
        else:
            self.calculate_shiratani_date = ''
            self.calculate_witness = ''
            self.calculate_witness_phone = ''
            self.pic_name = ''
            self.calculate_name = ''
            self.calculate_note = ''
            self.calculate_estimated_shipping_date = ''
            self.calculate_payment_term = ''
            self.sale_orders = False

class StockMove(models.Model):
  _inherit = 'stock.move'
  calculate_packages = fields.Integer('Packages' , compute="_compute_calculate_packages")
  stock_move_product_size = fields.Char(compute="_compute_stock_move_related_sale_order_line")
  stock_move_sale_line_id= fields.Many2one('sale.order.line',compute="_compute_stock_move_related_sale_order_line")
  
  def _compute_calculate_packages(self):
    for move in self:
        if move.product_id.two_legs_scale:
            move.calculate_packages = math.ceil(move.product_uom_qty * move.product_id.two_legs_scale)
        else:
            move.calculate_packages = move.product_uom_qty
            
  def _compute_stock_move_related_sale_order_line(self):
    for move in self:
        sale_order_line = False
        product_size = ''
        if move.sale_line_id:
            sale_order_line = move.sale_line_id
            move.stock_move_sale_line_id = move.sale_line_id
        elif move.created_production_id:
            search_criteria = [ #limit 10 times
                    ('move_ids', 'in', [move_id.id for move_id in move.created_production_id.move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in move.created_production_id.move_dest_ids.move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in move.created_production_id.move_dest_ids.move_dest_ids.move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in move.created_production_id.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in move.created_production_id.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in move.created_production_id.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in move.created_production_id.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in move.created_production_id.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in move.created_production_id.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
                    ('move_ids', 'in', [move_id.id for move_id in move.created_production_id.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids]),
            ]

            for search in search_criteria: #find sale_order_line
                if self.env['sale.order.line'].search([search]):
                    sale_order_line = self.env['sale.order.line'].search([search])
                    break
            move.stock_move_sale_line_id = sale_order_line    
            sale_order_line = sale_order_line
        else:
            move.stock_move_sale_line_id = False
            sale_order_line = False
        
        if sale_order_line:
            move.stock_move_product_size = sale_order_line.product_size
        elif move.product_id.product_tmpl_id:
            if move.product_id.product_tmpl_id.width:
                product_size += 'W' + str(move.product_id.product_tmpl_id.width) + ' '
            if move.product_id.product_tmpl_id.depth:
                product_size += '*D' + str(move.product_id.product_tmpl_id.depth) + ' '
            if move.product_id.product_tmpl_id.height:
                product_size += '*H' + str(move.product_id.product_tmpl_id.height) + ' '
            if move.product_id.product_tmpl_id.diameter:
                product_size += 'Φ' + str(move.product_id.product_tmpl_id.diameter) + ' '
            if move.product_id.product_tmpl_id.sh:
                product_size += 'SH' + str(move.product_id.product_tmpl_id.sh) + ' '
            if move.product_id.product_tmpl_id.ah:
                product_size += 'AH' + str(move.product_id.product_tmpl_id.ah)   
            move.stock_move_product_size = product_size
        else:
            move.stock_move_product_size = ''
            
class StockPicking(models.Model):
    _inherit = 'stock.quant'

    current_print = fields.Char(compute="_compute_current_print")
    
    def _compute_current_print(self):
        for so in self:
            so.current_print = datetime.now().strftime('%Y-%m-%dT%H%M%S')