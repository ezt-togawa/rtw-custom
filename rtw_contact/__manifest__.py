# -*- coding: utf-8 -*-
{
    'name': "rtw_contact",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose""",

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
    'depends': ['base', 'contacts', 'sale','rtw_sf','sale_order_type'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/sale_order.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        
    ],
}
