odoo.define('custom_reports.CustomWidget', function(require)    {
    'use strict';

    var core = require('web.core');
    var publicWidget = require('web.public.widget');
    var _t = core._t;

    var PieChart = publicWidget.Widget.extend({
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],
        /**
         * @override
         * @param   {Object}    parent
         * @param   {Object}    data
         */
        init: function(parent, data)    {
            this._super.apply(this, arguments);
            this.data = data;
        },
        /**
         * @override
         */
        start: function()   {
            var labels = ['Nashville', 'Memphis', 'Knoxville', 'Chattanooga'];
            var data = [5000, 500, 50, 5,];
            var label = 'Population';
            var config = {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets:   [{
                        data: data,
                        label: label,
                    }]
                },
            };
            var canvas = this.$('canvas')[0];
            var context = canvas.getContext('2d');
            new Chart(context, config);
        },
    });

    publicWidget.registry.pieChart = publicWidget.Widget.extend({
        selector: '.o_pie_chart',
        

        /**
         * @override
         */
        start: function() {
            var self = this;
            this.charts = {};
            var defs = [];
            defs.push(this._super.apply(this, arguments));
            return Promise.all(defs).then(function (results)    {
                self.charts.emp_pie_chart = new PieChart();
                self.charts.emp_pie_chart.attachTo($('#emp_per_chart'));
                var rowWidth = $('#emp_per_chart').parent().width();
                var $chartCanvas = $('#emp_per_chart').find('canvas');
                $chartCanvas.height('20em');
            });
        },
    });

    return  {
        PieChart: PieChart,
    };
})