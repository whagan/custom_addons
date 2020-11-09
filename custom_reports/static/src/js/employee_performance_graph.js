odoo.define('custom_reports.EmployeePerformanceGraph', function(require)   {
    'use strict';

    var core = require('web.core');

    var BasicFields = require('web.basic_fields');
    var FieldRegistry = require('web.field_registry');

    var COLORS = ['#875a7b', '#21b799', '#E4A900', '#D5653E', '#5B899E', '#E46F78', '#8F8F8F'];

    var EmployeePerformanceGraph = BasicFields.FieldText.extend({
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],
        template: 'employee_performance_graph_template',
        xmlDependencies: ['custom_reports/static/src/xml/employee_performance_graph.xml'],
        
        /**
         * @override
         */
        init: function () {
            this._super.apply(this, arguments);
            this.graph_data = arguments[2].data.employee_performance_ids.data;
            this.graph_type = this.attrs.options.graph_type;
        },

        /**
         * @override
         */
        start: function()   {
            var self = this;
            var labels = [];
            var data = [];

            self.graph_data.forEach(graph_datum =>  {
                labels.push(graph_datum.data.employee_id.data.display_name);
                data.push(graph_datum.data.sales_hour);
            });

            var colors = self._getColors(data.length);

            switch (self.graph_type) {
                case 'bar':
                    self.config = self._getBarGraph(labels, data, colors);
                    break;
                // case 'line':
                //     self.config = self._getLineGraph(labels, data, colors);
                //     break;
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
                       label: 'Employee Performances',
                       data: data,
                       backgroundColor: colors,
                    }]
                },
            };
        },

        //  /**
        //  * Returns a line graph
        //  * @private
        //  */
        // _getLineGraph: function (labels, data, colors)   {
        //     return {
        //         type: 'line',
        //         data: {
        //            labels: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        //            datasets: [{
        //                label: 'ClickIt July Sale Ad',
        //                data: [20, 22, 24, 27, 25, 44, 35, 27, 12, 8, 7],
        //                borderColor: "#8e5ea2",
        //                fill: false
        //             },  {
        //                 label: 'ClickIt August Sale Ad',
        //                 data: [18, 20, 24, 29, 35, 37, 45, 50, 45, 40, 35],
        //                 borderColor: "#3cba9f",
        //                 fill: false

        //             },  {
        //                 label: 'ClickIt September Sale Ad',
        //                 data: [27, 25, 29, 32, 30, 37, 55, 60, 65, 50, 30],
        //                 borderColor: "#c45850",
        //                 fill: false
        //             },  {
        //                 label: 'ClickIt October Sale Ad',
        //                 data: [35, 29, 29, 32, 48, 50, 55, 60, 67, 70, 65],
        //                 borderColor: "#3e95cd",
        //                 fill: false
        //             }]
        //         },
        //     };
        // },

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
                       label: 'Employee Performances',
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
                       label: 'Employee Performances',
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
                       label: 'Employee Performances',
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
                       label: 'Employee Performances',
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
        _getColors: function(length) {
            var bgColors = [];
            for (var i = 0; i < length; i++) {
                bgColors.push(COLORS[i % COLORS.length]);  
            }
            return bgColors;
        },

    });

    FieldRegistry.add('employee_performance_graph', EmployeePerformanceGraph);

});
