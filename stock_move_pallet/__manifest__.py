# -*- coding: utf-8 -*-

{
    'name': "Stock Move Pallet",
    'author': "My Company",
    'category': 'stock',
    'summary': """Stock Move Pallet""",
    'website': 'http://www.yourcompany.com',
    'description': """
""",
    'version': '14.0.0.0',
    'depends': ['base', 'stock', 'rtw_stock_move_line'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/stock_move_pallet_wizard_view.xml',
        'views/stock_move_pallet.xml',
        'views/stock_move_line.xml',
        'views/templates.xml',
    ],
}
