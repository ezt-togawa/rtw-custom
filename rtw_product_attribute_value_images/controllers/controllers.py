# -*- coding: utf-8 -*-
# from odoo import http


# class RtwProductAttributeValueImages(http.Controller):
#     @http.route('/rtw_product_attribute_value_images/rtw_product_attribute_value_images/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_product_attribute_value_images/rtw_product_attribute_value_images/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_product_attribute_value_images.listing', {
#             'root': '/rtw_product_attribute_value_images/rtw_product_attribute_value_images',
#             'objects': http.request.env['rtw_product_attribute_value_images.rtw_product_attribute_value_images'].search([]),
#         })

#     @http.route('/rtw_product_attribute_value_images/rtw_product_attribute_value_images/objects/<model("rtw_product_attribute_value_images.rtw_product_attribute_value_images"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_product_attribute_value_images.object', {
#             'object': obj
#         })
