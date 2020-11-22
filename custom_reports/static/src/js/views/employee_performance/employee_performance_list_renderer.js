odoo.define('custom_reports.EmployeePerformanceListRenderer', function (require)  {
    "use strict";
    
    var ListRenderer = require('web.ListRenderer');
    
    var EmployeePerformanceListRenderer = ListRenderer.extend({
        /**
         * @override
         * 
         */
        init: function (parent, state, params)  {
            this._super(parent, state, params);
            this.hasSelectors = false;
        },
    });

    return EmployeePerformanceListRenderer;

});