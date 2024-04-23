# -*- coding: utf-8 -*-
{
    'name': "rtw_mrp_order_manage",

    'summary': """
        Manage the order status of production orders.""",

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
    'depends': ['base', 'mrp', 'sale_order_crm_case'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_order_manage.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
