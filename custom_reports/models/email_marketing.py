from odoo import models, fields, api
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
import datetime

class EmailMarketingReport(models.Model):
    _name = 'custom_reports.email_marketing_report'
    _description = "Email Marketing Report"
    
    mass_mailing_ids = fields.Many2many('mailing.mailing', relation='custom_reports_email_marketing_report_mail_rel', column1='email_marketing_id', column2='mass_mailing_id', string="Mass Mailings")
    


class MassMailing(models.Model):
    _inherit = 'mailing.mailing'

    product_ids = fields.Many2many('product.product', relation='custom_reports_email_marketing_report_product_rel', column1='mass_mailing_id', column2='product_id', string="Products")

    # sales with preset date ranges
    sales_prev_avg = fields.Float(string="Weekly Average Sales Previous Year", store=True, readonly=True, compute="_compute_sales")
    sales_since_avg = fields.Float(string="Weekly Average Sales Since Mailing", store=True, readonly=True, compute="_compute_sales")
    
    # percent change
    sales_avg_delta = fields.Float(string="Percent Change Average Sales", store=True, readonly=True, compute="_compute_avg_change")

    def _compute_sales(self):
        for record in self:
            if record.product_ids:
                total_sales = 0.0
                total_qty = 0
                for product_id in record.product_ids:
                    product_sales = record.env['sale.order.line'].search('product_id', '=', product_id.id)
                    total_sales += product_sales.untaxed_amount_invoiced
                    total_qty += product_sales.qty_invoiced

#            if record.state not in ('done'):
 #               record.sales_since_avg = 0.0
                




