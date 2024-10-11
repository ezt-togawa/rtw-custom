from odoo.http import request
from odoo import http
from odoo.addons.mail.controllers.main import MailController

class CustomMailController(MailController):
    @http.route('/mail/read_followers', type='json', auth='user')
    def read_followers(self, res_model, res_id):
        request.env[res_model].check_access_rights("read")
        if not request.env['mail.followers'].search([('res_model', '=', res_model), ('res_id', '=', res_id)]):
            return {
                'followers': [],
                'subtypes': None
            }
        result = super(CustomMailController, self).read_followers(res_model, res_id)
        return result