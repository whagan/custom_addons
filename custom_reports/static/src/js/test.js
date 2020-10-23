odoo.define('custom_reports.CustomWidget', function(require)    {
    console.log("HEY WILL");
    'use strict';

    var _t = require('web.core')._t;
    var ajax = require('web.ajax');
    var publicWidget = require('web.public.widget');
    
    publicWidget.registry.PieChart = publicWidget.Widget.extend({
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],
        /**
         * @override
         */
        start: function()   {
            var self = this;

            return this._super.apply(this, arguments).then(function ()  {
                self.chartConfig = self._getPieChartConfig();
                self._loadChart();
            });
        },
        // ----------------------------
        // Private
        // ----------------------------

        /**
         * @private
         */
        
        _getPieChartConfig: function() {
            var labels = ['Nashville', 'Memphis', 'Knoxville', 'Chattanooga'];
            var data = [5000, 500, 50, 5,];
            var label = 'Population';
            return {
                type: 'pie',
                data:   {
                    labels: labels,
                    datasets:   [{
                        data: data,
                        label: label,
                    }]
                }
            };
        },

        /**
         * @private
         */
        _loadChart: function()  {
            this.$el.css({position: 'relative'});
            var $canvas = this.$('canvas');
            var ctx = $canvas.get(0).getContext('2d');
            return new Chart(ctx, this.chartConfig);
        }
    });

    publicWidget.registry.CustomReportGraph = publicWidget.Widget.extend({
        selector: '.o_custom_report_graph',

        /**
         * @override
         */
        start: function()   {
            var self = this;
            return this._super.apply(this, arguments).then(function ()  {
                var allPromises = [];
                self.$('.custom_graph').each(function() {
                    allPromises.push(new publicWidget.registry.PieChart(self)
                    .attachTo($(this)));
                });
                if (allPromises.length !== 0)   {
                    return Promise.all(allPromises);
                }   else    {
                    return Promise.resolve();
                }

            });
        },

    });

   return   {
       chartWidget: publicWidget.registry.PieChart,
       customReportGraphWidget: publicWidget.registry.CustomReportGraph
   };
});

  