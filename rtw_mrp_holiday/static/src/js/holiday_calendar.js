odoo.define('rtw_mrp_holiday.holiday_calendar', function (require) {
    'use strict';

    var CalendarController = require('web.CalendarController');
    var CalendarRenderer = require('web.CalendarRenderer');

    // モデルごとの「開始予定日が休日か」を返す項目
    var HOLIDAY_FLAG_FIELDS = {
        'mrp.production': 'is_planned_start_holiday',
        'mrp.workorder': 'is_plan_date_holiday',
    };

    CalendarRenderer.include({
        _getFullCalendarOptions: function (fcOptions) {
            var self = this;
            var options = this._super(fcOptions);
            if (!HOLIDAY_FLAG_FIELDS[this.model]) {
                return options;
            }
            var datesRender = options.datesRender;
            options.datesRender = function () {
                if (datesRender) {
                    datesRender.apply(this, arguments);
                }
                self._paintHolidays(arguments[0].view);
            };
            return options;
        },

        _paintHolidays: function (view) {
            var self = this;
            $(this.calendarElement).addClass('o_rtw_holiday_calendar');
            var start = moment(view.activeStart).format('YYYY-MM-DD');
            var end = moment(view.activeEnd).subtract(1, 'day').format('YYYY-MM-DD');
            this._rpc({
                model: 'mrp.holiday',
                method: 'get_holiday_dates',
                args: [start, end],
            }).then(function (dates) {
                if (self.isDestroyed()) {
                    return;
                }
                var $cells = $(self.calendarElement).find('td[data-date], th[data-date]');
                $cells.removeClass('o_rtw_holiday');
                dates.forEach(function (date) {
                    $cells.filter('[data-date="' + date + '"]').addClass('o_rtw_holiday');
                });
            });
        },
    });

    CalendarController.include({
        _updateRecord: function (record) {
            var self = this;
            var promise = this._super.apply(this, arguments);
            var flagField = HOLIDAY_FLAG_FIELDS[this.modelName];
            if (!flagField || !record.id) {
                return promise;
            }
            return promise.then(function () {
                return self._warnIfHoliday(parseInt(record.id, 10), flagField);
            });
        },

        _warnIfHoliday: function (id, flagField) {
            var self = this;
            return this._rpc({
                model: this.modelName,
                method: 'read',
                args: [[id], [flagField]],
            }).then(function (rows) {
                if (rows.length && rows[0][flagField]) {
                    self.displayNotification({
                        type: 'warning',
                        title: '休日です',
                        message: '開始予定日が休日になっています。',
                    });
                }
            });
        },
    });
});
