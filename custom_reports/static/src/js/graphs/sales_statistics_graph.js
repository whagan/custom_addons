
odoo.define('custom_reports.SalesStatisticGraph', function(require)   {
    'use strict';

    var core = require('web.core');

    var BasicFields = require('web.basic_fields');
    var FieldRegistry = require('web.field_registry');

    var COLORS = ['#875a7b', '#21b799', '#E4A900', '#D5653E', '#5B899E', '#E46F78', '#8F8F8F'];

    var SalesStatisticGraph = BasicFields.FieldText.extend({
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],
        template: 'sales_statistic_graph_template',
        xmlDependencies: ['custom_reports/static/src/xml/sales_statistic_graph.xml'],
        
        /**
         * @override
         */
        init: function () {
            this._super.apply(this, arguments);
            this.graph_data = arguments[2].data.sales_statistic_ids.data;
            this.graph_type = this.attrs.options.graph_type;
        },

        /**
         * @override
         */
        start: function()   {
            var self = this;
            var labels = [];
            var data = [];

            // get data
            self.graph_data.forEach(graph_datum =>  {
                labels.push(graph_datum.data.location_id.data.display_name);
                data.push(graph_datum.data.sales_location);
            });

            // get colors
            var colors = self._getColors(data.length);

            // set graph type
            switch (self.graph_type) {
                case 'bar':
                    self.config = self._getBarGraph(labels, data, colors);
                    break;
                case 'pie':
                    self.config = self._getPieGraph(labels, data, colors);
                    break;
                case 'doughnut':
                    self.config = self._getDoughnutGraph(labels, data, colors);
                    break;
                case 'polarArea':
                    self.config = self._getPolarGraph(labels, data, colors);
                    break;
                case 'radar':
                    self.config = self._getRadarGraph(labels, data, colors);
                    break;
            }

            // load
            self._loadChart();
        },

        // ----------------------------
        // Private
        // ----------------------------

        /**
         * Returns a bar graph
         * @private
         */
        _getBarGraph: function (labels, data, colors)   {
            return {
                type: 'bar',
                data: {
                   labels: labels,
                   datasets: [{
                       label: 'Sales Statistics',
                       data: data,
                       backgroundColor: colors,
                    }]
                },
            };
        },

        /**
         * Returns a pie graph
         * @private
         */
        _getPieGraph: function (labels, data, colors)   {
            return {
                type: 'pie',
                data: {
                   labels: labels,
                   datasets: [{
                       label: 'Sales Statistics',
                       data: data,
                       backgroundColor: colors,
                    }]
                },
            };
        },

        /**
         * Returns a doughnut graph
         * @private
         */
        _getDoughnutGraph: function (labels, data, colors)   {
            return {
                type: 'doughnut',
                data: {
                   labels: labels,
                   datasets: [{
                       label: 'Sales Statistics',
                       data: data,
                       backgroundColor: colors,
                    }]
                },
            };
        },

        /**
         * Returns a polar graph
         * @private
         */
        _getPolarGraph: function (labels, data, colors)   {
            return {
                type: 'polarArea',
                data: {
                   labels: labels,
                   datasets: [{
                       label: 'Sales Statistics',
                       data: data,
                       backgroundColor: colors,
                    }]
                },
            };
        },

        /**
         * Returns a radar graph
         * @private
         */
        _getRadarGraph: function (labels, data, colors)   {
            return {
                type: 'radar',
                data: {
                   labels: labels,
                   datasets: [{
                       label: 'Sales Statistics',
                       data: data,
                       backgroundColor: colors,
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
        },

        /**
         * Returns an array of colors
         * @private
         */
        _getColors: function(length)    {
            var bgColors = [];
            for (var i = 0; i < length; i++)    {
                bgColors.push(COLORS[i % COLORS.length]);
            }
            return bgColors;
        },

    });

    FieldRegistry.add('sales_statistic_graph', SalesStatisticGraph);

});
