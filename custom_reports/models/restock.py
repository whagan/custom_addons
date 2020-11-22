from odoo import models, fields, api
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Main Report Model
class RestockReport(models.Model):
    _name = 'custom_reports.restock_report'
    _description = 'Inventory Restock Report'
    _rec_name = 'report_title'

    # basic properties
    report_title = fields.Char('Report Title', default="My Restock Report", required=True)
    product_ids = fields.Many2many('product.product', relation='custom_reports_restock_report_rel', column1='custom_report_id', column2='product_id')
    product_restock_ids = fields.One2many('custom_reports.product_restock', 'restock_report_id', string="Product Restock")
    
    # computed properties
    items = fields.Char(string='Items', store=False, readonly=True, compute="_compute_items")

    # methods
    # this compares lists and return false if something is different
    def is_identical(self, list1, list2):
        if len(list1) != len(list2):
            return False
        for item in list1:
            if item not in list2:
                return False
        return True

    # this computes a description of how many items are in the list
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
    
    # write override would adds and removes items on the subreport based on the whether items are in the new values or not
    def write(self, values):
        record = super(RestockReport, self).write(values)
        # find the list of items in the original subreport
        old_list = self.env['custom_reports.product_restock'].search([('restock_report_id', '=', self.id)])
        old_ids = []
        for old_id in old_list:
            old_ids.append(old_id.product_id.id)
        new_ids = values['product_ids'][0][2]
        remove_list = []
        add_records = []
        # if an old item is not in the new list, add item to the remove list
        for old_list_id in old_ids:
            if old_list_id not in new_ids:
                remove_list.append(old_list_id)
        # if a new item is not in the old list, add item to the add list
        for new_id in new_ids:
            if new_id not in old_ids:
                add_records.append({'product_id': new_id, 'restock_report_id':  self.id})
        # remove items in the remove list from the subreport
        remove_records = self.env['custom_reports.product_restock'].search([('product_id', 'in', remove_list)])
        remove_records.unlink()
        # add items in the add list to the subreport
        self.env['custom_reports.product_restock'].create(add_records)
        return record
    
    # create override would add all of the items on the list to the subreport's list
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

