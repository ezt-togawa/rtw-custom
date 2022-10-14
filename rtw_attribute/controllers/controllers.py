# -*- coding: utf-8 -*-
# from odoo import http


# class RtwAttribute(http.Controller):
#     @http.route('/rtw_attribute/rtw_attribute/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_attribute/rtw_attribute/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_attribute.listing', {
#             'root': '/rtw_attribute/rtw_attribute',
#             'objects': http.request.env['rtw_attribute.rtw_attribute'].search([]),
#         })

#     @http.route('/rtw_attribute/rtw_attribute/objects/<model("rtw_attribute.rtw_attribute"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_attribute.object', {
#             'object': obj
#         })
