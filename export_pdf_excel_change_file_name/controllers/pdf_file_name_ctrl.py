from odoo.addons.web.controllers.main import ReportController

from odoo import  _
import datetime
import json

import werkzeug
import werkzeug.exceptions
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from werkzeug.urls import url_decode

from odoo.tools.safe_eval import safe_eval, time
from odoo import http
from odoo.http import content_disposition,  request, serialize_exception as _serialize_exception
from odoo.tools import html_escape

class PdfFileNameCus(ReportController):

    @http.route(['/report/download'], type='http', auth="user")
    def report_download(self, data, token, context=None):
        """This function is used by 'action_manager_report.js' in order to trigger the download of
        a pdf/controller report.

        :param data: a javascript array JSON.stringified containg report internal url ([0]) and
        type [1]
        :returns: Response with a filetoken cookie and an attachment header
        """
        requestcontent = json.loads(data)
        url, type = requestcontent[0], requestcontent[1]
        try:
            if type in ['qweb-pdf', 'qweb-text']:
                converter = 'pdf' if type == 'qweb-pdf' else 'text'
                extension = 'pdf' if type == 'qweb-pdf' else 'txt'

                pattern = '/report/pdf/' if type == 'qweb-pdf' else '/report/text/'
                reportname = url.split(pattern)[1].split('?')[0]

                docids = None
                if '/' in reportname:
                    reportname, docids = reportname.split('/')

                if docids:
                    # Generic report:
                    response = self.report_routes(reportname, docids=docids, converter=converter, context=context)
                else:
                    # Particular report:
                    data = dict(url_decode(url.split('?')[1]).items())  # decoding the args represented in JSON
                    if 'context' in data:
                        context, data_context = json.loads(context or '{}'), json.loads(data.pop('context'))
                        context = json.dumps({**context, **data_context})
                    response = self.report_routes(reportname, converter=converter, context=context, **data)

                report = request.env['ir.actions.report']._get_report_from_name(reportname)
                filename = "%s.%s" % (report.name, extension)

                if docids:
                    ids = [int(x) for x in docids.split(",")]
                    obj = request.env[report.model].browse(ids)
                    if report.print_report_name and not len(obj) > 1:
                        report_name = safe_eval(report.print_report_name, {'object': obj, 'time': time})
                        filename = "%s.%s" % (report_name, extension)
                        
                    # custom export pdf list 
                    if len(obj) > 1:
                        if obj._name == 'purchase.order' or obj._name == 'mrp.production':
                            filename = "%s.%s" % (report.name + "-" + datetime.datetime.now().strftime('%Y-%m-%dT%H%M%S'), extension)
                        elif obj._name == 'purchase.order.line':
                            filename = "%s.%s" % ('発注書(部材用) ' + "-" + datetime.datetime.now().strftime('%Y-%m-%dT%H%M%S'), extension)
                    # custom export pdf list   
                
                response.headers.add('Content-Disposition', content_disposition(filename))
                response.set_cookie('fileToken', token)
                return response
            else:
                return
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            res = request.make_response(html_escape(json.dumps(error)))
            raise werkzeug.exceptions.InternalServerError(response=res) from e