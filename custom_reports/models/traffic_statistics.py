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

    def write(self, values):
        record = super(TrafficStatisticsReport, self).write(values)
        old_shops = self.env['custom_reports.traffic_statistic'].search([
            ('traffic_statistics_report_id', '=', self.id)
        ])
        old_shops_ids = []
        for old_shop in old_shops:
            old_shops_ids.append(old_shop.shop_id.id)
        new_shops_ids = values['shop_ids'][0][2]
        remove_list = []
        add_records = []
        for old_shop_id in old_shops_ids:
            if old_shop_id not in new_shops_ids:
                remove_list.append(old_shop_id)
        for new_shop_id in new_shops_ids:
            if new_shop_id not in old_shops_ids:
                add_records.append({
                    'shop_id': new_shop_id,
                    'traffic_statistics_report_id':  self.id,
                    'start_date': self.start_date,
                    'end_date': self.end_date
                })
        remove_records = self.env['custom_reports.traffic_statistic'].search([
            ('shop_id', 'in', remove_list)
        ])
        remove_records.unlink()
        self.env['custom_reports.traffic_statistic'].create(add_records)
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

    max_hour = fields.Char(string="Max Hour(s)", compute="_compute_rank_hour", readonly=False)
    min_hour = fields.Char(string="Min Hour(s)", compute="_compute_rank_hour", readonly=False)
    all_hour = fields.Char(string="All Hours", compute="_compute_rank_hour", readonly=False)

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
    def _compute_rank_hour(self):
        for record in self:
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
                    record.max_hour = str(record._max_hour(hours_sales_avg))
                    record.min_hour = str(record._min_hour(hours_sales_avg))
                    record.all_hour = str(hours_sales_avg)
                else:
                    record.max_hour = "[0]"
                    record.min_hour = "[0]"
                    record.all_hour = "[0]"
            else:
                raise exceptions.ValidationError(_("Error. Shop not found."))
            

    def _avg_per_hour(self, hour_list):
        if not hour_list:
            return round(0, 2)
        return round((sum(hour_list) / len(hour_list)), 2)

    def _max_hour(self, hour_list_avg):
        return [index for index, value in enumerate(hour_list_avg) if value == max(hour_list_avg)]
    
    def _min_hour(self, hour_list_avg):
        return [index for index, value in enumerate(hour_list_avg) if value == min(hour_list_avg)]
