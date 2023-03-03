# -*- coding: utf-8 -*-
# from odoo import http


# class RtwStockReportXlsx(http.Controller):
#     @http.route('/rtw_stock_report_xlsx/rtw_stock_report_xlsx/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_stock_report_xlsx/rtw_stock_report_xlsx/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_stock_report_xlsx.listing', {
#             'root': '/rtw_stock_report_xlsx/rtw_stock_report_xlsx',
#             'objects': http.request.env['rtw_stock_report_xlsx.rtw_stock_report_xlsx'].search([]),
#         })

#     @http.route('/rtw_stock_report_xlsx/rtw_stock_report_xlsx/objects/<model("rtw_stock_report_xlsx.rtw_stock_report_xlsx"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_stock_report_xlsx.object', {
#             'object': obj
#         })
