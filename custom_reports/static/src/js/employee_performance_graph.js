odoo.define('custom_reports.employee_performance_graph', function (require) {
    'use strict';
    
    var core = require('web.core');
    var publicWidget = require('web.public.widget');

    var _t = core._t;
    
    const AbstractAction = require('web.AbstractAction');    
    
    var OurAction = AbstractAction.extend({  
        template: "custom_reports.EmployeePerformanceGraph",  
        info: "this message comes from the JS"
    });
    core.action_registry.add('custom_reports.action', OurAction);

    var BarChart = publicWidget.Widget.extend({
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],
        // /**
        //  * @constructor
        //  * @param   {Object}    parent
        //  * @param   {object}    
        //  * @param   {Object}
        //  */
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
            new CharacterData(context, config);
        },
    });

    return  {
        BarChart: BarChart,
    };
});            