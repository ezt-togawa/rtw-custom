# -*- coding: utf-8 -*-
from odoo import api, models, fields
_STATES = [
    ("draft", "Draft"),
    ("to_approve", "To be approved"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("done", "Done"),
]


class shinsei(models.Model):
    _name = 'shinsei.shinsei'
    _description = 'shinsei.shinsei'
    _inherit = ["mail.thread", "mail.activity.mixin", "tier.validation"]
    _state_from = ["draft"]
    _state_to = ["approved"]

    _tier_validation_manual_config = False

    @api.model
    def _get_default_requested_by(self):
        return self.env["res.users"].browse(self.env.uid)

    state = fields.Selection(
        selection=_STATES,
        string="Status",
        index=True,
        tracking=True,
        required=True,
        copy=False,
        default="draft",
    )

    requested_by = fields.Many2one(
        comodel_name="res.users",
        string="Requested by",
        required=True,
        copy=False,
        tracking=True,
        default=_get_default_requested_by,
        index=True,
    )
    manager = fields.Many2one(
        comodel_name="res.users",
        string="manager",
        store=True,
        compute="_get_manager"
    )

    owner = fields.Many2one('res.users', 'OwnerId', default=lambda self: self.env.user)  # 所有者Id B
    # is_deleted = fields.Integer('IsDeleted')  # 削除フラグ C ★0のみ
    name = fields.Char('Name')  # 件名 D
    record_type_id = fields.Char('RecordTypeId')  # レコードタイプ E
    created_date = fields.Datetime('CreatedDate')  # 作成日 F
    created_by_id = fields.Many2one('res.users', 'CreatedById')  # 作成ID G
    last_modified_date = fields.Datetime('LastModifiedDate')  # 最終更新日 H
    last_modified_by_id = fields.Many2one('res.users', 'LastModifiedById')  # 最終更新者 I
    system_mod_stamp = fields.Datetime('SystemModstamp')  # システム最終更新日 J
    # last_activity_date = fields.Datetime('LastActivityDate')  # システム最終活動日 K ★空白のみ
    department = fields.Selection([
        ("営業部 東京支店", "営業部 東京支店"),
        ("営業部 大阪支店", "営業部 大阪支店"),
        ("営業部 福岡支店", "営業部 福岡支店"),
        ("東京支店パートナー", "東京支店パートナー"),
        ("大阪支店パートナー", "大阪支店パートナー"),
        ("福岡支店パートナー", "福岡支店パートナー"),
        ("広報", "広報"),
        ("企画戦略室", "企画戦略室"),
        ("生産管理課", "生産管理課"),
        ("品質管理課", "品質管理課"),
        ("製造部", "製造部"),
        ("糸島工場", "糸島工場"),
        ("総経部", "総経部"),
        ("海外営業部", "海外営業部"),
    ], string="busho__c")  # 所属部署 L
    start_date = fields.Datetime('start_day__c')  # 開始日 M
    end_date = fields.Datetime('end_day__c')  # 終了日 N
    number_of_days = fields.Char('kikan__c')  # 日数 O
    vacation_classification = fields.Char('kubun__c')  # 休暇区分 P
    application_reason = fields.Text('riyuu__c')  # 申請理由 Q　
    # comment = fields.Char('comment__c')  # コメント R ★空白のみ
    job_description = fields.Text('kinmu__c')  # 勤務内容 S
    day_off_work = fields.Datetime('emp_day__c')  # 休日出勤日 T
    applicant = fields.Char('Field24__c')  # 申請者 U
    scheduled_end_time = fields.Integer('End_time__c')  # 予定終了時間 V
    scheduled_transfer_date = fields.Datetime('furikae_day__c')  # 振替予定日 W
    claim_order_no = fields.Char('Field25__c')  # フェア/クレーム注番 X
    application_date = fields.Datetime('shinsei_day__c')  # 申請日 Y
    # scheduled_end_time2 = fields.Datetime('End_time2__c')  # 終了予定時間 Z ★空白のみ
    target_persons = fields.Char('Field26__c')  # 対象者 AA
    application_item = fields.Char('Field1__c')  # 申請項目 AB
    purpose = fields.Text('Field2__c')  # 用途・目的 AC
    reason = fields.Text('Field27__c')  # 内容/理由 AD
    time_zone = fields.Char('atwaork__c')  # 時間帯 AE
    scheduled_start_time = fields.Integer('starttime__c')  # 予定開始時間 AF
    cost = fields.Integer('Field28__c')  # 経費（税別） AG
    order_no = fields.Char('Ordering_no__c')  # 発注NO AH
    change = fields.Boolean('saiteisyutsu__c')  # 変更 AI ★0,1,空白
    revision = fields.Boolean('syuusei__c')  # 修正 AJ ★0,1,空白
    withdrawal = fields.Boolean('torisage__c')  # 取下げ AK ★0,1,空白
    other = fields.Boolean('sonota__c')  # その他 AL ★0,1,空白
    # specification_upholstery = fields.Char('Field4__c')  # 仕様（張地） AM ★空白のみ
    # specification_size = fields.Char('Field5__c')  # 仕様（サイズ_W/D/H) AN ★空白のみ
    postage = fields.Integer('Field29__c')  # 送料 AO
    situation_report = fields.Html('Field30__c')  # 状況報告 AP
    processed_contents = fields.Html('Field31__c')  # 処理内容 AQ
    # order_no2 = fields.Char('Field6__c')  # 注番 AR ★空白のみ
    comment_by_charge = fields.Text('Field32__c')  # 担当者コメント AS
    # comment_by_boss = fields.Char('Field33__c')  # 上司コメント AT ★空白のみ
    fixtures_name = fields.Char('Field34__c')  # 備品名 AU
    # payee = fields.Char('Field7__c')  # 交通機関/領収書名 AV ★空白のみ
    classification = fields.Selection([
        ("破損", "破損"),
        ("滅失", "滅失"),
        ("破損・滅失", "破損・滅失"),
    ], string='Field35__c')  # 種別 AW
    date_time = fields.Datetime('Field36__c')  # 日時 AX
    # interval_departure = fields.Char('Field8__c')  # 区間（出発） AY ★空白のみ
    verification_method = fields.Html('Field37__c')  # 検証方法 AZ
    target = fields.Text('Field38__c')  # 目標 BA
    # interval_arrival = fields.Char('Field9__c')  # 区間（到着） BB ★空白のみ
    desired_delivery_date = fields.Datetime('Field18__c')  # 希望納期 BC
    sample_total_amount = fields.Integer('Field20__c')  # サンプル合計 BD
    time_zone2 = fields.Char('furikae_jikan__c')  # 時間帯 BE
    place_of_business = fields.Char('Field10__c')  # 出張先 BF
    subtotal = fields.Integer('Ashoukei__c')  # 小計（明細） BG
    business_trip_start_date = fields.Datetime('Field11__c')  # 出張開始日 BH
    business_trip_end_date = fields.Datetime('Field12__c')  # 出張終了日 BI
    lodging_day_amount = fields.Float('Field13__c')  # 宿泊日数 BJ
    lodging_expense = fields.Integer('Field14__c')  # 宿泊費 BK
    daily_allowance = fields.Integer('Field15__c')  # 日当 BL
    temporary_advance = fields.Integer('karibarai__c')  # 仮払金 BM
    total_amount_tax_excluded = fields.Integer('zeinuki_goukei__c')  # 合計金額（税抜） BN
    cardboard_amount = fields.Integer('Field21__c')  # 強化段ボール数 BO
    purpose = fields.Text('Field39__c')  # 目的 BP
    delivery_location = fields.Selection([
        ("銀座急送", "銀座急送"),
        ("東京SR", "東京SR"),
        ("朝日町運輸", "朝日町運輸"),
        ("大阪SR", "大阪SR"),
        ("カンリク", "カンリク"),
        ("福岡本社", "福岡本社"),
        ("糸島工場", "糸島工場"),
        ("井相田倉庫", "井相田倉庫"),
        ("白谷運輸", "白谷運輸"),
        ("その他デポ", "その他デポ"),
    ], string="納品場所")  # 納品場所 BQ
    project_outline = fields.Text('Field40__c')  # 企画概要 BR
    no_product = fields.Boolean('Field41__c')  # 商品無し BS ★0,1,空白
    approval_process = fields.Char('Field42__c')  # 承認プロセス BT
    report = fields.Char('Field43__c')  # 報告書 BU
    request = fields.Many2one('rtw_sf.inquiry', string='Field44__c')  # 問題提起/要請 BV ★1件のみ
    progress = fields.Selection([
        ("申請", "申請"),
        ("受理", "受理"),
        ("承認", "承認"),
        ("総務受理", "総務受理"),
        ("却下", "却下"),
    ], string='Field45__c')  # 進捗 BW
    business_partner_manager = fields.Many2one('res.partner', 'Field46__c')  # 取引先責任者 BX
    progress_report = fields.Char('Field52__c')  # 進捗（報告書） BY
    shinsei_type = fields.Selection([
        ("sample", "サンプル制作依頼"),
        ("kikaku", "企画・広報関連申請"),
        ("bihin", "備品破損・滅失報告書"),
        ("syucho", "出張申請"),
        # ("buppin", "物品購入申請"),
        # ("keihi", "経費精算"),
    ], string="申請種別")
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

    @api.model
    def _get_under_validation_exceptions(self):
        res = super(shinsei, self)._get_under_validation_exceptions()
        res.append("route_id")
        return res

    @api.depends('requested_by')
    def _get_manager(self):
        for rec in self:
            if rec.requested_by.employee_id.parent_id:
                rec.manager = rec.requested_by.employee_id.parent_id.user_id
            else:
                rec.manager = rec.requested_by
