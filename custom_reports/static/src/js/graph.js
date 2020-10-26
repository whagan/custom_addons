odoo.define('custom_reports.graph', function(require)    {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var core = require('web.core');
    var field_registry = require('web.field_registry');
    var utils = require('web.utils');

    var _t = core._t;

    var GraphWidget = AbstractField.extend({
        className: "oe_custom_graph",
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],

        /**
         * @override
         * @private
         */
        _render: function() {
           
            var config =    {
                type: 'bar',
                data: {
                   labels: ['React', 'Angular', 'Vue', 'Hyperapp', 'Omi'],
                   datasets: [{
                       label: 'Github Stars',
                       data: [135850, 52122, 148825, 16939, 9763];
                   }]
                },
            }
        
            this.$canvas = $('<canvas/>');
            this.$el.empty();
            this.$el.append(this.$canvas);
            this.$el.css({position: 'relative'});
            var context = this.$canvas[0].getContext('2d');
            this.chart = new Chart(context,config);
        },
    });
    field_registry.add("custom_graph", CustomGraphWidget);
    return CustomGraphWidget;
})