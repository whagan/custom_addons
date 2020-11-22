odoo.define('custom_reports.CustomReportsListView', function(require)    {
    "use strict";

    var CustomReportsListController = require('custom_reports.CustomReportsListController');
    var CustomReportsListRenderer = require('custom_reports.CustomReportsListRenderer');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');

    var CustomReportsListView = ListView.extend({
        withControlPanel: false,
        config: _.extend({}, ListView.prototype.config, {
            Controller: CustomReportsListController,
            Renderer: CustomReportsListRenderer,
        }),
    });
    
    view_registry.add('custom_reports_list', CustomReportsListView);
    
    return CustomReportsListView;

});