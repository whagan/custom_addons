
from odoo import models, fields, api
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
import datetime
import logging
_logger = logging.getLogger(__name__)

 
#Sales By Location Report DataModel
class SalesByLocationReport(models.Model):
    _name = 'custom_reports.sales_by_location_report'
    _description = 'Sales By Location Report'
    
   # basic properties
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    company_ids = fields.Many2many('res.company', relation='sales_by_location_report_rel', column1='custom_report_id', column2='company_id', string="companies")
    sales_by_location_ids = fields.One2many('custom_reports.sales_by_location', 'sales_by_location_report_id', string="Sales By Location")

    # methods
    # method for the creation of a new instance of a report
    @api.model
    def create(self, values):
        record = super(SalesByLocationReport, self).create(values)
        company_ids = values['company_ids'][0][2]
        records = []
        for company_id in company_ids:
            records.append({
                'company': company_id,
                'sales_by_location_report_id': record.id,
                'start_date': record.start_date,
                'end_date': record.end_date
            })
        self.env['custom_reports.sales_by_location'].create(records)
        return record
    

#Sales By Location DataModel
class SalesByLocation(models.Model):
    _name = 'custom_reports.sales_by_location'
    _description = 'Sales By Location'
    
    
    # properties
    company = fields.Many2one('res.company', string="Company", ondelete='cascade', index=True, store=True)
    sales_by_location_report_id = fields.Many2one('custom_reports.sales_by_location_report', string="Sales By location", ondelete='cascade', store=True)
    
    start_date = fields.Datetime(related='sales_by_location_report_id.start_date', required=True)
    end_date = fields.Datetime(related='sales_by_location_report_id.end_date', required=True)
    
    total_sales = fields.Float(string="Total Sales", compute="_calculate_total_sales", readonly=False, store=True)
    
    
    #computing totals of the sales by location in a given time period
    @api.depends('company','start_date','end_date')
    def _calculate_total_sales(self):
        for record in self:
            total_sales = 00.0
            if record.company and (record.start_date <= record.end_date):
                orders = record.env['sale.order'].search([
                    ('company_id', '=', record.company.id),
                    ('state', 'in', ['sale', 'done']),
                    ('date_order', '>=', record.start_date),
                    ('date_order', '<=', record.end_date)
                    ])
                if orders: # if found in orders, sum the total sales
                    for sale in orders:
                        total_sales += sale.amount_total
            record.total_sales = total_sales