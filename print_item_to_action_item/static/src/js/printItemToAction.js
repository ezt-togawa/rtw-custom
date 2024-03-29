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

    const delivery_request = "配送作業依頼書"
    const inspection_order = "検品発注書"
    const invoice = "請求書"
    const shipping_form = "出荷依頼書"
    const purchase_order = "注文書"
    const purchase_order_part = "発注書(部材用）"
    const purchase_order_sheet = "発注書"
    const quotation = "御見積書"
    const quotation_over_sea = "御見積書（海外）"
    const list_price_quotation = "定価見積書"
    const unit_price_quotation = "単価見積り書"
    const inspection_check_sheet = "検品チェックシート(EXCEL)"
    const inventory_entry_list = "棚卸記入リスト(EXCEL)"
    const invoice_sticker = "送り状シール(EXCEL)"
    const prod_label_sticker = "商品ラベルシール(EXCEL)"
    const prod_spec_excel = "商品仕様書(EXCEL)"
    const prod_spec_pdf = "商品仕様書"
    const scheduled_arrival_list = "入荷予定リスト(EXCEL)"
    const payment_schedule_list = "支給予定リスト(EXCEL)"
    const shipping_schedule_list = "出荷予定リスト(EXCEL)"
    const inventory_status_list = "在庫状況一覧(EXCEL)"
    const supplied_parts_details = "支給部材明細(EXCEL)"
    const WIP_document_list = "仕掛品伝票一覧(EXCEL)"

    const english_names = {}
    const pdf = "custom_report_rtw"
    const excel = "rtw_excel_report"

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

        async english_name(japanese_name, list_translated) {
            let english_name_pdf = list_translated.filter(val => val.src === japanese_name && val.module === pdf);
            let english_name_excel = list_translated.filter(val => val.src === japanese_name && val.module === excel);
            if (english_name_pdf.length > 0) english_names[japanese_name + "_pdf"] = english_name_pdf[0].value;
            if (english_name_excel.length > 0) english_names[japanese_name + "_excel"] = english_name_excel[0].value;
            return;
        },

        async _loadData() {
            const list_translated = await this.rpc({
                model: 'ir.translation',
                method: 'search_read',
                args: [
                    [
                        '|',
                        ['module', '=', excel],
                        ['module', '=', pdf],
                        '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|',
                        ['src', '=', delivery_request], ['src', '=', inspection_order], ['src', '=', invoice], ['src', '=', shipping_form],
                        ['src', '=', purchase_order], ['src', '=', purchase_order_part], ['src', '=', purchase_order_sheet],
                        ['src', '=', quotation], ['src', '=', quotation_over_sea], ['src', '=', list_price_quotation], ['src', '=', unit_price_quotation],
                        ['src', '=', inspection_check_sheet], ['src', '=', inventory_entry_list], ['src', '=', invoice_sticker],
                        ['src', '=', prod_label_sticker], ['src', '=', prod_spec_excel], ['src', '=', prod_spec_pdf],
                        ['src', '=', scheduled_arrival_list], ['src', '=', payment_schedule_list], ['src', '=', shipping_schedule_list],
                        ['src', '=', inventory_status_list], ['src', '=', supplied_parts_details], ['src', '=', WIP_document_list]
                    ],
                    ['module', 'src', 'value'],
                ]
            });

            const uniqueObjects = {};
            list_translated.forEach(item => {
                const key = item.src + '-' + item.module; // Creating a combined key of src and module
                if (!(key in uniqueObjects) || uniqueObjects[key].id < item.id) {
                    uniqueObjects[key] = item;
                }
            });
            const unique_list_translated = Object.values(uniqueObjects);

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
                    await this.english_name(shipping_schedule_list, unique_list_translated)
                    await this.english_name(payment_schedule_list, unique_list_translated)
                    await this.english_name(scheduled_arrival_list, unique_list_translated)
                    let excel = [
                        shipping_schedule_list, english_names[shipping_schedule_list + "_pdf"], english_names[shipping_schedule_list + "_excel"],
                        payment_schedule_list, english_names[payment_schedule_list + "_pdf"], english_names[payment_schedule_list + "_excel"],
                        scheduled_arrival_list, english_names[scheduled_arrival_list + "_pdf"], english_names[scheduled_arrival_list + "_excel"]
                    ]

                    let isExcelTemplate2AtAction = action.some(val => excel.includes(val.display_name));
                    if (isExcelTemplate2AtAction) {
                        this.props.items.action = action.filter(val => val.display_name !== inspection_check_sheet && val.display_name !== invoice_sticker && val.display_name !== supplied_parts_details);
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

                    // hidePrint = ['配送作業依頼書', '出荷依頼書', 'Delivery Slip', '配送伝票']
                    await this.english_name(delivery_request, unique_list_translated)
                    await this.english_name(shipping_form, unique_list_translated)

                    hidePrint = [
                        delivery_request, english_names[delivery_request + "_pdf"], english_names[delivery_request + "_excel"],
                        shipping_form, english_names[shipping_form + "_pdf"], english_names[shipping_form + "_excel"],
                        '配送伝票', 'Delivery Slip'
                    ]
                    this.props.items.print = prints.filter(val => !val.display_name.includes('(EXCEL)') && !hidePrint.includes(val.name))
                }

                //  sale_order_view_list
                if (this.env.view.model == "sale.order") {
                    if (data_sale_order_list === null) {
                        data_sale_order_list = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let action = [...data_sale_order_list.action]
                    let prints = [...data_sale_order_list.print]
                    await this.english_name(prod_spec_excel, unique_list_translated)
                    await this.english_name(prod_spec_pdf, unique_list_translated)
                    await this.english_name(quotation, unique_list_translated)
                    await this.english_name(list_price_quotation, unique_list_translated)
                    await this.english_name(unit_price_quotation, unique_list_translated)
                    await this.english_name(purchase_order, unique_list_translated)
                    await this.english_name(quotation_over_sea, unique_list_translated)
                    await this.english_name(invoice, unique_list_translated)

                    hidePrint = [
                        "Quotation / Order", "見積 / オーダ",
                        prod_spec_excel, english_names[prod_spec_excel + "_pdf"], english_names[prod_spec_excel + "_excel"],
                        prod_spec_pdf, english_names[prod_spec_pdf + "_pdf"], english_names[prod_spec_pdf + "_excel"],
                        quotation, english_names[quotation + "_pdf"], english_names[quotation + "_excel"],
                        list_price_quotation, english_names[list_price_quotation + "_pdf"], english_names[list_price_quotation + "_excel"],
                        unit_price_quotation, english_names[unit_price_quotation + "_pdf"], english_names[unit_price_quotation + "_excel"],
                        purchase_order, english_names[purchase_order + "_pdf"], english_names[purchase_order + "_excel"],
                        quotation_over_sea, english_names[quotation_over_sea + "_pdf"], english_names[quotation_over_sea + "_excel"],
                        invoice, english_names[invoice + "_pdf"], english_names[invoice + "_excel"],
                    ]
                    hideExcel = [
                        prod_spec_excel, english_names[prod_spec_excel + "_pdf"], english_names[prod_spec_excel + "_excel"],
                        prod_spec_pdf, english_names[prod_spec_pdf + "_pdf"], english_names[prod_spec_pdf + "_excel"],
                    ]

                    this.props.items.print = prints.filter(val => !hidePrint.includes(val.name))
                    this.props.items.action = action.filter(val => !hideExcel.includes(val.name))
                }

                // task_invoice_list
                if (this.env.view.model == "account.move") {
                    if (data_account_move_list === null) {
                        data_account_move_list = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    this.props.items.print = []
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
                    await this.english_name(WIP_document_list, unique_list_translated)
                    await this.english_name(prod_label_sticker, unique_list_translated)
                    let excel = [
                        WIP_document_list, english_names[WIP_document_list + "_pdf"], english_names[WIP_document_list + "_excel"],
                        prod_label_sticker, english_names[prod_label_sticker + "_pdf"], english_names[prod_label_sticker + "_excel"]
                    ]
                    let excelArray = prints.filter(val => {
                        if (excel.includes(val.display_name)) {
                            val.name = val.name.split("(")[0]
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        }
                    })
                    this.props.items.action = [...action, ...excelArray];
                    this.props.items.print = [];
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
                    await this.english_name(inventory_entry_list, unique_list_translated)
                    let excel = [inventory_entry_list, english_names[inventory_entry_list + "_pdf"], english_names[inventory_entry_list + "_excel"]]
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

                // task_purchase_order_for_part = [purchase_order_part]
                if (this.env.view.model == "purchase.order") {
                    if (data_purchase_list === null) {
                        data_purchase_list = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let prints = [...data_purchase_list.print]
                    await this.english_name(purchase_order_part, unique_list_translated)
                    const purchase_for_part = [purchase_order_part, english_names[purchase_order_part + "_pdf"], english_names[purchase_order_part + "_excel"]];
                    this.props.items.print = prints.filter(val => !purchase_for_part.includes(val.display_name));
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

                    await this.english_name(prod_spec_excel, unique_list_translated)
                    const prod_spec = [prod_spec_excel, english_names[prod_spec_excel + "_pdf"], english_names[prod_spec_excel + "_excel"]]
                    let excel = prints.filter(val => {
                        if (prod_spec.includes(val.display_name)) {
                            val.name = val.name.split("(")[0]
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        }
                    })

                    let showActionItem = [...action, ...excel]
                    let sortAction = ['', '', '', '', '', '', '', '', '', '']
                    await this.english_name(quotation, unique_list_translated)
                    await this.english_name(quotation_over_sea, unique_list_translated)
                    await this.english_name(list_price_quotation, unique_list_translated)
                    await this.english_name(unit_price_quotation, unique_list_translated)
                    await this.english_name(purchase_order, unique_list_translated)
                    await this.english_name(prod_spec_excel, unique_list_translated)
                    await this.english_name(prod_spec_pdf, unique_list_translated)
                    await this.english_name(invoice, unique_list_translated)
                    const sortItem4 = [quotation, english_names[quotation + "_pdf"], english_names[quotation + "_excel"]]
                    const sortItem5 = [quotation_over_sea, english_names[quotation_over_sea + "_pdf"], english_names[quotation_over_sea + "_excel"]]
                    const sortItem6 = [list_price_quotation, english_names[list_price_quotation + "_pdf"], english_names[list_price_quotation + "_excel"]]
                    const sortItem7 = [unit_price_quotation, english_names[unit_price_quotation + "_pdf"], english_names[unit_price_quotation + "_excel"]]
                    const sortItem8 = [purchase_order, english_names[purchase_order + "_pdf"], english_names[purchase_order + "_excel"]]
                    const sortItem9 = [prod_spec_excel, english_names[prod_spec_excel + "_pdf"], english_names[prod_spec_excel + "_excel"]]
                    const sortItem10 = [prod_spec_pdf, english_names[prod_spec_pdf + "_pdf"], english_names[prod_spec_pdf + "_excel"]]
                    const sortItem11 = [invoice, english_names[invoice + "_pdf"], english_names[invoice + "_excel"]]

                    showActionItem.filter(val => {
                        if (val.name === "Generate a Payment Link" || val.name === "支払用リンクを生成"|| val.name === "Genera link di pagamento") sortAction[0] = val
                        if (val.name === "Share" || val.name === "共有"|| val.name === "Condividi") sortAction[1] = val
                        if (val.name === "Mark Quotation as Sent" || val.name === "見積もりを送信済みとしてマーク"|| val.name === "Segna preventivo come inviato") sortAction[2] = val 
                        if (sortItem4.includes(val.name)) sortAction[3] = val
                        if (sortItem5.includes(val.name)) sortAction[4] = val
                        if (sortItem6.includes(val.name)) sortAction[5] = val
                        if (sortItem7.includes(val.name)) sortAction[6] = val
                        if (sortItem8.includes(val.name)) sortAction[7] = val
                        if (sortItem9.includes(val.display_name)) sortAction[8] = val
                        if (sortItem11.includes(val.display_name)) sortAction[9] = val
                        if (val.name === "Send a Cart Recovery Email" || val.name === "カートリカバリEメールを送信"|| val.name === "Invia e-mail di recupero carrello") sortAction[10] = val
                    })
                    this.props.items.action = sortAction
                    await this.english_name(prod_spec_excel, unique_list_translated)
                    hidePrint = [
                        "見積 / オーダ", "Quotation / Order",
                        prod_spec_excel, english_names[prod_spec_excel + "_pdf"], english_names[prod_spec_excel + "_excel"]
                    ]
                    let showPrint = prints.filter(val => !hidePrint.includes(val.display_name))
                    let sortPrint = ['', '', '', '', '', '','']
                    showPrint.filter(async val => {
                        if (sortItem4.includes(val.name)) sortPrint[0] = val
                        if (sortItem5.includes(val.name)) sortPrint[1] = val
                        if (sortItem6.includes(val.name)) sortPrint[2] = val
                        if (sortItem7.includes(val.name)) sortPrint[3] = val
                        if (sortItem8.includes(val.name)) sortPrint[4] = val
                        if (sortItem10.includes(val.display_name)) sortPrint[5] = val
                        if (sortItem11.includes(val.display_name)) sortPrint[6] = val
                    })
                    this.props.items.print = sortPrint
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
                    await this.english_name(invoice, unique_list_translated)
                    showPrint = [invoice, english_names[invoice + "_pdf"], english_names[invoice + "_excel"]]
                    this.props.items.print = prints.filter(val => showPrint.includes(val.name) && (val.report_name.startsWith("custom_report_rtw.report_invoice_3") || val.report_name.startsWith("rtw_excel_report")))
                }

                // task_inventory_manfac_form= ["商品ラベルシール"]
                if (this.env.view.model === "mrp.production") {
                    if (data_manufacture_form === null) {
                        data_manufacture_form = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }

                    // let action = [...data_manufacture_form.action]
                    let prints = [...data_manufacture_form.print]

                    // let excel = prints.filter(val => {
                    //     if (val.display_name === prod_label_sticker) {
                    //         val.name = val.name.split("(")[0]
                    //         val.type = 'ir.actions.act_window'
                    //         val.binding_type = 'action'
                    //         return val
                    //     }
                    // })
                    // this.props.items.action = [...action, ...excel]
                    // this.props.items.action = [...action]
                    await this.english_name(purchase_order_sheet, unique_list_translated)
                    await this.english_name(inspection_order, unique_list_translated)
                    showPrint = [
                        purchase_order_sheet, english_names[purchase_order_sheet + "_pdf"], english_names[purchase_order_sheet + "_excel"],
                        inspection_order, english_names[inspection_order + "_pdf"], english_names[inspection_order + "_excel"]
                    ]
                    this.props.items.print = prints.filter(val => showPrint.includes(val.name))
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
                    await this.english_name(inventory_status_list, unique_list_translated)
                    const stock_list = [inventory_status_list, english_names[inventory_status_list + "_pdf"], english_names[inventory_status_list + "_excel"]]
                    let excel = prints.filter(val => {
                        if (stock_list.includes(val.display_name)) {
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
                    // task_inventory_delivery_form = ["送り状シール(EXCEL)",supplied_parts_details] +recept
                    if (data_delivery_receipt_form === null) {
                        data_delivery_receipt_form = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let action = [...data_delivery_receipt_form.action]
                    let prints = [...data_delivery_receipt_form.print]
                    await this.english_name(invoice_sticker, unique_list_translated)
                    await this.english_name(supplied_parts_details, unique_list_translated)
                    await this.english_name(inspection_check_sheet, unique_list_translated)
                    let excel = [
                        invoice_sticker, english_names[invoice_sticker + "_pdf"], english_names[invoice_sticker + "_excel"],
                        supplied_parts_details, english_names[supplied_parts_details + "_pdf"], english_names[supplied_parts_details + "_excel"],
                        inspection_check_sheet, english_names[inspection_check_sheet + "_pdf"], english_names[inspection_check_sheet + "_excel"]
                    ]
                    let isExcelTemplate2AtAction = action.some(val => excel.includes(val.display_name));
                    if (isExcelTemplate2AtAction) {
                        this.props.items.action = action.filter(val => val.display_name !== shipping_schedule_list && val.display_name !== payment_schedule_list && val.display_name !== scheduled_arrival_list);
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
                    hidePrint = ['Delivery Slip', '配送伝票']
                    this.props.items.print = prints.filter(val => !val.display_name.includes('(EXCEL)') && !hidePrint.includes(val.name))
                }
            }
            this.actionItems = await this._setActionItems(this.props);
            this.printItems = await this._setPrintItems(this.props);
        },

        async _updateData(nextProps) {
            const list_translated = await this.rpc({
                model: 'ir.translation',
                method: 'search_read',
                args: [
                    [
                        '|',
                        ['module', '=', 'rtw_excel_report'],
                        ['module', '=', 'custom_report_rtw'],
                        '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|',
                        ['src', '=', delivery_request], ['src', '=', inspection_order], ['src', '=', invoice], ['src', '=', shipping_form],
                        ['src', '=', purchase_order], ['src', '=', purchase_order_part], ['src', '=', purchase_order_sheet],
                        ['src', '=', quotation], ['src', '=', quotation_over_sea], ['src', '=', list_price_quotation], ['src', '=', unit_price_quotation],
                        ['src', '=', inspection_check_sheet], ['src', '=', inventory_entry_list], ['src', '=', invoice_sticker],
                        ['src', '=', prod_label_sticker], ['src', '=', prod_spec_excel], ['src', '=', prod_spec_pdf],
                        ['src', '=', scheduled_arrival_list], ['src', '=', payment_schedule_list], ['src', '=', shipping_schedule_list],
                        ['src', '=', inventory_status_list], ['src', '=', supplied_parts_details], ['src', '=', WIP_document_list]
                    ],
                    ['module', 'src', 'value'],
                ]
            });

            const uniqueObjects = {};
            list_translated.forEach(item => {
                if (!(item.src in uniqueObjects) || uniqueObjects[item.src].id < item.id) {
                    uniqueObjects[item.src] = item;
                }
            });

            const unique_list_translated = Object.values(uniqueObjects);

            let view_type_now = this.env.view.type
            if (view_type_now === "list") {
                if (this.env.view.model == "stock.picking") {
                    let action = [...data_delivery_receipt_list.action]
                    let prints = [...data_delivery_receipt_list.print]

                    // task_inventory_delivery_list = ["出荷予定リスト"]  inventory_receipt_list = ["支給予定リスト", "入荷予定リスト"]
                    await this.english_name(shipping_schedule_list, unique_list_translated)
                    await this.english_name(payment_schedule_list, unique_list_translated)
                    await this.english_name(scheduled_arrival_list, unique_list_translated)
                    let excel = [
                        shipping_schedule_list, english_names[shipping_schedule_list + "_pdf"], english_names[shipping_schedule_list + "_excel"],
                        payment_schedule_list, english_names[payment_schedule_list + "_pdf"], english_names[payment_schedule_list + "_excel"],
                        scheduled_arrival_list, english_names[scheduled_arrival_list + "_pdf"], english_names[scheduled_arrival_list + "_excel"]
                    ]
                    let isExcelTemplate2AtAction = action.some(val => excel.includes(val.display_name));
                    if (isExcelTemplate2AtAction) {
                        nextProps.items.action = action.filter(val => val.display_name !== inspection_check_sheet && val.display_name !== invoice_sticker && val.display_name !== supplied_parts_details);
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
                    await this.english_name(delivery_request, unique_list_translated)
                    await this.english_name(shipping_form, unique_list_translated)
                    hidePrint = [
                        delivery_request, english_names[delivery_request + "_pdf"], english_names[delivery_request + "_excel"],
                        shipping_form, english_names[shipping_form + "_pdf"], english_names[shipping_form + "_excel"],
                        '配送伝票', 'Delivery Slip'
                    ]
                    nextProps.items.print = prints.filter(val => !val.display_name.includes('(EXCEL)') && !hidePrint.includes(val.name))
                }

                // let task_sale_order_list
                if (this.env.view.model == "sale.order") {
                    let action = [...data_sale_order_list.action]
                    let prints = [...data_sale_order_list.print]
                    await this.english_name(prod_spec_excel, unique_list_translated)
                    await this.english_name(prod_spec_pdf, unique_list_translated)
                    await this.english_name(quotation, unique_list_translated)
                    await this.english_name(list_price_quotation, unique_list_translated)
                    await this.english_name(unit_price_quotation, unique_list_translated)
                    await this.english_name(purchase_order, unique_list_translated)
                    await this.english_name(quotation_over_sea, unique_list_translated)

                    hidePrint = [
                        "Quotation / Order", "見積 / オーダ",
                        prod_spec_excel, english_names[prod_spec_excel + "_pdf"], english_names[prod_spec_excel + "_excel"],
                        prod_spec_pdf, english_names[prod_spec_pdf + "_pdf"], english_names[prod_spec_pdf + "_excel"],
                        quotation, english_names[quotation + "_pdf"], english_names[quotation + "_excel"],
                        list_price_quotation, english_names[list_price_quotation + "_pdf"], english_names[list_price_quotation + "_excel"],
                        unit_price_quotation, english_names[unit_price_quotation + "_pdf"], english_names[unit_price_quotation + "_excel"],
                        purchase_order, english_names[purchase_order + "_pdf"], english_names[purchase_order + "_excel"],
                        quotation_over_sea, english_names[quotation_over_sea + "_pdf"], english_names[quotation_over_sea + "_excel"],
                    ]
                    hideExcel = [
                        prod_spec_excel, english_names[prod_spec_excel + "_pdf"], english_names[prod_spec_excel + "_excel"],
                        prod_spec_pdf, english_names[prod_spec_pdf + "_pdf"], english_names[prod_spec_pdf + "_excel"],
                    ]
                    nextProps.items.print = prints.filter(val => !hidePrint.includes(val.name))
                    nextProps.items.action = action.filter(val => !hideExcel.includes(val.name))
                }

                // let task_invoice_list
                if (this.env.view.model == "account.move") {
                    nextProps.items.print = []
                }

                // let task_manfac_list = ["仕掛品伝票一覧"]
                if (this.env.view.model == "mrp.production") {
                    let action = [...data_manufacture_list.action]
                    let prints = [...data_manufacture_list.print]
                    await this.english_name(WIP_document_list, unique_list_translated)
                    await this.english_name(prod_label_sticker, unique_list_translated)
                    let excel = [
                        WIP_document_list, english_names[WIP_document_list + "_pdf"], english_names[WIP_document_list + "_excel"],
                        prod_label_sticker, english_names[prod_label_sticker + "_pdf"], english_names[prod_label_sticker + "_excel"]
                    ]
                    let excelArray = prints.filter(val => {
                        if (excel.includes(val.display_name)) {
                            val.name = val.name.split("(")[0]
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        }
                    })
                    nextProps.items.action = [...action, ...excelArray];
                    nextProps.items.print = [];
                }

                // let task_reporting = ["棚卸記入リスト"]
                if (this.env.view.model == "stock.quant") {
                    let action = [...data_reporting_list.action]
                    let prints = [...data_reporting_list.print]
                    await this.english_name(inventory_entry_list, unique_list_translated)
                    let excel = [inventory_entry_list, english_names[inventory_entry_list + "_pdf"], english_names[inventory_entry_list + "_excel"]]
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

                // task_purchase_order_for_part = [purchase_order_part]
                if (this.env.view.model == "purchase.order") {
                    let prints = [...data_purchase_list.print]
                    await this.english_name(purchase_order_part, unique_list_translated)
                    const purchase_for_part = [purchase_order_part, english_names[purchase_order_part + "_pdf"], english_names[purchase_order_part + "_excel"]];
                    nextProps.items.print = prints.filter(val => !purchase_for_part.includes(val.display_name));
                }
            }

            this.actionItems = await this._setActionItems(nextProps);
            this.printItems = await this._setPrintItems(nextProps);
        }
    });
});
