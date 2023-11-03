# -*- coding: utf-8 -*-
# from odoo import http


# class CustomReportRtw(http.Controller):
#     @http.route('/custom_report_rtw/custom_report_rtw/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_report_rtw/custom_report_rtw/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_report_rtw.listing', {
#             'root': '/custom_report_rtw/custom_report_rtw',
#             'objects': http.request.env['custom_report_rtw.custom_report_rtw'].search([]),
#         })

#     @http.route('/custom_report_rtw/custom_report_rtw/objects/<model("custom_report_rtw.custom_report_rtw"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_report_rtw.object', {
#             'object': obj
#         })
