import time
import calendar
from datetime import datetime
import threading
from odoo import models

class mailing_mailing(models.Model):
    _inherit = "mailing.mailing"
    
    def delayed_check_contact_info(self,time_cron):
        time.sleep(time_cron)
        mailing_trace= self.env['mailing.trace'].search([('mass_mailing_id','=',self.id)])
        if mailing_trace:
            for l in  mailing_trace:
                l._compute_contact()
        return
        
    def time_cron(self,time_cron,time_type):
        if time_type == 'months':
            now = datetime.now()
            days_in_month = calendar.monthrange(now.year, now.month)[1]
            time_cron *= 86400 * int(days_in_month)
        else:
            time_multipliers = {'minutes': 60, 'hours': 3600,'day': 86400,'weeks': 86400 * 7}
            multiplier = time_multipliers.get(time_type)
            if multiplier is not None:
                time_cron *= multiplier
        return time_cron
    
    def write(self, values):
        res = super(mailing_mailing, self).write(values)
        mail_cron = self.env['ir.cron'].search([('code','=','model._process_mass_mailing_queue()')])
        if mail_cron:
            time_cron = self.time_cron(mail_cron.interval_number,mail_cron.interval_type)
            t = threading.Thread(target=self.delayed_check_contact_info, args=(time_cron,))
            t.start()
        return res
