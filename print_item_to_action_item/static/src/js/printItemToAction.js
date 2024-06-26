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
    var data_purchase_order_form = null;
    var data_template_form = null;

    //sale order 
    //pdf
    const quotation = "御見積書"
    const quotation_over_sea = "御見積書（海外）"
    const list_price_quotation = "定価見積書"
    const unit_price_quotation = "単価見積り書"
    const purchase_order = "注文書"
    const purchase_order2_pdf = "定価注文書"
    const prod_spec_pdf = "商品仕様書"
    const delivery_request_sale_pdf = "配送作業依頼書"
    const invoice = "請求書"
    //excel
    const quotation_excel = "御見積書"
    const quotation_oversea_excel = "御見積書（海外）"
    const list_price_quotation_excel = "定価御見積書"
    const unit_price_quotation_excel = "単価御見積書"
    const purchase_order_excel = "注文書"
    const purchase_order2_excel = "定価注文書"
    const prod_spec_excel = "商品仕様書"
    const delivery_request_sale_excel = "配送作業依頼書"
    const invoice_excel = "請求書"

    //invoice
    const invoice_excel_account_move = "請求書(EXCEL)2"

    //delivery
    const delivery_request = "配送作業依頼書"
    const shipping_form = "出荷依頼書"
    ////delivery list
    const inspection_check_sheet = "検品チェックシート(EXCEL)"
    const invoice_sticker = "送り状シール(EXCEL)"
    const supplied_parts_details = "支給部材明細(EXCEL)"

    //purchase
    const purchase_order_part = "発注書(部材用）"
    const purchase_for_part_excel = "発注書(部材用）-(EXCEL)"

    //mrp
    const purchase_order_sheet = "発注書"
    const inspection_order = "検品発注書"
    const purchase_order_sheet_EX = "発注書(EXCEL)"
    const inspection_order_EX = "検品発注書(EXCEL)"


    const inventory_entry_list = "棚卸記入リスト(EXCEL)"
    const prod_label_sticker = "商品ラベルシール(EXCEL)"
    const scheduled_arrival_list = "入荷予定リスト(EXCEL)"
    const payment_schedule_list = "支給予定リスト(EXCEL)"
    const shipping_schedule_list = "出荷予定リスト(EXCEL)"
    const inventory_status_list = "在庫状況一覧(EXCEL)"
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

        async show_name(name_origin, list_translated, module, lang) {
            if (lang === 'en_US') {
                if (module == excel) {
                    let name_ex = await list_translated.filter(val => val.src === name_origin && val.module === excel);
                    if (name_ex.length > 0) {
                        return name_ex[0].value;
                    }
                } else {
                    let name_pdf = await list_translated.filter(val => val.src === name_origin && val.module === pdf);

                    if (name_pdf.length > 0) {
                        return name_pdf[0].value;
                    }
                }
            } else {
                return name_origin
            }
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
                        '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|',
                        ['src', '=', quotation_excel], ['src', '=', quotation_oversea_excel], ['src', '=', list_price_quotation_excel], ['src', '=', unit_price_quotation_excel], ['src', '=', purchase_order2_pdf],
                        ['src', '=', quotation], ['src', '=', quotation_over_sea], ['src', '=', list_price_quotation], ['src', '=', unit_price_quotation],
                        ['src', '=', delivery_request], ['src', '=', inspection_order], ['src', '=', invoice], ['src', '=', shipping_form],
                        ['src', '=', purchase_order], ['src', '=', purchase_order_excel], ['src', '=', purchase_order2_excel], ['src', '=', purchase_order_part], ['src', '=', purchase_order_sheet],
                        ['src', '=', invoice_excel],
                        ['src', '=', purchase_order_sheet_EX], ['src', '=', inspection_order_EX],
                        ['src', '=', inspection_check_sheet], ['src', '=', inventory_entry_list], ['src', '=', invoice_sticker],
                        ['src', '=', prod_label_sticker], ['src', '=', prod_spec_excel], ['src', '=', prod_spec_pdf],
                        ['src', '=', scheduled_arrival_list], ['src', '=', payment_schedule_list], ['src', '=', shipping_schedule_list],
                        ['src', '=', inventory_status_list], ['src', '=', supplied_parts_details], ['src', '=', WIP_document_list], ['src', '=', invoice_excel_account_move],
                        ['src', '=', purchase_for_part_excel], ['src', '=', delivery_request_sale_pdf], ['src', '=', delivery_request_sale_excel]
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
            let lang = await this.env.action.context.lang || 'ja_JP'
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

                    const quotation_name_ex = await this.show_name(quotation_excel, unique_list_translated, excel, lang)
                    const quotation_name_pdf = await this.show_name(quotation, unique_list_translated, pdf, lang)
                    const quotation_oversea_name_ex = await this.show_name(quotation_oversea_excel, unique_list_translated, excel, lang)
                    const quotation_over_sea_name_pdf = await this.show_name(quotation_over_sea, unique_list_translated, pdf, lang)
                    const list_price_quotation_name_ex = await this.show_name(list_price_quotation_excel, unique_list_translated, excel, lang)
                    const list_price_quotation_name_pdf = await this.show_name(list_price_quotation, unique_list_translated, pdf, lang)
                    const unit_price_quotation_name_ex = await this.show_name(unit_price_quotation_excel, unique_list_translated, excel, lang)
                    const unit_price_quotation_name_pdf = await this.show_name(unit_price_quotation, unique_list_translated, pdf, lang)
                    const purchase_order_name_ex = await this.show_name(purchase_order_excel, unique_list_translated, excel, lang)
                    const purchase_order_name_pdf = await this.show_name(purchase_order, unique_list_translated, pdf, lang)
                    const purchase_order2_name_ex = await this.show_name(purchase_order2_excel, unique_list_translated, excel, lang)
                    const purchase_order2_name_pdf = await this.show_name(purchase_order2_pdf, unique_list_translated, pdf, lang)
                    const p_spec_name_ex = await this.show_name(prod_spec_excel, unique_list_translated, excel, lang)
                    const p_spec_name_pdf = await this.show_name(prod_spec_pdf, unique_list_translated, pdf, lang)
                    const delivery_request_name_ex = await this.show_name(delivery_request_sale_excel, unique_list_translated, excel, lang)
                    const delivery_request_name_pdf = await this.show_name(delivery_request_sale_pdf, unique_list_translated, pdf, lang)
                    const invoice_name_ex = await this.show_name(invoice_excel, unique_list_translated, excel, lang)
                    const invoice_name_pdf = await this.show_name(invoice, unique_list_translated, pdf, lang)
                    hideName = [
                        quotation_name_ex, quotation_oversea_name_ex, list_price_quotation_name_ex,
                        unit_price_quotation_name_ex, purchase_order_name_ex, purchase_order2_name_ex,
                        p_spec_name_ex, delivery_request_name_ex, invoice_name_ex,
                        quotation_name_pdf, quotation_over_sea_name_pdf, list_price_quotation_name_pdf,
                        unit_price_quotation_name_pdf, purchase_order_name_pdf, purchase_order2_name_pdf,
                        p_spec_name_pdf, delivery_request_name_pdf, invoice_name_pdf,
                        '見積 / オーダ', 'Quotation / Order'
                    ]

                    this.props.items.print = prints.filter(val => !hideName.includes(val.name))
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
                    await this.english_name(purchase_order_sheet, unique_list_translated)
                    await this.english_name(inspection_order, unique_list_translated)
                    await this.english_name(purchase_order_sheet_EX, unique_list_translated)
                    await this.english_name(inspection_order_EX, unique_list_translated)

                    let excel = [
                        purchase_order_sheet_EX, english_names[purchase_order_sheet_EX + "_pdf"], english_names[purchase_order_sheet_EX + "_excel"],
                        inspection_order_EX, english_names[inspection_order_EX + "_pdf"], english_names[inspection_order_EX + "_excel"],
                        WIP_document_list, english_names[WIP_document_list + "_pdf"], english_names[WIP_document_list + "_excel"],
                        prod_label_sticker, english_names[prod_label_sticker + "_pdf"], english_names[prod_label_sticker + "_excel"]
                    ]

                    let excelArray = [];
                    excel.forEach(excelItem => {
                        let foundItem = prints.find(val => val.display_name === excelItem);
                        if (foundItem) {
                            foundItem.name = foundItem.name.split("(")[0];
                            excelArray.push(foundItem);
                        }
                    });
                    this.props.items.action = [...action, ...excelArray];

                    showPrint = [
                        purchase_order_sheet, english_names[purchase_order_sheet + "_pdf"], english_names[purchase_order_sheet + "_excel"],
                        inspection_order, english_names[inspection_order + "_pdf"], english_names[inspection_order + "_excel"]
                    ]
                    this.props.items.print = prints.filter(val => showPrint.includes(val.display_name))
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
                    const prints = [...data_purchase_list.print]
                    const actions = [...data_purchase_list.action]
                    await this.english_name(purchase_order_part, unique_list_translated)
                    await this.english_name(purchase_for_part_excel, unique_list_translated)

                    const purchase_for_part_pdf = [purchase_order_part, english_names[purchase_order_part + "_pdf"], english_names[purchase_order_part + "_excel"]]
                    const purchase_for_part_ex = [purchase_for_part_excel, english_names[purchase_for_part_excel + "_pdf"], english_names[purchase_for_part_excel + "_excel"]]

                    let excel_arr = prints.filter(val => {
                        if (purchase_for_part_ex.includes(val.display_name)) {
                            val.name = val.name.split("-")[0]
                            return val
                        }
                    })

                    this.props.items.action = [...excel_arr, ...actions]
                    this.props.items.print = prints.filter(val => purchase_for_part_pdf.includes(val.display_name))
                }
            }

            if (view_type_now === 'form') {
                // purchase_order_view_form
                if (this.env.view.model === "purchase.order") {
                    if (data_purchase_order_form === null) {
                        data_purchase_order_form = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let prints = [...data_purchase_order_form.print]
                    let actions = [...data_purchase_order_form.action]

                    await this.english_name(purchase_for_part_excel, unique_list_translated)
                    await this.english_name(purchase_order_part, unique_list_translated)

                    const purchase_for_part_pdf = [purchase_order_part, english_names[purchase_order_part + "_pdf"], english_names[purchase_order_part + "_excel"]]
                    const purchase_for_part_ex = [purchase_for_part_excel, english_names[purchase_for_part_excel + "_pdf"], english_names[purchase_for_part_excel + "_excel"]]
                    let excel_arr = prints.filter(val => {
                        if (purchase_for_part_ex.includes(val.display_name)) {
                            val.name = val.name.split("-")[0]
                            return val
                        }
                    })
                    this.props.items.action = [...actions, ...excel_arr]
                    this.props.items.print = prints.filter(val => purchase_for_part_pdf.includes(val.display_name))
                }
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

                    const quotation_name_ex = await this.show_name(quotation_excel, unique_list_translated, excel, lang)
                    const quotation_name_pdf = await this.show_name(quotation, unique_list_translated, pdf, lang)

                    const quotation_oversea_name_ex = await this.show_name(quotation_oversea_excel, unique_list_translated, excel, lang)
                    const quotation_over_sea_name_pdf = await this.show_name(quotation_over_sea, unique_list_translated, pdf, lang)

                    const list_price_quotation_name_ex = await this.show_name(list_price_quotation_excel, unique_list_translated, excel, lang)
                    const list_price_quotation_name_pdf = await this.show_name(list_price_quotation, unique_list_translated, pdf, lang)

                    const unit_price_quotation_name_ex = await this.show_name(unit_price_quotation_excel, unique_list_translated, excel, lang)
                    const unit_price_quotation_name_pdf = await this.show_name(unit_price_quotation, unique_list_translated, pdf, lang)

                    const purchase_order_name_ex = await this.show_name(purchase_order_excel, unique_list_translated, excel, lang)
                    const purchase_order_name_pdf = await this.show_name(purchase_order, unique_list_translated, pdf, lang)

                    const purchase_order2_name_ex = await this.show_name(purchase_order2_excel, unique_list_translated, excel, lang)
                    const purchase_order2_name_pdf = await this.show_name(purchase_order2_pdf, unique_list_translated, pdf, lang)

                    const p_spec_name_ex = await this.show_name(prod_spec_excel, unique_list_translated, excel, lang)
                    const p_spec_name_pdf = await this.show_name(prod_spec_pdf, unique_list_translated, pdf, lang)

                    const delivery_request_name_ex = await this.show_name(delivery_request_sale_excel, unique_list_translated, excel, lang)
                    const delivery_request_name_pdf = await this.show_name(delivery_request_sale_pdf, unique_list_translated, pdf, lang)

                    const invoice_name_ex = await this.show_name(invoice_excel, unique_list_translated, excel, lang)
                    const invoice_name_pdf = await this.show_name(invoice, unique_list_translated, pdf, lang)

                    let name_excel = [
                        quotation_name_ex, quotation_oversea_name_ex, list_price_quotation_name_ex,
                        unit_price_quotation_name_ex, purchase_order_name_ex, purchase_order2_name_ex,
                        p_spec_name_ex, delivery_request_name_ex, invoice_name_ex
                    ]

                    let excel_arr = prints.filter(val => {
                        if (name_excel.includes(val.display_name) && val.xml_id.startsWith(excel)) return val
                    })

                    let showActionItem = [...action, ...excel_arr]
                    let sortAction = ['', '', '', '', '', '', '', '', '', '', '', '']

                    showActionItem.filter(val => {
                        if (val.name === "Generate a Payment Link" || val.name === "支払用リンクを生成" || val.name === "Genera link di pagamento") sortAction[0] = val
                        if (val.name === "Share" || val.name === "共有" || val.name === "Condividi") sortAction[1] = val
                        if (val.name === "Mark Quotation as Sent" || val.name === "見積もりを送信済みとしてマーク" || val.name === "Segna preventivo come inviato") sortAction[2] = val
                        if (quotation_name_ex == val.display_name) sortAction[3] = val
                        if (quotation_oversea_name_ex == val.display_name) sortAction[4] = val
                        if (list_price_quotation_name_ex == val.display_name) sortAction[5] = val
                        if (unit_price_quotation_name_ex == val.display_name) sortAction[6] = val
                        if (purchase_order_name_ex == val.display_name) sortAction[7] = val
                        if (purchase_order2_name_ex == val.display_name) sortAction[8] = val
                        if (p_spec_name_ex == val.display_name) sortAction[9] = val
                        if (delivery_request_name_ex == val.display_name) sortAction[10] = val
                        if (invoice_name_ex == val.display_name) sortAction[11] = val
                        if (val.name === "Send a Cart Recovery Email" || val.name === "カートリカバリEメールを送信" || val.name === "Invia e-mail di recupero carrello") sortAction[12] = val
                    })
                    this.props.items.action = sortAction

                    let name_pdf = [
                        quotation_name_pdf, quotation_over_sea_name_pdf, list_price_quotation_name_pdf,
                        unit_price_quotation_name_pdf, purchase_order_name_pdf, purchase_order2_name_pdf,
                        p_spec_name_pdf, delivery_request_name_pdf, invoice_name_pdf
                    ]
                    this.props.items.print = prints.filter(val => name_pdf.includes(val.display_name) && val.xml_id.startsWith(pdf))
                }

                // task_invoice_form
                if (this.env.view.model == "account.move") {
                    if (data_account_move_list === null) {
                        data_account_move_list = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let prints = [...data_account_move_list.print]

                    await this.english_name(invoice, unique_list_translated)
                    await this.english_name(invoice_excel_account_move, unique_list_translated)

                    const invoice_pdf_account_move = [invoice, english_names[invoice + "_pdf"], english_names[invoice + "_excel"]]
                    const invoice_ex_account_move = [invoice_excel_account_move, english_names[invoice_excel_account_move + "_pdf"], english_names[invoice_excel_account_move + "_excel"]]
                    let split_name_excel = [...invoice_ex_account_move]
                    let excel_arr = prints.filter(val => {
                        if (split_name_excel.includes(val.display_name)) {
                            val.name = val.name.split("(")[0]
                            return val
                        }
                    })
                    this.props.items.action = [...data_account_move_list.action, ...excel_arr ? excel_arr : []]
                    this.props.items.print = prints.filter(val => invoice_pdf_account_move.includes(val.name) && (val.report_name.startsWith("custom_report_rtw.report_invoice_3")))
                }

                // task_inventory_manfac_form= ["商品ラベルシール"]
                if (this.env.view.model === "mrp.production") {
                    if (data_manufacture_form === null) {
                        data_manufacture_form = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let prints = [...data_manufacture_form.print]
                    let actions = [...data_manufacture_form.action]

                    //excel
                    await this.english_name(purchase_order_sheet_EX, unique_list_translated)
                    await this.english_name(inspection_order_EX, unique_list_translated)

                    const inspec_order_ex = [inspection_order_EX, english_names[inspection_order_EX + "_pdf"], english_names[inspection_order_EX + "_excel"]]
                    const pur_order_sheet_ex = [purchase_order_sheet_EX, english_names[purchase_order_sheet_EX + "_pdf"], english_names[purchase_order_sheet_EX + "_excel"]]


                    let split_name_excel = [...pur_order_sheet_ex, ...inspec_order_ex]
                    let excelArray = [];
                    split_name_excel.forEach(excelItem => {
                        let foundItem = prints.find(val => val.display_name === excelItem);
                        if (foundItem) {
                            foundItem.name = foundItem.name.split("(")[0];
                            excelArray.push(foundItem);
                        }
                    });
                    this.props.items.action = [...actions, ...excelArray]

                    //pdf
                    await this.english_name(purchase_order_sheet, unique_list_translated)
                    await this.english_name(inspection_order, unique_list_translated)
                    showPrint = [
                        purchase_order_sheet, english_names[purchase_order_sheet + "_pdf"], english_names[purchase_order_sheet + "_excel"],
                        inspection_order, english_names[inspection_order + "_pdf"], english_names[inspection_order + "_excel"]
                    ]
                    this.props.items.print = prints.filter(val => showPrint.includes(val.display_name))
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
                        ['module', '=', excel],
                        ['module', '=', pdf],
                        '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|',
                        ['src', '=', quotation_excel], ['src', '=', quotation_oversea_excel], ['src', '=', list_price_quotation_excel], ['src', '=', unit_price_quotation_excel], ['src', '=', purchase_order2_pdf],
                        ['src', '=', quotation], ['src', '=', quotation_over_sea], ['src', '=', list_price_quotation], ['src', '=', unit_price_quotation],
                        ['src', '=', delivery_request], ['src', '=', inspection_order], ['src', '=', invoice], ['src', '=', shipping_form],
                        ['src', '=', purchase_order], ['src', '=', purchase_order_excel], ['src', '=', purchase_order2_excel], ['src', '=', purchase_order_part], ['src', '=', purchase_order_sheet],
                        ['src', '=', invoice_excel],
                        ['src', '=', purchase_order_sheet_EX], ['src', '=', inspection_order_EX],
                        ['src', '=', inspection_check_sheet], ['src', '=', inventory_entry_list], ['src', '=', invoice_sticker],
                        ['src', '=', prod_label_sticker], ['src', '=', prod_spec_excel], ['src', '=', prod_spec_pdf],
                        ['src', '=', scheduled_arrival_list], ['src', '=', payment_schedule_list], ['src', '=', shipping_schedule_list],
                        ['src', '=', inventory_status_list], ['src', '=', supplied_parts_details], ['src', '=', WIP_document_list], ['src', '=', invoice_excel_account_move],
                        ['src', '=', purchase_for_part_excel], ['src', '=', delivery_request_sale_pdf], ['src', '=', delivery_request_sale_excel]
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
            let lang = await this.env.action.context.lang || 'ja_JP'

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
                    if (data_sale_order_list === null) {
                        data_sale_order_list = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let action = [...data_sale_order_list.action]
                    let prints = [...data_sale_order_list.print]
                    const quotation_name_ex = await this.show_name(quotation_excel, unique_list_translated, excel, lang)
                    const quotation_name_pdf = await this.show_name(quotation, unique_list_translated, pdf, lang)
                    const quotation_oversea_name_ex = await this.show_name(quotation_oversea_excel, unique_list_translated, excel, lang)
                    const quotation_over_sea_name_pdf = await this.show_name(quotation_over_sea, unique_list_translated, pdf, lang)
                    const list_price_quotation_name_ex = await this.show_name(list_price_quotation_excel, unique_list_translated, excel, lang)
                    const list_price_quotation_name_pdf = await this.show_name(list_price_quotation, unique_list_translated, pdf, lang)
                    const unit_price_quotation_name_ex = await this.show_name(unit_price_quotation_excel, unique_list_translated, excel, lang)
                    const unit_price_quotation_name_pdf = await this.show_name(unit_price_quotation, unique_list_translated, pdf, lang)
                    const purchase_order_name_ex = await this.show_name(purchase_order_excel, unique_list_translated, excel, lang)
                    const purchase_order_name_pdf = await this.show_name(purchase_order, unique_list_translated, pdf, lang)
                    const purchase_order2_name_ex = await this.show_name(purchase_order2_excel, unique_list_translated, excel, lang)
                    const purchase_order2_name_pdf = await this.show_name(purchase_order2_pdf, unique_list_translated, pdf, lang)
                    const p_spec_name_ex = await this.show_name(prod_spec_excel, unique_list_translated, excel, lang)
                    const p_spec_name_pdf = await this.show_name(prod_spec_pdf, unique_list_translated, pdf, lang)
                    const delivery_request_name_ex = await this.show_name(delivery_request_sale_excel, unique_list_translated, excel, lang)
                    const delivery_request_name_pdf = await this.show_name(delivery_request_sale_pdf, unique_list_translated, pdf, lang)
                    const invoice_name_ex = await this.show_name(invoice_excel, unique_list_translated, excel, lang)
                    const invoice_name_pdf = await this.show_name(invoice, unique_list_translated, pdf, lang)
                    hideName = [
                        quotation_name_ex, quotation_oversea_name_ex, list_price_quotation_name_ex,
                        unit_price_quotation_name_ex, purchase_order_name_ex, purchase_order2_name_ex,
                        p_spec_name_ex, delivery_request_name_ex, invoice_name_ex,
                        quotation_name_pdf, quotation_over_sea_name_pdf, list_price_quotation_name_pdf,
                        unit_price_quotation_name_pdf, purchase_order_name_pdf, purchase_order2_name_pdf,
                        p_spec_name_pdf, delivery_request_name_pdf, invoice_name_pdf,
                        '見積 / オーダ', 'Quotation / Order'
                    ]

                    nextProps.items.print = prints.filter(val => !hideName.includes(val.name))
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
                    await this.english_name(purchase_order_sheet, unique_list_translated)
                    await this.english_name(inspection_order, unique_list_translated)
                    await this.english_name(purchase_order_sheet_EX, unique_list_translated)
                    await this.english_name(inspection_order_EX, unique_list_translated)
                    let excel = [
                        purchase_order_sheet_EX, english_names[purchase_order_sheet_EX + "_pdf"], english_names[purchase_order_sheet_EX + "_excel"],
                        inspection_order_EX, english_names[inspection_order_EX + "_pdf"], english_names[inspection_order_EX + "_excel"],
                        WIP_document_list, english_names[WIP_document_list + "_pdf"], english_names[WIP_document_list + "_excel"],
                        prod_label_sticker, english_names[prod_label_sticker + "_pdf"], english_names[prod_label_sticker + "_excel"]
                    ]
                    let excelArray = [];
                    excel.forEach(excelItem => {
                        let foundItem = prints.find(val => val.display_name === excelItem);
                        if (foundItem) {
                            foundItem.name = foundItem.name.split("(")[0];
                            excelArray.push(foundItem);
                        }
                    })
                    nextProps.items.action = [...action, ...excelArray];

                    showPrint = [
                        purchase_order_sheet, english_names[purchase_order_sheet + "_pdf"], english_names[purchase_order_sheet + "_excel"],
                        inspection_order, english_names[inspection_order + "_pdf"], english_names[inspection_order + "_excel"],
                    ]
                    nextProps.items.print = prints.filter(val => showPrint.includes(val.display_name));
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
                    let actions = [...data_purchase_list.action]
                    let prints = [...data_purchase_list.print]
                    await this.english_name(purchase_order_part, unique_list_translated)
                    await this.english_name(purchase_for_part_excel, unique_list_translated)
                    const purchase_for_part_pdf = [purchase_order_part, english_names[purchase_order_part + "_pdf"], english_names[purchase_order_part + "_excel"]]
                    const purchase_for_part_ex = [purchase_for_part_excel, english_names[purchase_for_part_excel + "_pdf"], english_names[purchase_for_part_excel + "_excel"]]

                    let excel_arr = prints.filter(val => {
                        if (purchase_for_part_ex.includes(val.display_name)) {
                            val.name = val.name.split("-")[0]
                            return val
                        }
                    })
                    nextProps.items.action = [...excel_arr, ...actions]
                    nextProps.items.print = prints.filter(val => purchase_for_part_pdf.includes(val.display_name))
                }
            }

            this.actionItems = await this._setActionItems(nextProps);
            this.printItems = await this._setPrintItems(nextProps);
        }
    });
});
