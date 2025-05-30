# -*- coding: utf-8 -*-
{
    'name': "rtw_popup_set_item_location_prod_label_excel",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Enzantrades",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp','rtw_stock_move_line'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/location_item_excel_prod_label.xml',
        'views/stock_move.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
