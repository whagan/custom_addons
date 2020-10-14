from odoo import models, fields, api
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
#from datetime import date
import logging
_logger = logging.getLogger(__name__)

class EmailMarketingReport(models.Model):
    _name = 'custom_reports.email_marketing_report'
    _description = "Email Marketing Report"
    
    mass_mailing_ids = fields.Many2many('mailing.mailing', relation='custom_reports_email_marketing_report_mail_rel', column1='email_marketing_id', column2='mass_mailing_id', string="Mass Mailings")
    


class MassMailing(models.Model):
    _inherit = 'mailing.mailing'

    product_ids = fields.Many2many('product.product', relation='custom_reports_email_marketing_report_product_rel', column1='mass_mailing_id', column2='product_id', string="Products")

    sales_prev_avg = fields.Float(string="Avg Weekly Sales Prev 6 mos", readonly=True, compute="_compute_prev_sales")
    sales_since_avg = fields.Float(string="Avg Weekly Sales Since Mailing", readonly=True, compute="_compute_since_sales")
    
    # percent change
    #sales_avg_delta = fields.Float(string="Percent Change Average Sales", store=True, readonly=True, compute="_compute_avg_change")

    @api.depends('product_ids')
    def _compute_prev_sales(self):
        for record in self:
            total_sales = 0.0
            total_qty = 0
            prev_date = record.sent_date - relativedelta(days=180)
            _logger.debug("PREVVVV DATE: ", prev_date)
            if record.product_ids:
                for product_id in record.product_ids:
                    product_sales = record.env['sale.order.line'].search([
                        ('product_id', '=', product_id.id),
                        ('order_id.date_order', '<', record.sent_date),
                        ('order_id.date_order', '>=', record.sent_date - relativedelta(days=180)),
                        ('state', 'in', ['sale', 'done'])
                    ])
                    for product_sale in product_sales:
                        total_sales += product_sale.price_subtotal
                record.sales_prev_avg = total_sales / (180.0 / 7.0)
            else:
                record.sales_prev_avg = total_sales / (180.0 / 7.0)
    
    @api.depends('product_ids')
    def _compute_since_sales(self):
        for record in self:
            total_sales = 0.0
            total_qty = 0
            date_delta = datetime.now() - record.sent_date
            if record.product_ids:
                for product_id in record.product_ids:
                    product_sales = record.env['sale.order.line'].search([
                        ('product_id', '=', product_id.id),
                        ('order_id.date_order', '>=', record.sent_date),
                        ('state', 'in', ['sale', 'done'])
                    ])
                    for product_sale in product_sales:
                        total_sales += product_sale.price_subtotal
                record.sales_since_avg = total_sales / (date_delta.days / 7.0)
            else:
                record.sales_since_avg = total_sales / (date_delta.days / 7.0)
     