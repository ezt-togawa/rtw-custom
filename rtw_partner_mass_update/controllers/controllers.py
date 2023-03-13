# -*- coding: utf-8 -*-
# from odoo import http


# class RtwPartnerMassUpdate(http.Controller):
#     @http.route('/rtw_partner_mass_update/rtw_partner_mass_update/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rtw_partner_mass_update/rtw_partner_mass_update/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rtw_partner_mass_update.listing', {
#             'root': '/rtw_partner_mass_update/rtw_partner_mass_update',
#             'objects': http.request.env['rtw_partner_mass_update.rtw_partner_mass_update'].search([]),
#         })

#     @http.route('/rtw_partner_mass_update/rtw_partner_mass_update/objects/<model("rtw_partner_mass_update.rtw_partner_mass_update"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rtw_partner_mass_update.object', {
#             'object': obj
#         })
