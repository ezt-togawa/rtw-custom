# -*- coding: utf-8 -*-
# from odoo import http


# class RtwStockMoveLine(http.Controller):
#     @http.route('/rtw_stock_move_line/rtw_stock_move_line/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_stock_move_line/rtw_stock_move_line/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_stock_move_line.listing', {
#             'root': '/rtw_stock_move_line/rtw_stock_move_line',
#             'objects': http.request.env['rtw_stock_move_line.rtw_stock_move_line'].search([]),
#         })

#     @http.route('/rtw_stock_move_line/rtw_stock_move_line/objects/<model("rtw_stock_move_line.rtw_stock_move_line"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_stock_move_line.object', {
#             'object': obj
#         })
