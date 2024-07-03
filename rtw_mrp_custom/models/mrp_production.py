# -*- coding: utf-8 -*-
from odoo import models, fields, api
from dateutil.parser import parse
from datetime import datetime
import pytz

class MrpProductionCus(models.Model):
    _inherit = 'mrp.production'

    revised_edition_ids = fields.One2many(
        comodel_name="mrp.revised_edition",
        inverse_name="mrp_id",
        string="revised edition")
    prod_parts_arrival_schedule = fields.Char(string="製造部材入荷予定")
    is_drag_drop_calendar = fields.Boolean()
    
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

    def _compute_display_name(self):
        for record in self:
            
            order_no = ''
            product_no = ''
            date_planned = ''
            
            if record.sale_reference:
                order_no = record.sale_reference
                child_MO = self.env["mrp.production"].search([('sale_reference', '=', order_no), ('origin', '=', record.name)])
                if child_MO and record.move_raw_ids:
                    arrival_schedule = ''
                    for move in record.move_raw_ids:
                        if move.forecast_expected_date:
                            arrival_schedule += str(move.forecast_expected_date) + "\n"
                            
                    record.prod_parts_arrival_schedule = arrival_schedule.rstrip('\n')
                
            if record.product_id and record.product_id.product_no:
                product_no = record.product_id.product_no
            if record.estimated_shipping_date:
                date_planned = str(record.estimated_shipping_date)
            
            display_name = ''
            if record.is_drag_drop_calendar:
                display_name = '[✔] '
                
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
                
            record.display_name = display_name
            
    def write(self, vals):
        old_date_planned_start = {record.id: record.date_planned_start for record in self}

        res = super(MrpProductionCus, self).write(vals)
        for record in self:
            if record.sale_reference and 'estimated_shipping_date' in vals:
                so = self.env['sale.order'].search([('name', '=', record.sale_reference)])
                so.estimated_shipping_date = vals['estimated_shipping_date']

            if 'date_planned_start' in vals:
                old_date = old_date_planned_start.get(record.id)
                new_date = vals['date_planned_start']

                if isinstance(new_date, str):
                    new_date = parse(new_date)

                if new_date and old_date and new_date < old_date:
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
    
    @api.model
    def update_date_planned_start(self, record):
        id = int(record.get('id'))
        time_str = str(record.get('time'))
        if id and time_str:
            manu_oder = self.env["mrp.production"].search([('id', '=', id)])
            if manu_oder:
                for mo in manu_oder:
                    mo.is_drag_drop_calendar = True
                    convert_date = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                    # Convert to UTC timezone
                    utc_datetime = convert_date.astimezone(pytz.utc)
                    naive_datetime = utc_datetime.replace(tzinfo=None)
                    mo.date_planned_start = naive_datetime
        return True
            
class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        if self.estimated_shipping_date:
            mrp_production = self.env['mrp.production'].search(
                [('sale_reference', '=', self.name)])
            if mrp_production:
                for mrp in mrp_production:
                    mrp.write({"estimated_shipping_date":self.estimated_shipping_date})
        return result