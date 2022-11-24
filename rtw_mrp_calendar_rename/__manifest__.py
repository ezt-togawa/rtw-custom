# -*- coding: utf-8 -*-
{
    'name': "rtw_mrp_calendar_rename",

    'summary': """
        workcenter_line_calendar title rename""",

    'description': """
        workcenter_line_calendar title rename
    """,

    'author': "Leverage",
    'website': "https://leverage-system.jp",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
