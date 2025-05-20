# -*- coding: utf-8 -*-

from odoo import models, fields, api
class rtw_purchase(models.Model):
    _inherit = "purchase.order"
    
    schedule_check = fields.Selection([('warning', 'Alert'), ('danger', 'Error')], string="Schedule Check")
    
    check_schedule_boolean = fields.Boolean()
    check_schedule_icon = fields.Char('Icon', default="fa-warning")

    sale_order_ids = fields.Char("sale order", compute='_compute_sale_order')
    sale_order_names = fields.Char("sale order title")
    operation_type = fields.Many2one('stock.picking.type' , string="オペレーションタイプ", compute='_compute_operation_type')
    working_notes = fields.Char(string='作業メモ')
    destination_note = fields.Text('送り先注記')
    resend = fields.Char('再送')
    filter_so_ids = fields.Char("filter so ids")

    def _compute_operation_type(self):
            operation_type_value = self.order_line.move_dest_ids.group_id.mrp_production_ids | self.order_line.move_ids.move_dest_ids.group_id.mrp_production_ids
            if operation_type_value:
                self.operation_type = operation_type_value[0].picking_type_id
            else:
                self.operation_type = False

    # @api.model
    def action_purchase_form(self):
        self.ensure_one()
        action = self.env.ref("purchase.purchase_form_action")
        form = self.env.ref("purchase.purchase_order_form")
        action = action.read()[0]
        action["views"] = [(form.id, "form")]
        action["target"] = "new"
        action["res_id"] = self.id
        return action

    def _get_so_from_mrp(self , mrp_production , count = 0):
        if count >= 10:
            return False
        if not mrp_production.origin:
            return False
        
        sale_order_id = False
        if '/MO/' in mrp_production.origin:
            mrp = self.env['mrp.production'].search([('name','=',mrp_production.origin)])
            if mrp:
                count += 1
                sale_order_id = self._get_so_from_mrp(mrp, count)
        else:
            sale_order_id = self.env['sale.order'].search([('name','=',mrp_production.origin)])
        return sale_order_id
    
    @api.depends('order_line.move_dest_ids.group_id.mrp_production_ids')
    def _compute_sale_order(self):
        for purchase in self:
            purchase.sale_order_ids = False
            move_dest_ids = purchase.order_line.move_dest_ids.group_id.mrp_production_ids | purchase.order_line.move_ids.move_dest_ids.group_id.mrp_production_ids
            if move_dest_ids:
                order = []
                name = []
                order_ids=[]
                for rec in move_dest_ids:
                    if rec.origin:
                        sale_order = self._get_so_from_mrp(rec)
                        if sale_order and not sale_order.id in order_ids:
                            if sale_order.name:
                                order.append(sale_order.name)
                            if sale_order.title:
                                name.append(sale_order.title)
                            order_ids.append(sale_order.id)
                    
                    purchase.sale_order_ids = ','.join(order)
                    purchase.filter_so_ids = ','.join(order)
                    purchase.sale_order_names = ','.join(name)
            else:
                if purchase.origin:
                    check_sale_order = self.env['sale.order'].search([('name', '=', purchase.origin)], limit=1)
                    if check_sale_order:
                        purchase.sale_order_ids = purchase.origin
                        purchase.filter_so_ids = purchase.origin
                        purchase.sale_order_names = check_sale_order.title
                    else:
                        purchase.sale_order_ids = ''
                        purchase.sale_order_names = ''
                        purchase.filter_so_ids = ''
                elif purchase.purchase_order_line and purchase.purchase_order_line[0].sale_order_ids:
                    purchase.sale_order_ids = purchase.purchase_order_line[0].sale_order_ids
                    purchase.filter_so_ids = purchase.purchase_order_line[0].sale_order_ids
                    purchase.sale_order_names = purchase.purchase_order_line[0].sale_order_names
                else:
                    purchase.sale_order_ids = ''
                    purchase.filter_so_ids = ''
                    purchase.sale_order_names = ''

                # sale_order = self.env['sale.order'].search([('name', '=', move_dest_ids)])
            # move_dest_ids.write({
            #     'name': self.invoice_id.name,
            #     'warranty_request_ids': [(4, self.id, {
            #     })]
            #     })
            
    def toggle_check_schedule(self):
        for line in self:
            line.check_schedule_boolean = False
            
    def button_confirm(self):
        res = super(rtw_purchase, self).button_confirm()
        user_login = self.env.user
        res_user = self.env["res.users"].search([("id", "=", user_login.id)])
        po = self.env["purchase.order"].search([("id", "=", self.id)])
        if not po.user_id:
            po.user_id = res_user
        return res