from odoo import models, fields, api
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)

class RestockReport(models.Model):
    _name = 'custom_reports.restock_report'
    _description = 'Inventory Restock Report'

    report_title = fields.Char('Report Title', required=True)
    product_ids = fields.Many2many('product.product', relation='custom_reports_restock_report_rel', column1='custom_report_id', column2='product_id')
    product_restock_ids = fields.One2many('custom_reports.product_restock', 'restock_report_id', string="Product Restock")


    @api.model
    def create(self, values):
        record = super(RestockReport, self).create(values)
        product_ids = values['product_ids'][0][2]
        records = []
        for product_id in product_ids:
            records.append({
                'product_id': product_id,
                'restock_report_id': record.id,
            })
        self.env['custom_reports.product_restock'].create(records)
        return record

class Restock(models.Model):
    _name = 'custom_reports.product_restock'
    _description = 'Product Restock'

    product_id = fields.Many2one('product.product', string="Product", ondelete='cascade', index=True, store=True)
    restock_report_id = fields.Many2one('custom_reports.restock_report', string="Restock Report", ondelete='cascade', store=True)

    #computed fields
    unit_prev_avg = fields.Float(string="Avg Units Sold Prev 12 mos", readonly=False, compute="_compute_prev_units")
    unit_prev_month = fields.Float(string="Units Sold Prev month", readonly=False, compute="_compute_prev_month")
    unit_current = fields.Float(string="Current", readonly=False, compute="_compute_current")

    @api.depends('product_id')
    def _compute_prev_units(self):
        for record in self:
            units_sold = 0.0
            if record.product_id:
                unit_orders = record.env['sale.order.line'].search([
                    ('product_id', '=', record.product_id.id),
                    ('state', 'in', ['sale', 'done']),
                    ('order_id.date_order', '<', datetime.now()),
                    ('order_id.date_order', '>=', datetime.now() - relativedelta(months=12))
                ])
                for unit_order in unit_orders:
                    units_sold += unit_order.product_uom_qty
                record.unit_prev_avg = units_sold / 12.0
            else:
                record.unit_prev_avg = units_sold / 12.0
    
    @api.depends('product_id')
    def _compute_prev_month(self):
        for record in self:
            units_sold = 0.0
            if record.product_id:
                unit_orders = record.env['sale.order.line'].search([
                    ('product_id', '=', record.product_id.id),
                    ('state', 'in', ['sale', 'done']),
                    ('order_id.date_order', '<', datetime.now()),
                    ('order_id.date_order', '>=', datetime.now() - relativedelta(days=30))
                ])
                for unit_order in unit_orders:
                    units_sold += unit_order.product_uom_qty
                record.unit_prev_month = units_sold
            else:
                record.unit_prev_month = units_sold
    
    @api.depends('product_id')
    def _compute_current(self):
        for record in self:
            units_sold = 0.0
            if record.product_id:
                unit_orders = record.env['sale.order.line'].search([
                    ('product_id', '=', record.product_id.id),
                    ('state', 'in', ['sale', 'done']),
                    ('order_id.date_order', '<', datetime.now()),
                    ('order_id.date_order', '>=', datetime.now() - relativedelta(days=30))
                ])
                for unit_order in unit_orders:
                    units_sold += unit_order.product_uom_qty
                record.unit_prev_month = units_sold
            else:
                record.unit_prev_month = units_sold

