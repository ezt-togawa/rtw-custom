# -*- coding: utf-8 -*-
# from odoo import http


# class RtwExcelReport(http.Controller):
#     @http.route('/rtw_excel_report/rtw_excel_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_excel_report/rtw_excel_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_excel_report.listing', {
#             'root': '/rtw_excel_report/rtw_excel_report',
#             'objects': http.request.env['rtw_excel_report.rtw_excel_report'].search([]),
#         })

#     @http.route('/rtw_excel_report/rtw_excel_report/objects/<model("rtw_excel_report.rtw_excel_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_excel_report.object', {
#             'object': obj
#         })
