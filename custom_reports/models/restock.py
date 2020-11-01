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

    report_title = fields.Char('Report Title', default="My Restock Report", required=True)
    product_ids = fields.Many2many('product.product', relation='custom_reports_restock_report_rel', column1='custom_report_id', column2='product_id')
    product_restock_ids = fields.One2many('custom_reports.product_restock', 'restock_report_id', string="Product Restock")
    items = fields.Char(string='Items', store=False, readonly=True, compute="_compute_items")

    def is_identical(self, list1, list2):
        if len(list1) != len(list2):
            return False
        for item in list1:
            if item not in list2:
                return False
        return True

    @api.depends('product_ids')
    def _compute_items(self):
        products = self.env['product.product'].search([('active', '=', True)])
        products_count = len(products)
        for report in self:
            report_product_count = len(report.product_ids)
            if report_product_count < products_count:
                report.items = str(report_product_count) + " of " + str(products_count) + " items"
            elif report_product_count < products_count:
                report.items = "report has more items in this report than there are products"
            elif report.is_identical(products, report.product_ids):
                report.items = "all items"
            else:
                report.items = "report has a few inactive products"
    
    # @api.onchange('product_ids')
    # def onchange_product_ids(self):
    #     for report in self:
    #         records = []
    #         for restock in report.product_restock_ids:
    #             if restock.product_id in report.product_ids:
    #                 records.append(restock.product_id)
    #             else:
    #                 report.product_restock_ids.remove(restock)
    #         for product_id in report.product_ids:
    #             if product_id.id not in records:
    #                 report.product_restock_ids.append({
    #                     'product_id': product_id.id,
    #                     'restock_report_id': report.id
    #                 })
    

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
    # product_tmpl_id = fields.Many2one('product.template', string='Template', related="product_id.product_tmpl_id")
    restock_report_id = fields.Many2one('custom_reports.restock_report', string="Restock Report", ondelete='cascade', store=True)

    # computed fields
    name = fields.Char(string="Product Name", compute="_get_name")
    unit_price = fields.Float(string="Unit Price", readonly=True, compute="_compute_unit_price")
    unit_price_real = fields.Float(string="Real Unit Price", readonly=True, compute="_compute_unit_price")
    unit_current = fields.Float(string="Stock", readonly=True, compute="_compute_current", help="Currently in stock")
    unit_y_avg = fields.Float(string="Sold 1Y avg", readonly=True, compute="_compute_unit_sale", help="Avg monthly sold over the past year")
    unit_90d_avg = fields.Float(string="Sold 3M avg", readonly=True, compute="_compute_unit_sale", help="Avg monthly sold over the last 90 days")
    unit_month = fields.Float(string="Sold 1M", readonly=True, compute="_compute_unit_sale", help="Sold over the last month")
    sale_y_avg = fields.Float(string="Sales 1Y avg", readonly=True, compute="_compute_unit_sale", help="Avg monthly sales over the past year")
    sale_90d_avg = fields.Float(string="Sales 3M avg", readonly=True, compute="_compute_unit_sale", help="Avg monthly sales over the last 90 days")
    sale_month = fields.Float(string="Sales 1M", readonly=True, compute="_compute_unit_sale", help="Sales over the last month")
    income_y_avg = fields.Float(string="Income 1Y", readonly=True, compute="_compute_unit_sale", help="Avg monthly income over the last year")
    income_90d_avg = fields.Float(string="Income 3M", readonly=True, compute="_compute_unit_sale", help="Avg monthly income over the last 90 days")
    income_month = fields.Float(string="RealIncome 1M", readonly=True, compute="_compute_unit_sale", help="Sales over the last month")
    income_y_avg_r = fields.Float(string="Real Income 1Y", readonly=True, compute="_compute_unit_sale", help="Avg monthly real income over the last year")
    income_90d_avg_r = fields.Float(string="Real Income 3M", readonly=True, compute="_compute_unit_sale", help="Avg monthly real income over the last 90 days")
    income_month_r = fields.Float(string="Real Income 1M", readonly=True, compute="_compute_unit_sale", help="Real Sales over the last month")

    estimated_stock = fields.Integer(string="Estimated stock based on 1M", readonly=True, compute="_estimated_stock")
    estimated_stock_90d = fields.Integer(string="Estimated stock based on 3M", readonly=True, compute="_estimated_stock")
    estimated_stock_y = fields.Integer(string="Estimated stock based on 1Y", readonly=True, compute="_estimated_stock")
    restock_recommended = fields.Boolean(string="Should Restock", readonly=True, compute="_get_recommandation", help="You ought to restock this!")

    @api.depends('product_id')
    def _get_name(self):
        for record in self:
            record.name = record.product_id.name
    
    @api.depends('product_id')
    def _compute_unit_price(self):
        for record in self:
            record.unit_price = record.product_id.product_tmpl_id.standard_price
            # purchase orders
            po_qty = 0.0
            po_total = 0.0
            pos = record.env['purchase.order.line'].search([('product_id','=',record.product_id.id)])
            for po in pos:
                po_qty += po.product_qty
                po_total += po.price_subtotal
            if po_qty == 0:
                record.unit_price_real = record.unit_price
            else:
                record.unit_price_real = po_total / po_qty

    @api.depends('product_id')
    def _compute_current(self):
        for record in self:
            total_qty = 0.0
            if record.product_id:
                lines = record.env['stock.inventory.line'].search([('product_id','=',record.product_id.id)])
                for line in lines:
                    total_qty += line.product_qty
            record.unit_current = total_qty

    @api.depends('product_id','unit_price','unit_price_real')
    def _compute_unit_sale(self):
        for record in self:
            units_sold_year = 0.0
            units_sold_90d = 0.0
            units_sold_month = 0.0
            sale_year = 0.0
            sale_90d = 0.0
            sale_month = 0.0
            date_year = datetime.now() - relativedelta(months=12)
            date_90d = datetime.now() - relativedelta(months=3)
            date_month = datetime.now() - relativedelta(months=1)
            if record.product_id:
                unit_orders = record.env['sale.order.line'].search([
                    ('product_id', '=', record.product_id.id),
                    ('state', 'in', ['sale', 'done']),
                    ('order_id.date_order', '<', datetime.now()),
                    ('order_id.date_order', '>=', date_year)
                ])
                for unit_order in unit_orders:
                    if unit_order.order_id.date_order > date_90d:
                        units_sold_90d += unit_order.product_uom_qty
                        sale_90d += unit_order.price_subtotal
                    if unit_order.order_id.date_order > date_month:
                        units_sold_month += unit_order.product_uom_qty
                        sale_month += unit_order.price_subtotal
                    units_sold_year += unit_order.product_uom_qty
                    sale_year += unit_order.price_subtotal  
            record.unit_y_avg = units_sold_year / 12.0
            record.unit_90d_avg = units_sold_90d / 3.0
            record.unit_month = units_sold_month
            record.sale_y_avg = sale_year / 12.0
            record.sale_90d_avg = sale_90d / 3.0
            record.sale_month = sale_month
            record.income_y_avg = record.sale_y_avg - (record.unit_y_avg * record.unit_price)
            record.income_90d_avg = record.sale_90d_avg - (record.unit_90d_avg * record.unit_price)
            record.income_month = sale_month - (units_sold_month * record.unit_price)
            record.income_y_avg_r = record.sale_y_avg - (record.unit_y_avg * record.unit_price_real)
            record.income_90d_avg_r = record.sale_90d_avg - (record.unit_90d_avg * record.unit_price_real)
            record.income_month_r = sale_month - (units_sold_month * record.unit_price_real)

    @api.depends('unit_current','unit_y_avg','unit_90d_avg','unit_month')
    def _estimated_stock(self):
        for record in self:
            record.estimated_stock = record.unit_current - record.unit_month
            record.estimated_stock_90d = record.unit_current - record.unit_90d_avg
            record.estimated_stock_y = record.unit_current - record.unit_y_avg

    @api.depends('estimated_stock','unit_month','sale_month')
    def _get_recommandation(self):
        for record in self:
            # $15 and $45 is a made up number...
            if record.estimated_stock <= 0 and record.income_month_r > 0 or \
                record.estimated_stock_90d <= 0 and record.income_90d_avg_r > 0 or \
                record.estimated_stock_y <= 0 and record.income_y_avg_r > 0:
                record.restock_recommended = True
            else:
                record.restock_recommended = False