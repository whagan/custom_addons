odoo.define('custom_reports.CustomWidgetTwo', function(require)    {
    console.log("HEY WILL");
    'use strict';

    var _t = require('web.core')._t;
    var ajax = require('web.ajax');
    var publicWidget = require('web.public.widget');
    
    publicWidget.registry.PieChartTwo = publicWidget.Widget.extend({
        selector: '#o_custom_report_graph_two',
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],
        /**
         * @override
         * @param   {Object}    parent
         */
        start: function(parent)   {
            var defs = [this._super.apply(this, arguments)];

            return Promise.all(defs);
        },
    });

    
   return publicWidget.registry.PieChartTwo;

});

  