from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_round
from datetime import datetime
from dateutil.relativedelta import relativedelta


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.depends('origin')
    def _compute_reference_value(self):
        for value in self:
            sale_ids = self.env['sale.order'].search([('name', '=', value.origin)])
            #             print(sale_ids,'mrp')
            if sale_ids:
                value.sale_reference = sale_ids.name
            else:
                mrp_ids = self.env['mrp.production'].search([('name', '=', value.origin)])
                value.sale_reference = mrp_ids.sale_reference
            #             print(value.sale_reference,'sale')

    @api.depends('name')
    def _compute_reference_mo(self):
        for value in self:
            if value.state == 'draft':
                sale_ids = self.env['sale.order'].search([('name', '=', value.origin)])
                if sale_ids:
                    value.mrp_reference = value.name
                #                     print(value.mrp_reference,'mrp_reference')

                else:
                    mrp_ids = self.env['mrp.production'].search([('name', '=', value.origin)])
                    value.mrp_reference = mrp_ids.mrp_reference
            #                     print(value.mrp_reference,'MO')

            if not value.origin:
                value.mrp_reference = value.name

            else:
                mrp_ids = self.env['mrp.production'].search([('name', '=', value.mrp_reference)])
                for ele in mrp_ids:
                    value.mrp_reference = ele.mrp_reference

    def _compute_production_type(self):
        for record in self:
                list_custom_config = ''
                production_type = ''
                production_memo = ''
                sale_order_line = False

                search_criteria = [ #limit 10 times
                    ('move_ids', 'in', record.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.id),
                ]

                for search in search_criteria: #find sale_order_line
                    if self.env['sale.order.line'].search([search]):
                        sale_order_line = self.env['sale.order.line'].search([search])
                        break

                if sale_order_line:
                    config_custom_values = self.env['product.config.session.custom.value'].search([('cfg_session_id','=',sale_order_line.config_session_id.id)])

                    for custom in config_custom_values: #get list config custom of order line
                        list_custom_config = list_custom_config + '<div>'+ custom.attribute_id.name + ' : ' + custom.value +'</div>'

                    for line in sale_order_line: #get p_type and memo of order line
                        if line.product_id == self.product_id:
                            if line.p_type:
                                if line.p_type == 'special':
                                    p_type = '別注'
                                elif line.p_type == 'custom':
                                    p_type = '特注'
                            else:
                                p_type = ''

                            if line.memo:
                                memo = line.memo
                            else:
                                memo = ''

                            if memo:
                                production_memo = memo
                            if p_type:
                                production_type = p_type

                    record.production_type = production_type + list_custom_config
                    record.production_memo = production_memo
                else:
                    record.production_type = ''
                    record.production_memo = ''

    def _inverse_production_memo(self):
        for record in self:
                sale_order_line = []
                search_criteria = [ #limit 10 times
                    ('move_ids', 'in', record.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.id),
                    ('move_ids', 'in', record.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.move_dest_ids.id),
                ]

                for search in search_criteria: #find sale_order_line
                    if self.env['sale.order.line'].search([search]):
                        sale_order_line = self.env['sale.order.line'].search([search])
                        break

                if sale_order_line:
                    for line in sale_order_line:
                        line.write({'memo': record.production_memo})


    sale_reference = fields.Char('SO Reference', compute='_compute_reference_value', store=True)
    mrp_reference = fields.Char('MO Reference', compute='_compute_reference_mo', store=True)
    production_type = fields.Char('製品タイプ' , compute='_compute_production_type')
    production_memo = fields.Char('memo' , compute='_compute_production_type' , inverse='_inverse_production_memo')

class Workorder(models.Model):
    _inherit = 'mrp.workorder'

    sale_reference = fields.Char('SO Reference', related='production_id.sale_reference')
    mrp_reference = fields.Char('MO Reference', related='production_id.mrp_reference')
