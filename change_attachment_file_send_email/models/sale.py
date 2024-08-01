from odoo import models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _find_mail_template(self, force_confirmation_template=False):
        self.ensure_one()
        
        return  self.env['ir.model.data'].xmlid_to_res_id('change_attachment_file_send_email.send_by_email_button_sale_cus', raise_if_not_found=False)
