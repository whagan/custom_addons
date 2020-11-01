from odoo import models, fields, api
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
import datetime
import logging
_logger = logging.getLogger(__name__)

#Sales Statistics Report DataModel
class SalesStatisticsReport(models.Model):
    _name = 'custom_reports.sales_statistics_report'
    _description = 'Sales Statistics Report'

   # Basic properties
    start_date = fields.Datetime(string = 'Start Date')
    end_date = fields.Datetime(string = 'End Date')
    location_ids = fields.Many2many('stock.location', relation='sales_statistics_report_rel', column1='custom_report_id', column2='location_id', string="Location")
    sales_statistic_ids = fields.One2many('custom_reports.sales_statistic', 'sales_statistics_report_id', string="Sales Statistics")

 
    @api.model
    def create(self, values):
        record = super(SalesStatisticsReport, self).create(values)
        location_ids = values['location_ids'][0][2]
        records = []
        for location_id in location_ids:
            records.append({
                'location_id': location_id,
                'sales_statistics_report_id': record.id,
                'start_date': record.start_date,
                'end_date': record.end_date
            })
        self.env['custom_reports.sales_statistic'].create(records)
        return record



#sales Statistics DataModel
class SalesStatistics(models.Model):
    _name = 'custom_reports.sales_statistic'
    _description = 'Sales Statistic'

    # properties
    location_id = fields.Many2one('stock.location', string="Location", ondelete='cascade', index=True, store=True)
    sales_statistics_report_id = fields.Many2one('custom_reports.sales_statistics_report', string="Sales Statistics Report", ondelete='cascade', store=True)
    start_date = fields.Datetime(related='sales_statistics_report_id.start_date', required=True)
    end_date = fields.Datetime(related='sales_statistics_report_id.end_date', required=True)

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
    
    
