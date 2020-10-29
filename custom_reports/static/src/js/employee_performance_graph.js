odoo.define('custom_reports.Graph', function(require)   {
    'use strict';

    // var Widget = require('web.Widget');
    // var Registry = require('web.widget_registry');
    var core = require('web.core');

    var BasicFields = require('web.basic_fields');
    var FieldRegistry = require('web.field_registry');


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
            console.log(this);
            console.log(arguments);

            console.log('Widget initialized');

            console.log(this.attrs.options.graph_type);
            this.graph_type = this.attrs.options.graph_type;
        },

        /**
         * @override
         */
        start: function()   {
            var self = this;
            
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
        },

    });

    FieldRegistry.add('employee_performance_graph', EmployeePerformanceGraph);

    // var RenderGraphWidget = Widget.extend({
    //     selector: '.o_employee_performance_graph',

    //     /**
    //      * @override
    //      */
    //     start: function()   {
    //         var self = this;
    //         console.log('Widget started');

    //         var graph_type = self.$('widget').attr('graph_type');
    //         console.log(graph_type);
            
    //         var defs = [this._super.apply(this, arguments)];

    //         return Promise.all(defs).then(function()    {
    //             self.pie_chart = new EmployeePerformanceGraph(self, "doughnut");
    //             self.pie_chart.attachTo($('#hang_graph'));
    //         });

        
    //     },

    // });

    // Registry.add('render_graph', RenderGraphWidget);

});
