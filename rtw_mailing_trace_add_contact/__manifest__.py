# -*- coding: utf-8 -*-
{
    'name': "rtw_mailing_trace_add_contact",

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
    'depends': ['base', 'contacts', 'sale','mass_mailing','rtw_sf','contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/mailing_trace.xml',
        'views/mailing_hide_display_name_res_partner.xml',
        'views/contact.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
