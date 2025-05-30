# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from dateutil.parser import parse


class MrpProductionCus(models.Model):
    _inherit = 'mrp.production'
    _cache = {}

    revised_edition_ids = fields.One2many(
        comodel_name="mrp.revised_edition",
        inverse_name="mrp_id",
        string="revised edition")
    prod_parts_arrival_schedule = fields.Char(string="製造部材入荷予定", store=True)
    is_drag_drop_calendar = fields.Boolean()
    mrp_ship_address_id = fields.Many2one(comodel_name='mrp.ship.address', string="最終配送先")
    combined_shipment = fields.Char(string='同梱',compute = "_combined_shipment_compute")
    working_notes = fields.Char(string='作業メモ')
    address_ship = fields.Selection([ ('倉庫', '倉庫'),
    ('直送', '直送'),
    ('デポ１', 'デポ１'),
    ('デポ２', 'デポ２')], string="送付先")
    waypoint_option = fields.Text(compute="_compute_waypoint_option")
    storehouse_id = fields.Many2one(comodel_name='stock.warehouse', string="倉庫")
    duration = fields.Float('Duration', help="Track duration in hours.")
    color = fields.Integer(string='Event Color', default=1)
    sales_order = fields.Char(string='販売オーダー', compute="_compute_sales_order")
    calendar_display_name = fields.Text(compute="_compute_display_name_calendar", store=True)
    shipping = fields.Char(compute="_compute_shipping", string="送付先")
    

    def _combined_shipment_compute(self):
        for line in self:
            if line.sale_reference:
                sale_order = self.env['sale.order'].search([('name', '=', line.sale_reference)], limit=1)
                if sale_order:
                    sale_order_line = self.env['sale.order.line'].search([
                    ("order_id", "=", sale_order.id),
                    ("product_id", "=", line.product_id.id)
                ], limit=1)
                    if sale_order_line:
                        for order_line in sale_order_line:
                            if order_line.combined_shipment:
                                line.combined_shipment = order_line.combined_shipment.name
                            else:
                                line.combined_shipment = False
                    else:
                        line.combined_shipment = False
                else:
                    line.combined_shipment = False
            else:
                line.combined_shipment = False

    @api.depends('address_ship')
    def _compute_waypoint_option(self):
        sale_order = self.env['sale.order'].search([('name', '=', self.sale_reference)], limit=1)
        if self.address_ship == "デポ１":
            self.waypoint_option = sale_order.waypoint.name
        elif self.address_ship == "デポ２":
            self.waypoint_option = sale_order.waypoint_2.name
        else:
            self.waypoint_option = ""        

    def _compute_shipping(self):
        for line in self:
            if line.address_ship == "倉庫":
                line.shipping = "白谷運輸"
            else:
                line.shipping = ""
            
    def _compute_sales_order(self):
        for line in self:
            order_no = ''
            if line.origin:
                if '/MO/' not in line.origin:
                    order_no = line.origin
                else:
                    source_mo = self.env['mrp.production'].search([('name', '=', line.origin)], limit=1)
                    while source_mo and source_mo.origin and '/MO/' in source_mo.origin:
                        source_mo = self.env['mrp.production'].search([('name', '=', source_mo.origin)], limit=1)

                    if source_mo:
                        order_no = source_mo.origin
                    else:
                        order_no = line.origin

            line.sales_order = order_no

    @api.model
    def create(self, vals):
        record = super(MrpProductionCus, self).create(vals)
        if 'address_ship' not in vals:
            if record.is_child_mo:
                record.address_ship = '倉庫'
                record._onchange_address_ship()
            else:
                sale_order = self.env['sale.order'].search([('name', '=', record.sale_reference)], limit=1)
                warehouse_name = record.picking_type_id.warehouse_id.name
                if warehouse_name in ["糸島工場","日東木工","アサヒ", "酒見椅子"]:
                    if sale_order.sipping_to:
                        if sale_order.sipping_to == 'direct':
                            record.address_ship = '直送' 
                        else:
                            record.address_ship = '倉庫'
                        record._onchange_address_ship()
                    else:
                        record.address_ship = '倉庫'
                    record._onchange_address_ship()
                else:
                    if sale_order.sipping_to:
                        if sale_order.sipping_to == 'direct':
                            record.address_ship = '直送' 
                        else:
                            record.address_ship = 'デポ１'
                        record._onchange_address_ship()
                    else:
                        record.address_ship = 'デポ１'
                    record._onchange_address_ship()
        return record

    @api.onchange('address_ship')
    def _onchange_address_ship(self):
        for record in self:
            warehouse = False
            if record.is_child_mo and record.address_ship == '倉庫':
                source_mo = self.env["mrp.production"].search([('name', '=', record.origin)], limit=1)
                if source_mo and source_mo.move_raw_ids:
                    for move in source_mo.move_raw_ids:
                        if move.product_id.id == record.product_id.id:
                            biggest_move_id = self.env['stock.move'].search(
                                [('origin', '=', source_mo.name), ('product_id', '=', move.product_id.id)],
                                order='id desc', limit=1)
                            if biggest_move_id:
                                warehouse = self.env["stock.warehouse"].search(
                                    [('lot_stock_id', '=', biggest_move_id.location_dest_id.id)], limit=1)
            # source mo
            elif record.address_ship == '倉庫':
                shiratani = self.env["stock.warehouse"].search([('name', '=', '白谷運輸')], limit=1)
                warehouse= shiratani.id or False
            record.storehouse_id = warehouse

    # 新規作成時に製造部材入荷予定を設定
    # @api.depends('name')
    # def _compute_prod_parts_arrival_schedule(self):
    #     for record in self:
    #         print('_compute_prod_parts_arrival_schedule', record.name)
    #         if record.origin:
    #             order_no = record.origin
    #             parent_mo = self.env["mrp.production"].search([('name', '=', order_no)])
    #             child_mo = self.env["mrp.production"].search(
    #                 [('sale_reference', '=', parent_mo.sale_reference), ('origin', '=', parent_mo.name)])
    #             if child_mo and parent_mo.move_raw_ids:
    #                 arrival_schedule = ''
    #                 for move in parent_mo.move_raw_ids:
    #                     if move.forecast_expected_date:
    #                         arrival_schedule += str(parent_mo._convert_timezone(move.forecast_expected_date)) + "\n"
    #                         print('move.forecast_expected_date', move.forecast_expected_date)
    #                 parent_mo.prod_parts_arrival_schedule = arrival_schedule.rstrip('\n') if arrival_schedule else ''
 
    def create_revised_edition(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.revised_edition',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_mrp_id': self.id,
                'default_owner_id': self.env.user.id,
            }
        }

    @api.depends('is_drag_drop_calendar', 'itoshima_shipping_date', 'sale_reference')
    def _compute_display_name_calendar(self):
        for record in self:
            display_name = ''
            if record.is_drag_drop_calendar:
                display_name = '[✔] '

            order_no = record.sale_reference or ''
            product_no = ''
            date_planned = ''

            if record.product_id and record.product_id.product_no:
                product_no = record.product_id.product_no
            elif record.product_id and not record.product_id.product_no and record.product_id.name:
                product_no = record.product_id.name
            if record.itoshima_shipping_date:
                date_planned = str(record.itoshima_shipping_date)

            if order_no:
                if product_no and date_planned:
                    display_name += f'{order_no}/{product_no}/{date_planned}'
                elif product_no:
                    display_name += f'{order_no}/{product_no}'
                elif date_planned:
                    display_name += f'{order_no}/{date_planned}'
                else:
                    display_name += order_no
            elif product_no:
                if date_planned:
                    display_name += f'{product_no}/{date_planned}'
                else:
                    display_name += product_no
            elif date_planned:
                display_name += date_planned

            record.calendar_display_name = display_name

    @api.depends(lambda self: (self._rec_name,) if self._rec_name else ())
    def _compute_display_name(self):
        cache_map = {key: value for key, value in self._cache.items()}
        mrp_id_dragging = cache_map.get('mrp_id_dragging')
        for record in self:
            mrp_date_planned_reset = cache_map.get("date_planned_reset_" + str(record.id))
            if record.id == mrp_date_planned_reset:
                # 製造開始予定日が自動再計算された場合は除外（編集扱いにしない）
                record.color = 1
                record.is_drag_drop_calendar = False

            elif record.id == mrp_id_dragging and record.color != 4:
                # just add color + tick mark for mrp_id_dragging and that mrp has a color other than blue
                record.color = 4
                record.is_drag_drop_calendar = True

            record.display_name = record.calendar_display_name

            if mrp_date_planned_reset:
                del record._cache['date_planned_reset_' + str(record.id)]

        if mrp_id_dragging:
            del self._cache['mrp_id_dragging']

    def write(self, vals):
        old_date_planned_start = {record.id: record.date_planned_start for record in self}

        res = super(MrpProductionCus, self).write(vals)
        for record in self:
            if 'date_planned_start' in vals:
                old_date_planned = old_date_planned_start.get(record.id)
                new_date_planned = vals['date_planned_start']

                if isinstance(new_date_planned, str):
                    new_date_planned = parse(new_date_planned)

                # dragging date_planned_start ( mrp_calendar or mrp_form)
                if new_date_planned and old_date_planned:
                    # just update (not create)
                    if record.create_date != record.write_date:
                        cache_key = 'mrp_id_dragging'
                        if cache_key in record._cache:
                            del record._cache[cache_key]
                        record._cache[cache_key] = record.id

                    if new_date_planned < old_date_planned:
                        po = self.env["purchase.order"].search([('origin', 'ilike', record.name)])
                        if po:
                            for p in po:
                                p.check_schedule_boolean = True

                        mo_child = self.env["mrp.production"].search([('mrp_reference', 'ilike', record.name)])
                        if mo_child:
                            for mo in mo_child:
                                po_child = self.env["purchase.order"].search([('origin', 'ilike', mo.name)])
                                if po_child:
                                    for po in po_child:
                                        po.check_schedule_boolean = True
        return res


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        if self.estimated_shipping_date:
            mrp_production = self.env['mrp.production'].search(
                [('sale_reference', '=', self.name)])
            if mrp_production:
                for mrp in mrp_production:
                    mrp.write({"estimated_shipping_date": self.estimated_shipping_date})
        return result

    def action_view_mrp_production(self):
        self.ensure_one()
        procurement_groups = self.env['procurement.group'].search([('sale_id', 'in', self.ids)])
        mrp_production_ids = set(
            procurement_groups.stock_move_ids.created_production_id.procurement_group_id.mrp_production_ids.ids) | \
                             set(procurement_groups.mrp_production_ids.ids)
        action = {
            'res_model': 'mrp.production',
            'type': 'ir.actions.act_window',
        }
        if len(mrp_production_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': mrp_production_ids.pop(),
            })
        else:
            tree_view_id = self.env.ref('rtw_mrp_custom.sale_to_mrp_list_view_tree').id
            action.update({
                'name': _("Manufacturing Orders Generated by %s", self.name),
                'domain': [('id', 'in', list(mrp_production_ids))],
                'view_mode': 'tree,form',
                'views': [(tree_view_id, 'tree'), (False, 'form')]
            })
        return action