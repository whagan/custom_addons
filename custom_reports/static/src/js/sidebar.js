odoo.define('custom_reports.bh_sidebar', function(require)   {
    'use strict';

    var Widget = require('web.Widget');
    var Registry = require('web.widget_registry');
    var core = require('web.core');

    var QWeb =  core.qweb;
    var _t = core._t;

    var bh_sidebar = Widget.extend({
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],
        template: 'bh_sidebar_template',
        
        /**
         * @override
         */
        init: function(parent) {
            var self = this;
            this._super(parent);
            console.log()
            console.log('Widget initialized');

        },

        start: function()   {
            var self = this;
            console.log(this.getParent().$el);
            //this.$el.append(QWeb.render('bh_sidebar_template'));
        },

    


    });

    Registry.add('bh_sidebar', bh_sidebar);

});