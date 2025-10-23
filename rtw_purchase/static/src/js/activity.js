odoo.define('rtw_purchase.check_schedule_activity', function (require) {
    'use strict';

    var AbstractField = require('web.AbstractField');
    var field_registry = require('web.field_registry');
    var ListRenderer = require('web.ListRenderer');
    var core = require('web.core');
    const _lt = core._lt;
    var ActionManager = require('web.ActionManager');

    ActionManager.include({
        _handleAction: function (action, options) {
            if (action.type === 'ir.actions.act_url' && action.target && action.target !== 'self') {
                window.open(action.url, action.target);
                return Promise.resolve();
            }
            return this._super.apply(this, arguments);
        },
    });

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

    var HtmlButtonWidget = AbstractField.extend({
        supportedFieldTypes: ['html'],
        
        init: function () {
            this._super.apply(this, arguments);
        },
        
        _render: function () {
            this.$el.html(this.value || '');
            this._bindButtonEvents();
        },
        
        _bindButtonEvents: function () {
            var self = this;
            
            this.$el.off('click.html_button');
            
            this.$el.on('click.html_button', 'button', function (event) {
                event.preventDefault();
                event.stopPropagation();
                
                var $button = $(event.currentTarget);
                var methodName = $button.attr('name');
                var recordId = $button.data('id');
                
                if (methodName) {
                    var targetId = recordId ? parseInt(recordId) : (self.record ? self.record.data.id : null);
                    
                    if (targetId) {
                        self._rpc({
                            model: self.model,
                            method: methodName,
                            args: [[targetId]],
                            context: self.record ? self.record.getContext() : {},
                        }).then(function (result) {
                            if (result && result.type) {
                                self.do_action(result);
                            }
                        }).catch(function (error) {
                            console.error("Error calling method:", error);
                        });
                    } else {
                        console.error("No record ID found");
                    }
                }
            });
        },
    });

    field_registry.add('html_button', HtmlButtonWidget);

    return CheckScheduleActivity;
});
