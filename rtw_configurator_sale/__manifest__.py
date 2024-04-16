# -*- coding: utf-8 -*-
{
    'name': "rtw_configurator_sale",

    'summary': """
        Custom OCA <product_configurator_sale>""",

    'description': """
        Long description of module's purpose
    """,
    
     'author': "Enzantrades",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['product_configurator_sale'],

    # always loaded
    'data': [
        'views/product_configurator.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        
    ],
}
