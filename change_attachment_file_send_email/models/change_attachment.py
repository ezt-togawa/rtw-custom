from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.http import request
from odoo.tools.safe_eval import time
from odoo.exceptions import UserError
import tempfile
from contextlib import closing
import os
import subprocess
import logging
from odoo.tools.misc import find_in_path, ustr

_logger = logging.getLogger(__name__)

    
def _get_wkhtmltopdf_bin():
    return find_in_path('wkhtmltopdf')

class CustomIrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    # override attachments file for : sale.order(quotation) | purchase.order(purchase) | account.move(invoice)
    def _render_template(self, template, values=None):        
        if values is None:
            values = {}
        context = dict(self.env.context, inherit_branding=False)
        user = self.env['res.users'].browse(self.env.uid)
        website = None
        if request and hasattr(request, 'website'):
            if request.website is not None:
                website = request.website
                context = dict(context, translatable=context.get('lang') != request.env['ir.http']._get_default_lang().code)
        view_obj = self.env['ir.ui.view'].sudo().with_context(context)

        #custom
        active_model = self.env.context.get('active_model')
        if active_model == "sale.order":
            template = "custom_report_rtw.report_quotation"
        if active_model == "purchase.order":
            template = "custom_report_rtw.report_purchase_order_sheet_for_part"
        if active_model == "account.move":
            template = "custom_report_rtw.report_invoice_3"
        #custom

        values.update(
        time=time,
        context_timestamp=lambda t: fields.Datetime.context_timestamp(self.with_context(tz=user.tz), t),
        user=user,
        res_company=self.env.company,
        website=website,
        web_base_url=self.env['ir.config_parameter'].sudo().get_param('web.base.url', default=''),
    )
        return view_obj._render_template(template, values)      
    

    # override  paper_format to show pdf  for : sale.order(quotation) | purchase.order(purchase) | account.move(invoice)
    @api.model
    def _run_wkhtmltopdf(
            self,
            bodies,
            header=None,
            footer=None,
            landscape=False,
            specific_paperformat_args=None,
            set_viewport_size=False):
        
        paperformat_id = self.get_paperformat() 

        #custom
        active_model = self.env.context.get('active_model')
        if active_model == "sale.order":
            paperformat_id = self.env["report.paperformat"].search([('name',"=","Quotation")])
        if active_model == "purchase.order":
            paperformat_id = self.env["report.paperformat"].search([('name',"=","Purchase Order")])
        if active_model == "account.move":
            paperformat_id = self.env["report.paperformat"].search([('name',"=","Invoice")])
        #custom
    
        command_args = self._build_wkhtmltopdf_args(
            paperformat_id,
            landscape,
            specific_paperformat_args=specific_paperformat_args,
            set_viewport_size=set_viewport_size)
        files_command_args = []
        temporary_files = []
        if header:
            head_file_fd, head_file_path = tempfile.mkstemp(suffix='.html', prefix='report.header.tmp.')
            with closing(os.fdopen(head_file_fd, 'wb')) as head_file:
                head_file.write(header)
            temporary_files.append(head_file_path)
            files_command_args.extend(['--header-html', head_file_path])
        if footer:
            foot_file_fd, foot_file_path = tempfile.mkstemp(suffix='.html', prefix='report.footer.tmp.')
            with closing(os.fdopen(foot_file_fd, 'wb')) as foot_file:
                foot_file.write(footer)
            temporary_files.append(foot_file_path)
            files_command_args.extend(['--footer-html', foot_file_path])
        paths = []
        for i, body in enumerate(bodies):
            prefix = '%s%d.' % ('report.body.tmp.', i)
            body_file_fd, body_file_path = tempfile.mkstemp(suffix='.html', prefix=prefix)
            with closing(os.fdopen(body_file_fd, 'wb')) as body_file:
                body_file.write(body)
            paths.append(body_file_path)
            temporary_files.append(body_file_path)
        pdf_report_fd, pdf_report_path = tempfile.mkstemp(suffix='.pdf', prefix='report.tmp.')
        os.close(pdf_report_fd)
        temporary_files.append(pdf_report_path)
        try:
            wkhtmltopdf = [_get_wkhtmltopdf_bin()] + command_args + files_command_args + paths + [pdf_report_path]
            process = subprocess.Popen(wkhtmltopdf, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            err = ustr(err)
            if process.returncode not in [0, 1]:
                if process.returncode == -11:
                    message = _(
                        'Wkhtmltopdf failed (error code: %s). Memory limit too low or maximum file number of subprocess reached. Message : %s')
                else:
                    message = _('Wkhtmltopdf failed (error code: %s). Message: %s')
                _logger.warning(message, process.returncode, err[-1000:])
                raise UserError(message % (str(process.returncode), err[-1000:]))
            else:
                if err:
                    _logger.warning('wkhtmltopdf: %s' % err)
        except:
            raise
        with open(pdf_report_path, 'rb') as pdf_document:
            pdf_content = pdf_document.read()
        for temporary_file in temporary_files:
            try:
                os.unlink(temporary_file)
            except (OSError, IOError):
                _logger.error('Error when trying to remove file %s' % temporary_file)
        return pdf_content

#special case for invoice : print apart
class CustomAccountMove(models.Model):
    _inherit = "account.move"

    def action_invoice_print(self):
        if any(not move.is_invoice(include_receipts=True) for move in self):
            raise UserError(_("Only invoices could be printed."))

        self.filtered(lambda inv: not inv.is_move_sent).write({'is_move_sent': True})
        if self.user_has_groups('account.group_account_invoice'):
            return self.env.ref('custom_report_rtw.report_invoice_rtw_3').report_action(self)
        else:
            return self.env.ref('custom_report_rtw.report_invoice_rtw_3').report_action(self)
