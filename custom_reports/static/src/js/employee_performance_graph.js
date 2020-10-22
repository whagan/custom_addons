odoo.define('custom_reports.employee_performance_graph', function (require) {
    'use strict';
    
    var core = require('web.core');
    var publicWidget = require('web.public.widget');

    var _t = core._t;
    
    var BarChart = publicWidget.Widget.extend({
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],
        
        init: function () {
			this._super.apply(this, arguments);
		},

        start: function()   {
            var config = {
                type: 'line',
                data:   {
                    labels: ['Nashville', 'Memphis', 'Knoxville', 'Chattanooga'],
                    datasets:   [{
                        label: 'Population',
                        data:   [
                            5000,
                            500,
                            50,
                            5,
                        ],
                        backgroundColor: '#ebf2f7',
                        borderColor: '#6aa1ca',
                    }]
                },
            };
            var canvas = this.$('canvas')[0];
            var context = canvas.getContext('2d');
            new Chart(context, config);
        },
    });

    publicWidget.registry.employeePerformanceGraph = publicWidget.Widget.extend({
        selector: '.o_emp_perform_graph',
        /**
         * @override
         */
        start: function()   {
            var self = this;
            this.charts = {};
            self.charts.emp_bar_chart = new BarChart();
            self.charts.emp_bar_chart.attachTo($('#emp_bar_clicks_chart'));
          
        }

    });

    return  {
        BarChart: BarChart,
    };
});            
