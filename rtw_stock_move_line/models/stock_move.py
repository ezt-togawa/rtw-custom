
from odoo import models, fields, api
import math
class rtw_stock_move(models.Model):
    _inherit = "stock.move"
    sai = fields.Float(compute="_get_sai", group_operator="sum", store=True)
    depo_date = fields.Date(compute="_get_sale",  store=True)
    shiratani_date = fields.Date(compute="_get_shiratani_date", store=True)
    date_planned = fields.Datetime(
        related='sale_line_id.date_planned', store=True)
    sale_id = fields.Many2one(
        'sale.order', compute="_get_sale_id", group_operator="sum",store=True)
    customer_id = fields.Many2one(related='sale_id.partner_id', string='顧客')
    title = fields.Char(related='sale_id.title', string='案件名')
    spec = fields.Many2many(
        related="sale_line_id.product_id.product_template_attribute_value_ids")
    custom = fields.One2many(
        related="sale_line_id.config_session_id.custom_value_ids")
    overseas = fields.Boolean(
        related="sale_id.overseas", string="海外")
    factory = fields.Many2one(related="production_id.picking_type_id")
    memo = fields.Char(related='sale_line_id.memo')
    area = fields.Many2one('res.country.state', compute="_get_area", string='エリア', store=True)
    forwarding_address = fields.Text(
        compute="_get_forwarding_address", string='到着地',store=True)
    shipping_to = fields.Text(
        string="配送", compute="_get_shipping_to",store=True)
    warehouse_arrive_date = fields.Date(
        compute="_get_warehouse_arrive_date",store=True )
    mrp_production_id = fields.Char(
        string="製造オーダー", compute="_get_mrp_production_id",store=True)
    product_package_quantity = fields.Float(string="個口数")
    invoice_number = fields.Char(string="送り状番号")
   

    @api.model_create_multi
    def create(self, vals_list):
        mls = super().create(vals_list)
        for move in mls:
            if move.product_id and move.product_id.two_legs_scale:
                move.product_package_quantity = math.ceil(move.product_qty * move.product_id.two_legs_scale)
            else:
                move.product_package_quantity = 0
        return mls
    @api.depends('product_id')
    def _get_sai(self):
        for rec in self:
            if rec.product_id.sai:
                rec.sai = rec.product_id.sai
            else:
                rec.sai = 0

    @api.depends('product_id')
    def _get_sale(self):
        for rec in self:
            if rec.sale_line_id.depo_date:
                rec.depo_date = rec.sale_line_id.depo_date
            else:
                rec.depo_date = False

    @api.depends('sale_line_id', 'picking_id')
    def _get_sale_id(self):
        for rec in self:
            if rec.sale_line_id.order_id:
                rec.sale_id = rec.sale_line_id.order_id
            elif rec.picking_id:
                if rec.picking_id.sale_id:
                    rec.sale_id = rec.picking_id.sale_id
                elif rec.picking_id.origin and '/MO/' in rec.picking_id.origin:
                        mrp = self.env['mrp.production'].search([('name','=',rec.picking_id.origin)])
                        if mrp:
                            rec.sale_id = self.env['sale.order'].search([('name','=',mrp.origin)]).id
                        else:
                            rec.sale_id = False
                elif rec.picking_id.origin and rec.picking_id.origin.startswith('P'):
                        purchase_order_origin = self.env['purchase.order'].search([('name','=',rec.picking_id.origin)]).origin  
                        if purchase_order_origin  and '/MO/' in purchase_order_origin :          
                            mrp_origin=self.env['mrp.production'].search([('name','=',purchase_order_origin)]).origin     
                            if mrp_origin:
                                rec.sale_id = self.env['sale.order'].search([('name','=',mrp_origin)]).id
                            else:
                                rec.sale_id = False   
                        else:
                            rec.sale_id = False        
                elif rec.created_production_id:
                    rec.sale_id = self.env['sale.order'].search([('name','=',rec.created_production_id.sale_reference)]).id
                else:
                    rec.sale_id = False
            else:
                rec.sale_id = False


    @api.depends('production_id', 'picking_id')
    def _get_mrp_production_id(self):
      for rec in self:
        if rec.production_id:
            rec.mrp_production_id = rec.production_id.name
        elif rec.created_production_id:
            rec.mrp_production_id = rec.created_production_id.name
        elif rec.picking_id.origin and '/MO/' in rec.picking_id.origin:
            rec.mrp_production_id = self.env['mrp.production'].search([('name','=',rec.picking_id.origin)]).name    
        elif rec.picking_id.origin and rec.picking_id.origin.startswith('P'):
            rec.mrp_production_id = self.env['purchase.order'].search([('name','=',rec.picking_id.origin)]).origin  
        else:
            mrp = self.env['mrp.production'].search(
                [('origin', '=', rec.picking_id.sale_id.name), ('product_id', '=', rec.product_id.id)], limit=1)
            if mrp:
                rec.mrp_production_id = mrp.name
            else:
                rec.mrp_production_id = None

    @api.depends('picking_id','picking_id.forwarding_address','sale_id','sale_id.forwarding_address')
    def _get_forwarding_address(self):
         for rec in self:
            if rec.picking_id:
                rec.forwarding_address = rec.picking_id.forwarding_address
                if rec.sale_id and not rec.picking_id.forwarding_address:
                    rec.forwarding_address = rec.sale_id.forwarding_address
            elif rec.sale_id:
                rec.forwarding_address = rec.sale_id.forwarding_address
            else:
                rec.forwarding_address = False
                            
    @api.depends('sale_line_id', 'sale_line_id.shiratani_date', 'sale_id', 'sale_id.shiratani_entry_date')
    def _get_shiratani_date(self):
        for rec in self:
            if rec.sale_line_id.shiratani_date:
                rec.shiratani_date = rec.sale_line_id.shiratani_date
            elif rec.sale_id:
                rec.shiratani_date = rec.sale_id.shiratani_entry_date
            else:
                rec.shiratani_date = False
         
    @api.depends('sale_line_id.depo_date','sale_line_id.depo_date','sale_line_id','sale_id','sale_id.warehouse_arrive_date')
    def _get_warehouse_arrive_date(self):
        for rec in self:
            if rec.sale_line_id.depo_date:
                rec.warehouse_arrive_date = rec.sale_line_id.depo_date
            elif rec.sale_id:
              
                rec.warehouse_arrive_date = rec.sale_id.warehouse_arrive_date
            else:
                rec.warehouse_arrive_date = False

    @api.depends('picking_id', 'picking_id.sipping_to', 'sale_id', 'sale_id.sipping_to')
    def _get_shipping_to(self):
     for rec in self:
        sipping_to = ""  
        if rec.picking_id and rec.picking_id.sipping_to:
            if rec.picking_id.sipping_to == "depo":
                sipping_to = "デポ入れまで"
            elif rec.picking_id.sipping_to == "inst":
                sipping_to = "搬入設置まで"
            elif rec.picking_id.sipping_to == "inst_depo":
                sipping_to = "搬入設置（デポ入）"
            elif rec.picking_id.sipping_to == "direct":
                sipping_to = "直送"
            elif rec.picking_id.sipping_to == 'container':
                sipping_to = 'オランダコンテナ出荷'
            elif rec.picking_id.sipping_to == 'pick_up':
                sipping_to = '引取'
            elif rec.picking_id.sipping_to == 'bring_in':
                sipping_to = '持込'
            rec.shipping_to = sipping_to
        elif rec.sale_id and rec.sale_id.sipping_to:
            if rec.sale_id.sipping_to == "depo":
                sipping_to = "デポ入れまで"
            elif rec.sale_id.sipping_to == "inst":
                sipping_to = "搬入設置まで"
            elif rec.sale_id.sipping_to == "inst_depo":
                sipping_to = "搬入設置（デポ入）"
            elif rec.sale_id.sipping_to == "direct":
                sipping_to = "直送"
            elif rec.sale_id.sipping_to == 'container':
                sipping_to = 'オランダコンテナ出荷'
            elif rec.sale_id.sipping_to == 'pick_up':
                sipping_to = '引取'
            elif rec.sale_id.sipping_to == 'bring_in':
                sipping_to = '持込'
            rec.shipping_to = sipping_to

        else:
            rec.shipping_to = False


    @api.depends('sale_id','sale_id','picking_id.waypoint', 'sale_id.waypoint', 'picking_id.waypoint.state_id', 'sale_id.waypoint.state_id')
    def _get_area(self):
        for rec in self:
            if rec.picking_id and rec.picking_id.waypoint:
                rec.area = rec.picking_id.waypoint.state_id
                if rec.sale_id and not rec.picking_id.waypoint.state_id:
                    rec.area = rec.sale_id.waypoint.state_id
            elif rec.sale_id and rec.sale_id.waypoint:
                rec.area = rec.sale_id.waypoint.state_id
            else:
                rec.area = False     
   