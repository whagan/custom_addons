odoo.define('custom_reports.EmailMarketingGraph', function(require)   {
    'use strict';

    var Widget = require('web.Widget');
    var Registry = require('web.widget_registry');
    var core = require('web.core');


    var EmailMarketingGraph = Widget.extend({
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],
        template: 'email_marketing_graph_template',
        xmlDependencies: ['custom_reports/static/src/xml/email_marketing_graph.xml'],
        
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
            self.graph_type = "line";
    
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
                case 'line':
                    self.config = self._getLineGraph();
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
         * Returns a line graph
         * @private
         */
        _getLineGraph: function ()   {
            return {
                type: 'line',
                data: {
                   labels: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                   datasets: [{
                       label: 'ClickIt July Sale Ad',
                       data: [20, 22, 24, 27, 25, 44, 35, 27, 12, 8, 7],
                       borderColor: "#8e5ea2",
                       fill: false
                    },  {
                        label: 'ClickIt August Sale Ad',
                        data: [18, 20, 24, 29, 35, 37, 45, 50, 45, 40, 35],
                        borderColor: "#3cba9f",
                        fill: false

                    },  {
                        label: 'ClickIt September Sale Ad',
                        data: [27, 25, 29, 32, 30, 37, 55, 60, 65, 50, 30],
                        borderColor: "#c45850",
                        fill: false
                    },  {
                        label: 'ClickIt October Sale Ad',
                        data: [35, 29, 29, 32, 48, 50, 55, 60, 67, 70, 65],
                        borderColor: "#3e95cd",
                        fill: false
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

    Registry.add('email_marketing_graph', EmailMarketingGraph);

});
