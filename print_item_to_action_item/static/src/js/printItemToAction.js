odoo.define('print_item_to_action_item.ChangeProp', function (require) {

    const { patch } = require('web.utils');
    const components = { ActionMenus: require('web.ActionMenus') };

    var originalData = null;
    var originalData2 = null;

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
            // var breadcrumbElement = document.querySelector('.breadcrumb');
            // if (breadcrumbElement === null) return
            // let location_now = ""
            // if (breadcrumbElement) {
            //     location_now = breadcrumbElement.textContent?.trim();
            // } else {
            //     location_now = this.env.action.name || this.env.action.display_name
            // }
            let view_type_now = this.env.view.type
            if (view_type_now === 'list') {
                if (this.env.view.model == "stock.picking") {
                    if (originalData === null) {
                        console.log('start chi tao 1 lagn originalData');
                        originalData = {
                            action: [...this.props.items.action],
                            print: [...this.props.items.print],
                        };
                    }
                    let action = [...originalData.action]
                    let prints = [...originalData.print]
                    // task_inventory_delivery_list = ["出荷予定リスト"]    // task_inventory_receipt_list = ["支給予定リスト", "入荷予定リスト"]
                    let excel = ["Add to batch", "Validate", "Unreserve", "出荷予定リスト", "支給予定リスト", "入荷予定リスト"]
                    this.props.items.action = action.filter(val => excel.includes(val.name))
                    // this.nextProps = this.props.items.action.filter(val => excel.includes(val.name))

                    let pdf = ['配送作業依頼書', '出荷依頼書']
                    this.props.items.print = prints.filter(val => !val.display_name.includes('(EXCEL)') && !pdf.includes(val.name))
                }

                // sale_order_view_list
                if (this.env.view.model == "sale.order") {
                    let sale_order_list_print = ['Quotation', '御見積書', '定価見積書', '単価見積り書', '配送作業依頼書', '注文書', '発注書', '請求書', '商品仕様書', '出荷依頼書', '発注書(部材用）', '商品仕様書(EXCEL)']
                    let sale_order_list_action = ['御見積書', '定価見積書', '単価見積り書', '注文書', '発注書', '発注書(部材用）', '商品仕様書']
                    const filterPrintItems = this.props.items.print.filter(val => {
                        return !sale_order_list_print.includes(val.name);
                    });
                    if (filterPrintItems) this.props.items.print = [...filterPrintItems]
                    const filterActionItems = this.props.items.action.filter(val => {
                        return !sale_order_list_action.includes(val.name);
                    });
                    if (filterActionItems) this.props.items.action = [...filterActionItems]
                }

                // task_invoice_list
                if (this.env.view.model == "account.move") {
                    let sale_order_list_print = ['請求書']
                    let sale_order_list_action = ['請求書']
                    const filterPrintItems = this.props.items.print.filter(val => {
                        return !sale_order_list_print.includes(val.name);
                    });
                    if (filterPrintItems) this.props.items.print = [...filterPrintItems]
                    const filterActionItems = this.props.items.action.filter(val => {
                        return !sale_order_list_action.includes(val.name);
                    });
                    if (filterActionItems) this.props.items.action = [...filterActionItems]
                }

                // task_inventory_manfac_list = ["仕掛品伝票一覧"]
                if (this.env.view.model == "mrp.production") {
                    const filterActionItems = this.props.items.print.filter(val => val.display_name.includes('(EXCEL)'));
                    if (filterActionItems) {
                        const actionItemsChange = filterActionItems.filter(val => {
                            if (val.display_name == "仕掛品伝票一覧(EXCEL)" || val.display_name == "商品ラベルシール(EXCEL)") {
                                val.name = val.name.split('(')[0]
                                val.type = 'ir.actions.act_window'
                                val.binding_type = 'action'
                                return val
                            }
                        })
                        this.props.items.action = [...this.props.items.action, ...actionItemsChange]
                    }
                    this.props.items.print = this.props.items.print.filter(val => !val.display_name.includes('(EXCEL)') && val.display_name !== "発注書");
                }

                // task_inventory_reporting = ["棚卸記入リスト"]
                if (this.env.view.model == "stock.quant") {
                    const filterActionItems = this.props.items.print.filter(val => val.display_name === '棚卸記入リスト(EXCEL)');
                    if (filterActionItems) {
                        const actionItemsChange = filterActionItems.filter(val => {
                            val.name = '棚卸記入リスト'
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        })
                        this.props.items.action = [...this.props.items.action, ...actionItemsChange]
                    }
                    this.props.items.print = this.props.items.print.filter(val => !val.display_name.includes('(EXCEL)'));
                }
            }

            if (view_type_now === 'form') {
                // sale_order_view_form
                if (this.env.view.model === "sale.order") {
                    let filterActionItem = this.props.items.print.filter(val => val.display_name === "商品仕様書(EXCEL)")
                    let actionItemFilter = this.props.items.action.filter(val => val.name !== "発注書" && val.name !== "発注書(部材用）")
                    if (filterActionItem) {
                        let actionItem = filterActionItem.filter(val => {
                            val.name = val.name.split("(")[0]
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        })
                        this.props.items.action = [...actionItemFilter, ...actionItem]
                    }
                    const print_items = ['定価見積書', '単価見積り書', '注文書', '御見積書', "商品仕様書"]
                    let filter_print_items = this.props.items.print.filter(val => print_items.includes(val.name))
                    this.props.items.print = filter_print_items.filter(val => val.display_name !== "商品仕様書(EXCEL)")
                }

                // task_inventory_manfac_form= ["商品ラベルシール"]
                if (this.env.view.model === "mrp.production") {
                    const filterActionItems = this.props.items.print.filter(val => val.display_name === '商品ラベルシール(EXCEL)')
                    if (filterActionItems) {
                        const actionItemsChange = filterActionItems.filter(val => {
                            val.name = '商品ラベルシール'
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        })
                        this.props.items.action = [...this.props.items.action, ...actionItemsChange]
                    }
                    this.props.items.print = this.props.items.print.filter(val => !val.display_name.includes('(EXCEL)'));
                }

                // task_template = ["在庫状況一覧"]
                if (this.env.view.model === "product.template") {
                    const filterActionItems = this.props.items.print.filter(val => val.display_name.includes('(EXCEL)'));
                    if (filterActionItems) {
                        const actionItemsChange = filterActionItems.filter(val => {
                            val.name = val.name.split('(')[0]
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        })
                        this.props.items.action = [...this.props.items.action, ...actionItemsChange]
                    }
                    this.props.items.print = this.props.items.print.filter(val => !val.display_name.includes('(EXCEL)'));
                }
                if (this.env.view.model === "stock.picking") {
                    // task_inventory_delivery_form = ["送り状シール(EXCEL)","支給部材明細(EXCEL)"] +recept
                    let excel = ["送り状シール", '配送作業依頼書', '出荷依頼書', "支給部材明細", "検品チェックシート"]
                    this.props.items.action = this.props.items.action.filter(val => excel.includes(val.name))
                    this.props.items.print = this.props.items.print.filter(val => !val.display_name.includes('(EXCEL)'))
                }
            }
            this.actionItems = await this._setActionItems(this.props);
            this.printItems = await this._setPrintItems(this.props);
        },

        async _updateData(nextProps) {
            var breadcrumbElement = document.querySelector('.breadcrumb');
            if (breadcrumbElement === null) return
            let location_now = ""
            if (breadcrumbElement) {
                location_now = breadcrumbElement.textContent?.trim();
            } else {
                location_now = this.env.action.name || this.env.action.display_name
            }
            let view_type_now = this.env.view.type
            if (view_type_now === "list") {
                if (this.env.view.model == "stock.picking") {
                    // // task_inventory_delivery_list = ["出荷予定リスト"]
                    // if (location_now.includes("配送") || location_now.includes("Delivery Orders")) {
                    //     nextProps.items.action = this.nextProps
                    //     let pdf = ['配送作業依頼書', '出荷依頼書']
                    //     nextProps.items.print = nextProps.items.print.filter(val => !val.display_name.includes("(EXCEL)") && !pdf.includes(val.name))
                    // }

                    // // task_inventory_receipt_list = ["支給予定リスト", "入荷予定リスト"]
                    // if (location_now.includes("入荷") || location_now.includes("Receipts")) {
                    //     nextProps.items.action = this.nextProps
                    //     let pdf = ['配送作業依頼書', '出荷依頼書']
                    //     nextProps.items.print = nextProps.items.print.filter(val => !val.display_name.includes('(EXCEL)') && !pdf.includes(val.name))
                    // }

                    if (!originalData2) {
                        console.log('update chi tao 1 lagn originalData');
                        originalData2 = {
                            action: [...nextProps.items.action],
                            print: [...nextProps.items.print],
                        };
                        localStorage.setItem('originalData', originalData)
                    }
                    let action = [...originalData2.action]
                    let prints = [...originalData2.print]
                    let excelArr = ["出荷予定リスト", "支給予定リスト", "入荷予定リスト"]
                    let excelShow = prints.filter(val => excelArr.includes(val.name))
                    nextProps.items.action = [...action, ...excelShow]
                    let pdf = ['配送作業依頼書', '出荷依頼書']
                    nextProps.items.print = prints.filter(val => !val.display_name.includes('(EXCEL)') && !pdf.includes(val.name))
                }

                // let task_sale_order_list
                if (this.env.view.model == "sale.order") {
                    let sale_order_list_print = ['Quotation', '御見積書', '定価見積書', '単価見積り書', '配送作業依頼書', '注文書', '発注書', '請求書', '商品仕様書', '出荷依頼書', '発注書(部材用）', '商品仕様書(EXCEL)']
                    let sale_order_list_action = ['御見積書', '定価見積書', '単価見積り書', '注文書', '発注書', '発注書(部材用）']
                    const filterPrintItems = nextProps.items.print.filter(val => {
                        return !sale_order_list_print.includes(val.name);
                    });
                    if (filterPrintItems) nextProps.items.print = [...filterPrintItems]
                    const filterActionItems = nextProps.items.action.filter(val => {
                        return !sale_order_list_action.includes(val.name);
                    });
                    if (filterActionItems) nextProps.items.action = [...filterActionItems]
                }

                // let task_invoice_list
                if (this.env.view.model == "account.move") {
                    let sale_order_list_print = ['請求書']
                    const filterPrintItems = nextProps.items.print.filter(val => {
                        return !sale_order_list_print.includes(val.name);
                    });
                    if (filterPrintItems) nextProps.items.print = [...filterPrintItems]
                    let sale_order_list_action = ['請求書']
                    const filterActionItems = nextProps.items.action.filter(val => {
                        return !sale_order_list_action.includes(val.name);
                    });
                    if (filterActionItems) nextProps.items.action = [...filterActionItems]
                }

                // let task_manfac_list = ["仕掛品伝票一覧"]
                if (this.env.view.model == "mrp.production") {
                    const filterActionItems = nextProps.items.print.filter(val => val.display_name === "仕掛品伝票一覧(EXCEL)" || val.display_name == "商品ラベルシール(EXCEL)");
                    if (filterActionItems) {
                        nextProps.items.action = [...nextProps.items.action, ...filterActionItems]
                    }
                    nextProps.items.print = nextProps.items.print.filter(val => !val.display_name.includes('(EXCEL)') && val.name !== "発注書");
                }

                // let task_reporting = ["棚卸記入リスト"]
                if (this.env.view.model == "stock.quant") {
                    const filterActionItems = nextProps.items.print.filter(val => val.display_name === '棚卸記入リスト(EXCEL)');
                    if (filterActionItems) {
                        nextProps.items.action = [...nextProps.items.action, ...filterActionItems]
                    }
                    nextProps.items.print = nextProps.items.print.filter(val => !val.display_name.includes('(EXCEL)'));
                }
            }

            // if(view_type_now ==="form"){}
            this.actionItems = await this._setActionItems(nextProps);
            this.printItems = await this._setPrintItems(nextProps);
        }
    });
});
