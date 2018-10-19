openerp.web_window_title = function(instance, local) {
    instance.web.WebClient.include({
        init: function() {
            this._super.apply(this, arguments);
            this.set('title_part', {"zopenerp": document.title});
        }
    });
};