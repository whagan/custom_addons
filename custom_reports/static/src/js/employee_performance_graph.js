odoo.define('custom_reports.EmployeePerformanceGraph', function(require)   {
    'use strict';

    var Widget = require('web.Widget');
    var Registry = require('web.widget_registry');
    var core = require('web.core');


    var EmployeePerformanceGraph = Widget.extend({
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],
        template: 'employee_performance_graph_template',
        xmlDependencies: ['custom_reports/static/src/xml/employee_performance_graph.xml'],
        
        /**
         * @override
         */
        init: function(parent) {
            var self = this;
            this._super(parent);
            console.log('Widget initialized');

        },

        start: function()   {
            var self = this;
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
         * Returns a pie graph
         * @private
         */
        _getPieGraph: function ()   {
            return {
                type: 'pie',
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

    Registry.add('employee_performance_graph', EmployeePerformanceGraph);

});
