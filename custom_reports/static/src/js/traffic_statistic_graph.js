odoo.define('custom_reports.TrafficStatisticGraph', function(require)   {
    'use strict';

    var BasicFields = require('web.basic_fields');
    var FieldRegistry = require('web.field_registry');

    var TrafficStatisticGraph = BasicFields.FieldText.extend({
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],
        template: 'traffic_statistic_graph_template',
        xmlDependencies: ['custom_reports/static/src/xml/traffic_statistic_graph.xml'],
        
        /**
         * @override
         */
        init: function () {
            this._super.apply(this, arguments);
            console.log(this);
            console.log('Widget initialized');
        },

        /**
         * @override
         */
        start: function()   {
            var self = this;
            // self.graph_type = "pie";
            
    
            console.log(this.$('canvas').attr('id'));
            self.config = self._getBarGraph();



            
            self._loadChart();
            
        },

        // ----------------------------
        // Private
        // ----------------------------

        /**
         * Returns a bar graph
         * @private
         */
        _getBarGraph: function ()   {
            return {
                type: 'bar',
                data: {
                   labels: ['Marc Demo', 'Mitchell Admin', 'Paul Williams', 'Ronnie Hart', 'Randall Lewis'],
                   datasets: [{
                       label: 'Employee Performances',
                       data: [44, 24, 37, 12, 8],
                       backgroundColor: ["#1f77b4", "#c5b0d5", "#e377c2", "#7f7f7f", "#dbdb8d"],
                    }]
                },
            };
        },



        /**
         * Loads chart 
         * @private
         */
        _loadChart: function()  {
            var canvas = this.$('canvas')[0];
            var context = canvas.getContext('2d');
            return new Chart(context, this.config);
        }

    });

    FieldRegistry.add('traffic_statistic_graph', TrafficStatisticGraph);

});
