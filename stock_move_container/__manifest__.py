# -*- coding: utf-8 -*-

{
    'name': "Stock Move Container",
    'author': "My Company",
    'category': 'stock',
    'summary': """Stock Move Container""",
    'website': 'http://www.yourcompany.com',
    'description': """
""",
    'version': '14.0.0.0',
    'depends': ['base', 'stock', 'rtw_stock_move_line', 'stock_move_pallet'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/stock_move_container_wizard_view.xml',
        'views/stock_move.xml',
        'views/stock_move_pallet.xml',
        'views/stock_move_container.xml',
        'views/stock_picking.xml',
        'views/templates.xml',
        'data/container_sequence.xml',
    ],
}
