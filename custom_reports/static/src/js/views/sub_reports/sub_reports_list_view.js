odoo.define('custom_reports.SubReportsListView', function(require)    {
    "use strict";

    var SubReportsListController = require('custom_reports.SubReportsListController');
    var SubReportsListRenderer = require('custom_reports.SubReportsListRenderer');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');

    var SubReportsListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: SubReportsListController,
            Renderer: SubReportsListRenderer,
        }),
    });
    
    view_registry.add('sub_reports_list', SubReportsListView);
    
    return SubReportsListView;

});