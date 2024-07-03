odoo.define('rtw_mrp_custom.calendar_drag_drop', function (require) {

    var CalendarRenderer = require('web.CalendarRenderer');
    var core = require('web.core');

    CalendarRenderer.include({
        /**
         * Override _getFullCalendarOptions to extend FullCalendar options and handle event drag and drop.
         *
         * @override
         * @param {Object} fcOptions - Existing FullCalendar options
         * @returns {Object} - Extended FullCalendar options
         */
        _getFullCalendarOptions: function (fcOptions) {
            var self = this;
            var options = this._super(fcOptions);

            options.eventDrop = function (eventDropInfo) {
                var event = self._convertEventToFC3Event(eventDropInfo.event);
                self._handleMRPProductionDrag(eventDropInfo.event);
                self.trigger_up('dropRecord', event);
            };
            return options;
        },

        /**
         * Custom method to handle MRP production order drag and drop.
         *
         * @param {Object} event - FullCalendar event object
         * @private
         */
        _handleMRPProductionDrag: async function (event) {
            var record_drag_drop = {
                id: event.id,
                time: event.end.toISOString()
            };
            await this._rpc({
                model: 'mrp.production',
                method: 'update_date_planned_start',
                args: [record_drag_drop],
            });
            return
        },
    });
});
