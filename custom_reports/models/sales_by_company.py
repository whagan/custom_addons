
from odoo import models, fields, api, _
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
import datetime
 
#Sales By Company Report DataModel (main report)
class SalesByCompanyReport(models.Model):
    _name = 'custom_reports.sales_by_company_report'
    _description = 'Sales By Company Report'
    _rec_name = 'report_title'

    # properties
    report_title = fields.Char('Report Title', required=True)
    start_date = fields.Datetime(string='Start Date', required=True, ValidationError='_check_date_validity')
    end_date = fields.Datetime(string='End Date', required=True, ValidationError='_check_date_validity')
    company_ids = fields.Many2many('res.company', relation='custom_reports_sales_by_company_report_rel', column1='custom_report_id', column2='company_id', string="companies")
    sales_by_company_ids = fields.One2many('custom_reports.sales_by_company', 'sales_by_company_report_id', string="Sales By Company")
    sales_by_company_graph = fields.Text('Sales Graph', default = 'SalesGraph' )
    
    # methods
    # create override would add all of the items on the list to the subreport's list
    @api.model
    def create(self, values):
        record = super(SalesByCompanyReport, self).create(values)
        company_ids = values['company_ids'][0][2]
        records = []
        for company_id in company_ids:
            records.append({
                'company': company_id,
                'sales_by_company_report_id': record.id,
                'start_date': record.start_date,
                'end_date': record.end_date
            })
        self.env['custom_reports.sales_by_company'].create(records)
        return record

    # write override would adds and removes items on the subreport based on the whether items are in the new values or not
    def write(self, values):
        record = super(SalesByCompanyReport, self).write(values)
        # find the list of items in the original subreport
        old_companies = self.env['custom_reports.sales_by_company'].search([
            ('sales_by_company_report_id', '=', self.id)
        ])
        old_companies_ids = []
        for old_company in old_companies:
            old_companies_ids.append(old_company.company.id)
        new_companies_ids = values['company_ids'][0][2]
        remove_list = []
        add_records = []
        # if an old item is not in the new list, add item to the remove list
        for old_company_id in old_companies_ids:
            if old_company_id not in new_companies_ids:
                remove_list.append(old_company_id)
        # if a new item is not in the old list, add item to the add list
        for new_company_id in new_companies_ids:
            if new_company_id not in old_companies_ids:
                add_records.append({
                    'company': new_company_id,
                    'sales_by_company_report_id':  self.id,
                    'start_date': self.start_date,
                    'end_date': self.end_date
                })
        # remove items in the remove list from the subreport
        remove_records = self.env['custom_reports.sales_by_company'].search([
            ('company', 'in', remove_list)
        ])
        remove_records.unlink()
        # add items in the add list to the subreport
        self.env['custom_reports.sales_by_company'].create(add_records)
        return record

    # check date validity
    @api.constrains('start_date','end_date')
    def _check_date_validity(self):
        for report in self:
            if report.start_date and report.end_date:
                if report.start_date > report.end_date:
                    raise ValidationError(_("Error. Start date must be earlier than end date."))
    

#Sales By Company DataModel (sub report)
class SalesByCompany(models.Model):
    _name = 'custom_reports.sales_by_company'
    _description = 'Sales By Company'
    
    # properties
    company = fields.Many2one('res.company', string="Company", ondelete='cascade', index=True, store=True)
    sales_by_company_report_id = fields.Many2one('custom_reports.sales_by_company_report', string="Sales By Company", ondelete='cascade', store=True)
    start_date = fields.Datetime(related='sales_by_company_report_id.start_date', required=True)
    end_date = fields.Datetime(related='sales_by_company_report_id.end_date', required=True)
    
    # computed properties
    total_sales = fields.Float(string="Total Sales", compute="_calculate_total_sales", readonly=False, store=True)
    
    #computing totals of the sales by company in a given time period
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