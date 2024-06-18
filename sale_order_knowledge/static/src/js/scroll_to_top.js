odoo.define('sale_order_knowledge.scroll_on_button_click', function (require) {

    var core = require('web.core');

    core.bus.on('DOM_updated', null, function () {
        var observer = new MutationObserver(function (mutations) {
            var knowledgeSupplementButton = document.querySelector('button[name="knowledge_supplement"]');
            var knowledgeSpecialButton = document.querySelector('button[name="knowledge_special"]');

            if (knowledgeSupplementButton) {
                knowledgeSupplementButton.addEventListener('click', function () {
                    scrollToTop();
                });
            }
            if (knowledgeSpecialButton) {
                knowledgeSpecialButton.addEventListener('click', function () {
                    scrollToTop();
                });
            }
        });

        observer.observe(document.body, { childList: true, subtree: true });
    });

    function scrollToTop() {
        var interval = setInterval(function () {
            var modalBody = document.querySelector('.modal-body');
            if (modalBody) {
                modalBody.scrollTop = 0;
                clearInterval(interval);
            }
        }, 500);
    }

});
