odoo.define('custom_reports.current_date', function (require) {
    var publicWidget = require('web.public.widget');
    publicWidget.registry.current_date = publicWidget.Widget.extend({
  
      selector: '#my-container.current-date',
  
      start: function (parent) {
        this._renderDate();
      },
  
      // Renders date in M/D/YY format
      _renderDate: function() {
        var now = new Date();
        var formatted = [
          (now.getMonth() + 1),
          now.getDate(),
          now.getFullYear() - 2000
        ].join('/');
        this.$('span').text(formatted);
      }
    });
    return publicWidget.registry.current_date;
  });