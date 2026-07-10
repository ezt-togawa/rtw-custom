# -*- coding: utf-8 -*-
{
    'name': "rtw_recreate",

    'summary': """
        This module is designed to re-create sales and manufacturing data.
        It covers related manufacturing, purchasing, and shipping processes.""",

    'description': """
        販売と製造の再作成を行う、紐づく製造/購買/運送が対象
    """,

    'author': "Enzantrades",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'mrp', 'mrp_production_back_to_draft', 'sale_stock'],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'views/mrp_production.xml',
        'views/sale_order.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
