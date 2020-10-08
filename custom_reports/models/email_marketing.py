from odoo import models, fields, api
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
import datetime

class EmailMarketingReport(models.Model):
    _name = 'custom_reports.email_marketing_report'
    _description = "Email Marketing Report"
    
    # basic properties
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    mass_mailing_ids = fields.Many2many('mailing.mailing', relation='custom_reports_email_marketing_report_mail_rel', column1='email_marketing_id', column2='mass_mailing_id', string="Mass Mailings")
    


class MassMailing(models.Model):
    _inherit = 'mailing.mailing'

    product_ids = fields.Many2many('product.product', relation='custom_reports_email_marketing_report_product_rel', column1='mass_mailing_id', column2='product_id', string="Products")

    #email_marketing_report_ids = fields.Many2one('custom_reports.email_marketing_report', string="Email Marketing Report", ondelete='cascade', store=True)
    