# -*- coding: utf-8 -*-

{
    'name': "custom_chatter",
    'author': "Enzantrades",
    'category': 'mail',
    'summary': """
        OCAモジュール mail_restrict_send_button の不備対応：chater.js の更新
        →不要として未使用とする。OCA側の「mail_restrict_send_button」からchater.js自体を使わなくするように変更。
        """,
    'website': 'http://www.yourcompany.com',
    'description': """
""",
    'version': '14.0.0.0',
    'depends': ['base','mail','mail_restrict_send_button'],
    'data': [
        'views/template.xml'
    ],
}
