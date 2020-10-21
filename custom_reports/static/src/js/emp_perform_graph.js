odoo.define('custom_reports_view.EmpPerformGraph', function (require)   {
    "use strict";

    var core = require('web.core');
    var ajax = require('web.ajax');
    var publicWidget = require('web.public.widget');

    // should var name below be same as name in line 1?
    /**
     * In Odoo, to create a custom widget, you typically create a view and then
     * register that view with the field_registry.
     */
    publicWidget.registry.EmpPerformGraph = publicWidget.Widget.extend({
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],
        /**
         * Initializes the widget based on its defined graph_type and loads chart.
         * @override
         */
        start: function()   {
            var self = this;
            return this._super.apply(this, arguments).then(function ()  {
                self.graphData = self.$el.data("graphData");

                switch(self.$el.data("graphType"))  {
                    case 'pie':
                        self.chartConfig = self._getPieChartConfig();
                        break;
                    case 'bar':
                        self.chartConfig = self._getBarChartConfig();
                        break;
                }
                self._loadChart();
            });
        },

        //------------------------------------/
        // Private
        //-----------------------------------/

        /** 
         * returns standard pie chart configuration
         * 
         * @private
         */
        _getPieChartConfig: function()  {
            var counts = this.graphData.map(function (point)    {
                return point.count;
            });
            return  {
                type: 'pie',
                data: {
                    labels: this.graphData.map(function (point) {
                        return point.text;
                    }),
                    datasets: [{
                        label: '',
                        data: counts,
                    }]
                }
            };
        },

        //------------------------------------/
        // Private
        //-----------------------------------/

        /** 
         * returns standard bar chart configuration
         * 
         * @private
         */
        _getBarChartConfig: function()  {
            return  {
                type: 'bar',
                data: {
                    labels: this.graphData[0].values.map(function (value)   {
                        return value.text;
                    }),
                    datasets: this.graphData.map(function (group)   {
                        var data = group.values.map(function (value)    {
                            return value.count;
                        });
                        return  {
                            label: group.key,
                            data: data,
                        };
                    })
                },
                options:    {
                    legend: {
                        display: false,
                    },
                    scales: {
                        xAxes:  [{
                            ticks:  {
                                callback: this._customTick(35),
                            },
                        }],
                        yAxes: [{
                            ticks:  {
                                precision: 0,
                            },
                        }],
                    },
                    tooltips:   {
                        enabled: false,
                    }
                },
            };
        },

        /** 
         * Custom Ticks function to replace overflowing text with '...'
         * 
         * @private
         * @param {Integer} tickLimit
         */
        _customTick: function(tickLimit)    {
            return function(label)  {
                if (label.length <= tickLimit)  {
                    return label;
                }   else    {
                    return label.slice(0, tickLimit) + '...';
                }
            };
        },

        /**
         * Loads the chart using provided Chart library
         * @private
         */
        _loadChart: function()  {
            this.$el.css({position: 'relative'});
            var $canvas = this.$('canvas');
            var ctx = $canvas.get(0).getContext('2d');
            return new Chart(ctx, this.chartConfig);
        }

    }); 

    return  {
        chartWidget: publicWidget.registry.EmpPerformGraph,
    };

});