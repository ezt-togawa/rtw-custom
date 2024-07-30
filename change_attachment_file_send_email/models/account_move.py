from odoo import models, _

class AccountMoveCus(models.Model):
    _inherit = "account.move"
    
    def action_invoice_sent(self):
        res = super(AccountMoveCus, self).action_invoice_sent()
        template_id = self.env['ir.model.data'].xmlid_to_res_id('change_attachment_file_send_email.send_by_email_button_invoice_cus', raise_if_not_found=False)
        context = dict(res.get('context', {}))
        context.update({
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
        })
        
        res['context'] = context
        return res
    