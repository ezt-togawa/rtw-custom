# -*- coding: utf-8 -*-
# from odoo import http


# class RtwSf(http.Controller):
#     @http.route('/rtw_sf/rtw_sf/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_sf/rtw_sf/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_sf.listing', {
#             'root': '/rtw_sf/rtw_sf',
#             'objects': http.request.env['rtw_sf.rtw_sf'].search([]),
#         })

#     @http.route('/rtw_sf/rtw_sf/objects/<model("rtw_sf.rtw_sf"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_sf.object', {
#             'object': obj
#         })
