odoo.define('sale_order_rtw.accepting_order', function (require) {
    "use strict";

    var FormController = require('web.FormController');

    FormController.include({
        _onButtonClicked: function (ev) {
            if (ev.data.attrs.name === 'accepting_order' && ev.data.attrs.type === 'object') {
                ev.stopPropagation();
                var self = this;
                this._disableButtons();

                var originalStatus = this.model.get(this.handle).data.status || 'draft';

                this.model.notifyChanges(this.handle, { status: 'done' }).then(function (changedFields) {
                    var state = self.model.get(self.handle);
                    return self.renderer.confirmChange(state, state.id, changedFields);
                }).then(function () {
                    var invalidFields = self.renderer.canBeSaved(self.handle);
                    if (invalidFields.length) {
                        self._notifyInvalidFields(invalidFields);
                        var invalidEls = [];
                        invalidFields.forEach(function (fieldName) {
                            var allWidgets = self.renderer.allFieldWidgets[self.handle] || [];
                            allWidgets.forEach(function (widget) {
                                if (widget.name === fieldName) {
                                    var $label = widget.$el.closest('tr').find('.o_td_label .o_form_label');
                                    invalidEls.push({
                                        $widget: widget.$el,
                                        $label: $label,
                                    });
                                }
                            });
                        });
                        return self.model.notifyChanges(self.handle, { status: originalStatus }).then(function (fields) {
                            var state = self.model.get(self.handle);
                            return self.renderer.confirmChange(state, state.id, fields);
                        }).then(function () {
                            invalidEls.forEach(function (info) {
                                info.$widget.addClass('o_field_invalid o_required_modifier');
                                info.$label.addClass('o_field_invalid');
                            });
                            self._enableButtons();
                        });
                    }
                    return self.saveRecord(self.handle, { stayInEdit: true }).then(function () {
                        var record = self.model.get(ev.data.record.id);
                        return self._callButtonAction(ev.data.attrs, record);
                    }).then(function () {
                        self._enableButtons();
                    }).guardedCatch(function () {
                        self._enableButtons();
                    });
                }).guardedCatch(function () {
                    self.model.notifyChanges(self.handle, { status: originalStatus });
                    self._enableButtons();
                });
                return;
            }
            this._super.apply(this, arguments);
        },
    });
});
