# -*- coding: utf-8 -*-
# from odoo import http


# class ConfirmedShippingDate(http.Controller):
#     @http.route('/confirmed_shipping_date/confirmed_shipping_date/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/confirmed_shipping_date/confirmed_shipping_date/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('confirmed_shipping_date.listing', {
#             'root': '/confirmed_shipping_date/confirmed_shipping_date',
#             'objects': http.request.env['confirmed_shipping_date.confirmed_shipping_date'].search([]),
#         })

#     @http.route('/confirmed_shipping_date/confirmed_shipping_date/objects/<model("confirmed_shipping_date.confirmed_shipping_date"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('confirmed_shipping_date.object', {
#             'object': obj
#         })
