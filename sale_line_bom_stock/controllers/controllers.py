# -*- coding: utf-8 -*-
# from odoo import http


# class SaleLineBomStock(http.Controller):
#     @http.route('/sale_line_bom_stock/sale_line_bom_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_line_bom_stock/sale_line_bom_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_line_bom_stock.listing', {
#             'root': '/sale_line_bom_stock/sale_line_bom_stock',
#             'objects': http.request.env['sale_line_bom_stock.sale_line_bom_stock'].search([]),
#         })

#     @http.route('/sale_line_bom_stock/sale_line_bom_stock/objects/<model("sale_line_bom_stock.sale_line_bom_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_line_bom_stock.object', {
#             'object': obj
#         })
