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
            this.graph_data = this.record.data.traffic_statistic_ids.data;
            console.log(this.graph_data);
        },

        /**
         * @override
         */
        start: function()   {
            var self = this;
            // var colors = self._getColors(data.length);
            // var datasets = []

            var labels = [];
            // var data = [];

            self.graph_data.forEach(graph_datum =>  {
                labels.push(graph_datum.data.shop_id.data.display_name);
            //     data.push(graph_datum.data.sales_hour.toFixed(2));
            });

            console.log(labels);

            self.config = self._getLineGraph();
            self._loadChart();
            
        },

        // ----------------------------
        // Private
        // ----------------------------


         /**
         * Returns a line graph
         * @private
         */
        _getLineGraph: function ()   {
            return {
                type: 'line',
                data: {
                   labels: ['12AM', '1AM', '2AM', '3AM', '4AM', '5AM', '6AM', '7AM', '8AM', '9AM', '10AM', '11AM',
                            '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM', '11PM'],
                   datasets: [{
                       label: 'ClickIt July Sale Ad',
                       data: [7, 5, 8, 5, 7, 10, 8, 7, 2, 4, 3, 1, 2, 3, 4, 5, 6, 6, 7, 3, 4, 5, 5, 9],
                       borderColor: "#8e5ea2",
                       fill: false
                    },  {
                        label: 'ClickIt August Sale Ad',
                        data: [7, 5, 8, 5, 9, 10, 6, 7, 5, 4, 3, 1, 2, 3, 4, 5, 4, 4, 7, 3, 4, 7, 10, 9],
                        borderColor: "#3cba9f",
                        fill: false

                    },  {
                        label: 'ClickIt September Sale Ad',
                        data: [4, 5, 3, 5, 6, 1, 6, 9, 5, 4, 5, 2, 2, 3, 4, 5, 7, 3, 7, 3, 4, 7, 8, 7],
                        borderColor: "#c45850",
                        fill: false
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
