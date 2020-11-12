odoo.define('custom_reports.TrafficStatisticGraph', function(require)   {
    'use strict';

    var BasicFields = require('web.basic_fields');
    var FieldRegistry = require('web.field_registry');

    var COLORS = ['#875a7b', '#21b799', '#E4A900', '#D5653E', '#5B899E', '#E46F78', '#8F8F8F'];

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
            
            var datasets = [];
            var colors = self._getColors(self.graph_data.length);

            self.graph_data.forEach(function (graph_datum, index)   {
                datasets.push({
                    label: graph_datum.data.shop_id.data.display_name,
                    data: JSON.parse(graph_datum.data.all_hour),
                    borderColor: colors[index],
                    fill: false
                })
            });

            console.log(datasets);

            self.config = self._getLineGraph(datasets);
            self._loadChart();
            
        },

        // ----------------------------
        // Private
        // ----------------------------

         /**
         * Returns a line graph
         * @private
         */
        _getLineGraph: function (datasets)   {
            return {
                type: 'line',
                data: {
                   labels: ['12AM', '1AM', '2AM', '3AM', '4AM', '5AM', '6AM', '7AM', '8AM', '9AM', '10AM', '11AM',
                            '12PM', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM', '8PM', '9PM', '10PM', '11PM'],
                   datasets: datasets,
                },
                options:    {
                    title:  {
                        display: true,
                        text: 'Sales per Hour in Day'
                    },
                    scales: {
                        yAxes:  [{
                            ticks:  {
                                beginAtZero: true,
                                callback: function(value, index, values)    {
                                    value = value.toString();
                                    value = value.split(/(?=(?:...)*$)/);
                                    value = value.join('.');
                                    return '$' + value;
                                }
                            }
                        }]
                    }
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
        },

        /**
         * Returns an array of colors
         * @private
         */
        _getColors: function(length) {
            var bgColors = [];
            for (var i = 0; i < length; i++) {
                bgColors.push(COLORS[i % COLORS.length]);  
            }
            return bgColors;
        },

    });

    FieldRegistry.add('traffic_statistic_graph', TrafficStatisticGraph);

});
