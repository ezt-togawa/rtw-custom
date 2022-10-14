# -*- coding: utf-8 -*-
# from odoo import http


# class RtwLettermgmt(http.Controller):
#     @http.route('/rtw_lettermgmt/rtw_lettermgmt/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_lettermgmt/rtw_lettermgmt/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_lettermgmt.listing', {
#             'root': '/rtw_lettermgmt/rtw_lettermgmt',
#             'objects': http.request.env['rtw_lettermgmt.rtw_lettermgmt'].search([]),
#         })

#     @http.route('/rtw_lettermgmt/rtw_lettermgmt/objects/<model("rtw_lettermgmt.rtw_lettermgmt"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_lettermgmt.object', {
#             'object': obj
#         })
