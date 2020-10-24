odoo.define('custom_reports.bh_sidebar', function (require) {
    'use strict';
  
    var Widget = require('web.Widget');
    var widgetRegistry = require('web.widget_registry');
    var core = require('web.core');
  
    var QWeb = core.qweb;
    var _t = core._t;
  
    var bh_sidebar = Widget.extend({
      init: function () {
          var self = this;
          this._super(parent);
          console.log('Widget initialized!');
      },
  
      events: {},
  
      start: function () {
          this.$el.append(QWeb.render('bh_sidebar_template'));
      }
  
    });
  
    widgetRegistry.add(
      'bh_sidebar', bh_sidebar
    );
  });
  