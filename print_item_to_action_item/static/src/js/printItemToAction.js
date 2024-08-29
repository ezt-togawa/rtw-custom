odoo.define('print_item_to_action_item.ChangeProp', function (require) {

    const { patch } = require('web.utils');
    const components = { ActionMenus: require('web.ActionMenus') };

    const module_pdf = "custom_report_rtw"
    const module_excel = "rtw_excel_report"

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
            let view = this.env.view.type
            let model = this.env.view.model
            if (view === 'list') {
                if (model == "sale.order") {
                    this.props.items.print = this.props.items.print.filter(val => val.report_file.startsWith(module_pdf))
                } else if (model == "mrp.production") {
                    this.props.items.print = this.props.items.print.filter(val => val.report_file.startsWith(module_pdf) && val.xml_id.split('.')[1] != 'report_mrp_order_rtw')
                } else if (model == "stock.picking") {
                    this.props.items.print = this.props.items.print.filter(val => val.report_file.startsWith(module_pdf))
                } else if (model == "purchase.order") {
                    this.props.items.print = this.props.items.print.filter(val => val.report_file.startsWith(module_pdf) && val.xml_id.split('.')[1] != 'report_purchase_rtw')
                } else if (model == "account.move") {
                    this.props.items.print = this.props.items.print.filter(val => val.report_file.startsWith(module_pdf) && val.xml_id.split('.')[1] != 'report_invoice_rtw')
                } else if (model == "stock.quant") {
                    this.props.items.print = this.props.items.print.filter(val => val.report_file.startsWith(module_pdf))
                }
            }
            if (view == 'form') {
                if (model == "sale.order") {
                    let item_odoo = []
                    let item_cus = []
                    this.props.items.action.filter(val => {
                        if (val.xml_id && val.xml_id.split('.')[0].startsWith(module_excel)) {
                            if (val.xml_id.split('.')[1] == 'report_quotation') item_cus[0] = val
                            else if (val.xml_id.split('.')[1] == 'report_quotation_oversea') item_cus[1] = val
                            else if (val.xml_id.split('.')[1] == 'list_price_quotation') item_cus[2] = val
                            else if (val.xml_id.split('.')[1] == 'unit_price_quotation') item_cus[3] = val
                            else if (val.xml_id.split('.')[1] == 'report_purchase_order') item_cus[4] = val
                            else if (val.xml_id.split('.')[1] == 'report_purchase_order2') item_cus[5] = val
                            else if (val.xml_id.split('.')[1] == 'product_spec') item_cus[6] = val
                            else if (val.xml_id.split('.')[1] == 'sale_delivery_order') item_cus[7] = val
                            else if (val.xml_id.split('.')[1] == 'invoice_sale_order') item_cus[8] = val
                        } else {
                            item_odoo.push(val)
                        }
                    })
                    this.props.items.action = [...item_odoo, ...item_cus];
                    this.props.items.print = this.props.items.print.filter(val => val.report_file.startsWith(module_pdf))
                } else if (model == "mrp.production") {
                    this.props.items.print = this.props.items.print.filter(val => val.report_file.startsWith(module_pdf) && val.xml_id.split('.')[1] != 'report_mrp_order_rtw')
                } else if (model === "stock.picking") {
                    this.props.items.print = this.props.items.print.filter(val => val.report_file.startsWith(module_pdf))
                } else if (model == "purchase.order") {
                    this.props.items.print = this.props.items.print.filter(val => val.report_file.startsWith(module_pdf) && val.xml_id.split('.')[1] != 'report_purchase_rtw')
                } else if (model == "account.move") {
                    this.props.items.print = this.props.items.print.filter(val => val.report_file.startsWith(module_pdf) && val.xml_id.split('.')[1] != 'report_invoice_rtw')
                } else if (model === "product.template") {
                    this.props.items.print = this.props.items.print.filter(val => val.report_file.startsWith(module_pdf))
                }
            }
            this.actionItems = await this._setActionItems(this.props);
            this.printItems = await this._setPrintItems(this.props);
        },

        async _updateData(nextProps) {
            let view = this.env.view.type
            let model = this.env.view.model
            if (view === "list") {
                if (model == "sale.order") {
                    nextProps.items.print = nextProps.items.print.filter(val => val.report_file.startsWith(module_pdf) && val.xml_id.split('.')[1] != 'report_mrp_order_rtw')
                } else if (model == "mrp.production") {
                    nextProps.items.print = nextProps.items.print.filter(val => val.report_file.startsWith(module_pdf))
                } else if (model == "stock.picking") {
                    nextProps.items.print = nextProps.items.print.filter(val => val.report_file.startsWith(module_pdf))
                } else if (model == "account.move") {
                    nextProps.items.print = nextProps.items.print.filter(val => val.report_file.startsWith(module_pdf) && val.xml_id.split('.')[1] != 'report_invoice_rtw')
                } else if (model == "purchase.order") {
                    nextProps.items.print = nextProps.items.print.filter(val => val.report_file.startsWith(module_pdf) && val.xml_id.split('.')[1] != 'report_purchase_rtw')
                } else if (model == "stock.quant") {
                    nextProps.items.print = nextProps.items.print.filter(val => val.report_file.startsWith(module_pdf))
                }
            }
            this.actionItems = await this._setActionItems(nextProps);
            this.printItems = await this._setPrintItems(nextProps);
        }
    });
});
