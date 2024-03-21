# -*- coding: utf-8 -*-
# from odoo import http


# class RtwPartner(http.Controller):
#     @http.route('/rtw_partner/rtw_partner/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_partner/rtw_partner/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_partner.listing', {
#             'root': '/rtw_partner/rtw_partner',
#             'objects': http.request.env['rtw_partner.rtw_partner'].search([]),
#         })

#     @http.route('/rtw_partner/rtw_partner/objects/<model("rtw_partner.rtw_partner"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_partner.object', {
#             'object': obj
#         })
