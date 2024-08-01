from odoo import models

class PurchaseOrderCus(models.Model):
    _inherit = "purchase.order"

    def action_rfq_send(self):
        res = super(PurchaseOrderCus, self).action_rfq_send()
        template_id = self.env['ir.model.data'].xmlid_to_res_id('change_attachment_file_send_email.send_by_email_button_purchase_cus', raise_if_not_found=False)
        context = dict(res.get('context', {}))
        context.update({
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
        })
        
        res['context'] = context
        return res
