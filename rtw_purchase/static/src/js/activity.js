odoo.define('rtw_purchase.check_schedule_activity', function (require) {

    var AbstractField = require('web.AbstractField');
    var field_registry = require('web.field_registry');
    var core = require('web.core');
    var _t = core._t;

    var CheckScheduleActivity = AbstractField.extend({
        noLabel: true,
        fieldDependencies: _.extend({}, AbstractField.prototype.fieldDependencies, {
            check_schedule_icon: { type: 'char' },
            check_schedule_boolean: { type: 'boolean' },
        }),

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
                    self.$el.addClass("pull-right text-warning fa");
                    self.$el.addClass(self.recordData.check_schedule_icon || '');
                    self.$el.attr({
                        title: _t('日程確認')
                    });
                    self.$el.tooltip({
                        placement: 'top',
                        container: 'body'
                    });
                }
            }, 0);
        }
    });
    field_registry.add('check_schedule_activity', CheckScheduleActivity);

    return CheckScheduleActivity;
});
