# -*- coding: utf-8 -*-
# from odoo import http


# class RtwPurchase(http.Controller):
#     @http.route('/rtw_purchase/rtw_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_purchase/rtw_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_purchase.listing', {
#             'root': '/rtw_purchase/rtw_purchase',
#             'objects': http.request.env['rtw_purchase.rtw_purchase'].search([]),
#         })

#     @http.route('/rtw_purchase/rtw_purchase/objects/<model("rtw_purchase.rtw_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_purchase.object', {
#             'object': obj
#         })
