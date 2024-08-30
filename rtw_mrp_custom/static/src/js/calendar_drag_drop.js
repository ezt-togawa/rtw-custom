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

            options.eventRender = function (info) {
                var event = info.event;
                var element = $(info.el);
                var view = info.view;
                element.attr('data-event-id', event.id);
                if (view.type === 'dayGridYear') {
                    const color = this.getColor(event.extendedProps.color_index);
                    if (typeof color === 'string') {
                        element.css({
                            backgroundColor: color,
                        });
                    } else if (typeof color === 'number') {
                        element.addClass(`o_calendar_color_${color}`);
                    } else {
                        element.addClass('o_calendar_color_1');
                    }
                } else {
                    var $render = $(self._eventRender(event));
                    element.find('.fc-content').html($render.html());
                    element.addClass($render.attr('class'));
                    if (!element.find('.fc-bg').length) {
                        element.find('.fc-content').after($('<div/>', { class: 'fc-bg' }));
                    }
                    if (view.type === 'dayGridMonth' && event.extendedProps.record) {
                        var start = event.extendedProps.r_start || event.start;
                        var end = event.extendedProps.r_end || event.end;
                        var isSameDayEvent = moment(start).clone().add(1, 'minute').isSame(moment(end).clone().subtract(1, 'minute'), 'day');
                        if (!event.allDay && isSameDayEvent) {
                            element.addClass('o_cw_nobg');
                            if (event.extendedProps.showTime && !self.hideTime) {
                                const displayTime = moment(start).clone().format(self._getDbTimeFormat());
                                const qty = event.extendedProps.record.product_qty;
                                if (qty !== undefined && qty !== null && qty != 0) {
                                    element.find('.fc-content .fc-time').text(`${displayTime} ${qty}`);
                                } else {
                                    element.find('.fc-content .fc-time').text(`${displayTime}`);
                                }
                            }
                        }
                    }
                    element.on('dblclick', function () {
                        self.trigger_up('edit_event', { id: event.id });
                    });
                }
            }
            return options;
        },
    });
});
