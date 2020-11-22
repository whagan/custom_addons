odoo.define('custom_reports.ribbon', function (require)  {
    'use strict';

    var widgetRegistry = require('web.widget_registry');
    var Widget = require('web.Widget');

    var CustomRibbonWidget = Widget.extend({
        template: 'custom_reports.ribbon',
        xmlDependencies: ['/custom_reports/static/src/xml/ribbon.xml'],

        /**
         * @param   {Object}    options
         * @param   {string}    options.attrs.title
         * @param   {string}    options.attrs.text same as title
         * @param   {string}    options.attrs.tooltip
         * @param   {string}    options.attrs.bg_color
         */
        init:function(parent, data, options)    {
            this._super.apply(this, arguments);
            this.text = options.attrs.title || options.attrs.text;
            this.tooltip = options.attrs.tooltip;
            this.className = options.attrs.bg_color ? options.attrs.bg_color : 'bg-success';
            if (this.text.length > 15) {
                this.className += ' o_small';
            } else if (this.text.length > 10) {
                this.className += ' o_medium';
            }
        },
    });
    widgetRegistry.add('custom_ribbon', CustomRibbonWidget);

    return CustomRibbonWidget;


})