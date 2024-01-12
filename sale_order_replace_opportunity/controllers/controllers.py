# -*- coding: utf-8 -*-
# from odoo import http


# class SaleOrderRtw(http.Controller):
#     @http.route('/sale_order_rtw/sale_order_rtw/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_order_rtw/sale_order_rtw/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_order_rtw.listing', {
#             'root': '/sale_order_rtw/sale_order_rtw',
#             'objects': http.request.env['sale_order_rtw.sale_order_rtw'].search([]),
#         })

#     @http.route('/sale_order_rtw/sale_order_rtw/objects/<model("sale_order_rtw.sale_order_rtw"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_order_rtw.object', {
#             'object': obj
#         })
