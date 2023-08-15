# -*- coding: utf-8 -*-
# from odoo import http


# class SaleOrderLineCustomDate(http.Controller):
#     @http.route('/sale_order_line_custom_date/sale_order_line_custom_date/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_order_line_custom_date/sale_order_line_custom_date/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_order_line_custom_date.listing', {
#             'root': '/sale_order_line_custom_date/sale_order_line_custom_date',
#             'objects': http.request.env['sale_order_line_custom_date.sale_order_line_custom_date'].search([]),
#         })

#     @http.route('/sale_order_line_custom_date/sale_order_line_custom_date/objects/<model("sale_order_line_custom_date.sale_order_line_custom_date"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_order_line_custom_date.object', {
#             'object': obj
#         })
