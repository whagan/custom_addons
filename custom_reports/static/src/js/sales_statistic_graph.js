odoo.define('custom_reports.SalesStatisticGraph', function(require)   {
    'use strict';

    var Widget = require('web.Widget');
    var Registry = require('web.widget_registry');
    var core = require('web.core');


    var SalesStatisticsGraph = Widget.extend({
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],
        template: 'sales_statistics_graph_template',
        xmlDependencies: ['custom_reports/static/src/xml/sales_statistics_graph.xml'],
        
        /**
         * @override
         * @param   {Object}    parent
         * @param   {Object}    data
         */
        init: function (parent, data) {
            this._super.apply(this, arguments);
            this.data = data;
            console.log(this.data);
            console.log('Widget initialized');
        },

        /**
         * @override
         */
        start: function()   {
            var self = this;
            self.graph_type = "pie";
            
    
            console.log(this.$('canvas').attr('id'));


            switch (self.graph_type) {
                case 'polarArea':
                    self.config = self._getPolarGraph();
                    break;
                case 'bar':
                    self.config = self._getBarGraph();
                    break;
                case 'pie':
                    self.config = self._getPieGraph();
                    break;
                case 'doughnut':
                    self.config = self._getDoughnutGraph();
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
         * Returns a pie graph
         * @private
         */
        _getPieGraph: function ()   {
            return {
                type: 'pie',
                data: {
                   labels: ['Store A', 'Store B', 'Store C', 'Store D', 'Store F'],
                   datasets: [{
                       label: 'Store Sales Statistics',
                       data: [55, 78, 37, 10, 48],
                       backgroundColor: ["#1f77b4", "#c5b0d5", "#e377c2", "#7f7f7f", "#dbdb8d"],
                    }]
                },
            };
        },

        /**
         * Returns a doughnut graph
         * @private
         */
        _getDoughnutGraph: function ()   {
            return {
                type: 'doughnut',
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
         * Returns a polar graph
         * @private
         */
        _getPolarGraph: function ()   {
            return {
                type: 'polarArea',
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
         * Returns a radar graph
         * @private
         */
        _getRadarGraph: function ()   {
            return {
                type: 'radar',
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

    Registry.add('sales_statistics_graph', SalesStatisticsGraph);

});
