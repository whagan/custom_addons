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
         * @param {Widget} parent
         * @param {Object} params
         * @param {string} options.graph_type
         */
        init: function (parent, params) {
            this._super.apply(this, arguments);
            this.graph_type = options.graph_type == undefined ? 'bar' : options.graph_type
            console.log('Widget initialized');
        },

        /**
         * @override
         */
        start: function()   {
            var self = this;
            
            if (self.graph_type != undefined) {
                if (self.graph_type == 'bar') {
                    self.config = self._getBarGraph();
                }
                else if (self.graph_type == 'pie')    {
                    self.config = self._getPieGraph();
                }
                else    {
                    self.config = self._getPolarGraph();
                }
            }
            else    {
                self.config = self._getDoughnutGraph();
            }

            

            // self.config = self._getBarGraph();
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
