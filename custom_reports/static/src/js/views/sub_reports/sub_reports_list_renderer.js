odoo.define('custom_reports.SubReportsListRenderer', function (require)  {
    "use strict";
    
    var ListRenderer = require('web.ListRenderer');
    
    var SubReportsListRenderer = ListRenderer.extend({
        /**
         * @override
         * 
         */
        init: function (parent, state, params)  {
            this._super(parent, state, params);
            this.activeActions.export_xlsx = false;
        },
    });

    return SubReportsListRenderer;

});