# -*- coding: utf-8 -*-

{
    'name': "Collective Shipping",
    'author': "My Company",
    'category': 'stock',
    'summary': """Collective Shipping""",
    'website': 'http://www.yourcompany.com',
    'description': """
""",
    'version': '14.0.0.0',
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/collective_shipping_wizard_view.xml',
        'views/templates.xml',
    ],
}
