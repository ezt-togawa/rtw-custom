# -*- coding: utf-8 -*-

from odoo import models, fields, api


class contract(models.Model):
    _name = 'rtw_sf.inquiry'
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]
    _description = 'inquiry'
    _rec_name = "name"

    owner_id = fields.Many2one('res.users', 'OwnerId')  # 所有者Id
    name = fields.Char('Name')
    record_type_id = fields.Many2one('rtw_sf.record_type', 'RecordTypeId',
                                     domain="['|', '|','|',('name', '=', '問合せ'),"
                                            " ('name', '=', 'アンケート2018'), "
                                            "('name', '=', '出張報告書'), "
                                            "('name', '=', 'アンケート2019')]")
    record_type_id_name = fields.Char(related="record_type_id.name", string="record_type_id_name")
    created_date = fields.Datetime('CreatedDate')  # 作成日 AM列
    created_by_id = fields.Many2one('res.users', 'CreatedById')  # 作成ID AN列
    last_modified_date = fields.Datetime('LastModifiedDate')  # 最終更新日 AO列
    last_modified_by_id = fields.Many2one('res.users', 'LastModifiedById')  # 最終更新者 AP列
    system_mod_stamp = fields.Datetime('SystemModstamp')  # システム最終更新日 AQ列
    last_activity_date = fields.Datetime('LastActivityDate')  # システム最終活動日 AR列　★空白のみ
    toi_no = fields.Char('toi_no')  # 問い合わせNo
    vendor = fields.Char('vendor')  # 納品業者
    campaign_id = fields.Many2one('utm.campaign', 'campaign')  # キャンペーン
    lead_source = fields.Selection([
        ('1', '紹介（家具店・住宅関係者）'),
        ('2', '紹介（家族・知人）'),
        ('3', '雑誌'),
        ('4', 'インターネット'),
        ('5', 'SNS・ソーシャルメディア'),
        ('6', 'TABROOM'),
        ('7', '展示場・ショップ'),
        ('8', 'Rオーナー'),
        ('9', 'R営業'),
        ('10', 'ふるさと納税'),
        ('11', 'G住宅ﾎﾟｲﾝﾄ'),
        ('12', 'その他'),
    ], default='',
        string="lead_source")  # リードソース
    broad_category = fields.Selection([
        ('event_sale', 'イベント・セール'),
        ('catalog', 'カタログ依頼（メール・ＦＡＸ）'),
        ('claim', 'クレーム'),
        ('show_room', 'ショールーム'),
        ('other', 'その他'),
        ('campaign', '広報・キャンペーン関連'),
        ('buy_method', '購入方法'),
        ('merchandise', '商品関連'),
        ('delivery_problems', '納品トラブル'),
        ('delivery_related', '納品関連')
    ], string="broad_category",
     default='')  # 大分類 OK
    support = fields.Selection([
        ('1', 'ＳＲ予約'),
        ('2', 'カタログ送付'),
        ('3', 'サンプル送付'),
        ('4', 'その他'),
        ('5', 'ソファ'),
        ('6', 'ダイニングテーブル'),
        ('7', 'チェア'),
        ('8', 'ボード'),
        ('9', 'メール回答完了'),
        ('10', 'メンテナンスキット紹介'),
        ('11', 'メンテナンスキット販売'),
        ('12', 'リビングテーブル'),
        ('13', '営業引継ぎ'),
        ('14', '営業日・営業時間'),
        ('15', '見積り依頼'),
        ('16', '商品資料送付'),
        ('17', '注文（受注）'),
        ('18', '注文書送付'),
        ('19', '電話回答完了'),
        ('20', '納品日決定'),
        ('21', '納品日変更'),
        ('22', '訪問'),
    ], string="support",
     default='')   # 対応
    product_name1 = fields.Char("product_name1")  # ①商品名
    product_name2 = fields.Char("product_name2")  # ②商品名
    product_name3 = fields.Char("product_name3")  # ③商品名
    product_name4 = fields.Char("product_name4")  # ④商品名
    product_name5 = fields.Char("product_name5")  # ⑤商品名
    product_name6 = fields.Char("product_name6")  # ⑥商品名
    contact_person = fields.Many2one("res.partner", 'contact_person')  # 取引先担当者
    accounts = fields.Many2one("res.partner", 'accounts')  # 取引先
    summary = fields.Text("summary")  # 概要
    customer_testimonials = fields.Text("customer_testimonials")  # お客様の声
    satisfaction_level = fields.Selection([
        ('5', '大変満足'),
        ('4', 'やや満足'),
        ('3', '普通'),
        ('2', 'やや不満'),
        ('1', '大変不満'),
    ], string="satisfaction_level",
     default='')  # 商品の満足度
    name_of_magazine_other = fields.Char("name_of_magazine_other")  # 雑誌名（その他）
    situation = fields.Selection([
        ('buy', '購入後'),
        ('not_buy', '購入前'),
    ], string="situation",
     default='')  # 状況
    magazine_site = fields.Selection([
        ('1', 'モダンリビング'),
        ('2', 'エルデコ'),
        ('3', "I'm home"),
        ('4', '商店建築'),
        ('5', 'シグネチャー'),
        ('6', 'ゲーテ'),
        ('7', 'Pen'),
        ('8', 'Passione'),
        ('9', 'ONLINEサイト'),
        ('10', 'その他'),
        ('11', '不明'),
    ], string="magazine_site",
     default='')  # 雑誌／サイト名
    proposal_to_send_catalog = fields.Boolean('proposal_to_send_catalog', default=0)  # カタログ送付提案
    sr_attracting = fields.Boolean('sr_attracting', default=0)  # ＳＲ誘致
    confirm_user_information = fields.Boolean('confirm_user_information', default=0)  # ユーザー情報確認
    event_information_notices = fields.Boolean('event_information_notices', default=0)  # イベント情報告知
    handover_matters = fields.Text('handover_matters')  # 引継ぎ事項
    deign = fields.Boolean('deign')  # デザイン
    use = fields.Boolean('use')  # 使い心地
    sense_of_materials = fields.Boolean('sense_of_materials')  # 素材感
    sales_staff_evaluation = fields.Selection([
        ('5', '大変満足'),
        ('4', 'やや満足'),
        ('3', '普通'),
        ('2', 'やや不満'),
        ('1', '大変不満'),
    ], string="sales_staff_evaluation",
     default='')  # 営業スタッフの評価
    originator = fields.Selection([
        ('1', 'IC・設計・クライアント'),
        ('2', 'オーナー・エンドユーザー'),
        ('3', 'その他'),
        ('4', 'メーカー・サプライヤー'),
    ], string="originator",
     default='')  # 発信者
    price = fields.Boolean('price')  # 価格
    image_atmosphere = fields.Boolean('image_atmosphere')  # イメージ雰囲気
    sales_staff_response = fields.Boolean('sales_staff_response')  # 営業スタッフの対応
    recommendation_from_a_friend = fields.Boolean('recommendation_from_a_friend')  # 友人の勧め
    inet_reputation_and_wom = fields.Boolean('inet_reputation_and_wom')  # ネット評判・口コミ
    glad_bought_it_before = fields.Boolean('glad_bought_it_before')  # 以前購入してよかった
    non_response = fields.Boolean('non_response')  # 無回答
    evaluation_of_delivery_staff = fields.Selection([
        ('5', '大変満足'),
        ('4', 'やや満足'),
        ('3', '普通'),
        ('2', 'やや不満'),
        ('1', '大変不満'),
    ], string="evaluation_of_delivery_staff",
     default='')  # 納品スタッフの評価
    yes = fields.Boolean('yes')  # YES
    no = fields.Boolean('no')  # NO
    need_dm = fields.Boolean('need_dm')  # DM希望
    not_need_dm = fields.Boolean('not_need_dm')  # DM不要
    mid_category = fields.Selection([
        ('1', '-'),
        ('2', 'ＳＲ展示品について'),
        ('3', "SR予約"),
        ('4', 'セール'),
        ('5', 'プレゼント・キャンペーン'),
        ('6', 'メンテナンス'),
        ('7', '営業日時・時間'),
        ('8', '購入ルート'),
        ('9', '支払い・決済方法'),
        ('10', '資料請求'),
        ('11', '取引条件の確認'),
        ('12', '商品クレーム'),
        ('13', '商品不具合・破損'),
        ('14', '新規注文検討'),
        ('15', '注文済商品'),
        ('16', '納品済商品（メンテ）'),
    ], string="mid_category",
     default='')  # 中分類
    detail = fields.Selection([
        ('1', '-'),
        ('2', 'スペアカバー・部材購入'),
        ('3', "セール実施予定の確認"),
        ('4', 'セール商品内容'),
        ('5', 'デザイン（特徴・コンセプト・デザイナーほか）'),
        ('6', '画像・資料提供'),
        ('7', '供給（在庫・納期ほか）'),
        ('8', '仕様（価格・サイズ・重量・別注対応ほか）'),
        ('9', '修理・張り替え'),
        ('10', '商品名・品番確認'),
        ('11', '日常的なお手入れ'),
        ('12', '納品日の確認'),
        ('13', '納品方法の確認'),
        ('14', '補修的なメンテ'),
    ], string="detail",
     default='')  # 内容
    survey_no = fields.Char('survey_no')  # アンケートNO
    other = fields.Boolean('other')  # その他(4)
    date_time = fields.Datetime('date_time')  # 日時
    means = fields.Selection([
        ('1', 'WEBフォーム'),
        ('2', 'メール'),
        ('3', "来場"),
        ('4', '電話'),
        ('5', 'その他'),
    ], string="means",
     default='')  # 手段
    number = fields.Char('no')  # NO
    confirmation = fields.Boolean('confirmation')  # 確認
    not_meet = fields.Boolean('not_meet')  # 会っていない
    not_meet_2 = fields.Boolean('not_meet_2')  # 会っていない
    crm_1 = fields.Many2one('crm.lead', 'crm_1')  # 関連商談①
    crm_2 = fields.Many2one('crm.lead', '関連商談②')  # 関連商談②
    order_no = fields.Char("order_no")
    product_category_1 = fields.Char("product_category_1")
    product_category_2 = fields.Char("product_category_2")
    product_category_3 = fields.Char("product_category_3")
    product_category_4 = fields.Char("product_category_4")
    product_category_5 = fields.Char("product_category_5")
    product_category_6 = fields.Char("product_category_6")
    score = fields.Integer("score")
    status_report = fields.Html("status_report")
    request = fields.Html("request")
    comment = fields.Text("comment")
    classification = fields.Selection([
        ('1', '社内業務改善'),
        ('2', 'ツール・資料制作依頼'),
    ], string="classification",
     default='')
    progress = fields.Selection([
        ('1', '申請'),
        ('2', '完了'),
    ], string="progress",
     default='')
    contact = fields.Many2one('res.users', 'contact')
    admitted = fields.Selection([
        ('1', '未'),
        ('2', '済'),
    ], string="admitted",
     default='1')
    report_progress = fields.Selection([
        ('1', '提出'),
        ('2', '受理'),
        ('3', '承認'),
        ('4', '総務受理'),
        ('5', '差し戻し'),
    ], string="report_progress",
     default='1')
    proposal_ability = fields.Selection([
        ('5', '感動'),
        ('4', '満足'),
        ('3', '普通'),
        ('2', '不満'),
        ('1', '大変不満'),
    ], string="proposal_ability",
     default='')  #
    speed = fields.Selection([
        ('5', '感動'),
        ('4', '満足'),
        ('3', '普通'),
        ('2', '不満'),
        ('1', '大変不満'),
    ], string="speed",
     default='')  #
    greeting1 = fields.Selection([
        ('5', '感動'),
        ('4', '満足'),
        ('3', '普通'),
        ('2', '不満'),
        ('1', '大変不満'),
    ], string="greeting1",
     default='')  #
    appearance = fields.Selection([
        ('5', '感動'),
        ('4', '満足'),
        ('3', '普通'),
        ('2', '不満'),
        ('1', '大変不満'),
    ], string="appearance",
     default='')  #
    delivery_work = fields.Selection([
        ('5', '感動'),
        ('4', '満足'),
        ('3', '普通'),
        ('2', '不満'),
        ('1', '大変不満'),
    ], string="delivery_work",
     default='')  #
    description = fields.Selection([
        ('5', '感動'),
        ('4', '満足'),
        ('3', '普通'),
        ('2', '不満'),
        ('1', '大変不満'),
    ], string="description",
     default='')  #
    greeting_2 = fields.Selection([
        ('5', '感動'),
        ('4', '満足'),
        ('3', '普通'),
        ('2', '不満'),
        ('1', '大変不満'),
    ], string="greeting_2",
     default='')  #
    appearance_2 = fields.Selection([
        ('5', '感動'),
        ('4', '満足'),
        ('3', '普通'),
        ('2', '不満'),
        ('1', '大変不満'),
    ], string="appearance_2",
     default='')  #
    progress = fields.Selection([
        ('1', '提出'),
        ('2', '受理'),
        ('3', '承認'),
        ('4', '総務受理'),
        ('5', '差し戻し'),
    ], default='',
        string='Field62__c')  # 報告書進捗
    approval = fields.Selection([
        ('1', '未'),
        ('2', '済'),
    ], default='',
        string='Field61__c')  # 上長承認
    inq_type = fields.Selection([
        ('1', '社内業務改善'),
        ('2', '営業活動'),
        ('3', 'ツール・資料制作依頼'),
        ('4', 'WEB・広報関連'),
        ('5', 'その他'),
    ], default='',
        string='Field58__c')  # 種別
    yousei = fields.Selection([
        ('1', '申請'),
        ('2', '受理'),
        ('3', '進行中'),
        ('4', '完了'),
    ], default='',
        string='Field59_yousei__c')  # 進捗

    owners_desk = fields.Boolean("オーナーズデスク")

    def open_one2many_line(self, context=None):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Open Line',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': self.id,
            'target': 'current',
        }