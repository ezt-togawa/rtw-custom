# -*- coding: utf-8 -*-
from random import randint

from odoo import models, fields


class MrpProductionTag(models.Model):
    _name = 'mrp.production.tag'
    _description = '製造タグ'
    _order = 'name'

    name = fields.Char(string='製造タグ', required=True)
    color = fields.Integer(string='色', default=lambda self: randint(1, 11))
    active = fields.Boolean(string='有効', default=True,
                            help="無効（アーカイブ）にすると、既存の製造オーダーには表示が残り、新たな指定はできなくなります。")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'タグ名は既に存在します。'),
    ]
