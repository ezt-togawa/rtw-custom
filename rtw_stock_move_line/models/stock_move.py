from odoo import models, fields, api
import math
class rtw_stock_move(models.Model):
    _inherit = "stock.move"
    sai = fields.Float(compute="_get_sai", group_operator="sum", store=True)
    depo_date = fields.Date(compute="_get_sale",  store=True)
    shiratani_date = fields.Date(compute="_get_shiratani_date",store=True)
    shiratani_date_delivery = fields.Date(string="白谷到着日", compute="_get_shiratani_date_delivery", inverse="_set_shiratani_date_delivery",store=True)
    date_planned = fields.Datetime(
        related='sale_line_id.date_planned', store=True)
    sale_id = fields.Many2one(
        'sale.order', compute="_get_sale_id",store=True)
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
    area = fields.Text( compute="_get_area", string='エリア', store=True)
    area_2 = fields.Text( compute="_get_area_2", store=True)
    forwarding_address = fields.Text(
        compute="_get_forwarding_address", string='到着地',store=True)
    shipping_to = fields.Text(
        string="配送", compute="_get_shipping_to",store=True)
    warehouse_arrive_date = fields.Date(
        compute="_get_warehouse_arrive_date",store=True )
    warehouse_arrive_date_2 = fields.Date(
        compute="_get_warehouse_arrive_date_2",store=True )
    mrp_production_id = fields.Char(
        string="製造オーダー", compute="_get_mrp_production_id",store=True)
    product_package_quantity = fields.Float(string="個口数")
    invoice_number = fields.Char(string="送り状番号")
    primary_shipment_stock_move = fields.Boolean('一次出荷',
        compute="_get_primary_shipment_stock_move",
    )
    operational_Notes = fields.Char(string='運用メモ')
    itoshima_shiratani_shipping_notes=fields.Text(string="糸島/白谷配送注記",compute="_compute_itoshima_shiratani_shipping_notes")
    itoshima_shiratani_shipping_notes_first_line = fields.Char(
        string="糸島/白谷配送注記", compute="_compute_first_line"
    )
    arrival_date_itoshima = fields.Date(string="糸島出荷日" , compute= "_compute_arrival_date_itoshima",inverse="_inverse_arrival_date_itoshima") 
    arrival_date_itoshima_inherit_2 = fields.Date()
    arrival_date_itoshima_inherit = fields.Date()

    def _compute_arrival_date_itoshima(self):
        for move in self:
            if move.mrp_production_id:
                mrp = self.env["mrp.production"].search([('name', '=', move.mrp_production_id)], limit=1)
                if move.arrival_date_itoshima_inherit_2:
                    if mrp.itoshima_shipping_date != move.arrival_date_itoshima_inherit_2:
                        move.arrival_date_itoshima =  mrp.itoshima_shipping_date
                        move.arrival_date_itoshima_inherit = mrp.itoshima_shipping_date
                    else:
                         move.arrival_date_itoshima = move.arrival_date_itoshima_inherit_2
                elif move.arrival_date_itoshima_inherit and mrp.is_active == False: 
                    move.arrival_date_itoshima = move.arrival_date_itoshima_inherit
                else:
                    if mrp:
                        move.arrival_date_itoshima =  mrp.itoshima_shipping_date
                        move.arrival_date_itoshima_inherit = mrp.itoshima_shipping_date
            else: 
                move.arrival_date_itoshima = False
        
           
    def _inverse_arrival_date_itoshima(self):
        mrp = ""
        for rec in self:
            if rec.mrp_production_id:
                mrp = self.env["mrp.production"].search([('name', '=', rec.mrp_production_id)], limit=1)
                if mrp:
                    mrp.write({'arrival_date_itoshima_stock_move': rec.arrival_date_itoshima})
                    mrp.write({'is_active': False})
                    stock_move = self.env['stock.move'].search([
                            ('id', '=', rec.id),
                        ])
                    if stock_move:
                        stock_move.arrival_date_itoshima = rec.arrival_date_itoshima 
                        stock_move.arrival_date_itoshima_inherit_2 = stock_move.arrival_date_itoshima
                    else:
                        return
                else:
                    return
        else:
            return


    def _compute_first_line(self):
        for move in self:
            if move.itoshima_shiratani_shipping_notes:
                move.itoshima_shiratani_shipping_notes_first_line =  move.sale_id.itoshima_shiratani_shipping_notes.split("\n")[0]
            else:
                move.itoshima_shiratani_shipping_notes_first_line = ""
    
    def _compute_itoshima_shiratani_shipping_notes(self):
        for move in self:
            if move.sale_id.itoshima_shiratani_shipping_notes:
                move.itoshima_shiratani_shipping_notes = move.sale_id.itoshima_shiratani_shipping_notes
            else:
                move.itoshima_shiratani_shipping_notes = ''

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
            if not rec.group_id:
                continue

            # 調達グループから取得（運用や設定的に複数はないはずだが、あった場合は先頭から）
            group = rec.group_id[0]
            # 調達グループは販売or製造or購買、購買の場合は単独購買なのでスルーされる
            if group:
                sale = self.env['sale.order'].search([('name', '=', group.name)])
                if sale:
                    rec.sale_id = sale
                else:
                    # 製造の親も子sole_referenceに注番が設定されているので、そこから取得
                    mrp = self.env['mrp.production'].search([('name', '=', group.name)])
                    if mrp:
                        rec.sale_id = self.env['sale.order'].search([('name', '=', mrp.sale_reference)])
                    else:
                        rec.sale_id = False
            else:
                rec.sale_id = False

    @api.depends('production_id', 'picking_id')
    def _get_mrp_production_id(self):

        for rec in self:
            if not rec.group_id and not rec.move_orig_ids:
                continue

            # 調達グループから取得（運用や設定的に複数はないはずだが、あった場合は先頭から）
            group = False
            if rec.group_id:
                group = rec.group_id[0]
            if not group and rec.move_orig_ids:
                # 調達グループがない場合を考慮して、紐づく運送から取得する（オーダー再規則や手動などで製造オーダー作成された場合など）
                if rec.move_orig_ids.group_id:
                    group = rec.move_orig_ids.group_id[0]

            # 調達グループは販売or製造or購買、製造ではない場合はスルーされる
            if group:
                mrp = self.env['mrp.production'].search([('name', '=', group.name)])
                if mrp:
                    rec.mrp_production_id = mrp.name
                else:
                    rec.mrp_production_id = None
            else:
                rec.mrp_production_id = None

            # 調達グループに製造が紐づいていない場合、販売直下の配送＝製品の配送が考えられるため対象の製造オーダーをstock.picking経由で取得する
            if not rec.mrp_production_id and rec.product_id:
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

    # @api.depends('sale_line_id', 'sale_line_id.shiratani_date', 'sale_id', 'sale_id.shiratani_entry_date')
    @api.depends('mrp_production_id','sale_id')
    def _get_shiratani_date(self):
        for rec in self:
            if rec.mrp_production_id:
                mrp_shiratani_date = self.env['mrp.production'].search([('name', '=', rec.mrp_production_id)])
                if mrp_shiratani_date and mrp_shiratani_date.shiratani_date:
                    rec.shiratani_date = mrp_shiratani_date.shiratani_date
                else:
                    related_shiratani_date = self.env['stock.move'].search([('sale_id', '=', rec.sale_id.id)])
                    for move in related_shiratani_date:
                        if move.shiratani_date:
                            rec.shiratani_date = move.shiratani_date
                            break  
            else:
                    rec.shiratani_date = False        
            # if rec.sale_line_id.shiratani_date:
            #     rec.shiratani_date = rec.sale_line_id.shiratani_date
            # elif rec.sale_id:
            #     rec.shiratani_date = rec.sale_id.shiratani_entry_date
            # else:
            #     rec.shiratani_date = False

    @api.depends('sale_line_id.depo_date','sale_line_id.depo_date','sale_line_id','sale_id','sale_id.warehouse_arrive_date')
    def _get_warehouse_arrive_date(self):
        for rec in self:
            if rec.sale_line_id.depo_date:
                rec.warehouse_arrive_date = rec.sale_line_id.depo_date
            elif rec.sale_id:
                rec.warehouse_arrive_date = rec.sale_id.warehouse_arrive_date
            else:
                rec.warehouse_arrive_date = False

    @api.depends('sale_id','sale_id.warehouse_arrive_date_2')
    def _get_warehouse_arrive_date_2(self):
        for rec in self:
            if rec.sale_id:
                rec.warehouse_arrive_date_2 = rec.sale_id.warehouse_arrive_date_2
            else:
                rec.warehouse_arrive_date_2= False

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

    @api.depends('sale_id','sale_id','picking_id.waypoint', 'sale_id.waypoint', 'picking_id.waypoint.display_name', 'sale_id.waypoint.display_name')
    def _get_area(self):
        for rec in self:
            if rec.picking_id and rec.picking_id.waypoint:
                rec.area = rec.picking_id.waypoint.display_name
                if rec.sale_id and not rec.picking_id.waypoint:
                    rec.area = rec.sale_id.waypoint.display_name
            elif rec.sale_id and rec.sale_id.waypoint:
                rec.area = rec.sale_id.waypoint.display_name
            else:
                rec.area = False

    @api.depends('sale_id','sale_id','picking_id.waypoint_2', 'sale_id.waypoint_2', 'picking_id.waypoint_2.display_name', 'sale_id.waypoint_2.display_name')
    def _get_area_2(self):
        for rec in self:
            if rec.picking_id and rec.picking_id.waypoint_2:
                rec.area_2 = rec.picking_id.waypoint_2.display_name
                if rec.sale_id and not rec.picking_id.waypoint_2:
                    rec.area_2 = rec.sale_id.waypoint_2.display_name
            elif rec.sale_id and rec.sale_id.waypoint_2:
                rec.area_2 = rec.sale_id.waypoint_2.display_name
            else:
                rec.area_2 = False
            
                
    def _get_primary_shipment_stock_move(self):
        for move in self:
            if move.picking_id:
               move.primary_shipment_stock_move = move.picking_id.primary_shipment 
            else:
                move.primary_shipment_stock_move = False
    @api.depends('shiratani_date')
    def _get_shiratani_date_delivery(self):
        for rec in self:
                rec.shiratani_date_delivery = rec.shiratani_date
            
    @api.depends('shiratani_date_delivery')
    def _set_shiratani_date_delivery(self):
        for rec in self:
            rec.shiratani_date = rec.shiratani_date_delivery
            if rec.product_id:
                mrp_production = self.env['mrp.production'].search([('name', '=', rec.mrp_production_id)])
                if mrp_production:
                    # 製造に紐づく運送/配送の白谷到着日を更新
                    move_list = self.env["stock.move"].search([('mrp_production_id', '=', mrp_production.name)])
                    if move_list:
                        move_list.write({'shiratani_date': rec.shiratani_date_delivery})

                    mrp_production.write({'shiratani_date': rec.shiratani_date_delivery})
                    if rec.picking_id:
                        picking_ids = self.env['stock.move'].search([
                            ('product_id', '=', rec.product_id.id),
                            ('origin', '=', rec.origin),
                            ('description_picking' ,'=', rec.description_picking)
                        ])
                        for move in picking_ids:
                            move.shiratani_date = rec.shiratani_date_delivery 
                    else:
                        return
                else:
                    return
        else:
            return               