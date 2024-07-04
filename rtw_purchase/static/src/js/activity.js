odoo.define('rtw_purchase.check_schedule_activity', function (require) {
    'use strict';

    var AbstractField = require('web.AbstractField');
    var field_registry = require('web.field_registry');
    var core = require('web.core');
    const _lt = core._lt;

    var CheckScheduleActivity = AbstractField.extend({
        fieldDependencies: _.extend({}, AbstractField.prototype.fieldDependencies, {
            check_schedule_icon: { type: 'char' },
            check_schedule_boolean: { type: 'boolean' },
        }),
        label: _lt('日程確認'),
        /**
         * There is no edit mode for this widget, the icon is always readonly.
         *
         * @override
         * @private
         */
        _renderEdit: function () {
            return this._renderReadonly();
        },

        /**
         * Displays the exception icon if there is one.
         *
         * @override
         * @private
         */
        _renderReadonly: function () {
            var self = this;
            this.$el.empty();

            setTimeout(function () {
                if (self.recordData.check_schedule_boolean) {
                    self.$el.removeClass('o_field_empty');
                    self.$el.addClass("text-center text-warning fa fa-lg w-100");
                    self.$el.addClass(self.recordData.check_schedule_icon || '');
                }
            }, 0);
        }
    });
    field_registry.add('check_schedule_activity', CheckScheduleActivity);

    return CheckScheduleActivity;
});
