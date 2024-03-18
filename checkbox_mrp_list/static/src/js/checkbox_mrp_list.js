odoo.define('checkbox_mrp_list.checkbox_onchange', function (require) {

    var ListController = require('web.ListController');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;

    ListController.include({
        renderButtons: function ($node) {
            console.log(222222222222222222222222);
            var self = this;
            this._super.apply(this, arguments);

            // Bắt sự kiện onchange của checkbox
            $('body').on('click', '.o_list_record_selector', function() {
                console.log(1111111111111111111111111111111111111111);
                // if ($(this).hasClass('custom-control-input')) {
                //     // Nếu đây là checkbox "Chọn tất cả"  
                //     console.log('Chọn tất cả được chọn');
                //     // Code xử lý khi checkbox "Chọn tất cả" thay đổi trạng thái
                // } else {
                //     // Nếu đây là các checkbox riêng lẻ
                //     console.log('Checkbox riêng lẻ được chọn');
                //     // Code xử lý khi các checkbox riêng lẻ thay đổi trạng thái
                // }
            });

            // $('body').on('change', '.custom-control-input', function() {
            //     if ($(this).hasClass('o_select_all_rows')) {
            //         // Nếu đây là checkbox "Chọn tất cả"
            //         console.log('Chọn tất cả được chọn');
            //         // Code xử lý khi checkbox "Chọn tất cả" thay đổi trạng thái
            //     } else {
            //         // Nếu đây là các checkbox riêng lẻ
            //         console.log('Checkbox riêng lẻ được chọn');
            //         // Code xử lý khi các checkbox riêng lẻ thay đổi trạng thái
            //     }
            // });
            
            
            

            // $('.o_data_row').on('click', function() {
            //     var isChecked = $(this).find('.custom-control-input').prop('checked');
            //     if (isChecked) {
            //         // Nếu checkbox được chọn
            //         // Thực hiện các hành động cụ thể ở đây
            //         console.log("Checkbox is checked");
            //     } else {
            //         // Nếu checkbox không được chọn
            //         // Thực hiện các hành động cụ thể ở đây
            //         console.log("Checkbox is unchecked");
            //     }
            // });
            

            // this.$buttons.find('.custom-control-input').on('change', function () {
            //     var isChecked = $(this).prop('checked');
            //     if (isChecked) {
            //         console.log(1111111111111111111111);
            //         // Nếu checkbox được chọn
            //         // Thực hiện các hành động cụ thể ở đây
            //         console.log("Checkbox is checked");
            //     } else {
            //         // Nếu checkbox không được chọn
            //         // Thực hiện các hành động cụ thể ở đây
            //         console.log("Checkbox is unchecked");
            //     }
            // });
        },
    });
});
