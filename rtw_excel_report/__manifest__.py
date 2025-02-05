# -*- coding: utf-8 -*-
{
    'name': "rtw_excel_report",

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
    'depends': ['base', 'excel_import_export', 'sale_management', 'sale','sale_sourced_by_line','product','purchase','stock_move_container','stock_move_pallet'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/proforma.xml',
        'report/report.xml',
        # 'report_quotation/actions.xml',
        # 'report_quotation/templates.xml',
        # 'report_quotation_oversea/actions.xml',
        # 'report_quotation_oversea/templates.xml',
        # 'report_list_price_quotation/actions.xml',
        # 'report_list_price_quotation/templates.xml',
        # 'report_unit_price_quotation/actions.xml',
        # 'report_unit_price_quotation/templates.xml',
        # 'report_invoice/actions.xml',
        # 'report_invoice/templates.xml',
        # 'report_invoice_sale_order/actions.xml',
        # 'report_invoice_sale_order/templates.xml',

        # 'report_purchase_order/actions.xml',
        # 'report_purchase_order/templates.xml',

        # 'report_purchase_order_sheet/actions.xml',
        # 'report_purchase_order_sheet/templates.xml',
        # 'report_inspection_order_form/actions.xml',
        # 'report_inspection_order_form/templates.xml',

        # 'report_purchase_order_for_part/actions.xml',
        # 'report_purchase_order_for_part/templates.xml',
        # 'report_delivery_request_form/actions.xml',
        # 'report_delivery_request_form/templates.xml',
        # 'report_ship_order/actions.xml',
        # 'report_ship_order/templates.xml',
        'views/views.xml',
        # sale form
        'views/sale_quotation.xml',
        'views/sale_quotation_oversea.xml',
        'views/sale_list_price_quotation.xml',
        'views/sale_unit_price_quotation.xml',
        'views/sale_order_form.xml',
        'views/sale_list_order_form.xml',
        'views/sale_product_spec.xml',
        'views/sale_delivery.xml',
        'views/sale_invoice.xml',

        # picking
        'views/picking_delivery_order.xml',      #form
        'views/picking_ship_order.xml',          #form 
        #picking
        'views/picking_scheduled_supply_list.xml',  #支給予定リスト list
        'views/picking_scheduled_arrival_list.xml', #入荷予定リスト list
        'views/picking_scheduled_shipment_list.xml',#出荷予定リスト list
        
        'views/picking_supplied_parts_details.xml',#支給部材明細       form
        'views/picking_inspection_check_sheet.xml', #検品チェックシート  form
        'views/picking_shipping_form_seal.xml',         #送り状シール       form

        # invoice
        'views/account_invoice.xml',

        # purchase order
        'views/purchase_order_component.xml',     #list,form

        # mrp
        'views/mrp_purchase_order.xml',           #form
        'views/mrp_purchase_order_inspection.xml',#form
        
        'views/mrp_product_label_seal.xml',       #list,form
        'views/mrp_wip_product_list.xml',         #list,form
        
        #stock quant 
        'views/stock_quant_inventory_entry_list.xml',
        
        #product template
        'views/prod_tmpl_inventory_status_list.xml',
        
        'views/stock_move_pallet.xml',
        
        # 'report_stock_move_pallet/actions.xml',
        # 'report_stock_move_pallet/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
