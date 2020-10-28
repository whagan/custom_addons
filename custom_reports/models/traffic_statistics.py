from odoo import models, fields, api
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
import datetime
import logging
_logger = logging.getLogger(__name__)

#Traffic Statistics Report DataModel
class TrafficStatisticsReport(models.Model):
    _name = 'custom_reports.traffic_statistics_report'
    _description = 'Traffic Statistics Report'

   # Basic properties
    start_date = fields.Datetime(string = 'Start Date')
    end_date = fields.Datetime(string = 'End Date')
    order_ids = fields.Many2many('pos.order', relation='traffic_statistics_report_rel', column1='custom_report_id', column2='order_id', string="orders")
    traffic_statistics_ids = fields.One2many('custom_reports.traffic_statistics', 'traffic_statistics_report_id', string="Traffic Statistics")


    @api.model
    def create(self, values):
        record = super(TrafficStatisticsReport, self).create(values)
        order_ids = values['order_ids'][0][2]
        records = []
        for company_id in company_ids:
            records.append({
                'order': order_id,
                'traffic_statistics_report_id': record.id,
                'start_date': record.start_date,
                'end_date': record.end_date
            })
        self.env['custom_reports.traffic_statistics'].create(records)
        return record



#Traffic Statistics DataModel
class TrafficStatistics(models.Model):
    _name = 'custom_reports.traffic_statistics'
    _description = 'Traffic Statistics'

    # properties
    order_id = fields.Many2one('pos.order', string="order", ondelete='cascade', index=True, store=True)
    traffic_statistics_report_id = fields.Many2one('custom_reports.traffic_statistics_report', string="Traffic Statistics Report", ondelete='cascade', store=True)
    
    start_date = fields.Datetime(related='traffic_statistics_report_id.start_date', required=True)
    end_date = fields.Datetime(related='traffic_statistics_report_id.end_date', required=True)
    
    
