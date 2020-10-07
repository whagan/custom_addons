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