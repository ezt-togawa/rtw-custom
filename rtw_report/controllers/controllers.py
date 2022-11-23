# -*- coding: utf-8 -*-
# from odoo import http


# class RtwReport(http.Controller):
#     @http.route('/rtw_report/rtw_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_report/rtw_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_report.listing', {
#             'root': '/rtw_report/rtw_report',
#             'objects': http.request.env['rtw_report.rtw_report'].search([]),
#         })

#     @http.route('/rtw_report/rtw_report/objects/<model("rtw_report.rtw_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_report.object', {
#             'object': obj
#         })
