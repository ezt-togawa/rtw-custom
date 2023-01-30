# -*- coding: utf-8 -*-

import datetime
from odoo import models, fields, api


class calendar_event_rtw(models.Model):
    _inherit = 'calendar.event'

    sr = fields.Many2one('calendar.sr', 'SR__c')  # SR AY
    new_sales = fields.Boolean('new_customer_2__c')  # 新規営業 AZ ★0,1,空白
    situation = fields.Selection([
        ('0', '---なし---'),
        ('1', '予定'),
        ('2', '調整中'),
        ('3', 'アポ済'),
        ('4', '完了'),
        ('5', 'キャンセル'),
    ], default="0", string='Field1__c')  # 状況 AX
    # SR来場情報
    reservation = fields.Selection([
        ('1', '---なし---'),
        ('2', '事前予約'),
        ('3', '当日予約'),
        ('4', '予約なし'),
    ], default="1", string='Field20__c')  # 予約 BN
    estimate_flg = fields.Boolean('Field19__c')  # 事前提案・見積り有 BM ★0,1,空白
    visitor_type = fields.Selection([
        ('1', '---なし---'),
        ('2', '一般ユーザー'),
        ('3', 'ユーザー+取引先'),
        ('4', '取引先(IC・設計)'),
        ('5', '取引先(販売店他)'),
        ('6', 'オーナー（法人）'),
        ('7', 'オーナー+取引先'),
        ('8', 'メディア'),
        ('9', '業者'),
        ('10', 'その他'),
    ], default="1", string='Field18__c')  # 来場者タイプ BL
    visitor_set_count = fields.Integer('Field11__c')  # 来場組数 BF
    visitor_count = fields.Integer('Field10__c')  # 来場人数 BC
    lead = fields.Selection([
        ('1', '---なし---'),
        ('2', '紹介（IC・設計）'),
        ('3', '紹介（ショップ・販売店）'),
        ('4', '紹介(知人)'),
        ('5', '施主指定'),
        ('6', 'DM・ニュースレター'),
        ('7', '雑誌・広告'),
        ('8', 'SNS'),
        ('9', 'TABROM'),
        ('10', 'カタログギフト'),
        ('11', 'ふるさと納税'),
        ('12', 'G住宅ﾎﾟｲﾝﾄ'),
        ('13', '展示場・納入先'),
        ('14', 'WEB検索サイト'),
        ('15', '他SRから'),
        ('16', '再来場'),
        ('17', 'Rオーナー(追加・リピート)'),
        ('18', 'Rオーナー(アフター）'),
        ('19', '通りがかり'),
        ('20', '回答なし'),
        ('21', '未確認/声かけのみ'),
        ('22', 'R営業誘致（営業活動）'),
        ('23', 'ミラノサローネ'),
        ('25', '広報 (PR)'),
        ('26', '通常営業'),
        ('27', '紹介（知人・外部）'),
        ('24', 'その他'),
    ], default="1", string='Field17__c')  # リード（来場） BK
    visitor_purpose = fields.Selection([
        ('1', '---なし---'),
        ('2', '見学（全体確認）'),
        ('3', '購入検討（プランニング）'),
        ('4', '購入検討（選定内容確認）'),
        ('5', '購入（注文・支払い）'),
        ('6', '追加購入'),
        ('7', 'アフター・メンテ'),
        ('8', '打合せ（プランニング）'),
        ('9', '打合せ（その他）'),
        ('10', 'SRフェア'),
        ('11', 'イベント'),
        ('12', '勉強会'),
        ('13', '立ち寄り'),
        ('14', '営業'),
        ('15', '取材など'),
        ('16', 'その他'),
    ], default="1", string='Field16__c')  # 来場目的 BJ
    guest_book = fields.Selection([
        ('0', '---なし---'),
        ('1', '取得済'),
        ('2', '未記入'),
    ], default="0", string='Field30__c')  # 芳名帳/アンケート BQ
    estimated_accrual = fields.Boolean('Field31__c')  # 見積発生（新規商談） BR ★0,1,空白
    payment_method = fields.Boolean('Field26__c')  # クレジット/現金購入 BI ★0,1,空白
    omotesando = fields.Boolean('Field35__c')  # 表参道来店 BS ★0,1,空白
    customer_service_staff = fields.Many2one('res.users')  # 接客担当 BD
    r_uid = fields.Many2one('res.users', '担当者')  # 接客担当 BD
    created_date = fields.Datetime('CreatedDate')  # 作成日 W列
    created_by_id = fields.Many2one('res.users', 'CreatedById')  # 作成ID X列
    last_modified_date = fields.Datetime('LastModifiedDate')  # 最終更新日 Y列
    last_modified_by_id = fields.Many2one('res.users', 'LastModifiedById')  # 最終更新者 Z列
    system_mod_stamp = fields.Datetime('SystemModstamp')  # システム最終更新日 AA列
    short_description = fields.Char(compute="_get_sort_description")
    campaign = fields.Many2one("utm.campaign")
    crm_date_deadline = fields.Date(related="opportunity_id.date_deadline")
    currency_id = fields.Many2one('res.currency', compute='_get_currency_id')
    crm_expected_revenue = fields.Monetary(related="opportunity_id.expected_revenue")
    crm_stage_id = fields.Many2one(related="opportunity_id.stage_id")
    crm_r_id = fields.Many2one(related="opportunity_id.user_id")

    def _get_currency_id(self):
        for rec in self:
            rec.currency_id = rec.env.ref('base.main_company').currency_id

    def _get_sort_description(self):
        for rec in self:
            if rec.description:
                rec.short_description = rec.description
            else:
                rec.short_description = False
    
    @api.model
    def _get_public_fields(self):
        res = super()._get_public_fields()
        res.update(
            {'sr'}
        )
        return res

    @api.onchange('sr', 'situation', 'start')
    def _crm_set(self):
        for rec in self:
            if rec.opportunity_id:
                rec.opportunity_id.last_event = rec.start
                rec.opportunity_id.event_showroom = rec.sr.name
                rec.opportunity_id.event_situations = dict(rec._fields['situation'].selection).get(rec.situation)

