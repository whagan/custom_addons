odoo.define('custom_reports.CustomReportsListRenderer', function (require)  {
    "use strict";
    
    var ListRenderer = require('web.ListRenderer');
    
    var CustomReportsListRenderer = ListRenderer.extend({
        /**
         * @override
         * 
         */
        init: function (parent, state, params)  {
            this._super(parent, state, params);
            this.hasSelectors = false;
        },
    });

    return CustomReportsListRenderer;

});