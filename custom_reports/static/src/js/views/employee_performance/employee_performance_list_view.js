odoo.define('custom_reports.EmployeePerformanceListView', function(require)    {
    "use strict";

    var EmployeePerformanceListController = require('custom_reports.EmployeePerformanceListController');
    var EmployeePerformanceListRenderer = require('custom_reports.EmployeePerformanceListRenderer');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');

    var EmployeePerformanceListView = ListView.extend({
        withControlPanel: false,
        config: _.extend({}, ListView.prototype.config, {
            Controller: EmployeePerformanceListController,
            Renderer: EmployeePerformanceListRenderer,
        }),
    });
    
    view_registry.add('employee_performance_list', EmployeePerformanceListView);
    
    return EmployeePerformanceListView;

});