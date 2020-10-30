from odoo import models, fields, api
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta

class RestockReport(models.Model):
    _name = 'custom_reports.restock_report'
    _description = 'Inventory Restock Report'

    report_name = fields.Char('Report Title', required=True)
    product_ids = fields.Many2many('product.product', relation='custom_reports_restock_report_rel', column1='custom_report_id', column2='product_id')
    product_restock_ids = fields.One2many('custom_reports.product_restock', 'restock_report_id', string="Product Restock")


    @api.model
    def create(self, values):
        record = super(RestockReport, self).create(values)
        product_ids = values['product_ids'][0][2]
        records = []
        for product_id in product_ids:
            records.append({
                'product_id': product_id
            })
        self.env['custom_reports.product_restock'].create(records)
        return record

class Restock(models.Model):
    _name = 'custom_reports.product_restock'
    _description = 'Product Restock'

    product_id = fields.Many2one('product,product', string="Product", ondelete='cascade', index=True, store=True)
    restock_report_id = fields.Many2one('custom_reports.restock_report', string="Restock Report", ondelete='cascade', store=True)

    #computed fields
    unit_prev_avg = fields.Float(string="Avg Units Sold Prev 12 mos", readonly=False, compute="_compute_prev_units")
    #unit_prev_month = fields.Float(string="Units Sold Prev month", readonly=False, compute="_compute_prev_month")
    #unit_current = fields.Float(string="Current", readonly=False, compute="_compute_current")

    @api.depends('product_id')
    def _compute_prev_units(self):
        for record in self:
            units_sold = 0.0
            if record.product_id:
                unit_orders = record.env['sale.order.line'].search([
                    ('product_id', '=', record.product_id.id),
                    ('state', 'in', ['sale', 'done']),
                    ('order_id.date_order', '<', datetime.now()),
                    ('order_id.date_order', '>', datetime.now() - relativedelta(months=12))
                ])
                for unit_order in unit_orders:
                    units_sold += product_uom_qty
                record.unit_prev_avg = units_sold / 12.0
            else:
                record.unit_prev_avg = units_sold / 12.0









    # product_id = fields.Many2one('product.product', string='Product', ondelete="cascade", required=True)
    # product_template_id = fields.Many2one('product.template', string='Template', related="product_id.product_tmpl_id")
    # inventory_line_ids = fields.One2many('stock.inventory.line','product_id', string='Stocks')
    
    # product_stock = fields.Integer(string="Stock", readonly=True, compute="_compute_stocks")
    # sales_quantity = fields.Integer(string="Last Month Sales Quantity", readonly=True, compute="_compute_sales")
    # estimated_stock = fields.Integer(string="Estimated", readonly=True, compute="_estimated_stock")
    # sales_total = fields.Float(string="Last Month Sales Total", readonly=True, compute="_compute_sales")
    # restock_recommended = fields.Boolean(string="Should Restock", readonly=True, compute="_get_recommandation")

    # def _compute_stocks(self):
    #     product_qty = sum(t.get('product_qty', 0.0) for t in self.inventory_line_ids)
    #     # product_qty = 0
    #     # for line in self.inventory_line_ids:
    #     #     product_qty = line.product_qty
    #     self.product_stock = product_qty

    # def _compute_sales(self):
    #     total_qty = 0
    #     total_sale = 0.0
    #     for record in self:
    #         product_sales = record.env['sale.order.line'].search([
    #             ('product_id', '=', record.product_id),
    #             ('order_id.date_order', '>=', fields.Date.today() - timedelta(months=1)),
    #             ('order_id.date_order', '<=', fields.Date.today())])
    #         for product_sale in product_sales:
    #             total_qty += product_sale.product_uom_qty
    #             total_sale += product_sale.price_subtotal
    #         record.update({
    #             'sales_quantity': total_qty,
    #             'sales_total': total_sale
    #         })
    #         # record.sales_quantity = total_qty
    #         # record.sales_total = total_sale

    # @api.depends('product_stock','sales_quantity')
    # def _estimated_stock(self):
    #     self.estimated_stock = self.product_stock - self.sales_quantity

    # @api.depends('estimated_stock','sales_quantity','sales_total')
    # def _get_recommandation(self):
    #     if self.estimated_stock <= 0 and self.sales_total > 10 or \
    #         self.estimated_stock - self.sales_quantity <= 0 and self.sales_total > 50:
    #         self.restock_recommended = True
    #     else:
    #         self.restock_recommended = False

    # def unlink(self):
    #     unlink_records = self.env['custom_reports.restock_report']
    #     unlink_lines = self.env['stock.inventory.line']
    #     for record in self:
    #         # Check if stock still exists, in case it has been unlinked by unlinking its template
    #         if not record.exists():
    #             continue
    #         unlink_records |= record
    #     res = super(RestockReport, unlink_records).unlink()
    #     unlink_lines.unlink()
    #     self.clear_caches()
    #     return res

    # # def _compute_sales(self):
    # #     for record in self:
    # #         total_sale = 0.0
    # #         product_sales = record.env['sale.order.line'].search([
    # #             ('product_id', '=', record.product_id),
    # #             ('order_id.date_order', '>=', fields.Date.today() - relativedelta(months=1)),
    # #             ('order_id.date_order', '<=', fields.Date.today())
    # #         ])
    # #         for product_sale in product_sales:
    # #             total_sale += product_sale.price_subtotal
    # #         record.sales_total = total_sale