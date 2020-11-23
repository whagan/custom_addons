from odoo import models, fields, api, _
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
import datetime

#Sales Statistics Report DataModel
class SalesStatisticsReport(models.Model):
    _name = 'custom_reports.sales_statistics_report'
    _description = 'Sales Statistics Report'
    _rec_name = 'report_title'
    
    # Basic properties
    report_title = fields.Char('Report Title', required=True)
    start_date = fields.Datetime(string = 'Start Date', required=True, ValidationError='_check_date_validity')
    end_date = fields.Datetime(string = 'End Date', required=True, ValidationError='_check_date_validity')
    location_ids = fields.Many2many('stock.location', relation='sales_statistics_report_rel', column1='custom_report_id', column2='location_id', string="Location")
    sales_statistic_ids = fields.One2many('custom_reports.sales_statistic', 'sales_statistics_report_id', string="Sales Statistics")
    sales_statistics_graph = fields.Text('Sales Graph', default = 'SalesGraph' )
 
    # methods
    # create override would add all of the items on the list to the subreport's list
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

    # write override would adds and removes items on the subreport based on the whether items are in the new values or not
    def write(self, values):
        record = super(SalesStatisticsReport, self).write(values)
        # find the list of items in the original subreport
        old_locations = self.env['custom_reports.sales_statistic'].search([
            ('sales_statistics_report_id', '=', self.id)
        ])
        old_locations_ids = []
        for old_location in old_locations:
            old_locations_ids.append(old_location.location_id.id)
        new_locations_ids = values['location_ids'][0][2]
        remove_list = []
        add_records = []
        # if an old item is not in the new list, add item to the remove list
        for old_location_id in old_locations_ids:
            if old_location_id not in new_locations_ids:
                remove_list.append(old_location_id)
        # if a new item is not in the old list, add item to the add list
        for new_location_id in new_locations_ids:
            if new_location_id not in old_locations_ids:
                add_records.append({
                    'location_id': new_location_id,
                    'sales_statistics_report_id':  self.id,
                    'start_date': self.start_date,
                    'end_date': self.end_date
                })
        # remove items in the remove list from the subreport
        remove_records = self.env['custom_reports.sales_statistic'].search([
            ('location_id', 'in', remove_list)
        ])
        remove_records.unlink()
        # add items in the add list to the subreport
        self.env['custom_reports.sales_statistic'].create(add_records)
        return record

    # check date validity
    @api.constrains('start_date','end_date')
    def _check_date_validity(self):
        for report in self:
            if report.start_date and report.end_date:
                if report.start_date > report.end_date:
                    raise ValidationError(_("Error. Start date must be earlier than end date."))

#sales Statistics DataModel (sub report)
class SalesStatistics(models.Model):
    _name = 'custom_reports.sales_statistic'
    _description = 'Sales Statistic'

    # properties
    location_id = fields.Many2one('stock.location', string="Location", ondelete='cascade', index=True, store=True)
    sales_statistics_report_id = fields.Many2one('custom_reports.sales_statistics_report', string="Sales Statistics Report", ondelete='cascade', store=True)
    start_date = fields.Datetime(related='sales_statistics_report_id.start_date', required=True)
    end_date = fields.Datetime(related='sales_statistics_report_id.end_date', required=True)

    # computed properites
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
                if sales:
                    for sale in sales:
                        sales_location += sale.amount_total
            record.sales_location = sales_location
    
    
