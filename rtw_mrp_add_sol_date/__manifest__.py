# -*- coding: utf-8 -*-
{
    'name': "rtw_mrp_add_sol_date",

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
    'category': '',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp','sales_mo_sequence', 'sale_order_rtw'],

    # always loaded
    'data': [
        'views/mrp_production.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
