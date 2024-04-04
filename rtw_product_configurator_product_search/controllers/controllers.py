# -*- coding: utf-8 -*-
# from odoo import http


# class RtwProductConfiguratorCtm(http.Controller):
#     @http.route('/rtw_product_configurator_ctm/rtw_product_configurator_ctm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_product_configurator_ctm/rtw_product_configurator_ctm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_product_configurator_ctm.listing', {
#             'root': '/rtw_product_configurator_ctm/rtw_product_configurator_ctm',
#             'objects': http.request.env['rtw_product_configurator_ctm.rtw_product_configurator_ctm'].search([]),
#         })

#     @http.route('/rtw_product_configurator_ctm/rtw_product_configurator_ctm/objects/<model("rtw_product_configurator_ctm.rtw_product_configurator_ctm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_product_configurator_ctm.object', {
#             'object': obj
#         })
