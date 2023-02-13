# -*- coding: utf-8 -*-
# from odoo import http


# class RtwPresence(http.Controller):
#     @http.route('/rtw_presence/rtw_presence/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_presence/rtw_presence/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_presence.listing', {
#             'root': '/rtw_presence/rtw_presence',
#             'objects': http.request.env['rtw_presence.rtw_presence'].search([]),
#         })

#     @http.route('/rtw_presence/rtw_presence/objects/<model("rtw_presence.rtw_presence"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_presence.object', {
#             'object': obj
#         })
