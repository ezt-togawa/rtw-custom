# -*- coding: utf-8 -*-
{
    'name': "rtw_mrp_holiday",
    'summary': "製造休日マスタ、製造・作業カレンダーの休日表示と警告",
    'author': "Enzantrades",
    'category': 'Manufacturing',
    'version': '14.0.1.0.0',
    'depends': ['mrp', 'rtw_update_mrp_workorder'],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_holiday.xml',
        'views/mrp_production.xml',
        'views/mrp_workorder.xml',
        'views/templates.xml',
    ],
    'installable': True,
}
