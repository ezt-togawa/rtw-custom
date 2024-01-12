# -*- coding: utf-8 -*-
# from odoo import http


# class RtwCrm(http.Controller):
#     @http.route('/rtw_crm/rtw_crm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_crm/rtw_crm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_crm.listing', {
#             'root': '/rtw_crm/rtw_crm',
#             'objects': http.request.env['rtw_crm.rtw_crm'].search([]),
#         })

#     @http.route('/rtw_crm/rtw_crm/objects/<model("rtw_crm.rtw_crm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_crm.object', {
#             'object': obj
#         })
