odoo.define('custom_reports_view.CustomReportsView', function (require) {
"use strict";


var AbstractController = require('web.AbstractController');
var AbstractModel = require('web.AbstractModel');
var AbstractRenderer = require('web.AbstractRenderer');
var AbstractView = require('web.AbstractView');
//var ListRenderer = require('web.ListRenderer');
var viewRegistry = require('web.view_registry');


var CustomReportsController = AbstractController.extend({});
var CustomReportsRenderer = AbstractRenderer.extend({});
var CustomReportsModel = AbstractModel.extend({});

/*AbstractView.include({
    init: function (parent, state, params)  {
        this._super(parent, state, params);
        this.withSearchBar = false;
    },
});*/
var CustomReportsView = AbstractView.extend({
    withControlPanel: false,
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
