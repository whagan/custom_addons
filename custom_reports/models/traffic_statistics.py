from odoo import models, fields, api, _
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
import datetime
import logging
_logger = logging.getLogger(__name__)

class TrafficStatisticsReport(models.Model):
    _name = 'custom_reports.traffic_statistics_report'
    _description = 'Traffic Statistics Report'
    _rec_name = 'report_title'
    
    report_title = fields.Char('Report Title', required=True)
    start_date = fields.Datetime(string = 'Start Date', required=True, ValidationError='_check_date_validity')
    end_date = fields.Datetime(string = 'End Date', required=True, ValidationError='_check_date_validity')
    shop_ids = fields.Many2many('pos.config', relation='traffic_statistics_report_rel', column1='custom_report_id', column2='shop_id', string="Shop")
    traffic_statistic_ids = fields.One2many('custom_reports.traffic_statistic', 'traffic_statistics_report_id', string="Traffic Statistics")
    traffic_statistic_graph = fields.Text('Traffic Graph', default='TrafficGraph')

 
    @api.model
    def create(self, values):
        record = super(TrafficStatisticsReport, self).create(values)
        shop_ids = values['shop_ids'][0][2]
        records = []
        for shop_id in shop_ids:
            records.append({
                'shop_id': shop_id,
                'traffic_statistics_report_id': record.id,
                'start_date': record.start_date,
                'end_date': record.end_date
            })
        self.env['custom_reports.traffic_statistic'].create(records)
        return record

    @api.constrains('start_date','end_date')
    def _check_date_validity(self):
        for report in self:
            if report.start_date and report.end_date:
                if report.start_date > report.end_date:
                    raise ValidationError(_("Error. Start date must be earlier than end date."))


class TrafficStatistic(models.Model):
    _name = 'custom_reports.traffic_statistic'
    _description = 'Traffic Statistic'

    shop_id = fields.Many2one('pos.config', string="Shop", ondelete='cascade', index=True, store=True)
    traffic_statistics_report_id = fields.Many2one('custom_reports.traffic_statistics_report', string="Traffic Statistics Report", ondelete='cascade', store=True)
    start_date = fields.Datetime(related='traffic_statistics_report_id.start_date', required=True)
    end_date = fields.Datetime(related='traffic_statistics_report_id.end_date', required=True)
    first_hour = fields.Integer(string="Top Hour", compute="_compute_avg_hour", readonly=False)

    @api.depends('shop_id', 'start_date', 'end_date')
    def _compute_sales_shop(self):
        for record in self:
            sales_shop = 0.0           
            if record.shop_id and (record.start_date <= record.end_date):
                sales = record.env['pos.order'].search([
                    ('session_id', '=', record.shop_id.id),
                    ('date_order', '<=', record.end_date),
                    ('date_order', '>=', record.start_date)
                ])
                if sales:
                    for sale in sales:
                        sales_shop += sale.amount_total
            record.sales_shop = sales_location
    
    @api.depends('shop_id', 'start_date', 'end_date')
    def _compute_avg_hour(self):
        for record in self:
            sales_shop = 0.0
            if record.shop_id and (record.start_date <= record.end_date):
                sales = record.env['pos.order'].search([
                    ('session_id', '=', record.shop_id.id),
                    ('date_order', '<=', record.end_date),
                    ('date_order', '>=', record.start_date)
                ])
                if sales:
                    hours_sales = [[] for i in range(24)]
                    hours_sales_avg = []
                    for sale in sales:
                        hours_sales[sale.date_order.hour].append(sale.amount_total)
                    _logger.debug("THIS IS THE hours_sales: ", hours_sales)
                    for hour in hours_sales:
                        hours_sales_avg.append(record._avg_per_hour(hour))
                    _logger.debug("THIS IS THE hours_sales_avg: ", hours_sales_avg)
                record.first_hour = hours_sales_avg.index(max(hours_sales_avg))
            record.first_hour = 1
            

    def _avg_per_hour(self, hour_list):
        if not hour_list:
            return round(0, 2)
        return round((sum(hour_list) / len(hour_list)), 2)
                       
    
    
