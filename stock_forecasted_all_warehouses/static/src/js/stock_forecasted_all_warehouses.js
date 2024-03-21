odoo.define('stock_forecasted_all_warehouses.custom_forecasted', function (require) {
  "use strict";

  const clientAction = require('report.client_action');
  const core = require('web.core');
  const dom = require('web.dom');
  const GraphView = require('web.GraphView');

  const qweb = core.qweb;
  const _t = core._t;
  const ReplenishReportCustom = core.action_registry.map.replenish_report.include({
    /**
        * TODO
        * @returns {Promise}
        */
    _renderWarehouseFilters: function () {
      return this._rpc({
        model: 'report.stock.report_product_product_replenishment',
        method: 'get_filter_state',
        context: this.context
      }).then((res) => {
        const warehouses = res.warehouses;
        if (!warehouses) {
          return ReplenishReportCustom
        }
        const active_warehouse = (this.active_warehouse && this.active_warehouse.id) || res.active_warehouse;
        if (active_warehouse) {
          this.active_warehouse = _.findWhere(warehouses, { id: active_warehouse });
        } else {
          this.active_warehouse = warehouses[0];
        }
        const $filters = $(qweb.render('warehouseFilter', {
          active_warehouse: this.active_warehouse,
          warehouses: warehouses,
          displayWarehouseFilter: (warehouses.length >= 1),
          active_id: this.context.active_id
        }));
        // Bind handlers.
        $filters.on('click', '.warehouse_filter', this._onClickFilter.bind(this));
        this.$('.o_search_options').append($filters);
      });
    },
    /** @returns {Array}
     */
    _getReportDomain: function () {
      const domain = [
        ['state', '=', 'forecast'],
        ['warehouse_id', '=', this.active_warehouse ? this.active_warehouse.id : null],
      ];
      if (this.resModel === 'product.template') {
        domain.push(['product_tmpl_id', '=', this.productId]);
      } else if (this.resModel === 'product.product') {
        domain.push(['product_id', '=', this.productId]);
      }
      return domain;
    },
  });
  return ReplenishReportCustom;

});

