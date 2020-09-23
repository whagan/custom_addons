odoo.define('custom_reports_view.CustomReportsView', function (require) {
"use strict";


var AbstractController = require('web.AbstractController');
var AbstractModel = require('web.AbstractModel');
var AbstractRenderer = require('web.AbstractRenderer');
var AbstractView = require('web.AbstractView');
var viewRegistry = require('web.view_registry');


var CustomReportsController = AbstractController.extend({});
var CustomReportsRenderer = AbstractRenderer.extend({});
var CustomReportsModel = AbstractModel.extend({});

var CustomReportsView = AbstractView.extend({
    config: {
        Model: CustomReportsModel,
        Controller: CustomReportsController,
        Renderer: CustomReportsRenderer,
    },
    viewType: 'custom_reports',
});
viewRegistry.add('custom_reports', CustomReportsView);
return CustomReportsView;
});
