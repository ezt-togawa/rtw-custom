# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import datetime


class rtw_crm(models.Model):
    _inherit = 'crm.lead'

    # crm_seq = fields.Char('Opportunity No', readonly=True, copy=False)
    crm_seq = fields.Char('Opportunity No', readonly=True, copy=False, default=lambda self: _("New"))
    stage_sort_order = fields.Integer('StageSortOrder')  # 受注段階コード H列
    # expected_revenue = fields.Monetary('ExpectedRevenue')  # 予想売上高 K列
    reference_price = fields.Monetary(compute="_get_reference_price", currency_field='company_currency', store=True,
                                      tracking=True)
    # close_date = fields.Datetime('CloseDate')  # 完了日 M列
    x_type = fields.Char('Type')  # N列
    nextstep = fields.Char('NextStep', tracking=True)  # 次の段階 O列
    lead_source = fields.Selection([
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
        ('-', '-'),
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
        string='LeadSource', tracking=True)  # 見込み顧客の獲得方法 P列
    isclosed = fields.Boolean('IsClosed')  # 完了済みフラグ Q列
    is_won = fields.Boolean('IsWon')  # 成約フラグ R列
    forecast_category = fields.Char('ForecastCategory')  # 予測カテゴリ S列
    forecast_category_name = fields.Selection([
        ('1', 'ロスト'),
        ('2', '進行中'),
        ('3', '見込み有'),
        ('4', '最終交渉'),
        ('5', '受注成立'),
    ], default='',
        string='ForecastCategoryName', tracking=True)  # 予測カテゴリ名 T列
    # campaign_id = fields.Char('CampaignId')  # キャンペーンId U列
    # has_opportunity_line_item = fields.Char('HasOpportunityLineItem')  # 段階名 V列
    # price_book2_id = fields.Char('Pricebook2Id')  # 段階名 W列
    # owner_id = fields.Many2one('res.users', 'OwnerId')  # 所有者Id X列 1
    r_partner_id = fields.Many2one('res.users', 'Partner')
    created_date = fields.Datetime('CreatedDate')  # 作成日 AM列
    created_by_id = fields.Many2one('res.users', 'CreatedById')  # 作成ID AN列
    last_modified_date = fields.Datetime('LastModifiedDate')  # 最終更新日 AO列
    last_modified_by_id = fields.Many2one('res.users', 'LastModifiedById')  # 最終更新者 AP列
    system_mod_stamp = fields.Datetime('SystemModstamp')  # システム最終更新日 AQ列
    last_activity_date = fields.Datetime('LastActivityDate')  # システム最終活動日
    last_stage_changed_date = fields.Datetime('LastStageChangeDate')  # 最終ステージ変更日
    fiscal_year = fields.Integer('FiscalYear')  # 会計年度　注意
    fiscal_quarter = fields.Integer('FiscalQuarter')  # 会計四半期
    contact_id = fields.Many2one('res.partner', 'ContactId')  # コンタクトId
    primary_partner_Account_id = fields.Char('PrimaryPartnerAccountId')  # プライマリーパートナーId
    # synced_quote_id = fields.Char('SyncedQuoteId')  # 同期引用Id
    contract_id = fields.One2many('contract.contract', inverse_name="related_opportunity", string='ContractId',
                                  tracking=True)  # 契約Id
    last_amount_changed_history_id = fields.Char('LastAmountChangedHistoryId')  # 最終金額変更履歴
    last_close_date_changed_history_id = fields.Char('LastCloseDateChangedHistoryId')  # 最終完了日変更履歴
    progress_check_date = fields.Datetime('Field1__c', tracking=True)  # 進捗確認日 AN列
    quote_number_by_hukusuke = fields.Char('Field2__c', tracking=True)  # 福助で採番される見積番号 AO列
    quote_number = fields.Char('Field3_del__c')  # 見積番号 AP列
    previous_amount = fields.Float('previousamount__c', tracking=True)  # 直前の金額 AQ列
    opportunity_number = fields.Char('Field4__c')  # 商談番号 AR列　
    last_amount_changed_datetime = fields.Datetime('lastamountchangedatetime__c')  # 最終金額変更日時 AS列
    presentation = fields.Boolean('presentation__c')  # 通常プレゼン AT列 ★0，1，空白あり
    project_details = fields.Text('Field60__c')  # 案件詳細 AU列
    Determined_on_the_day = fields.Boolean('Determinedontheday__c', default=0)  # 当日確定 AV列 ★0，1，空白あり
    delivery_date_unknown = fields.Boolean('Field5__c', default=0, tracking=True)  # 納期不明 AW列 ★0，1，空白あり
    delivery_type = fields.Selection([
        ('1', '住宅系（戸建・マンション）'),
        ('2', '医療福祉（病院・老健等）'),
        ('3', '宿泊施設（旅館・ホテル等）'),
        ('4', '公共施設（空港・図書館・他文化施設等）'),
        ('5', '商業施設（飲食・物販等）'),
        ('6', 'オフィス・金融関連'),
        ('7', '小物（家具以外）'),
        ('8', 'その他'),
    ], default='',
        string='Field6__c', tracking=True)  # 納入先種別 AX列
    order_amount = fields.Float('Field7__c')  # 受注額 AY列　注意
    omotesando_visit = fields.Boolean('Field87__c', default=0, tracking=True)  # 表参道来店 AZ列 ★0，1，空白あり
    fair = fields.Char('Field22__c')  # Fair BA列
    million_amount = fields.Float('X100_amount__c')  # 100万金額 BB列
    million_order_amount = fields.Float('X100_amount_a__c')  # 100万受注額 BC列 注意
    competition_a = fields.Selection([
        ('1', '競合なし'),
        ('2', 'ACTUS'),
        ('3', 'ＡＤコア'),
        ('4', 'arflex'),
        ('5', 'cassina ixc.'),
        ('6', 'B&B Italia Japan'),
        ('7', 'Bo concept'),
        ('8', 'DREXEL HERITAGE'),
        ('9', 'Time&Style'),
        ('10', 'Minotti'),
        ('11', 'アイデック'),
        ('12', 'エスティック'),
        ('13', '大塚家具'),
        ('14', 'カリモク家具'),
        ('15', 'カンディハウス'),
        ('16', '日進木工'),
        ('17', '日本フクラ'),
        ('18', '飛騨産業'),
        ('19', '広松木工'),
        ('20', '冨士ファニチア'),
        ('21', 'マスターウォール'),
        ('22', 'マルニ木工'),
        ('23', 'その他'),
        ('24', '不明'),
    ], default='24',
        string='Field16__c')  # 競合A BD列
    fair_advance_plan = fields.Boolean('Field34_plan__c', default=0)  # フェア事前プラン BE列 ★0，1，空白あり
    product_others = fields.Char('Field14__c')  # 商品その他（補足） BF列
    our_strengths = fields.Text('Field30__c')  # 自社の強み BG列
    million_order_count = fields.Boolean('X100_count_a__c', default=0)  # 100万受注数 BH列 ★0，1，空白あり
    total_million_order_count = fields.Boolean('X100_count__c', default=0)  # 100万総数 BI列 ★0，1，空白あり
    Use_Purpose = fields.Text('Field61__c')  # 使用用途(その他） BJ列
    reason_selection = fields.Text('Field62__c')  # 選定理由 BK列
    Use_Purpose1 = fields.Selection([
        ('1', 'ダイニング'),
        ('2', 'ラウンジ・カフェ'),
        ('3', 'バー'),
        ('4', '待合・休憩（飲食なし）'),
        ('5', '接客・商談用'),
        ('6', '客室（病室/マンション含）'),
        ('7', '応接室'),
        ('8', '会議室'),
        ('9', 'ワークスペース'),
        ('10', 'その他'),
    ], default='',
        string='Field63_purpose__c', tracking=True)  # 使用用途① BL列
    Use_Purpose2 = fields.Selection([
        ('1', 'ダイニング'),
        ('2', 'ラウンジ・カフェ'),
        ('3', 'バー'),
        ('4', '待合・休憩（飲食なし）'),
        ('5', '接客・商談用'),
        ('6', '客室（病室/マンション含）'),
        ('7', '応接室'),
        ('8', '会議室'),
        ('9', 'ワークスペース'),
        ('10', 'その他'),
    ], default='',
        string='Field64_purpose__c', tracking=True)  # 使用用途② BM列
    Use_Purpose3 = fields.Selection([
        ('1', 'ダイニング'),
        ('2', 'ラウンジ・カフェ'),
        ('3', 'バー'),
        ('4', '待合・休憩（飲食なし）'),
        ('5', '接客・商談用'),
        ('6', '客室（病室/マンション含）'),
        ('7', '応接室'),
        ('8', '会議室'),
        ('9', 'ワークスペース'),
        ('10', 'その他'),
    ], default='',
        string='Field65_purpose__c', tracking=True)  # 使用用途③ BN列
    other = fields.Boolean('ITEM_other_08__c', default=0)  # その他 BO列 ★0，1，空白あり
    ac = fields.Boolean('CHAI_2__c', default=0)  # AC BP列 ★0，空白あり
    website = fields.Char('WEB__c', tracking=True)  # WEBサイト BQ列
    competitive_reason = fields.Text('Field31__c')  # 競合理由 BR列
    order_no = fields.Char('NO__c', tracking=True)  # 受注NO BS列
    facility_name = fields.Char('Field64__c', tracking=True)  # 施設名 BT列
    competition_other = fields.Char('Field17__c')  # 競合（その他） BU列
    competitive_product_d = fields.Selection([
        ('1', 'Dt'),
        ('2', 'ﾁｪｱ'),
        ('3', 'Dｾｯﾄ'),
        ('4', 'その他'),
    ], default='',
        string='Field18__c')  # 競合商品(D) BV列
    competitive_product_name = fields.Char('Field19__c')  # 競合商品名 BW列
    competitive_product_l = fields.Selection([
        ('1', 'ｿﾌｧ'),
        ('2', 'Lt'),
        ('3', 'ﾎﾞｰﾄﾞ'),
        ('4', 'Lｾｯﾄ'),
    ], default='',
        string='L__c')  # 競合商品(L) BX列
    competitive_product_other = fields.Selection([
        ('1', 'Sﾎﾞｰﾄﾞ'),
        ('2', 'ﾗｸﾞ'),
    ], default='',
        string='Field20__c')  # 競合商品（他） BY列
    other_strengths = fields.Text('Field21__c')  # 他社の強み BZ列
    competition_b = fields.Selection([
        ('1', 'ACTUS'),
        ('2', 'ＡＤコア'),
        ('3', 'arflex'),
        ('4', 'cassina ixc.'),
        ('5', 'B&B Italia Japan'),
        ('6', 'Bo concept'),
        ('7', 'DREXEL HERITAGE'),
        ('8', 'Time&Style'),
        ('9', 'Minotti'),
        ('10', 'アイデック'),
        ('11', 'エスティック'),
        ('12', '大塚家具'),
        ('13', 'カリモク家具'),
        ('14', 'カンディハウス'),
        ('15', '日進木工'),
        ('16', '日本フクラ'),
        ('17', '飛騨産業'),
        ('18', '広松木工'),
        ('19', '冨士ファニチア'),
        ('20', 'マスターウォール'),
        ('21', 'マルニ木工'),
    ], default='',
        string='B__c')  # 競合B CA列
    campaign = fields.Char('Field65__c')  # キャンペーン CB列
    product_list_other = fields.Selection([
        ('1', 'クッション'),
        ('2', 'スペアカバー'),
        ('3', '中材'),
        ('4', 'スペアカバー+中材'),
        ('5', 'プラパート'),
        ('6', 'その他部材'),
        ('7', 'オイルキット'),
        ('8', 'レザーキット'),
        ('9', 'オイル・レザーキット'),
        ('10', 'カレンダー'),
        ('11', 'その他'),
        ('-', '-'),
        ('12', 'ペリーニ'),
        ('13', 'キリム'),
    ], default='',
        string='Field68__c')  # 商品リスト（その他） CC列
    action1 = fields.Selection([
        ('1', '電話'),
        ('2', 'FAX'),
        ('3', '（R）WEBフォーム'),
        ('4', '（媒体）資料請求'),
        ('5', 'E-mail'),
        ('6', 'SR来場'),
        ('7', '表参道来店'),
        ('8', 'SRフェア'),
        ('9', 'インテリアフェア'),
        ('10', '訪問'),
        ('11', 'イベント参加'),
        ('12', 'ミラノサローネ'),
        ('13', 'その他'),
    ], default='',
        string='Field23__c', tracking=True)  # アクション① CD列
    memo = fields.Text('Field35_del__c')  # メモ CE列
    branch = fields.Char('Branch__c')  # Branch CF列
    action2 = fields.Selection([
        ('1', '問合せ'),
        ('2', '資料請求'),
        ('3', '見積依頼'),
        ('4', 'プレゼン依頼'),
        ('5', '注文'),
        ('6', 'SR来場'),
        ('7', '表参道来店'),
        ('8', 'インテリアフェア'),
        ('9', '(R)WEBフォーム'),
        ('10', 'その他'),
    ], default='',
        string='Field24__c', tracking=True)  # アクション② CG列
    last_event_comment = fields.Text('LastEventComment__c')  # 最終行動コメント CH列
    diana_count = fields.Float('DIANA__c')  # DIANA台数 CI列
    sample_sale = fields.Selection([
        ('all', '全て'),
        ('same', '一部'),
    ], default='',
        string='Field25__c', tracking=True)  # サンプル販売 CJ列
    sample_sales_amount = fields.Integer('Field26__c', tracking=True)  # サンプル販売金額 CK列
    push_c = fields.Float('Push_Counter__c', tracking=True)  # Push C(完了予定日を翌月以降に変更した回数をカウント) CL列
    area = fields.Char('Field32_del__c')  # エリア CM列
    pre_contract_presentation = fields.Boolean('Field34_plan2__c')  # 契約前プレゼン CN列
    overlap = fields.Char('Field34__c')  # Overlap CO列
    memo_other = fields.Char('Field28__c')  # メモ（台数など） CP列
    product_list_rug = fields.Selection([
        ('1', 'ペリーニ'),
        ('2', 'キリム'),
        ('3', 'その他'),
    ], default='',
        string='Field70__c')  # 商品リスト（ラグ） CQ列
    product_list_dt2 = fields.Selection([
        ('1', 'EX TABLE'),
        ('2', 'FV TABLE'),
        ('3', 'MC TABLE'),
        ('4', 'MCM TABLE'),
        ('5', 'MM TABLE'),
        ('6', 'MO TABLE(RO)'),
        ('7', 'MO TABLE(OB)'),
        ('8', 'MT TABLE'),
        ('9', 'QX TABLE'),
        ('10', '廃盤品'),
        ('11', '特注品'),
    ], default='',
        string='Dt2__c')  # 商品リスト(Dt2) CR列
    product_list_dt1 = fields.Selection([
        ('1', 'EX TABLE'),
        ('2', 'FV TABLE'),
        ('3', 'MC TABLE'),
        ('4', 'MCM TABLE'),
        ('5', 'MM TABLE'),
        ('6', 'MO TABLE(RO)'),
        ('7', 'MO TABLE(OB)'),
        ('8', 'MT TABLE'),
        ('9', 'QX TABLE'),
        ('10', '廃盤品'),
        ('11', '特注品'),
    ], default='',
        string='Dt1__c')  # 商品リスト(Dt1) CS列
    product_list_lt2 = fields.Selection([
        ('1', 'CM TABLE (L)'),
        ('2', 'CB TABLE(L)'),
        ('3', 'GO TABLE(L)'),
        ('4', 'JK TABLE (L)'),
        ('5', 'LW TABLE(L)'),
        ('6', 'MO TABLE(L)'),
        ('7', 'SI TABLE(L)'),
        ('8', '特注品'),
        ('-', '-以下使用しない-'),
        ('9', 'JK TABLE(L)'),
        ('10', 'CM TABLE(L)'),
    ], default='',
        string='Lt2__c')  # 商品リスト(Lt2) CT列
    fair_Year = fields.Datetime('Field33__c')  # フェア開催年 CU列
    product_list_lt1 = fields.Selection([
        ('1', 'CM TABLE (L)'),
        ('2', 'CB TABLE (L)'),
        ('3', 'GO TABLE (L)'),
        ('4', 'JK TABLE (L)'),
        ('5', 'LW TABLE (L)'),
        ('6', 'MO TABLE(L)'),
        ('7', 'SI TABLE(L)'),
        ('8', '特注品'),
    ], default='',
        string='Lt1__c')  # 商品リスト(Lt1) CV列
    product_list_ec1 = fields.Selection([
        ('1', 'BEATRIX(M)'),
        ('2', 'BEATRIX(L)'),
        ('3', 'RIVAGE(EC)'),
        ('4', 'RIVAGE(LC)'),
        ('5', 'BLAVA(EC)'),
        ('6', 'BLAVA(HEC)'),
        ('7', 'CLAUDE(EC)'),
        ('8', 'GRACE'),
        ('9', 'JK(EC)'),
        ('10', 'LE BEAU'),
        ('11', 'LOS'),
        ('12', 'LUPIN(LC)'),
        ('13', 'OSCAR'),
        ('-', '-'),
        ('14', 'MT BENCH(M)'),
        ('15', 'MT BENCH(L)'),
    ], default='',
        string='EC1__c')  # 商品リスト(EC1) CW列
    product_list_ec2 = fields.Selection([
        ('1', 'BEATRIX(M)'),
        ('2', 'BEATRIX(L)'),
        ('3', 'RIVAGE(EC)'),
        ('4', 'RIVAGE(LC)'),
        ('5', 'BLAVA(EC)'),
        ('6', 'BLAVA(HEC)'),
        ('7', 'CLAUDE(EC)'),
        ('8', 'GRACE'),
        ('9', 'JK(EC)'),
        ('10', 'LE BEAU'),
        ('11', 'LOS'),
        ('12', 'LUPIN(LC)'),
        ('13', 'OSCAR'),
        ('-', '-'),
        ('14', 'MT BENCH(M)'),
        ('15', 'MT BENCH(L)'),
    ], default='',
        string='EC2_2__c')  # 商品リスト(EC2) CX列
    l_set = fields.Integer('Lset__c')  # CY列
    product_list_st2 = fields.Selection([
        ('1', 'CM TABLE(S)'),
        ('2', 'CB TABLE(S)'),
        ('3', 'CR TABLE'),
        ('11', 'CR TABLE(S)'),
        ('4', 'GO TABLE(S)'),
        ('5', 'JK TABLE(S)'),
        ('6', 'LW TABLE(S)'),
        ('7', 'MO TABLE(S)'),
        ('8', 'OS TABLE(070)'),
        ('9', 'OS TABLE(040)'),
        ('10', 'RV TABLE'),
    ], default='',
        string='St2__c')  # 商品リスト(St2) CZ列
    product_list_st1 = fields.Selection([
        ('1', 'CM TABLE (S)'),
        ('2', 'CB TABLE (S)'),
        ('3', 'CR TABLE'),
        ('4', 'GO TABLE (S)'),
        ('5', 'JK TABLE(S)'),
        ('6', 'LW TABLE (S)'),
        ('7', 'MO TABLE (S)'),
        ('8', 'OS TABLE(070)'),
        ('9', 'OS TABLE(040)'),
        ('10', 'RV TABLE'),
    ], default='',
        string='St1__c')  # 商品リスト(St1) DA列
    opportunity_completion_date = fields.Datetime('Field72__c', tracking=True)  # 商談完了日 DB列
    product_list_ot_st1 = fields.Selection([
        ('1', 'BEATRIX(OT)'),
        ('2', 'BLAVA（OT)'),
        ('3', 'RIVAGE(ST)'),
        ('4', 'VINCENT(ST)'),
        ('5', 'C-LINE(ST)'),
        ('6', 'MO STOOL(S)'),
        ('7', 'MO STOOL(M)'),
    ], default='',
        string='ST1_1__c')  # 商品リスト(OT/ST1) DC列
    term = fields.Char('Term__c')  # Term DD列
    product_list_ot_st2 = fields.Selection([
        ('1', 'BEATRIX(OT)'),
        ('2', 'BLAVA(OT)'),
        ('3', 'RIVAGE(ST)'),
        ('4', 'VINCENT(ST)'),
        ('5', 'C-LINE(ST)'),
        ('6', 'MO STOOL(S)'),
        ('7', 'MO STOOL(M)'),
    ], default='',
        string='ST2_2__c')  # 商品リスト(OT/ST2) DE列
    product_list_board1 = fields.Selection([
        ('1', 'JABARA(SB)'),
        ('2', 'JABARA(TV)'),
        ('3', 'UNO'),
        ('4', 'CB 718'),
        ('5', 'MO SMALL DESK'),
    ], default='',
        string='BOARD1__c')  # 商品リスト(BOARD1) DF列
    product_list_board2 = fields.Selection([
        ('1', 'JABARA(SB)'),
        ('2', 'JABARA(TV)'),
        ('3', 'UNO'),
        ('4', 'CB 718'),
        ('5', 'MO SMALL DESK'),
    ], default='',
        string='BOARD2__c')  # 商品リスト(BOARD2) DG列
    year = fields.Integer('Year__c')  # Year DH列
    product_list_sofa3 = fields.Selection([
        ('1', 'ARLES'),
        ('2', 'ARMSTRONG'),
        ('3', 'AVENUE'),
        ('4', 'CARLOS'),
        ('5', 'CB SOFA'),
        ('6', 'DIANA'),
        ('7', 'LEBEAU'),
        ('8', 'LW SOFA'),
        ('9', 'LF SOFA'),
        ('10', 'PLAZA'),
        ('11', '廃盤品'),
    ], default='',
        string='X3__c')  # 商品リスト(ソファ3) DI列
    # completion_scheduled_date = fields.Datetime('A__c')  # 完了予定日（A) DJ列
    product_list_sofa1 = fields.Selection([
        ('1', 'ARLES'),
        ('2', 'ARMSTRONG'),
        ('3', 'AVENUE'),
        ('4', 'CARLOS'),
        ('5', 'CB SOFA'),
        ('6', 'DIANA'),
        ('7', 'LEBEAU'),
        ('8', 'LW SOFA'),
        ('9', 'LF SOFA'),
        ('10', 'PLAZA'),
        ('11', '廃盤品'),
    ], default='',
        string='X1__c')  # 商品リスト(ソファ1) DK列
    product_list_sofa2 = fields.Selection([
        ('1', 'ARLES'),
        ('2', 'ARMSTRONG'),
        ('3', 'AVENUE'),
        ('4', 'CARLOS'),
        ('5', 'CB SOFA'),
        ('6', 'DIANA'),
        ('7', 'LEBEAU'),
        ('8', 'LW SOFA'),
        ('9', 'LF SOFA'),
        ('10', 'PLAZA'),
        ('11', '廃盤品'),
    ], default='',
        string='X2_2__c')  # 商品リスト(ソファ2) DL列
    product_list_ec3 = fields.Selection([
        ('1', 'BEATRIX(M)'),
        ('2', 'BEATRIX(L)'),
        ('3', 'RIVAGE(EC)'),
        ('4', 'RIVAGE(LC)'),
        ('5', 'BLAVA(EC)'),
        ('6', 'BLAVA(HEC)'),
        ('7', 'CLAUDE(EC)'),
        ('8', 'GRACE'),
        ('9', 'JK(EC)'),
        ('10', 'LE BEAU'),
        ('11', 'LOS'),
        ('12', 'LUPIN(LC)'),
        ('13', 'OSCAR'),
        ('-', '-'),
        ('14', 'MT BENCH(M)'),
        ('15', 'MT BENCH(L)'),
    ], default='',
        string='EC3__c')  # 商品リスト(EC3) DM列
    product_list_chair1 = fields.Selection([
        ('1', 'ブラヴァ(C)'),
        ('2', 'ブラヴァ(AC)'),
        ('3', 'カレッツァ(C)'),
        ('4', 'カレッツァ(AC)'),
        ('5', 'チャーリー'),
        ('6', 'クロード(C)'),
        ('7', 'クロード(AC)'),
        ('8', 'シーライン(AC)'),
        ('9', 'JK(AC)'),
        ('10', 'クリント(C)'),
        ('11', 'クリント(AC)'),
        ('12', 'ルパン(C)'),
        ('13', 'ルパン(AC)'),
        ('14', 'マルセル'),
        ('15', 'リヴァージュ(AC)'),
        ('16', 'スコラー'),
        ('17', 'ルボー(AC)'),
    ], default='',
        string='Field29__c')  # 商品リスト(ﾁｪｱ1) DN列
    product_list_chair2 = fields.Selection([
        ('1', 'ブラヴァ(C)'),
        ('2', 'ブラヴァ(AC)'),
        ('3', 'カレッツァ(C)'),
        ('4', 'カレッツァ(AC)'),
        ('5', 'チャーリー'),
        ('6', 'クロード(C)'),
        ('7', 'クロード(AC)'),
        ('8', 'シーライン(AC)'),
        ('9', 'JK(AC)'),
        ('10', 'クリント(C)'),
        ('11', 'クリント(AC)'),
        ('12', 'ルパン(C)'),
        ('13', 'ルパン(AC)'),
        ('14', 'マルセル'),
        ('15', 'リヴァージュ(AC)'),
        ('16', 'スコラー'),
        ('17', 'ルボー(AC)'),
    ], default='',
        string='X2_5__c')  # 商品リスト(ﾁｪｱ2) DO列
    product_list_chair3 = fields.Selection([
        ('1', 'ブラヴァ(C)'),
        ('2', 'ブラヴァ(AC)'),
        ('3', 'カレッツァ(C)'),
        ('4', 'カレッツァ(AC)'),
        ('5', 'チャーリー'),
        ('6', 'クロード(C)'),
        ('7', 'クロード(AC)'),
        ('8', 'シーライン(AC)'),
        ('9', 'JK(AC)'),
        ('10', 'クリント(C)'),
        ('11', 'クリント(AC)'),
        ('12', 'ルパン(C)'),
        ('13', 'ルパン(AC)'),
        ('14', 'マルセル'),
        ('15', 'リヴァージュ(AC)'),
        ('16', 'スコラー'),
        ('17', 'ルボー(AC)'),
    ], default='',
        string='X3_4__c')  # 商品リスト(ﾁｪｱ3) DP列
    product_list_chair4 = fields.Selection([
        ('1', 'ブラヴァ(C)'),
        ('2', 'ブラヴァ(AC)'),
        ('3', 'カレッツァ(C)'),
        ('4', 'カレッツァ(AC)'),
        ('5', 'チャーリー'),
        ('6', 'クロード(C)'),
        ('7', 'クロード(AC)'),
        ('8', 'シーライン(AC)'),
        ('9', 'JK(AC)'),
        ('10', 'クリント(C)'),
        ('11', 'クリント(AC)'),
        ('12', 'ルパン(C)'),
        ('13', 'ルパン(AC)'),
        ('14', 'マルセル'),
        ('15', 'リヴァージュ(AC)'),
        ('16', 'スコラー'),
        ('17', 'ルボー(AC)'),
    ], default='',
        string='X4_1__c')  # 商品リスト(ﾁｪｱ4) DQ列
    progress_check = fields.Text('Field36__c')  # 進捗確認/経過報告 DR列
    opportunity_type = fields.Selection([
        ('1', '1.フェア'),
        ('2', '2.フェア外一般邸'),
        ('3', '3.展示場/SR'),
        ('4', '4.その他'),
    ], default='',
        string='Field37__c')  # 商談種別 DS列
    crm_type = fields.Selection([
        ('1', '戸建(ﾌｪｱ)'),
        ('2', '戸建(ﾌｪｱ外)'),
        ('3', 'ﾏﾝｼｮﾝ個人（ﾌｪｱ）'),
        ('4', 'ﾏﾝｼｮﾝ個人（ﾌｪｱ外）'),
        ('5', 'ﾏﾝｼｮﾝﾓﾃﾞﾙ'),
        ('6', 'ﾏﾝｼｮﾝ共用部'),
        ('7', 'ｺﾝﾄﾗｸﾄ'),
        ('8', 'ｺﾝﾄﾗｸﾄ（直販）'),
        ('9', 'OEM'),
        ('10', '住宅展示場'),
        ('11', 'SR・商談室'),
        ('12', 'ｻﾝﾌﾟﾙ貸出（展示会他）'),
        ('13', '撮影・セット用'),
        ('14', '関係者直販'),
        ('15', '海外レジデンシャル'),
        ('16', '海外コントラクト'),
        ('17', 'その他'),
        ('18', '集計用'),
        ('-', '以下未使用'),
        ('19', 'その他コントラクト'),
        ('20', '既存ビジネス'),
        ('21', '新規ビジネス'),
        ('22', 'インテリアフェア'),
        ('23', 'ハウスメーカーその他'),
        ('24', 'マンション個人（販売会含む）'),
        ('25', 'マンションその他'),
        ('26', '代理店・OEM'),
        ('27', 'ショールーム販売'),
        ('28', 'セール販売'),
        ('29', '海外'),
        ('30', '該当なし（不明）'),
        ('31', 'マンション一般邸（IC直販）'),
    ], default='',
        string="Type", tracking=True)
    accuracy = fields.Float('Field38__c', tracking=True)  # 確度（変更前） DT列　注意
    last_accuracy_changed_date = fields.Datetime('Field39__c')  # 最終確度変更日時 DU列
    result = fields.Selection([
        ('1', 'R〇競×'),
        ('2', 'R△競△'),
        ('3', 'R×競〇'),
        ('4', 'R×競×'),
        ('5', '不明'),
    ], default='',
        string='Field40__c')  # 結果 DV列
    On_site_delivery_date = fields.Datetime('Field43__c', tracking=True)  # 現場納品日 DW列
    beatrix_count = fields.Float('BEATRIX_count__c')  # BEATRIX台数 DX列
    jabara_count = fields.Float('JABARA__c')  # JABARA台数 DY列
    lf_set_count = fields.Float('LF__c')  # LFセット数 DZ列
    product_list_sofa_ot1 = fields.Selection([
        ('1', 'ARLES(OT)'),
        ('2', 'CB(OT)'),
        ('3', 'DIANA(OT)'),
        ('4', 'LF(OT)'),
        ('5', 'LW(OT)'),
        ('6', 'PLAZA(OT)'),
        ('7', '廃番品'),
        ('8', '特注'),
    ], default='',
        string='Sofa_OT__c')  # 商品リスト(ソファOT1) EA列
    product_list_sofa_ot2 = fields.Selection([
        ('1', 'ARLES(OT)'),
        ('2', 'CB(OT)'),
        ('3', 'DIANA(OT)'),
        ('4', 'LF(OT)'),
        ('5', 'LW(OT)'),
        ('6', 'PLAZA(OT)'),
        ('7', '廃番品'),
        ('8', '特注'),
    ], default='',
        string='OT2__c')  # 商品リスト(ソファOT2) EB列
    rate = fields.Float('Field74__c', tracking=True)  # 掛率 EC列
    dummy = fields.Boolean('Field75__c', default=0)  # ﾀﾞﾐｰ ED列
    lw_set_count = fields.Float('LW_5__c')  # LWセット数 EE列
    trw_candidate = fields.Boolean('TRW__c', default=0)  # TRW候補 EF列
    questionnaire = fields.Boolean('Field50__c', default=0)  # アンケート EG列
    letter_of_acceptance = fields.Boolean('Field51__c', default=0)  # 承諾書 EH列
    how_to_get_photos = fields.Selection([
        ('1', '建築写真を購入'),
        ('2', '自社でカメラマン手配'),
        ('3', 'その他'),
    ], default='',
        string='Field52__c')  # 写真入手方法 EI列
    memo_trw = fields.Text('TRW_2__c')  # TRWメモ EJ列
    examination = fields.Selection([
        ('archive', 'Archive'),
        ('project', 'Project'),
        ('trw', '★TRW'),
    ], default='archive',
        string='Field53__c')  # 審査 EK列
    cost = fields.Integer('Field54__c')  # 経費 EL列
    photographer = fields.Char('Field55__c')  # Photographer EM列
    shooting_date = fields.Datetime('Field56__c')  # 撮影日 EN列
    installation_floor = fields.Selection([
        ('1', '1F'),
        ('2', '2F'),
        ('3', '3F'),
        ('4', '4F～'),
        ('ug', '地下'),
    ], default='',
        string='Field57__c', tracking=True)  # 設置階 EO列
    delivery_route_required_confirmation = fields.Boolean('Field58__c', default=0, tracking=True)  # 搬入経路要確認 EP列
    elevator_having = fields.Boolean('EV__c', default=0, tracking=True)  # EV有 EQ列
    budget_data = fields.Boolean('SFDC_Budget__c', default=0)  # 予算データ ER列
    lost = fields.Float('Field59__c')  # ロスト ES列
    p_author = fields.Many2one('res.users', 'P__c')  # P作成者(代表） ET列
    product_list_sofa_bench1 = fields.Selection([
        ('1', 'MT BENCH(M)'),
        ('2', 'MT BENCH(L)'),
        ('3', 'MO BENCH(S)'),
        ('4', 'MO BENCH(M)'),
        ('5', 'MO BENCH(SQ)'),
        ('6', 'CB BENCH'),
        ('7', '廃番品'),
        ('8', '特注品'),
    ], default='',
        string='Bench1__c')  # 商品リスト（Bench1) EU列
    product_list_sofa_bench2 = fields.Selection([
        ('1', 'MT BENCH(M)'),
        ('2', 'MT BENCH(L)'),
        ('3', 'MO BENCH(S)'),
        ('4', 'MO BENCH(M)'),
        ('5', 'MO BENCH(SQ)'),
        ('6', 'CB BENCH'),
        ('7', '廃番品'),
        ('8', '特注品'),
    ], default='',
        string='Bench2__c')  # 商品リスト（Bench2) EV列
    procurement_company = fields.Many2one('res.partner', 'Field77__c', tracking=True)  # 調達会社 EW列
    address_no = fields.Char('Field78__c', tracking=True)  # 〒 EX列
    address = fields.Char('Field79__c', tracking=True)  # 住所 EY列
    tel = fields.Char('Field80__c', tracking=True)  # 電話 EZ列
    person_name = fields.Char('Field81__c', tracking=True)  # 名前 FA列
    furigana = fields.Char('Field82__c', tracking=True)  # フリガナ FB列
    depot = fields.Char('Field83__c', tracking=True)  # デポ FC列
    depot_arrival_date = fields.Datetime('Field84__c', tracking=True)  # デポ着日 FD列
    to_arrangement_depot = fields.Boolean('Field85__c', default=0, tracking=True)  # 手配デポまで FE列
    special_remarks = fields.Text('Field86__c')  # Photographer FF列
    case_ids = fields.One2many(
        comodel_name="rtw_sf_case",
        inverse_name="crm_id",
        string="case", )
    case_count = fields.Integer(string="case count", compute="_compute_case_count")
    calendar_ids = fields.One2many(
        comodel_name="calendar.event",
        inverse_name="opportunity_id",
        string="calendar", )
    belong = fields.Char(compute="_get_belong", store=True)

    tracking_deadline = fields.Date(compute="_set_deadline", store=True, tracking=True)
    presentation_flag = fields.Boolean(compute="_get_presentation_flag")
    sr_status = fields.Char(compute="_get_sr_status")

    @api.depends('date_deadline')
    def _set_deadline(self):
        for rec in self:
            rec.tracking_deadline = rec.date_deadline

    @api.depends('user_id')
    def _get_belong(self):
        for rec in self:
            rec.belong = self.env['crm.team'].search([('member_ids.id', '=', rec.user_id.id)]).name

    def _get_sr_status(self):
        for rec in self:
            if rec.calendar_ids:
                # print(rec.calendar_ids.situation.value)
                # print(rec.id)
                # res = rec.search([('calendar_ids.situation', '=', "4"),
                #                    ('id', '=', rec.id)])

                res = self.env['calendar.event'].search([('opportunity_id', '=', rec.id), ('situation', '=', "4")])

                if res:
                    rec.sr_status = min(res).sr.name + str(min(res).start.year)
                else:
                    rec.sr_status = ""
                # print(min(res.calendar_ids).sr.name)
                # for line in res:
                #     print(line.sr.name)
            else:
                rec.sr_status = ""
            sr_y = 0
            # for line in rec.calendar_ids:
            #     print(line.sr.name)
            # rec.sr_status = line.sr.name

    def _compute_case_count(self):
        for rec in self:
            case_count = self.env['rtw_sf_case'].search_count([('crm_id', '=', rec.id)])
            rec.case_count = case_count

    def _get_presentation_flag(self):
        for rec in self:
            if rec.presentation or rec.pre_contract_presentation or rec.fair_advance_plan:
                rec.presentation_flag = True
            else:
                rec.presentation_flag = False

    def action_open_case(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'case',
            'res_model': 'rtw_sf_case',
            'domain': [('crm_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
            'context': {
                'default_id': self.id,
                'default_contacts': self.partner_id.id,
                'default_created_by_id': self.env.user.id,
                'default_crm_id': self.id
            }
        }

    def create_case(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'rtw_sf_case',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_id': self.id,
                'default_contacts': self.partner_id.id,
                'default_created_by_id': self.env.user.id,
                'default_crm_id': self.id
            }
        }

    @api.onchange('stage_id')
    def _set_opportunity_completion_date(self):
        if not self.opportunity_completion_date:
            if self.stage_id.name == "受注成立" or self.stage_id.name == "ロスト":
                self.opportunity_completion_date = fields.datetime.now()
        elif self.opportunity_completion_date:
            if self.stage_id.name != "受注成立" or self.stage_id.name != "ロスト":
                self.opportunity_completion_date = False
            if self._origin.stage_id.name != self.stage_id.name:
                if self.stage_id.name == "受注成立" or self.stage_id.name == "ロスト":
                    self.opportunity_completion_date = fields.datetime.now()

    @api.depends('expected_revenue', 'rate')
    def _get_reference_price(self):
        for rec in self:
            if rec.rate > 0:
                reference_price = rec.expected_revenue / rec.rate * 100
                rec.reference_price = reference_price
            else:
                rec.reference_price = rec.expected_revenue

    @api.model
    def create(self, vals):

        if vals.get('crm_seq', 'New') == 'New':
            vals['crm_seq'] = self.env['ir.sequence'].next_by_code('crm.lead') or 'New'

        result = super(rtw_crm, self).create(vals)

        return result

    def _update_crm_seq(self, limit=1000):
        leads = self.search([("crm_seq", "=", "New")], order="id", limit=limit)
        print(leads)
        for lead in leads:
            lead.crm_seq = self.env["ir.sequence"].next_by_code("crm.lead")
            print(lead.crm_seq)
