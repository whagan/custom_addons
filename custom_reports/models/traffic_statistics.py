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
    location_ids = fields.Many2many('stock.location', relation='custom_reports_traffic_stats_rel', column1='stat_report_id', column2='location_id', string="Location")
    traffic_statistic_ids = fields.One2many('custom_reports.traffic_statistic', 'traffic_statistics_report_id', string="Traffic Statistics")

 
    @api.model
    def create(self, values):
        record = super(TrafficStatisticsReport, self).create(values)
        location_ids = values['location_ids'][0][2]
        records = []
        for location_id in location_ids:
            records.append({
                'location_id': location_id,
                'traffic_statistics_report_id': record.id,
                'start_date': record.start_date,
                'end_date': record.end_date
            })
        self.env['custom_reports.traffic_statistic'].create(records)
        return record



#Traffic Statistics DataModel
class TrafficStatistic(models.Model):
    _name = 'custom_reports.traffic_statistic'
    _description = 'Traffic Statistic'

    # properties
    location_id = fields.Many2one('stock.location', string="Location", ondelete='cascade', index=True, store=True)
    traffic_statistics_report_id = fields.Many2one('custom_reports.traffic_statistics_report', string="Traffic Statistics Report", ondelete='cascade', store=True)
    start_date = fields.Datetime(related='traffic_statistics_report_id.start_date', required=True)
    end_date = fields.Datetime(related='traffic_statistics_report_id.end_date', required=True)

    # computed values
    # sales per this location between start date and end date 
    sales_location = fields.Float(string="Sales / Location", compute="_compute_sales_location", readonly=False)


    # methods
    # this method gets the computed work hours between a time period
    @api.depends('location_id', 'start_date', 'end_date')
    def _compute_sales_location(self):
        for record in self:
            sales_location = 0.0           
            if record.location_id and (record.start_date <= record.end_date):
                sales = record.env['pos.order'].search([
                    ('location_id', '=', record.location_id.id),
                    ('date_order', '<=', record.end_date),
                    ('date_order', '>=', record.start_date)
                ])
                if sales: # if found in attendance, sum the worked_hours
                    for sale in sales:
                        sales_location += sale.amount_total
            record.sales_location = sales_location
    
    
