odoo.define('custom_reports_view.CustomReportsView', function (require) {
    "use strict";
    
    var AbstractView = require('web.AbstractView');
    var viewRegistry = require('web.view_registry');
    
    var CustomReportsModel = require('custom_reports.CustomReportsModel');
    var CustomReportsController = require('custom_reports.CustomReportsController');
    var CustomReportsRenderer = require('custom_reports.CustomReportsRenderer');
    
    var CustomReportsView = AbstractView.extend({
        config: {
                Model: CustomReportsModel,
                Controller: CustomReportsController,
                Renderer: CustomReportsRenderer,
        },
        withControlPanel: false,        
        viewType: 'custom_reports',        
    });

    viewRegistry.add('custom_reports', CustomReportsView);
    return CustomReportsView;
});
    