# -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api


class rtw_sf_partner(models.Model):
    _inherit = "res.partner"
    _description = 'Account.csv'
    # A ID
    is_deleted = fields.Boolean("IsDeleted", default=0)  # B 削除フラグ

    fax = fields.Char(string="fax", tracking=True)  # X OK
    contact_type = fields.Many2one('res.partner.contact_type', string="type", tracking=True)  # E OK
    channel = fields.Many2one('res.partner.channel', 'channel', tracking=True)  # BG OK
    account_number = fields.Char("AccountNumber", tracking=True)  # Y OK
    annual_revenue = fields.Char("AnnualRevenue", tracking=True)  # AC 年間売上 OK
    number_of_employees = fields.Integer("NumberOfEmployees", tracking=True)  # AD 従業員数 OK
    ownership = fields.Selection([
        ('1', '公開'),
        ('2', '非公開'),
        ('3', '関連子会社'),
        ('4', 'その他'),
    ], default='',
        string="ownership", )  # OK
    ticker_symbol = fields.Char("TickerSymbol", tracking=True)  # AF 銘柄コード OK
    description = fields.Text("Description")  # OK
    rating = fields.Selection([
        ('1', '重要顧客'),
        ('2', '平均的'),
        ('3', '見込み有り'),
        ('4', '見込み無し'),
        ('5', '将来見込み有り'),
        ('-', '以下未使用'),
        ('6', '見込み無'),
    ], default='',
        string="Rating")  # ok
    site = fields.Char("Site", tracking=True)  # OK
    supplier_no = fields.Char("supplier_no", tracking=True)  # OK 仕入先番号 Field5__c
    kana = fields.Char("kana", tracking=True)  # OK フリガナ Field5__c
    corporate_mail = fields.Boolean("corporate_mail", default=0, tracking=True)  # 法人宛郵便 OK  Field6__c
    transactions = fields.Many2one('res.partner.transactions', string="transactions", tracking=True)  # 取引方法 OK Field4__c
    payment_terms_1 = fields.Char("payment_terms_1", tracking=True)  # 支払い条件１ OK X1__c
    payment_terms_2 = fields.Char("payment_terms_2", tracking=True)  # 支払い条件2 OK X2__c
    multiplier_black = fields.Float("multiplier_black", tracking=True)  # 掛率(黒) OK Field7__c
    multiplier_green = fields.Float("multiplier_green", tracking=True)  # 掛率(黒) OK Field8__c
    fare_payment_terms = fields.Selection([
        ('1', '運賃込み(設置まで)'),
        ('2', '運賃別途'),
        ('3', '運賃込み(デポ入れまで)'),
        ('4', '運賃込み（設置まで）'),
    ], default='',
        string="fare_payment_terms", tracking=True)  # 支払条件運賃 OK Field9__c
    categorization = fields.Selection([
        ('1', '大手HM'),
        ('2', 'その他HM'),
        ('3', 'リフォーム'),
        ('4', '大手マンション'),
        ('5', 'その他マンション'),
        ('6', 'リノベーション'),
        ('7', 'IC事務所'),
        ('8', 'ID事務所'),
        ('9', '建築設計（アトリエ系）'),
        ('10', 'オフィス設計'),
        ('11', '内装施工'),
        ('12', '組織設計'),
        ('13', 'ゼネコン'),
        ('14', '小売/百貨店'),
        ('15', '商社/インテリア資材'),
        ('16', '問屋'),
        ('17', 'オフィス家具'),
        ('18', '家具メーカー'),
        ('19', 'リース業'),
        ('20', 'OEM'),
        ('21', '一般'),
        ('22', '法人'),
        ('23', '仕入会社'),
        ('24', '住設関係'),
        ('25', '関係者販売等'),
        ('26', 'HM/ビルダー先'),
        ('27', '競合他社'),
        ('28', 'メディア'),
        ('29', 'リクルート'),
        ('30', 'フォトグラファー'),
        ('31', 'プロダクトデザイナー'),
        ('32', '企業ブランディングデザイナー'),
        ('33', 'グラフィックデザイナー'),
        ('34', '独占販売権ディーラー'),
        ('35', '非独占販売権ディーラー'),
        ('36', '販売代行エージェント'),
        ('37', 'その他'),
        ('38', 'Ritzwell'),
        ('-', '以下無効'),
        ('39', '関係者販売'),
    ], default='',
        string="categorization")  # 分類 OK Field10__c
    situation = fields.Selection([
        ('1', '新規'),
        ('2', '既存'),
        ('3', '休眠'),
        ('4', '未取引'),
        ('5', '営業対象外'),
    ], default='1',
        string="situation", tracking=True)  # 状況 OK Field11__c
    address_confirmation_required = fields.Selection([('moving', '（不達）転居'), ('unknown', '（不達）不明')],
                                                     string="address_confirmation_required", tracking=True)  # 住所要確認 OK Field12__c
    last_contract_date = fields.Datetime("last_contract_date")  # 最新成約日 OK Field13__c
    total_number_of_transactions = fields.Integer("total_number_of_transactions")  # 累計取引回数 OK Field14__c
    cumulative_sales = fields.Float("cumulative_sales")  # 累計売上金額 OK Field15__c
    potential = fields.Selection([('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], string="potential",
                                 default='')  # ポテンシャル OK Field16__c
    kubun = fields.Selection([('internal', '国内'), ('external', '海外')], string="kubun")  # 区分 OK  Field20__c
    rival_companies = fields.Boolean("rival_companies", default=0, tracking=True)  # 競合他社 OK Field23__c
    group = fields.Char("group")  # G OK Field21__c
    transaction_category = fields.Selection([
        ('sundries', '諸口'),
        ('continuation', '継続'),
    ], default='sundries',
        string="transaction_category", tracking=True)  # 取引区分 OK Field27__c
    campaign_1 = fields.Char("campaign_1", tracking=True)  # キャンペーン① OK Field25__c
    campaign_2 = fields.Char("campaign_2", tracking=True)  # キャンペーン② OK Field26__c
    dummy = fields.Boolean("dummy", default=0, tracking=True)  # ダミー OK Field29__c
    # relation

    case = fields.One2many('rtw_sf_case', inverse_name='contacts')  # ケース OK
    # contact
    account_id = fields.Many2one('res.partner', "AccountId", tracking=True)  # OK
    first_name = fields.Char("FirstName")  # OK
    last_name = fields.Char("LastName")  # OK
    record_type = fields.Char("RecordTypeId")  # OK
    other_country = fields.Char("OtherCountry", tracking=True)  # OK
    other_postal_code = fields.Char("OtherPostalCode", tracking=True)  # OK
    other_state = fields.Char("OtherState", tracking=True)  # OK
    other_city = fields.Char("OtherCity", tracking=True)  # OK
    other_street = fields.Char("OtherStreet", tracking=True)  # OK
    mailing_country = fields.Char("MailingCountry", tracking=True)  # OK
    mailing_postal_code = fields.Char("MailingPostalCode", tracking=True)  # OK
    mailing_state = fields.Char("MailingState", tracking=True)  # OK
    mailing_city = fields.Char("MailingCity", tracking=True)  # OK
    mailing_street = fields.Char("MailingStreet", tracking=True)  # OK
    home_phone = fields.Char("HomePhone", tracking=True)  # OK
    other_phone = fields.Char("OtherPhone", tracking=True)  # OK
    reports_to_id = fields.Char("ReportsToId")  # OK
    department = fields.Char("Department", tracking=True)  # OK
    lead_source = send_catalog = fields.Selection([
        ('1', '通常営業'),
        ('2', 'リサーチ・新規開拓'),
        ('3', '紹介・提案(ＩＣ・設計)'),
        ('4', '紹介・提案(販売店FFE)'),
        ('5', '紹介・提案(小売店・百貨店)'),
        ('6', '納入先展示(展示場・MR)'),
        ('7', '納入先展示(店舗・施設等)'),
        ('8', '異動(取責)'),
        ('9', 'Web検索サイト'),
        ('10', 'SNS'),
        ('11', 'TABROOM'),
        ('12', '広報(広告）'),
        ('13', '広報（PR）'),
        ('14', 'DM・ニュースレター'),
        ('15', 'カタログギフト'),
        ('16', 'ふるさと納税'),
        ('17', 'G住宅ﾎﾟｲﾝﾄ'),
        ('18', 'ROC'),
        ('19', 'カレンダー購入'),
        ('20', 'Rオーナー(追加・リピート)'),
        ('21', 'Rオーナー（アフター）'),
        ('22', 'イベント参加'),
        ('23', '通りがかり'),
        ('24', 'フェア・展示会'),
        ('25', '外部イベント'),
        ('26', '紹介（知人・外部）'),
        ('27', '紹介(施主指定)'),
        ('28', '紹介（従業員）'),
        ('29', '海外展示会'),
        ('30', 'ミラノサローネ'),
        ('31', 'Architonic'),
        ('32', 'Archiproducts'),
        ('33', 'その他'),
        ('34', '不明'),
        ('-', '以下未使用'),
        ('35', '口コミ'),
        ('36', 'Fax'),
        ('37', '電話'),
        ('38', 'RitzwellWebフォーム'),
        ('39', 'インテリアフェア'),
        ('40', '仕入調達'),
        ('41', 'Email'),
        ('42', '物件情報'),
        ('43', 'IFFT2007(sozo_comm)'),
        ('44', '店舗'),
        ('45', 'コラボイベント'),
        ('46', '家具店・IC等からの紹介'),
        ('47', '(R)WEBページ'),
        ('48', '納品時の案内用紙'),
        ('49', '雑誌'),
        ('50', 'IFFT2007(sozo_comm)'),
        ('51', '店舗'),
        ('52', 'コラボイベント'),
        ('53', '家具店・IC等からの紹介'),
        ('54', '(R)WEBページ'),
        ('55', '納品時の案内用紙'),
        ('56', '雑誌'),
    ], default='',
        string="LeadSource", tracking=True)  # OK
    birthdate = fields.Datetime(string="Birthdate", tracking=True)  # OK
    opt_out_email = fields.Boolean(string="HasOptedOutOfEmail", default=0, tracking=True)  # OK
    opt_out_fax = fields.Boolean(string="HasOptedOutOfFax", default=0)  # ok
    do_not_call = fields.Boolean(string="DoNotCall", default=0)  # OK
    last_cu_request_date = fields.Datetime("LastCURequestDate")  # OK
    last_cu_update_date = fields.Datetime("LastCUUpdateDate")  # OK
    email_bounced_reason = fields.Text("EmailBouncedReason")  # OK
    email_bounced_date = fields.Datetime("EmailBouncedDate")  # OK
    ny_card = fields.Boolean("ny_card", default=0, tracking=True)  # 年賀状 OK Field1__c
    need_dm = fields.Boolean("need_dm", default=0, tracking=True)  # DM希望 OK DM__c
    gift = fields.Boolean("gift", default=0,
                          help="Customers, business partners, and suppliers who need to send gifts, gifts, mid-year gifts, New Year's gifts, and year-end gifts"
                          )  # 進物 OK Field2__c2
    summer_greeting = fields.Boolean("summer_greeting", default=0, tracking=True)  # 暑中見舞 OK Field3__c
    send_catalog = fields.Selection([
        ('send', '送付'),
        ('holdings ', '手持'),
    ], default='',
        string="send_catalog")  # カタログ配布 OK Field4__c
    gender = fields.Selection([
        ('1', '女性'),
        ('2', '男性'),
        ('3', 'その他'),
        ('4', '不明'),
        ('-', '以下不使用'),
        ('6', '男'),
        ('7', '女'),

    ], default='',
        string="gender", tracking=True)  # 性別 OK Field6__c
    in_has = fields.Char("in_has", tracking=True)  # R社内所有者 OK R__c
    do_not_dm = fields.Boolean("do_not_dm", default=0, tracking=True)  # DM不要 OK DoNotDM
    evaluation = fields.Selection([
        ('A', 'A優良顧客'),
        ('B', 'B平均的'),
        ('C', 'C見込み有'),
        ('D', 'D見込み無'),
    ], default='',
        string="evaluation", help="2015年～2017年　売上金額ベースの評価", tracking=True)  # 評価 OK Field8__c
    dm_unknown = fields.Boolean("dm_unknown", help=">DM欄　未記入", default=0, tracking=True)  # DM不明 OK DM_unknown__c
    action_1 = fields.Char("action1")  # アクション1⃣ OK
    action_2 = fields.Char("action2")  # アクション② OK
    related_attributes = fields.Selection([
        ('1', '施主(住宅系先）'),
        ('2', '施主（ﾏﾝｼｮﾝ系先）'),
        ('3', '施主（ｺﾝﾄﾗｸﾄ系先）'),
        ('4', '施主（販売店先）'),
        ('5', '取引先社員'),
        ('6', '取引先家族'),
        ('7', 'R関係者'),
        ('8', 'Ｒ社員'),
        ('9', 'Ｒ家族'),
        ('10', 'R友人'),
        ('11', 'その他'),
        ('-', '以下不使用'),
        ('12', '施主（その他住宅）'),
    ], default='',
        string="related_attributes", tracking=True)  # 関係者属性 OK HM_OB__c
    cs_number = fields.Char("cs_number", tracking=True)  # 取引先番号 OK Field12__c
    mc_subscriber = fields.Many2one('res.partner', "Contact", copy=False)  # コンタクト OK
    haihai_id = fields.Char("ID__c", tracking=True)  # OK
    mail_change = fields.Boolean("mail_change", default=0, tracking=True)  # メール変更 OK Field14_mail__c
    haihai_open_count = fields.Integer("haihai_open_count", tracking=True)  # 配配開封数 OKField14__c
    calender = fields.Boolean("calender", default=0, tracking=True)  # ｶﾚﾝﾀﾞｰ OKcalendar__c
    key_man = fields.Boolean("key_man", default=0)  # キーマン OKField17__c
    r_owner = fields.Boolean("r_owner", default=0, help="Ritzwell家具の購入実績がある", tracking=True)  # Rオーナー OKR_1__c
    sansancard = fields.Boolean("sansancard",
                                default=0)  # Created by Scan to Salesforce OKsansancard__CreatedByScanToSalesforce__c
    retirement = fields.Char("retirement")  # 退職 OKField18__c
    change = fields.Boolean("change", default=0)  # 異動 OKField19__c
    maternity_leave_and_vacation = fields.Boolean("maternity_leave_and_vacation", default=0)  # 育休・休暇 OK Field20__c2
    unknown = fields.Boolean("unknown", default=0)  # 不明 OKField21__c2
    lead_source_roc = fields.Selection([
        ('1', '(R)WEBページ'),
        ('2', '(R)SR'),
        ('3', '納品時の案内用紙'),
        ('4', '雑誌'),
        ('5', 'SNS'),
        ('6', 'DM'),
        ('7', '友人・知人の紹介'),
        ('8', 'イベント会場'),
        ('9', '家具店・IC等からの紹介'),
        ('10', 'その他'),
    ], default='',
        string="lead_source_roc", tracking=True)  # リードソース(ROC) OKROC__c
    interest_roc = fields.Char("interest_roc", tracking=True)  # 興味・関心(ROC) OK ROC_2__c
    Influencers = fields.Selection([
        ('h', '高'),
        ('m', '中'),
        ('l', '低'),
    ], default='',
        string="Influencers", )  # インフルエンサー度 OK Field22__c
    occupational_category = fields.Selection([
        ('1', '会社員（専門職以外）'),
        ('2', '会社幹部'),
        ('3', '会社役員'),
        ('4', '経営者'),
        ('5', '医師・歯科医師他'),
        ('6', '弁護士・検察官他'),
        ('7', '教員'),
        ('8', '大学教授'),
        ('9', '会計士'),
        ('10', '公務員'),
        ('11', '国家公務員・議会議員'),
        ('12', '研究者'),
        ('13', '技術者（建築・製造他）'),
        ('14', 'コンサルタント'),
        ('15', 'タレント・モデル・俳優'),
        ('16', '記者・ジャーナリスト'),
        ('17', '著述家（脚本家、評論家他）'),
        ('18', 'WEB・グラフィックデザイナー'),
        ('19', 'プロダクト・ファッションデザイナー'),
        ('20', '音楽家・舞踊家・演芸家他'),
        ('21', '美術家・彫刻家・書道家他'),
        ('22', '師範（武道・芸道他）'),
        ('23', '写真・映像'),
        ('24', '警察官・消防士他'),
        ('25', '植木職、造園師'),
        ('26', 'その他'),
    ], default='',
        string="occupational_category", tracking=True)  # 職種 OK Field23__c
    not_use = fields.Boolean("not_use", default=0, tracking=True)  # 使用不可 OK DM_4__c
    mail2 = fields.Char("mail2", tracking=True)  # メール2 OK Field24__c
    mail_1_2 = fields.Boolean("mail_1_2", default=0, tracking=True)  # メール1・2 OK X1_2__c
    haihai_count = fields.Integer("haihai_count")  # 配配送信数 OK Field25__c2
    region = fields.Selection([
        ('1', '東北・北海道'),
        ('2', '北関東'),
        ('3', '首都圏'),
        ('4', '甲信越'),
        ('5', '東海'),
        ('6', '北陸'),
        ('7', '関西'),
        ('8', '中国'),
        ('9', '四国'),
        ('10', '九州・沖縄'),
    ], default='', tracking=True)
    # region = fields.Char(compute="_get_region", string="region", store=True, ondelete='CASCADE')  # 地域 OK Field34__c
    stop_letter = fields.Boolean("stop_letter", default=0, tracking=True)  # LETTER停止 OK LETTER__c
    # kin = fields.Char("Field36__c")  # 親類（親戚・家族） OK
    kin = fields.Many2one('res.partner', "kin", copy=False, tracking=True)  # Field36__c
    mail3 = fields.Char("mail3")  # メール3 OK X3__c
    company_name = fields.Char("company_name")  # 会社名 OK Field37__c
    x20 = fields.Boolean("X20__c", default=0)  # OK
    x30 = fields.Boolean("X30__c", default=0)  # OK
    x40 = fields.Boolean("X40__c", default=0)  # OK
    x50 = fields.Boolean("X50__c", default=0)  # OK
    x60 = fields.Boolean("X60__c", default=0)  # OK
    x70 = fields.Boolean("X70__c", default=0)  # OK
    x80 = fields.Boolean("X80__c", default=0)  # OK
    joint_name = fields.Char("X1__c", tracking=True)  # 連名1 OK
    web = fields.Selection([
        ('fb', 'FB'),
        ('insta', 'insta'),
        ('twitter', 'Twitter'),
        ('google', 'Google検索'),
        ('tabroom', 'tabroom'),
        ('youtube', 'Youtube'),
        ('other', 'その他'),
    ], string="web",
        default='', tracking=True)  # WEBサイト OK WEB__c
    media_name = fields.Selection([
        ('1', 'モダンリビング'),
        ('2', "I'm home."),
        ('3', '商店建築'),
        ('4', '婦人画報'),
        ('5', '家庭画報'),
        ('6', 'ゲーテ'),
        ('7', 'Pen'),
        ('8', 'CasaBRUTUS'),
        ('9', 'シグネチャー'),
        ('10', 'ヴィズスタ'),
        ('11', 'その他'),

    ], default='',
        string="media_name", tracking=True)  # 媒体名 OK Field39__c
    case_count = fields.Integer(string="case count", compute="_compute_case_count")
    no_hyphen_phone = fields.Char("no_hyphen_phone", compute="_get_phone_non_hyphen", store=True)
    no_hyphen_mobile = fields.Char("no_hyphen_mobile", compute="_get_phone_non_mobile", store=True)

    age = fields.Integer("age", compute="_get_age", tracking=True)

    condition = fields.Many2many('res.partner.condition', track_visibility='always')

    # 関連項目
    rel_industry = fields.Char(related='parent_id.industry_id.name')
    rel_contact_type = fields.Char(related='parent_id.contact_type.name')
    rel_channel = fields.Char(related='parent_id.channel.name')

    # @api.depends('state_id')
    # def _get_region(self):
    #     area1 = ["東京都", "神奈川県", "千葉県", "埼玉県"]
    #     area2 = ["栃木県", "群馬県", "茨城県"]
    #     area3 = ["北海道", "青森県", "宮城県", "岩手県", "秋田県", "山形県", "福島県"]
    #     area4 = ["山梨県", "長野県", "新潟県"]
    #     area5 = ["静岡県", "三重県", "愛知県", "岐阜県"]
    #     area6 = ["石川県", "富山県", "福井県"]
    #     area7 = ["大阪府", "京都府", "滋賀県", "奈良県", "兵庫県", "和歌山県"]
    #     area8 = ["広島県", "岡山県", "山口県", "島根県", "鳥取県"]
    #     area9 = ["香川県", "愛媛県", "徳島県", "高知県"]
    #     area10 = ["福岡県", "大分県", "熊本県", "佐賀県", "長崎県", "宮崎県", "鹿児島県", "沖縄県"]
    #     for rec in self:
    #         if rec.state_id.name in area1:
    #             rec.region = "関東"
    #         elif rec.state_id.name in area2:
    #             rec.region = "北関東"
    #         elif rec.state_id.name in area3:
    #             rec.region = "東北・北海道"
    #         elif rec.state_id.name in area4:
    #             rec.region = "甲信越"
    #         elif rec.state_id.name in area5:
    #             rec.region = "東海"
    #         elif rec.state_id.name in area6:
    #             rec.region = "北陸"
    #         elif rec.state_id.name in area7:
    #             rec.region = "関西"
    #         elif rec.state_id.name in area8:
    #             rec.region = "中国"
    #         elif rec.state_id.name in area9:
    #             rec.region = "四国"
    #         elif rec.state_id.name in area10:
    #             rec.region = "九州・沖縄"
    #         else:
    #             rec.region = ""

    def _search_npp(self, no_hyphen_phone, args=None, operator='ilike', limit=100):
        if operator == 'like':
            operator = 'ilike'
        versions = self.search([('name', operator, no_hyphen_phone)], limit=limit)
        return versions.name_get()

    def _get_age(self):
        for rec in self:
            if rec.birthdate:
                today = date.today()
                birthday = rec.birthdate
                rec.age = (int(today.strftime("%Y%m%d")) - int(birthday.strftime("%Y%m%d"))) // 10000
            else:
                rec.age = False

    @api.depends("phone")
    def _get_phone_non_hyphen(self):
        for rec in self:
            if rec.phone:
                rec.no_hyphen_phone = rec.phone.replace("-", "")
            else:
                rec.no_hyphen_phone = False

    @api.depends("mobile")
    def _get_phone_non_mobile(self):
        for rec in self:
            if rec.mobile:
                rec.no_hyphen_mobile = rec.mobile.replace("-", "")
            else:
                rec.no_hyphen_mobile = False

    def _compute_case_count(self):
        for rec in self:
            case_count = self.env['rtw_sf_case'].search_count([('contacts', '=', rec.id)])
            rec.case_count = case_count

    def action_open_case(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'case',
            'res_model': 'rtw_sf_case',
            'domain': [('contacts', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
            'context': {
                'default_id': self.id,
                'default_contacts': self.id,
                'default_created_by_id': self.env.user.id
            }
        }

    @api.onchange("first_name", "last_name", "company_type")
    def _compute_get_name(self):
        for rec in self:
            name = rec.name
            if rec.company_type == "person":
                if rec.last_name == False and rec.first_name:
                    name = rec.first_name
                if rec.first_name == False and rec.last_name:
                    name = rec.last_name
                if rec.first_name and rec.last_name:
                    name = rec.last_name + " " + rec.first_name
            rec.name = name
