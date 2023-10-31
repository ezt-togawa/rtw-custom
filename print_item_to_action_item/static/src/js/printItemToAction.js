odoo.define('print_item_to_action_item.ChangeProp', function (require) {
    "use strict";
    const { patch } = require('web.utils');
    const components = { ActionMenus: require('web.ActionMenus') };

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
            var breadcrumbElement = document.querySelector('.breadcrumb');
            if (breadcrumbElement === null) return
            let location_now = ""
            if (breadcrumbElement) {
                location_now = breadcrumbElement.textContent?.trim();
            } else {
                location_now = this.env.action.name || this.env.action.display_name
            }
            let view_type_now = this.env.view.type

            if (view_type_now === 'list') {
                // sale_order_view_list
                if (location_now.includes("Quotations") || location_now.includes("Transfers")) {
                    if (this.env.view.model == "sale.order") {
                        let sale_order_list_print = ['御見積書', '定価見積書', '単価見積り書', '配送作業依頼書', '注文書', '発注書', '請求書', '商品仕様書', '出荷依頼書', '発注書(部材用）', '商品仕様書(EXCEL)']
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

                    if (this.env.view.model == "stock.picking") {
                        this.props.items.action = [...this.props.items.action, ...this.props.items.print.filter(val => {
                            if (val.display_name === "出荷予定リスト(EXCEL)") {
                                val.name = val.name.split("(")[0]
                                return val
                            }
                        })]
                        this.props.items.print = this.props.items.print.filter(val => !val.display_name.includes("(EXCEL)") && val.name !== "配送作業依頼書" && val.name !== "出荷依頼書")
                    }
                }
                // task_invoice_list
                if (location_now.includes("Invoices")) {
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

                // task_inventory_reporting = ["棚卸記入リスト"]
                if ((location_now.includes("Stock On Hand") || location_now.includes("Update Quantity"))) {
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

                // task_inventory_manfac_list = ["仕掛品伝票一覧"]
                if (location_now.includes("Manufacturing Orders")) {
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
                    this.props.items.print = this.props.items.print.filter(val => !val.display_name.includes('(EXCEL)') && !val.name.includes('発注書')&& !val.name.includes('発注書(部材用）'))
                }

                // task_inventory_delivery_list = ["出荷予定リスト"]
                if ((location_now.includes("Delivery Orders") || location_now.includes("To Do"))) {
                    const excelFilter = this.props.items.print.filter(val => val.display_name === "出荷予定リスト(EXCEL)")
                    if (excelFilter) {
                        const actionItemsChange = excelFilter.filter(val => {
                            val.name = val.name.split('(')[0]
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        })
                        this.props.items.action = [...this.props.items.action, ...actionItemsChange]
                    }
                    let pdf = ['配送作業依頼書', '出荷依頼書']
                    this.props.items.print = this.props.items.print.filter(val => !val.display_name.includes("(EXCEL)") && !pdf.includes(val.name))
                }

                // task_inventory_receipt_list = ["支給予定リスト", "入荷予定リスト"]
                if ((location_now.includes("Receipts") || location_now.includes("To Do"))) {
                    const excelFilter = this.props.items.print.filter(val => val.display_name === "支給予定リスト(EXCEL)" || val.display_name === "入荷予定リスト(EXCEL)")
                    if (excelFilter) {
                        const actionItemsChange = excelFilter.filter(val => {
                            val.name = val.name.split('(')[0]
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        })
                        this.props.items.action = [...this.props.items.action, ...actionItemsChange]
                    }
                    let pdf = ['配送作業依頼書', '出荷依頼書']
                    this.props.items.print = this.props.items.print.filter(val => !val.display_name.includes('(EXCEL)') && !pdf.includes(val.name))
                }
            }

            if (view_type_now === 'form') {
                // sale_order_view_form
                if (location_now.includes("Quotations") || location_now.includes("Transfers")) {
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
                        this.props.items.print = this.props.items.print.filter(val => !val.display_name.includes("EXCEL") && val.name !== "発注書" && val.name !== "発注書(部材用）" && val.name !== "請求書")
                    }

                    if (this.env.view.model === "stock.picking") {
                        const filterActionItem2 = this.props.items.print.filter(val => val.display_name === "送り状シール(EXCEL)" || val.display_name === "支給部材明細(EXCEL)")
                        if (filterActionItem2) {
                            const actionItemsChange = filterActionItem2.filter(val => {
                                val.name = val.name.split('(')[0]
                                val.type = 'ir.actions.act_window'
                                val.binding_type = 'action'
                                return val
                            })
                            this.props.items.action = [...this.props.items.action, ...actionItemsChange]
                        }
                        this.props.items.print = this.props.items.print.filter(val => !val.display_name.includes("EXCEL"))
                    }
                }

                // task_template = ["在庫状況一覧"]
                if (location_now.includes("Configurable Templates")) {
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

                // task_inventory_manfac_form= ["商品ラベルシール"]
                if (location_now.includes("Manufacturing Orders")) {
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

                // task_inventory_delivery_form = ["送り状シール(EXCEL)","支給部材明細(EXCEL)"]
                if (location_now.includes("Delivery Orders") || location_now.includes("To Do")) {
                    let active_id = window.location.href.split("&").filter(val => val.includes("active_id="))[0].split("=")[1]

                    const excelFilter = this.props.items.print.filter(val => val.display_name === "送り状シール(EXCEL)" || val.display_name === "支給部材明細(EXCEL)")
                    if (excelFilter) {
                        const actionItemsChange = excelFilter.filter(val => {
                            val.name = val.name.split('(')[0]
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        })
                        this.props.items.action = [...this.props.items.action, ...actionItemsChange]
                    }
                    this.props.items.print = this.props.items.print.filter(val => !val.display_name.includes('(EXCEL)'))
                }

                // task_inventory_receipt_form = ["検品チェックシート"]
                if ((location_now.includes("Receipts") || location_now.includes("To Do"))) {
                    const excelFilter = this.props.items.print.filter(val => val.display_name === "検品チェックシート(EXCEL)")
                    const filterActionItems = this.props.items.action.filter(val => !val.name === "配送作業依頼書" || !val.name === "出荷依頼書")
                    if (excelFilter && filterActionItems) {
                        const actionItemsChange = excelFilter.filter(val => {
                            val.name = val.name.split('(')[0]
                            val.type = 'ir.actions.act_window'
                            val.binding_type = 'action'
                            return val
                        })
                        this.props.items.action = [...filterActionItems, ...actionItemsChange]
                    }
                    let pdf = ['配送作業依頼書', '出荷依頼書']
                    this.props.items.print = this.props.items.print.filter(val => !val.display_name.includes('(EXCEL)') && !pdf.includes(val.name))
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

            // let task_sale_order_list
            if ((location_now.includes("Quotations") || location_now.includes("Transfers")) && (view_type_now === "list")) {
                if (this.env.view.model == "sale.order") {
                    let sale_order_list_print = ['御見積書', '定価見積書', '単価見積り書', '配送作業依頼書', '注文書', '発注書', '請求書', '商品仕様書', '出荷依頼書', '発注書(部材用）', '商品仕様書(EXCEL)']
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

                if (this.env.view.model == "stock.picking") {
                    nextProps.items.action = [...nextProps.items.action, ...nextProps.items.print.filter(val => val.display_name === "出荷予定リスト(EXCEL)")]
                    nextProps.items.print = nextProps.items.print.filter(val => !val.display_name.includes("(EXCEL)") && val.name !== "配送作業依頼書" && val.name !== "出荷依頼書")
                }
            }

            // let task_invoice_list
            if (location_now.includes("Invoices") && (view_type_now === "list")) {
                let sale_order_list_action = ['請求書']
                const filterActionItems = nextProps.items.action.filter(val => {
                    return !sale_order_list_action.includes(val.name);
                });
                if (filterActionItems) nextProps.items.action = [...filterActionItems]
            }

            // let task_reporting = ["棚卸記入リスト"]
            if ((location_now == "Stock On Hand" || location_now == "Update Quantity") && (view_type_now == "list")) {
                const filterActionItems = nextProps.items.print.filter(val => val.display_name === '棚卸記入リスト(EXCEL)');
                if (filterActionItems) {
                    nextProps.items.action = [...nextProps.items.action, ...filterActionItems]
                }
                nextProps.items.print = nextProps.items.print.filter(val => !val.display_name.includes('(EXCEL)'));
            }

            // let task_manfac_list = ["仕掛品伝票一覧"]
            if (location_now.includes("Manufacturing Orders") && view_type_now == "list") {
                const filterActionItems = nextProps.items.print.filter(val => val.display_name === "仕掛品伝票一覧(EXCEL)" || val.display_name == "商品ラベルシール(EXCEL)");
                if (filterActionItems) {
                    nextProps.items.action = [...nextProps.items.action, ...filterActionItems]
                }
                nextProps.items.print = nextProps.items.print.filter(val => !val.display_name.includes('(EXCEL)') && !val.name.includes('発注書')&& !val.name.includes('発注書(部材用）'));
            }

            // let task_manfac_form = ["商品ラベルシール"]
            if (location_now.includes("Manufacturing Orders") && view_type_now == "form") {
                const filterActionItems = nextProps.items.print.filter(val => val.display_name.includes('(EXCEL)'));
                if (filterActionItems) {
                    const actionItemsChange = filterActionItems.filter(val => {
                        if (val.name.split('(')[0] == "商品ラベルシール") {
                            return val
                        }
                    })
                    nextProps.items.action = [...nextProps.items.action, ...actionItemsChange]
                }
                nextProps.items.print = nextProps.items.print.filter(val => !val.display_name.includes('(EXCEL)'));
            }

            // let task_receipt_list = ["支給予定リスト", "入荷予定リスト"]
            if ((location_now.includes("Receipts") || location_now.includes("To Do")) && view_type_now == "list") {
                const excelFilter = nextProps.items.print.filter(val => val.display_name === "支給予定リスト(EXCEL)" || val.display_name === "入荷予定リスト(EXCEL)")
                if (excelFilter) {
                    nextProps.items.action = [...nextProps.items.action, ...excelFilter]
                }
                let pdf = ['配送作業依頼書', '出荷依頼書']
                nextProps.items.print = nextProps.items.print.filter(val => !val.display_name.includes("(EXCEL)") && !pdf.includes(val.name))
            }

            // let task_delivery_list = ["出荷予定リスト"]
            if ((location_now.includes("Delivery Orders") || location_now.includes("To Do")) && view_type_now == "list") {
                const excelFilter = nextProps.items.print.filter(val => val.display_name === "出荷予定リスト(EXCEL)")
                if (excelFilter) {
                    nextProps.items.action = [...nextProps.items.action, ...excelFilter]
                }

                let pdf = ['配送作業依頼書', '出荷依頼書']
                nextProps.items.print = nextProps.items.print.filter(val => !val.display_name.includes("(EXCEL)") && !pdf.includes(val.name))
            }

            this.actionItems = await this._setActionItems(nextProps);
            this.printItems = await this._setPrintItems(nextProps);
        }
    });
});
