# Copyright 2019-2020 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, models, fields
from datetime import datetime


class TierValidation_rtw(models.AbstractModel):
    _inherit = "tier.validation"
    _state_from = ["draft"]

    validated = fields.Boolean(
        compute="_compute_validated_rejected", search="_search_validated", store=True
    )

    def get_shinsei_type(self):
        if self.shinsei_type:
            if self.shinsei_type == 'sample':
                return 'サンプル制作依頼'
            elif self.shinsei_type == 'kikaku':
                return '企画・広報関連申請'
            elif self.shinsei_type == 'bihin':
                return '備品破損・滅失報告書'
            elif self.shinsei_type == 'syucho':
                return '出張申請'
        else:
            return ''

    def _notify_shinsei_done(self):
        recipients = ['t_ogawa@enzantrades.co.jp']
        body = '申請処理の完了通知' + '<br/><br/>' + '＜申請情報＞' + '<br/>' + '申請No: ' + str(self.id) + '<br/>' + '申請種別 :' + self.get_shinsei_type() + '<br/>' + '件名 :' + str(self.name) + '<br/>' + '申請日 :' + str(datetime.today().date()) + '<br/>' + '申請者 :' + (str(self.requested_by.name) if self.requested_by else '') + '<br/><br/>' + '※本メールはシステム自動配信です、返信は無効となります。'
        subscribe = "message_subscribe"
        post = "message_post"
        subject = "【RTW-Odoo】申請完了_" + self.name
        mail = self.env['mail.mail'].sudo().create({
            'email_from': self.env.user.email_formatted,
            'email_to': ','.join(recipients),
            'subject': subject,
            'body_html': body,
        })
        if mail:
            mail.send()

    def validate_tier(self):
        res = super(TierValidation_rtw, self).validate_tier()
        if all(review.status == 'approved' for review in self.review_ids):
            self.write({"shinsei_state": "done"})
            self.write({"validated": True})
            self._notify_shinsei_done()

            # self.write({"state": "done"})
            # print('>>>>>>>>>>>>>>>',not self._check_allow_write_under_validation())
        else:
            self.write({"shinsei_state": "approved"})

        return res

    def reject_tier(self):
        res = super(TierValidation_rtw, self).reject_tier()
        self.write({"shinsei_state": "rejected"})
        return res

    def request_validation(self):
        res = super(TierValidation_rtw, self).request_validation()
        self.write({"shinsei_state": "to_approve"})
        return res

    def restart_validation(self):
        res = super(TierValidation_rtw, self).restart_validation()
        self.write({"shinsei_state": "draft"})
        return res

    # def _notify_requested_review_body(self):
    #     res = super(TierValidation_rtw, self)._notify_requested_review_body()
    #     mail_content = '申請処理の完了通知'
    #     return _("A review has been requested by %s.") % (self.env.user.name)

    def _check_tier_state_transition(self, vals):
        if 'shinsei_state' or 'validated' in vals:  # TO ALLOW THIS FIELD PASS _check_tier_state_transition
            return False
        res = super(TierValidation_rtw,
                    self)._check_tier_state_transition(vals)
        return res
