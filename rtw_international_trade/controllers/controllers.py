# -*- coding: utf-8 -*-
# from odoo import http


# class RtwInternationalTrade(http.Controller):
#     @http.route('/rtw_international_trade/rtw_international_trade/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_international_trade/rtw_international_trade/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_international_trade.listing', {
#             'root': '/rtw_international_trade/rtw_international_trade',
#             'objects': http.request.env['rtw_international_trade.rtw_international_trade'].search([]),
#         })

#     @http.route('/rtw_international_trade/rtw_international_trade/objects/<model("rtw_international_trade.rtw_international_trade"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_international_trade.object', {
#             'object': obj
#         })