# Sub Report Model
class Restock(models.Model):
    _name = 'custom_reports.product_restock'
    _description = 'Product Restock'

    # basic properties
    product_id = fields.Many2one('product.product', string="Product", ondelete='cascade', index=True, store=True)
    restock_report_id = fields.Many2one('custom_reports.restock_report', string="Restock Report", ondelete='cascade', store=True)

    # computed properties
    name = fields.Char(string="Product Name", compute="_get_name")
    unit_price = fields.Float(string="Unit Price", readonly=True, compute="_compute_unit_price")
    unit_price_real = fields.Float(string="Real Unit Price", readonly=True, compute="_compute_unit_price")
    unit_current = fields.Float(string="In Stock", readonly=True, compute="_compute_current", help="Currently in stock")
    unit_1Y_avg = fields.Float(string="Sold 1Y avg", readonly=True, compute="_compute_unit_sale", help="Avg monthly sold over the past year")
    unit_3M_avg = fields.Float(string="Sold 3M avg", readonly=True, compute="_compute_unit_sale", help="Avg monthly sold over the last 3 months")
    unit_1M = fields.Float(string="Sold 1M", readonly=True, compute="_compute_unit_sale", help="Sold over the last month")
    sale_1Y_avg = fields.Float(string="Sales 1Y avg", readonly=True, compute="_compute_unit_sale", help="Avg monthly sales over the past year")
    sale_3M_avg = fields.Float(string="Sales 3M avg", readonly=True, compute="_compute_unit_sale", help="Avg monthly sales over the last 3 months")
    sale_1M = fields.Float(string="Sales 1M", readonly=True, compute="_compute_unit_sale", help="Sales over the last month")
    income_1Y_avg = fields.Float(string="P Income 1Y avg", readonly=True, compute="_compute_unit_sale", help="Avg monthly income based on standard price over the last year")
    income_3M_avg = fields.Float(string="P Income 3M avg", readonly=True, compute="_compute_unit_sale", help="Avg monthly income based on standard price over the last 3 months")
    income_1M = fields.Float(string="P Income 1M", readonly=True, compute="_compute_unit_sale", help="Income based on standard price over the last month")
    income_1Y_avg_r = fields.Float(string="Income 1Y avg", readonly=True, compute="_compute_unit_sale", help="Avg monthly income over the last year")
    income_3M_avg_r = fields.Float(string="Income 3M avg", readonly=True, compute="_compute_unit_sale", help="Avg monthly income over the last 3 months")
    income_1M_r = fields.Float(string="Income 1M", readonly=True, compute="_compute_unit_sale", help="Income over the last month")
    estimated_stock = fields.Integer(string="Estimated stock in 1M", readonly=True, compute="_estimated_stock")
    estimated_stock_3M = fields.Integer(string="Estimated stock in 3M", readonly=True, compute="_estimated_stock")
    estimated_stock_1Y = fields.Integer(string="Estimated stock in 1Y", readonly=True, compute="_estimated_stock")
    restock_recommended = fields.Boolean(string="Should Restock", readonly=True, compute="_get_recommandation", help="You ought to restock this!")

    # methods
    # get name
    @api.depends('product_id')
    def _get_name(self):
        for record in self:
            record.name = record.product_id.name
    
    # compute unit price by looking for the purchasing cost of item
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

    # compute current in stock amount for item
    @api.depends('product_id')
    def _compute_current(self):
        for record in self:
            total_qty = 0.0
            if record.product_id:
                lines = record.env['stock.inventory.line'].search([('product_id','=',record.product_id.id)])
                for line in lines:
                    total_qty += line.product_qty
            record.unit_current = total_qty

    # compute unit sales net and net income sums and averages by 1 year, 3 months, and 1 month
    @api.depends('product_id','unit_price','unit_price_real')
    def _compute_unit_sale(self):
        for record in self:
            units_sold_1Y = 0.0
            units_sold_3M = 0.0
            units_sold_1M = 0.0
            sale_1Y = 0.0
            sale_3M = 0.0
            sale_1M = 0.0
            date_1Y = datetime.now() - relativedelta(months=12)
            date_3M = datetime.now() - relativedelta(months=3)
            date_1M = datetime.now() - relativedelta(months=1)
            if record.product_id:
                unit_orders = record.env['sale.order.line'].search([
                    ('product_id', '=', record.product_id.id),
                    ('state', 'in', ['sale', 'done']),
                    ('order_id.date_order', '<', datetime.now()),
                    ('order_id.date_order', '>=', date_1Y)
                ])
                for unit_order in unit_orders:
                    if unit_order.order_id.date_order >= date_3M:
                        units_sold_3M += unit_order.product_uom_qty
                        sale_3M += unit_order.price_subtotal
                    if unit_order.order_id.date_order >= date_1M:
                        units_sold_1M += unit_order.product_uom_qty
                        sale_1M += unit_order.price_subtotal
                    units_sold_1Y += unit_order.product_uom_qty
                    sale_1Y += unit_order.price_subtotal  
            record.unit_1Y_avg = units_sold_1Y / 12.0
            record.unit_3M_avg = units_sold_3M / 3.0
            record.unit_1M = units_sold_1M
            record.sale_1Y_avg = sale_1Y / 12.0
            record.sale_3M_avg = sale_3M / 3.0
            record.sale_1M = sale_1M
            record.income_1Y_avg = record.sale_1Y_avg - (record.unit_1Y_avg * record.unit_price)
            record.income_3M_avg = record.sale_3M_avg - (record.unit_3M_avg * record.unit_price)
            record.income_1M = sale_1M - (units_sold_1M * record.unit_price)
            record.income_1Y_avg_r = record.sale_1Y_avg - (record.unit_1Y_avg * record.unit_price_real)
            record.income_3M_avg_r = record.sale_3M_avg - (record.unit_3M_avg * record.unit_price_real)
            record.income_1M_r = sale_1M - (units_sold_1M * record.unit_price_real)

    # estimate the amount of stocks left by next month based on the 1y and 3m averages or last month's sales
    @api.depends('unit_current','unit_1Y_avg','unit_3M_avg','unit_1M')
    def _estimated_stock(self):
        for record in self:
            record.estimated_stock = record.unit_current - record.unit_1M
            record.estimated_stock_3M = record.unit_current - record.unit_3M_avg
            record.estimated_stock_y = record.unit_current - record.unit_1Y_avg

    # get recommendations based on estimated stock and whether the item made money
    @api.depends('estimated_stock','unit_1M','sale_1M')
    def _get_recommandation(self):
        for record in self:
            # estimated stock is less than 0 and it made money, recommend restock.
            if record.estimated_stock <= 0 and record.income_1M_r > 0 or \
                record.estimated_stock_3M <= 0 and record.income_3M_avg_r > 0:
                # or record.estimated_stock_y <= 0 and record.income_1Y_avg_r > 0: # removed due to lack of demo records
                record.restock_recommended = True
            else:
                record.restock_recommended = False