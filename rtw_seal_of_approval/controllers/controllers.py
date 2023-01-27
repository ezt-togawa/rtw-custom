# -*- coding: utf-8 -*-
# from odoo import http


# class RtwSealOfApproval(http.Controller):
#     @http.route('/rtw_seal_of_approval/rtw_seal_of_approval/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_seal_of_approval/rtw_seal_of_approval/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_seal_of_approval.listing', {
#             'root': '/rtw_seal_of_approval/rtw_seal_of_approval',
#             'objects': http.request.env['rtw_seal_of_approval.rtw_seal_of_approval'].search([]),
#         })

#     @http.route('/rtw_seal_of_approval/rtw_seal_of_approval/objects/<model("rtw_seal_of_approval.rtw_seal_of_approval"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_seal_of_approval.object', {
#             'object': obj
#         })
