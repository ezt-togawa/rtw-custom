# -*- coding: utf-8 -*-
# from odoo import http


# class RtwMrpCustom(http.Controller):
#     @http.route('/rtw_mrp_custom/rtw_mrp_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_mrp_custom/rtw_mrp_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_mrp_custom.listing', {
#             'root': '/rtw_mrp_custom/rtw_mrp_custom',
#             'objects': http.request.env['rtw_mrp_custom.rtw_mrp_custom'].search([]),
#         })

#     @http.route('/rtw_mrp_custom/rtw_mrp_custom/objects/<model("rtw_mrp_custom.rtw_mrp_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_mrp_custom.object', {
#             'object': obj
#         })
