# -*- coding: utf-8 -*-
{
    'name': "rtw_stock_move_line",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'product', 'product_spec_rtw', 'sale', 'sale_order_line_custom_date', 'sale_order_rtw','stock_picking_delivery_information','stock_picking_batch'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_move.xml',
        'views/sale_order.xml',
        'views/templates.xml',
        'views/stock_picking.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
