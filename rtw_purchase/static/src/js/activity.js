odoo.define('rtw_purchase.check_schedule_activity', function (require) {
    'use strict';

    var AbstractField = require('web.AbstractField');
    var field_registry = require('web.field_registry');
    var ListRenderer = require('web.ListRenderer');
    var core = require('web.core');
    const _lt = core._lt;

    // Override ListRenderer to disable sorting on specific columns
    ListRenderer.include({
        _renderHeaderCell: function (node) {
            var $th = this._super.apply(this, arguments);
            if (node.attrs.name === 'schedule_check') {
                $th.removeClass('o_column_sortable ');
            }
            return $th;
        }
    });

    var CheckScheduleActivity = AbstractField.extend({
        fieldDependencies: _.extend({}, AbstractField.prototype.fieldDependencies, {
            check_schedule_icon: { type: 'char' },
            check_schedule_boolean: { type: 'boolean' },
            schedule_check: { type: 'selection' },
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
