# -*- coding: utf-8 -*-
import dateutil.parser
from datetime import datetime, date, time
from odoo import models, fields, api


class rtw_sf_case(models.Model):
    _name = 'rtw_sf_case'
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]
    _description = 'case'
    _rec_name = "subject"
    _order = "id DESC"

    case_no = fields.Char("CaseNumber")
    crm_id = fields.Many2one('crm.lead')
    partner_ids = fields.Many2one('res.partner')
    contacts = fields.Many2one('res.partner', "Contact", copy=False)  # コンタクト
    accounts = fields.Many2one('res.partner', "Account", copy=False)  # アカウント
    parents = fields.Many2one('rtw_sf_case', "Parents", copy=False)  # 親ケース
    supplied_name = fields.Char('SuppliedName')  # K列
    supplied_email = fields.Char('SuppliedEmail')  # L列
    supplied_phone = fields.Char('SuppliedPhone')  # M列
    supplied_company = fields.Char('SuppliedCompany')  # N列
    record_type_id = fields.Many2one('rtw_sf.record_type', 'RecordTypeId')  # レコードタイプId AH列
    type = fields.Selection([
        ('1', '問合せ/アフター'),
        ('2', '問題/要対応'),
        ('3', '過剰要求/苦情'),
        ('4', 'その他'),
        ('5', '商品問合せ'),
        ('6', 'ショールームについて'),
        ('7', '購入方法について'),
        ('-', '-'),
        ('8', 'アフターメンテナンス'),
    ], string='Type')  # O列 種別
    status = fields.Selection([('new', '新規'),
                               ('sales_representative_is_responding', '営業担当対応中'),
                               ('sales_representative_response_completed', '営業担当対応完了'),
                               ('under_discussion', '協議中'),
                               ('pending', '保留'),
                               ('under_investigation', '調査中'),
                               ('processing_cost', 'コスト処理中'),
                               ('close', 'クローズ'),
                               ('1', '3'),
                               ('2', '1'),
                               ('3', '4'),
                               ('4', '商品部調査中'),
                               ('5', '商品部対応完了'),
                               ('6', '工場打診中'),
                               ('7', '工場対応中'),
                               ('8', '営業部対応完了'),
                               ('9', '10'),
                               ('10', '18'),
                               ('11', '9'),
                               ('12', '2'),
                               ('13', '16'),
                               ], string="Status",
                              default='new')  # ステータス
    reason =fields.Selection([
        ('1', '(営業）業務・手配ミス'),
        ('2', '（営業）打合せ・接客トラブル'),
        ('3', '（営業）得意先手配ミス'),
        ('4', '（工場）業務・手配ミス'),
        ('5', '（工場）製品不良・製造上ミス'),
        ('6', '（配送）運送・設置トラブル'),
        ('7', '（素材）素材・製品の特性'),
        ('8', '（環境）使用上の問題'),
        ('9', '（開発）設計要因'),
        ('10', '原因不明'),
        ('11', 'その他の問題'),
        ('-', '-'),
        ('12', '過剰要求・不満'),
        ('13', '部材部品の欠品'),
    ], default='',
        string='Reason')  # 原因
    origin = fields.Selection([
        ('1', '納品現場'),
        ('2', '納品現場前の外'),
        ('3', 'デポ先'),
        ('4', '配送中・配送時'),
        ('5', '工場検品・出荷時'),
        ('-', '-'),
        ('6', '電子メール'),
        ('7', '電話'),
        ('8', 'Web'),

    ], default='',
        string='Origin')  # 発生場所 v
    is_visible_in_self_service = fields.Boolean('IsVisibleInSelfService')  # 表示確認
    subject = fields.Char('Subject')  # 現象
    priority = fields.Selection([
        ('h', '高'),
        ('m', '中'),
        ('l', '低'),
        ], default='',
        string='Priority')  # 優先順位 v
    description = fields.Text('Description')  # 説明
    isclosed = fields.Boolean('IsClosed')  # 完了済みフラグ
    closed_date = fields.Datetime('ClosedDate')  # 完了日
    is_escalated = fields.Boolean('IsEscalated')  # エスカレーションフラグ
    has_comments_unread_by_owner = fields.Boolean('HasCommentsUnreadByOwner')  # 所有者によるコメント未読の有無
    has_self_service_comments = fields.Boolean('HasSelfServiceComments')  # セルフサービスコメント
    owner_id = fields.Many2one('res.users', 'OwnerId', default=lambda self: self.env.user)  # 所有者Id
    is_closed_on_create = fields.Boolean('IsClosedOnCreate')  # 作成同時完了フラグ
    is_self_service_closed = fields.Boolean('IsSelfServiceClosed')  # 自己完了
    created_date = fields.Datetime('CreatedDate')  # 作成日
    created_by_id = fields.Many2one('res.users', 'CreatedById')  # 作成ID
    last_modified_date = fields.Datetime('LastModifiedDate')  # 最終更新日
    last_modified_by_id = fields.Many2one('res.users', 'LastModifiedById')  # 最終更新者
    system_mod_stamp = fields.Datetime('SystemModstamp')  # システム最終更新日 v
    order_no = fields.Char('Field1__c')  # 受注番号
    cope_order_no_1 = fields.Char('X1__c')  # 対処受注番号1
    cope_order_no_2 = fields.Char('X2__c')  # 対処受注番号2
    cope_order_no_3 = fields.Char('X3__c')  # 対処受注番号3
    probate_by_president = fields.Boolean('Field6__c')  # 社長検認
    discoverer = fields.Selection([
        ('1', '施主'),
        ('2', 'IC・設計・建築家'),
        ('3', '取扱店・代理店担当'),
        ('4', '搬入業者'),
        ('5', '運送業者'),
        ('6', 'リッツウェル社員'),
        ('7', '工場関係者'),
    ], default='',
        string='Field52__c')  # 発見者
    opportunity = fields.Many2one('crm.lead', 'opportunity')  # 商談
    delivery_date = fields.Datetime('Field5__c')  # 納品日
    occurrence_status = fields.Selection([
        ('1', '納品後・使用中'),
        ('2', '納品時'),
        ('3', '開梱時'),
        ('4', '未開梱時'),
        ('5', '出荷前'),
    ], default='',
        string='Field53__c')  # 発生状況
    accounting_department_probate = fields.Boolean('Field7__c')  # 経理部検認
    sales_department_probate = fields.Boolean('Field8__c')  # 営業部検認
    manufacturing_department_probate = fields.Boolean('Field9__c')  # 製造部検認
    initial_explanation_by_person = fields.Text('Field10__c')  # 初動説明（担当者）
    action_details_by_quality_control = fields.Text('Field11__c')  # 対処内容(品管)
    total_sales = fields.Integer('Field12__c')  # 売上総額
    coping_cost = fields.Integer('Field13__c')  # 対処コスト
    billed_freight_cost = fields.Integer('Field42__c')  # 請求運賃コスト
    carrier = fields.Char('Field54__c')  # 運送･搬入業者
    delivery_prefectures = fields.Char('Field4__c')  # 納品先都道府県
    delivery_municipality = fields.Char('Field55__c')  # 納品先市町村郡
    delivery_type = fields.Selection([
        ('1', '一般邸戸建'),
        ('2', '一般邸マンション'),
        ('3', 'モデル戸建'),
        ('4', 'モデルマンション'),
        ('5', 'コントラクト'),
    ], default='',
        string='Field56__c')  # 納品種別
    delivery_product_name = fields.Char('Field57__c')  # 納品物件名
    reporter = fields.Selection([
        ('1', '施主'),
        ('2', 'IC・設計・建築家'),
        ('3', '取扱店・代理店担当'),
        ('4', '搬入業者'),
        ('5', '運送業者'),
        ('6', 'リッツウェル社員'),
        ('7', '工場関係者'),
    ], default='',
        string='Field58__c')  # 通報者
    support = fields.Selection([
        ('1', '電話・メール対応'),
        ('2', '現場確認・説明'),
        ('3', '現場対応・メンテ補修'),
        ('4', '部品・部材送付（無償）'),
        ('5', '修理・部材交換（無償）'),
        ('6', '本体交換（無償）'),
        ('7', '修理・部材交換（有償）'),
        ('8', '本体交換（有償）'),
        ('9', '新規購入'),
        ('10', 'その他'),
        ('-', '-'),
        ('対応', '対応'),
    ], default='',
        string='Field59__c')  # 対応
    quality_control_comments = fields.Text('Field60__c')  # 品管コメント
    cause_company_name = fields.Char('Field24__c')  # 原因会社名
    size = fields.Char('Field65__c')  # サイズ
    progress_check = fields.Boolean('Field77__c')  # 進捗確認
    cause_by_quality_control = fields.Char('Field61__c')  # 原因（品管検証）
    double_cause_by_quality_control = fields.Selection([
        ('1', '（営業）業務・手配ミス'),
        ('2', '（営業）打合せ・接客トラブル'),
        ('3', '（営業）得意先手配ミス'),
        ('4', '（工場）業務・手配ミス'),
        ('5', '（工場）製品不良・製造上ミス'),
        ('6', '（配送）運送・設置トラブル'),
        ('7', '（素材）素材・製品の特性'),
        ('8', '（環境）使用上の問題'),
        ('9', '（開発）設計要因'),
        ('10', '原因不明'),
        ('11', 'その他の問題'),
        ('-', '-'),
        ('12', '過剰要求・不満'),
    ], default='',
        string='Field62__c')  # 重複原因（品管検証）
    cause_person_name = fields.Char('Field30__c')  # 原因担当者名
    billing_coping_cost = fields.Integer('Field31__c')  # 請求対処コスト
    sales_department_comments = fields.Text('Field44__c')  # 営業部コメント
    report_date = fields.Datetime('Field34__c', default=lambda self: fields.Datetime.now())  # 通報日
    Initial_response_date_by_person = fields.Datetime('Field35__c')  # 初動対応日(担当者)
    Initial_response_date_by_quality_control = fields.Datetime('Field36__c')  # 初動対応日(品管)
    double_cause = fields.Selection([
        ('1', '（営業）業務・手配ミス'),
        ('2', '（営業）打合せ・接客トラブル'),
        ('3', '（営業）得意先手配ミス'),
        ('4', '（工場）業務・手配ミス'),
        ('5', '（工場）製品不良・製造上ミス'),
        ('6', '（配送）運送・設置トラブル'),
        ('7', '（素材）素材・製品の特性'),
        ('8', '（環境）使用上の問題'),
        ('9', '（開発）設計要因'),
        ('10', '原因不明'),
        ('11', 'その他の問題'),
        ('-', '-'),
        ('12', '過剰要求・不満'),
        ('13', '（工場）業務手配ミス'),
    ], default='',
        string='Field37__c')  # 重複原因リスト
    follow_up_report_by_person = fields.Text('Field63__c')  # 続報（担当者）
    freight_cost = fields.Integer('Field41__c')  # 運賃コスト
    cooperative_factory_opinion = fields.Text('Field45__c')  # 協力工場見解
    manufacturing_department_status = fields.Selection([
        ('1', '調査中'),
        ('2', '対応中'),
        ('3', '対応完了'),
        ], default='',
        string='Field46__c')  # 製造部状況
    product_category = fields.Selection([
        ('1', 'ソファ'),
        ('2', 'チェア'),
        ('3', 'テーブル'),
        ('4', 'ボード・デスク'),
        ('5', '小物･ラグ'),
        ('6', '別注･特注'),
        ('7', 'OEM'),
        ('8', '仕入'),
        ('9', '付属品'),
        ('10', '廃盤ソファ'),
        ('11', '廃盤チェア'),
        ('12', '廃盤テーブル'),
        ('13', '廃盤ボード・デスク'),
        ('14', 'その他'),
    ], default='',
        string='Field47__c')  # 商品カテゴリ
    product_name = fields.Char('Field48__c')  # 商品名
    product_name2 = fields.Many2one('product.template', 'Field48__c')  # 商品名
    product_number = fields.Char('Field49__c')  # 品番
    specification = fields.Char('Field50__c')  # 仕様
    quantity = fields.Integer('Field51__c')  # 数量
    percentage_of_fault = fields.Float('percentage of fault')
    # , compute="_compute_percentage_of_fault")
    final_cost_total_sales = fields.Float('Final cost/total sales')
    display_id = fields.Integer(related="id")
    report_date_only = fields.Date(compute="_get_report_day", string="通報日")
    report_delivery_date = fields.Date(compute="_get_delivery_date", string="納品日")
    claim_no = fields.Char(string = 'クレーム注番',compute="_compute_claim_no")

    def _compute_claim_no(self):
        for rec in self:
            claim_no = ''
            menu_id = self.env['ir.ui.menu'].search([('name' ,'=','Sales'),('parent_id','=',False)]).id
            sale_order = self.env['sale.order'].search([('case_id' , '=' ,rec.id)])
            if sale_order:
                for sale in sale_order:
                    claim_no += f'<a href="/web#id={sale.id}&view_type=form&model=sale.order&menu_id={menu_id}">{sale.name}</a> '
            rec.claim_no =claim_no

    def _get_delivery_date(self):
        for rec in self:
            if rec.delivery_date:
                rec.report_delivery_date = rec.delivery_date.date()
            else:
                rec.report_delivery_date = False

    def _get_report_day(self):
        for rec in self:
            if rec.report_date:
                rec.report_date_only = rec.report_date.date()
            else:
                rec.report_date_only = False

                # , compute="_compute_final_cost_total_sales")

    # def _compute_percentage_of_fault(self):
    #     for rec in self:
    #         if rec.coping_cost == 0 and rec.freight_cost == 0:
    #             pof = 0
    #         else:
    #             pof = (1 - (rec.billing_coping_cost + rec.billed_freight_cost) / (rec.coping_cost + rec.freight_cost)) * 100
    #         # print(pof)
    #         rec.percentage_of_fault = pof
    #
    # def _compute_final_cost_total_sales(self):
    #     for rec in self:
    #         fcts = (
    #                 (rec.coping_cost + rec.freight_cost)
    #                 -
    #                 (rec.billing_coping_cost + rec.billed_freight_cost)
    #         ) / rec.total_sales * 100
    #         print(fcts)
    #         rec.final_cost_total_sales = fcts
    @api.onchange('contacts')
    def _parents_set(self):
        if self.contacts:
            self.accounts = self.contacts.parent_id

    def create_sale_order(self):
        return {
            'name': 'Create Sale Order',
            'view_mode': 'form',
            'view_id': self.env.ref('sale.view_order_form').id,
            'res_model': 'sale.order',
            'res_id': self.env['sale.order'].id,
            'type': 'ir.actions.act_window',
        }
