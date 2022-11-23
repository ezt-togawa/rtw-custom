# -*- coding: utf-8 -*-
# from odoo import http


# class RtwDmReport(http.Controller):
#     @http.route('/rtw_dm_report/rtw_dm_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_dm_report/rtw_dm_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_dm_report.listing', {
#             'root': '/rtw_dm_report/rtw_dm_report',
#             'objects': http.request.env['rtw_dm_report.rtw_dm_report'].search([]),
#         })

#     @http.route('/rtw_dm_report/rtw_dm_report/objects/<model("rtw_dm_report.rtw_dm_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_dm_report.object', {
#             'object': obj
#         })
