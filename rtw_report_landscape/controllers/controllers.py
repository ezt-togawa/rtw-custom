# -*- coding: utf-8 -*-
# from odoo import http


# class RtwReportLandscape(http.Controller):
#     @http.route('/rtw_report_landscape/rtw_report_landscape/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_report_landscape/rtw_report_landscape/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_report_landscape.listing', {
#             'root': '/rtw_report_landscape/rtw_report_landscape',
#             'objects': http.request.env['rtw_report_landscape.rtw_report_landscape'].search([]),
#         })

#     @http.route('/rtw_report_landscape/rtw_report_landscape/objects/<model("rtw_report_landscape.rtw_report_landscape"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_report_landscape.object', {
#             'object': obj
#         })
