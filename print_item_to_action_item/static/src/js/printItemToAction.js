odoo.define('print_item_to_action_item.ChangeProp', function (require) {

    const { patch } = require('web.utils');
    const components = { ActionMenus: require('web.ActionMenus') };

    var data_delivery_receipt_list = null;
    var data_delivery_receipt_form = null;

    var data_sale_order_list = null;
    var data_sale_order_form = null;

    var data_account_move_list = null;

    var data_manufacture_list = null;
    var data_manufacture_form = null;

    var data_reporting_list = null;

    var data_purchase_list = null;

    var data_template_form = null;

    patch(components.ActionMenus, 'print_item_to_action_item.ChangeProp', {
        async willStart() {
            return this._super(...arguments).then(() => {
                return this._loadData();
            });
        },

        async willUpdateProps(nextProps) {
            return this._super(nextProps).then(() => {
                return this._updateData(nextProps);
            });
        },
        async _loadData() {
            let view_type_now = this.env.view.type
            if (view_type_now === 'list') {
                if (this.env.view.model == "stock.picking") {
                    if (data_delivery_receipt_list === null) {
                        data_delivery_receipt_list = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let action = [...data_delivery_receipt_list.action]
                    let prints = [...data_delivery_receipt_list.print]

                    // task_inventory_delivery_list = ["出荷予定リスト"]  inventory_receipt_list = ["支給予定リスト", "入荷予定リスト"]
                    let excel = ["出荷予定リスト(EXCEL)", "支給予定リスト(EXCEL)", "入荷予定リスト(EXCEL)"]
                    let isExcelTemplate2AtAction = action.some(val => excel.includes(val.display_name));
                    if (isExcelTemplate2AtAction) {
                        this.props.items.action = action.filter(val => val.display_name !== "検品チェックシート(EXCEL)" && val.display_name !== "送り状シール(EXCEL)" && val.display_name !== "支給部材明細(EXCEL)");
                    } else {
                        let excelArray = prints.filter(val => {
                            if (excel.includes(val.display_name)) {
                                val.name = val.name.split("(")[0]
                                val.type = 'ir.actions.act_window'
                                val.binding_type = 'action'
                                return val
                            }
                        })
                        this.props.items.action = [...action, ...excelArray];
                    }
                    
                    hidePrint = ['配送作業依頼書', '出荷依頼書','Delivery Slip','配送伝票']
                    this.props.items.print = prints.filter(val => !val.display_name.includes('(EXCEL)') && !hidePrint.includes(val.name))
                }

                // sale_order_view_list
                if (this.env.view.model == "sale.order") {

                    if (data_sale_order_list === null) {
                        data_sale_order_list = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let action = [...data_sale_order_list.action]
                    let prints = [...data_sale_order_list.print]
                    hidePrint = ["Quotation / Order", "見積 / オーダ", "商品仕様書(EXCEL)", "御見積書", "定価見積書", "単価見積り書", "注文書", "商品仕様書", "御見積書（海外）"]
                    this.props.items.print = prints.filter(val => !hidePrint.includes(val.name))
                    this.props.items.action = [...action]
                }

                // task_invoice_list
                if (this.env.view.model == "account.move") {

                    if (data_account_move_list === null) {
                        data_account_move_list = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let action = [...data_account_move_list.action]
                    let prints = [...data_account_move_list.print]

                    hidePrint = ["Invoices", "Original Bills", "Invoices without Payment", "Multiple Invoice Copies","invoice", "Invoice", "請求書", "未払請求書", "オリジナル手形"]
                    this.props.items.print = prints.filter(val => !hidePrint.includes(val.name))
                }

                // task_inventory_manfac_list = ["仕掛品伝票一覧"]
                if (this.env.view.model == "mrp.production") {
                    if (data_manufacture_list === null) {
                        data_manufacture_list = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let action = [...data_manufacture_list.action]
                    let prints = [...data_manufacture_list.print]
                    let excel = ["仕掛品伝票一覧(EXCEL)", "商品ラベルシール(EXCEL)"]
                    let excelArray = prints.filter(val => {
                        if (excel.includes(val.display_name)) {
                            val.name = val.name.split("(")[0]
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        }
                    })
                    this.props.items.action = [...action, ...excelArray];
                    hidePrint = ["仕掛品伝票一覧", "商品ラベルシール", "発注書", "Production Order", "製造オーダ"]
                    this.props.items.print = prints.filter(val => !hidePrint.includes(val.name));
                }

                // task_inventory_reporting = ["棚卸記入リスト"]
                if (this.env.view.model == "stock.quant") {
                    if (data_reporting_list === null) {
                        data_reporting_list = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let action = [...data_reporting_list.action]
                    let prints = [...data_reporting_list.print]

                    let excel = ["棚卸記入リスト(EXCEL)"]
                    let excelArray = prints.filter(val => {
                        if (excel.includes(val.display_name)) {
                            val.name = val.name.split("(")[0]
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        }
                    })
                    this.props.items.action = [...action, ...excelArray];
                    this.props.items.print = prints.filter(val => !val.display_name.includes('(EXCEL)'));
                }

                // task_purchase_order_for_part = ["発注書(部材用）"]
                if (this.env.view.model == "purchase.order") {
                    if (data_purchase_list === null) {
                        data_purchase_list = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let prints = [...data_purchase_list.print]
                    this.props.items.print = prints.filter(val => val.display_name !== "発注書(部材用）");
                }
            }

            if (view_type_now === 'form') {
                // sale_order_view_form
                if (this.env.view.model === "sale.order") {
                    if (data_sale_order_form === null) {
                        data_sale_order_form = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let action = [...data_sale_order_form.action]
                    let prints = [...data_sale_order_form.print]

                    let excel = prints.filter(val => {
                        if (val.display_name === "商品仕様書(EXCEL)") {
                            val.name = val.name.split("(")[0]
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        }
                    })
                    this.props.items.action = [...action, ...excel]
                    hidePrint = ["Quotation / Order", "見積 / オーダ", "商品仕様書(EXCEL)"]
                    this.props.items.print = prints.filter(val => !hidePrint.includes(val.name))
                }

                // task_invoice_form
                if (this.env.view.model == "account.move") {

                    if (data_account_move_list === null) {
                        data_account_move_list = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let action = [...data_account_move_list.action]
                    let prints = [...data_account_move_list.print]
                    console.log('>>>>>>>>>>>>>>>>>', this.props.items);

                    hidePrint = ["Invoices", "Original Bills", "Invoices without Payment", "Multiple Invoice Copies", "invoice", "Invoice", "未払請求書", "オリジナル手形"]
                    this.props.items.print = prints.filter(val => !hidePrint.includes(val.name) && val.report_name === "custom_report_rtw.report_invoice_3")
                }

                // task_inventory_manfac_form= ["商品ラベルシール"]
                if (this.env.view.model === "mrp.production") {
                    if (data_manufacture_form === null) {
                        data_manufacture_form = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }

                    let action = [...data_manufacture_form.action]
                    let prints = [...data_manufacture_form.print]

                    let excel = prints.filter(val => {
                        if (val.display_name === "商品ラベルシール(EXCEL)") {
                            val.name = val.name.split("(")[0]
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        }
                    })
                    this.props.items.action = [...action, ...excel]
                    this.props.items.print = prints.filter(val => !val.display_name.includes('(EXCEL)') && val.name !== "Production Order" && val.name !== "製造オーダ")
                }

                // task_template = ["在庫状況一覧"]
                if (this.env.view.model === "product.template") {
                    if (data_template_form === null) {
                        data_template_form = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }

                    let action = [...data_template_form.action]
                    let prints = [...data_template_form.print]

                    let excel = prints.filter(val => {
                        if (val.display_name === "在庫状況一覧(EXCEL)") {
                            val.name = val.name.split("(")[0]
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        }
                    })
                    this.props.items.action = [...action, ...excel]

                    this.props.items.print = prints.filter(val => !val.display_name.includes('(EXCEL)'));
                }
                if (this.env.view.model === "stock.picking") {
                    // task_inventory_delivery_form = ["送り状シール(EXCEL)","支給部材明細(EXCEL)"] +recept
                    if (data_delivery_receipt_form === null) {
                        data_delivery_receipt_form = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let action = [...data_delivery_receipt_form.action]
                    let prints = [...data_delivery_receipt_form.print]
                    let excel = ["送り状シール(EXCEL)", "支給部材明細(EXCEL)", "検品チェックシート(EXCEL)"]
                    let isExcelTemplate2AtAction = action.some(val => excel.includes(val.display_name));
                    if (isExcelTemplate2AtAction) {
                        this.props.items.action = action.filter(val => val.display_name !== "出荷予定リスト(EXCEL)" && val.display_name !== "支給予定リスト(EXCEL)" && val.display_name !== "入荷予定リスト(EXCEL)");
                    } else {
                        let excelArray = prints.filter(val => {
                            if (excel.includes(val.display_name)) {
                                val.name = val.name.split("(")[0]
                                val.type = 'ir.actions.act_window'
                                val.binding_type = 'action'
                                return val
                            }
                        })
                        this.props.items.action = [...action, ...excelArray];
                    }
                    hidePrint = ['Delivery Slip','配送伝票']
                    this.props.items.print = prints.filter(val => !val.display_name.includes('(EXCEL)') && !hidePrint.includes(val.name) )
                }
            }
            this.actionItems = await this._setActionItems(this.props);
            this.printItems = await this._setPrintItems(this.props);
        },

        async _updateData(nextProps) {
            let view_type_now = this.env.view.type
            if (view_type_now === "list") {
                if (this.env.view.model == "stock.picking") {
                    let action = [...data_delivery_receipt_list.action]
                    let prints = [...data_delivery_receipt_list.print]

                    // task_inventory_delivery_list = ["出荷予定リスト"]  inventory_receipt_list = ["支給予定リスト", "入荷予定リスト"]
                    let excel = ["出荷予定リスト(EXCEL)", "支給予定リスト(EXCEL)", "入荷予定リスト(EXCEL)"]
                    let isExcelTemplate2AtAction = action.some(val => excel.includes(val.display_name));
                    if (isExcelTemplate2AtAction) {
                        nextProps.items.action = action.filter(val => val.display_name !== "検品チェックシート(EXCEL)" && val.display_name !== "送り状シール(EXCEL)" && val.display_name !== "支給部材明細(EXCEL)");
                    } else {
                        let excelArray = prints.filter(val => {
                            if (excel.includes(val.display_name)) {
                                val.name = val.name.split("(")[0]
                                val.type = 'ir.actions.act_window'
                                val.binding_type = 'action'
                                return val
                            }
                        })
                        nextProps.items.action = [...action, ...excelArray];
                    }
                    hidePrint = ['配送作業依頼書', '出荷依頼書','Delivery Slip','配送伝票']
                    nextProps.items.print = prints.filter(val => !val.display_name.includes('(EXCEL)') && !hidePrint.includes(val.name))
                }

                // let task_sale_order_list
                if (this.env.view.model == "sale.order") {
                    let action = [...data_sale_order_list.action]
                    let prints = [...data_sale_order_list.print]
                    hidePrint = ["Quotation / Order", "見積 / オーダ", "商品仕様書(EXCEL)", "御見積書", "定価見積書", "単価見積り書", "注文書", "商品仕様書", "御見積書（海外）"]
                    nextProps.items.print = prints.filter(val => !hidePrint.includes(val.name))
                    nextProps.items.action = [...action]
                }

                // let task_invoice_list
                if (this.env.view.model == "account.move") {
                    let prints = [...data_account_move_list.print]

                    hidePrint = ["Invoices", "Original Bills", "Invoices without Payment", "Multiple Invoice Copies","invoice", "Invoice", "請求書", "未払請求書", "オリジナル手形"]
                    nextProps.items.print = prints.filter(val => !hidePrint.includes(val.name))
                }

                // let task_manfac_list = ["仕掛品伝票一覧"]
                if (this.env.view.model == "mrp.production") {

                    let action = [...data_manufacture_list.action]
                    let prints = [...data_manufacture_list.print]

                    let excel = ["仕掛品伝票一覧(EXCEL)", "商品ラベルシール(EXCEL)"]
                    let excelArray = prints.filter(val => {
                        if (excel.includes(val.display_name)) {
                            val.name = val.name.split("(")[0]
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        }
                    })
                    nextProps.items.action = [...action, ...excelArray];
                    hidePrint = ["仕掛品伝票一覧", "商品ラベルシール", "発注書", "Production Order", "製造オーダ"]
                    nextProps.items.print = prints.filter(val => !hidePrint.includes(val.name));
                }

                // let task_reporting = ["棚卸記入リスト"]
                if (this.env.view.model == "stock.quant") {
                    let action = [...data_reporting_list.action]
                    let prints = [...data_reporting_list.print]
                    let excel = ["棚卸記入リスト(EXCEL)"]
                    let excelArray = prints.filter(val => {
                        if (excel.includes(val.display_name)) {
                            val.name = val.name.split("(")[0]
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        }
                    })
                    nextProps.items.action = [...action, ...excelArray];
                    nextProps.items.print = prints.filter(val => !val.display_name.includes('(EXCEL)'));
                }

                // task_purchase_order_for_part = ["発注書(部材用）"]
                if (this.env.view.model == "purchase.order") {
                    let prints = [...data_purchase_list.print]
                    nextProps.items.print = prints.filter(val => val.display_name !== "発注書(部材用）");
                }
            }

            this.actionItems = await this._setActionItems(nextProps);
            this.printItems = await this._setPrintItems(nextProps);
        }
    });
});
