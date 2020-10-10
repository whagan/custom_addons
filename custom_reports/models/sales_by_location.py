
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
    company_ids = fields.Many2many('sale.order', relation='sales_by_location_report_rel', column1='custom_report_id', column2='company_id', string="companies")
   
    # methods
    @api.model
    def create(self, values):
        record = super(SalesByLocationReport, self).create(values)
        company_ids = values['company_ids']
        records = []
        for company_id in company_ids:
            records.append({
                'company_id': company_id,
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
    sale_id = fields.Many2one('sale.order', string="Company", ondelete='cascade', index=True, store=True)
    company_id = fields.Many2one(related='sale_id.company_id', store=True, readonly=True)
    sales_by_location_report_id = fields.Many2one('custom_reports.sales_by_location_report', string="Sales By location", ondelete='cascade', store=True)
    start_date = fields.Datetime(related='sales_by_location_id.start_date', required=True)
    end_date = fields.Datetime(related='sales_by_location_report_id.end_date', required=True)
    