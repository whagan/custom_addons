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
    sales_delta = fields.Float(string="Change in Avg Sales", readonly=True, compute="_compute_avg_diff")
    sales_delta_per = fields.Char(string="Change in Avg Sales Percent", readonly=True, compute="_compute_avg_diff")
   
    @api.depends('product_ids')
    def _compute_prev_sales(self):
        for record in self:
            total_sales = 0.0
            total_qty = 0
            prev_date = record.sent_date - relativedelta(days=180)
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
    
    @api.depends('sales_prev_avg', 'sales_since_avg')
    def _compute_avg_diff(self):
        for record in self:
            diff_avg = record.sales_since_avg - record.sales_prev_avg
            record.sales_delta = diff_avg

            if (record.sales_prev_avg == 0.0):
                record.sales_delta_per = "No previous sales"
            elif (record.sales_prev_avg  > 0.0):
                if (diff_avg < 0.0):
                    record.sales_delta_per = "Down {0}{1}".format('%0.0f' % ((diff_avg / record.sales_prev_avg) * 100), "%")
                elif (diff_avg == 0.0):
                    record.sales_delta_per = "No change"
                else:
                    record.sales_delta_per = "Up {0}{1}".format('%0.0f' % ((diff_avg / record.sales_prev_avg) * 100), "%")
            else:
                raise ValidationError(_("Error. The previous sales average %s is less than 0.00.", s = str(record.sales_prev_avg)))
