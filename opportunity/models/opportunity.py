# -*- coding: utf-8 -*-

from odoo import models, fields, api


class opportunity(models.Model):
    _name = 'opportunity.opportunity'
    _inherit = [
        'mail.thread',
        'mail.activity.mixin'
    ]
    _description = 'opportunity.opportunity'
    _rec_name = "subject_name"

    accounts = fields.Many2one('res.partner', "Account", copy=False)  # アカウント
    subject_name = fields.Char('Name')  # 案件名 E列
    description = fields.Text('Description')  # 説明 F列
    stage_name = fields.Char('StageName')  # 段階名 G列
    stage_sort_order = fields.Integer('StageSortOrder')  # 受注段階コード H列
    amount = fields.Float('Amount')  # 金額 I列
    probability = fields.Integer('Probability')  # 確率 J列
    expected_revenue = fields.Float('ExpectedRevenue')  # 予想売上高 K列
    # total_opportunity_quantity = fields.Float('TotalOpportunityQuantity')  # 契約金額合計 L列
    close_date = fields.Datetime('CloseDate')  # 完了日 M列
    type = fields.Char('Type')  # N列
    nextstep = fields.Char('NextStep')  # 次の段階 O列
    lead_source = fields.Char('LeadSource')  # 見込み顧客の獲得方法 P列
    isclosed = fields.Boolean('IsClosed')  # 完了済みフラグ Q列
    is_won = fields.Boolean('IsWon')  # 成約フラグ R列
    forecast_category = fields.Char('ForecastCategory')  # 予測カテゴリ S列
    forecast_category_name = fields.Char('ForecastCategoryName')  # 予測カテゴリ名 T列
    campaign_id = fields.Char('CampaignId')  # キャンペーンId U列
    # has_opportunity_line_item = fields.Char('HasOpportunityLineItem')  # 段階名 V列
    # price_book2_id = fields.Char('Pricebook2Id')  # 段階名 W列
    owner_id = fields.Many2one('res.users', 'OwnerId')  # 所有者Id X列 1
    created_date = fields.Datetime('CreatedDate')  # 作成日 Y列
    created_by_id = fields.Many2one('res.users', 'CreatedById')  # 作成ID Z列
    last_modified_date = fields.Datetime('LastModifiedDate')  # 最終更新日
    last_modified_by_id = fields.Many2one('res.users', 'LastModifiedById')  # 最終更新者
    system_mod_stamp = fields.Datetime('SystemModstamp')  # システム最終更新日
    last_activity_date = fields.Datetime('LastActivityDate')  # システム最終活動日
    last_stage_changed_date = fields.Datetime('LastStageChangeDate')  # 最終ステージ変更日
    fiscal_year = fields.Integer('FiscalYear')  # 会計年度
    fiscal_quarter = fields.Integer('FiscalQuarter')  # 会計四半期
    contact_id = fields.Many2one('res.partner', 'ContactId')  # コンタクトId
    primary_partner_Account_id = fields.Char('PrimaryPartnerAccountId')  # プライマリーパートナーId
    # synced_quote_id = fields.Char('SyncedQuoteId')  # 同期引用Id
    contract_id = fields.One2many('contract.contract', inverse_name="related_opportunity", string='ContractId')  # 契約Id
    last_amount_changed_history_id = fields.Char('LastAmountChangedHistoryId')  # 最終金額変更履歴
    last_close_date_changed_history_id = fields.Char('LastCloseDateChangedHistoryId')  # 最終完了日変更履歴
    progress_check_date = fields.Datetime('Field1__c')  # 進捗確認日 AN列
    quote_number_by_hukusuke = fields.Char('Field2__c')  # 福助で採番される見積番号 AO列
    quote_number = fields.Char('Field3_del__c')  # 見積番号 AP列
    previous_amount = fields.Float('previousamount__c')  # 直前の金額 AQ列
    opportunity_number = fields.Char('Field4__c')  # 商談番号 AR列　
    last_amount_changed_datetime = fields.Datetime('lastamountchangedatetime__c')  # 最終金額変更日時 AS列
    presentation = fields.Integer('presentation__c')  # 通常プレゼン AT列 ★0，1，空白あり
    project_details = fields.Text('Field60__c')  # 案件詳細 AU列
    Determined_on_the_day = fields.Boolean('Determinedontheday__c', default=0)  # 当日確定 AV列 ★0，1，空白あり
    delivery_date_unknown = fields.Boolean('Field5__c', default=0)  # 納期不明 AW列 ★0，1，空白あり
    delivery_type = fields.Char('Field6__c')  # 納入先種別 AX列
    order_amount = fields.Float('Field7__c')  # 受注額 AY列
    omotesando_visit = fields.Boolean('Field87__c', default=0)  # 表参道来店 AZ列 ★0，1，空白あり
    fair = fields.Char('Field22__c')  # Fair BA列
    million_amount = fields.Float('X100_amount__c')  # 100万金額 BB列
    million_order_amount = fields.Float('X100_amount_a__c')  # 100万受注額 BC列
    competition_a = fields.Char('Field16__c')  # 競合A BD列
    fair_advance_plan = fields.Boolean('Field34_plan__c', default=0)  # フェア事前プラン BE列 ★0，1，空白あり
    product_others = fields.Char('Field14__c')  # 商品その他（補足） BF列
    our_strengths = fields.Text('Field30__c')  # 自社の強み BG列
    million_order_count = fields.Boolean('X100_count_a__c', default=0)  # 100万受注数 BH列 ★0，1，空白あり
    total_million_order_count = fields.Boolean('X100_count__c', default=0)  # 100万総数 BI列 ★0，1，空白あり
    Use_Purpose = fields.Text('Field61__c')  # 使用用途(その他） BJ列
    reason_selection = fields.Text('Field62__c')  # 選定理由 BK列
    Use_Purpose1 = fields.Char('Field63_purpose__c')  # 使用用途① BL列
    Use_Purpose2 = fields.Char('Field64_purpose__c')  # 使用用途② BM列
    Use_Purpose3 = fields.Char('Field65_purpose__c')  # 使用用途③ BN列
    other = fields.Boolean('ITEM_other_08__c', default=0)  # その他 BO列 ★0，1，空白あり
    ac = fields.Boolean('CHAI_2__c', default=0)  # AC BP列 ★0，空白あり
    website = fields.Char('WEB__c')  # WEBサイト BQ列
    competitive_reason = fields.Text('Field31__c')  # 競合理由 BR列
    order_no = fields.Char('NO__c')  # 受注NO BS列
    facility_name = fields.Char('Field64__c')  # 施設名 BT列
    competition_other = fields.Char('Field17__c')  # 競合（その他） BU列
    competitive_product_d = fields.Char('Field18__c')  # 競合商品(D) BV列
    competitive_product_name = fields.Char('Field19__c')  # 競合商品名 BW列
    competitive_product_l = fields.Char('L__c')  # 競合商品(L) BX列
    competitive_product_other = fields.Char('Field20__c')  # 競合商品（他） BY列
    other_strengths = fields.Text('Field21__c')  # 他社の強み BZ列
    competition_b = fields.Char('B__c')  # 競合B CA列
    campaign = fields.Char('Field65__c')  # キャンペーン CB列
    product_list_other = fields.Char('Field68__c')  # 商品リスト（その他） CC列
    action1 = fields.Char('Field23__c')  # アクション① CD列
    memo = fields.Text('Field35_del__c')  # メモ CE列
    branch = fields.Char('Branch__c')  # Branch CF列
    action2 = fields.Char('Field24__c')  # アクション② CG列
    last_event_comment = fields.Text('LastEventComment__c')  # 最終行動コメント CH列
    diana_count = fields.Float('DIANA__c')  # DIANA台数 CI列
    sample_sale = fields.Char('Field25__c')  # サンプル販売 CJ列
    sample_sales_amount = fields.Integer('Field26__c')  # サンプル販売金額 CK列
    push_c = fields.Float('Push_Counter__c')  # Push C(完了予定日を翌月以降に変更した回数をカウント) CL列
    area = fields.Char('Field32_del__c')  # エリア CM列
    pre_contract_presentation = fields.Integer('Field34_plan2__c')  # 契約前プレゼン CN列
    overlap = fields.Char('Field34__c')  # Overlap CO列
    memo_other = fields.Char('Field28__c')  # メモ（台数など） CP列
    product_list_rug = fields.Char('Field70__c')  # 商品リスト（ラグ） CQ列
    product_list_dt2 = fields.Char('Dt2__c')  # 商品リスト(Dt2) CR列
    product_list_dt1 = fields.Char('Dt1__c')  # 商品リスト(Dt1) CS列
    product_list_lt2 = fields.Char('Lt2__c')  # 商品リスト(Lt2) CT列
    fair_Year = fields.Datetime('Field33__c')  # フェア開催年 CU列
    product_list_lt1 = fields.Char('Lt1__c')  # 商品リスト(Lt1) CV列
    product_list_ec1 = fields.Char('EC1__c')  # 商品リスト(EC1) CW列
    product_list_ec2 = fields.Char('EC2_2__c')  # 商品リスト(EC2) CX列
    l_set = fields.Integer('Lset__c')  # Lセット CY列
    product_list_st2 = fields.Char('St2__c')  # 商品リスト(St2) CZ列
    product_list_st1 = fields.Char('St1__c')  # 商品リスト(St1) DA列
    opportunity_completion_date = fields.Datetime('Field72__c')  # 商談完了日 DB列
    product_list_ot_st1 = fields.Char('ST1_1__c')  # 商品リスト(OT/ST1) DC列
    term = fields.Char('Term__c')  # Term DD列
    product_list_ot_st2 = fields.Char('ST2_2__c')  # 商品リスト(OT/ST2) DE列
    product_list_board1 = fields.Char('BOARD1__c')  # 商品リスト(BOARD1) DF列
    product_list_board2 = fields.Char('BOARD2__c')  # 商品リスト(BOARD2) DG列
    year = fields.Integer('Year__c')  # Year DH列
    product_list_sofa3 = fields.Char('X3__c')  # 商品リスト(ソファ3) DI列
    completion_scheduled_date = fields.Datetime('A__c')  # 完了予定日（A) DJ列
    product_list_sofa1 = fields.Char('X1__c')  # 商品リスト(ソファ1) DK列
    product_list_sofa2 = fields.Char('X2_2__c')  # 商品リスト(ソファ2) DL列
    product_list_ec3 = fields.Char('EC3__c')  # 商品リスト(EC3) DM列
    product_list_chair1 = fields.Char('Field29__c')  # 商品リスト(ﾁｪｱ1) DN列
    product_list_chair2 = fields.Char('X2_5__c')  # 商品リスト(ﾁｪｱ2) DO列
    product_list_chair3 = fields.Char('X3_4__c')  # 商品リスト(ﾁｪｱ3) DP列
    product_list_chair4 = fields.Char('X4_1__c')  # 商品リスト(ﾁｪｱ4) DQ列
    progress_check = fields.Text('Field36__c')  # 進捗確認/経過報告 DR列
    opportunity_type = fields.Char('Field37__c')  # 商談種別 DS列
    accuracy = fields.Float('Field38__c')  # 確度（変更前） DT列
    last_accuracy_changed_date = fields.Datetime('Field39__c')  # 最終確度変更日時 DU列
    result = fields.Char('Field40__c')  # 結果 DV列
    On_site_delivery_date = fields.Datetime('Field43__c')  # 現場納品日 DW列
    beatrix_count = fields.Float('BEATRIX_count__c')  # BEATRIX台数 DX列
    jabara_count = fields.Float('JABARA__c')  # JABARA台数 DY列
    lf_set_count = fields.Float('LF__c')  # LFセット数 DZ列
    product_list_sofa_ot1 = fields.Char('Sofa_OT__c')  # 商品リスト(ソファOT1) EA列
    product_list_sofa_ot2 = fields.Char('OT2__c')  # 商品リスト(ソファOT2) EB列
    rate = fields.Float('Field74__c')  # 掛率 EC列
    dummy = fields.Boolean('Field75__c', default=0)  # ﾀﾞﾐｰ ED列
    lw_set_count = fields.Float('LW_5__c')  # LWセット数 EE列
    trw_candidate = fields.Boolean('TRW__c', default=0)  # TRW候補 EF列
    questionnaire = fields.Boolean('Field50__c', default=0)  # アンケート EG列
    letter_of_acceptance = fields.Boolean('Field51__c', default=0)  # 承諾書 EH列
    how_to_get_photos = fields.Char('Field52__c')  # 写真入手方法 EI列
    memo_trw = fields.Text('TRW_2__c')  # TRWメモ EJ列
    examination = fields.Char('Field53__c')  # 審査 EK列
    cost = fields.Integer('Field54__c')  # 経費 EL列
    photographer = fields.Char('Field55__c')  # Photographer EM列
    shooting_date = fields.Datetime('Field56__c')  # 撮影日 EN列
    installation_floor = fields.Char('Field57__c')  # 設置階 EO列
    delivery_route_required_confirmation = fields.Boolean('Field58__c', default=0)  # 搬入経路要確認 EP列
    elevator_having = fields.Boolean('EV__c', default=0)  # EV有 EQ列
    budget_data = fields.Boolean('SFDC_Budget__c', default=0)  # 予算データ ER列
    lost = fields.Float('Field59__c')  # ロスト ES列
    p_author = fields.Char('P__c')  # P作成者(代表） ET列
    product_list_sofa_bench1 = fields.Char('Bench1__c')  # 商品リスト（Bench1) EU列
    product_list_sofa_bench2 = fields.Char('Bench2__c')  # 商品リスト（Bench2) EV列
    procurement_company = fields.Char('Field77__c')  # 調達会社 EW列
    address_no = fields.Char('Field78__c')  # 〒 EX列
    address = fields.Char('Field79__c')  # 住所 EY列
    tel = fields.Char('Field80__c')  # 電話 EZ列
    person_name = fields.Char('Field81__c')  # 名前 FA列
    furigana = fields.Char('Field82__c')  # フリガナ FB列
    depot = fields.Char('Field83__c')  # デポ FC列
    depot_arrival_date = fields.Datetime('Field84__c')  # デポ着日 FD列
    to_arrangement_depot = fields.Boolean('Field85__c', default=0)  # 手配デポまで FE列
    special_remarks = fields.Text('Field86__c')  # Photographer FF列

#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
