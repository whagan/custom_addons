from odoo import models, fields, api
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
import datetime

class RestockReport(models.Model):
    _name = 'custom_reports.restock_report'
    _description = 'Inventory Restock Report'
    # _inherits = {'product.product': 'product_id'}

    product_id = fields.Many2one('product.product', string='Product', ondelete="cascade", required=True)
    product_template_id = fields.Many2one('product.template', string='Template', related="product_id.product_tmpl_id")
    inventory_line_ids = fields.One2many('stock.inventory.line','product_id', string='Stocks')
    
    product_stock = fields.Integer(string="Stock", readonly=True, compute="_compute_stocks")
    sales_quantity = fields.Integer(string="Last Month Sales Quantity", readonly=True, compute="_compute_sales")
    estimated_stock = fields.Integer(string="Estimated", readonly=True, compute="_estimated_stock")
    sales_total = fields.Float(string="Last Month Sales Total", readonly=True, compute="_compute_sales")
    restock_recommended = fields.Boolean(string="Should Restock", readonly=True, compute="_get_recommandation")

    def _compute_stocks(self):
        product_qty = sum(t.get('product_qty', 0.0) for t in self.inventory_line_ids)
        # product_qty = 0
        # for line in self.inventory_line_ids:
        #     product_qty = line.product_qty
        self.product_stock = product_qty

    def _compute_sales(self):
        total_qty = 0
        total_sale = 0.0
        for record in self:
            product_sales = record.env['sale.order.line'].search([
                ('product_id', '=', record.product_id),
                ('order_id.date_order', '>=', fields.Date.today() - timedelta(months=1)),
                ('order_id.date_order', '<=', fields.Date.today())])
            for product_sale in product_sales:
                total_qty += product_sale.product_uom_qty
                total_sale += product_sale.price_subtotal
            record.update({
                'sales_quantity': total_qty,
                'sales_total': total_sale
            })
            # record.sales_quantity = total_qty
            # record.sales_total = total_sale

    @api.depends('product_stock','sales_quantity')
    def _estimated_stock(self):
        self.estimated_stock = self.product_stock - self.sales_quantity

    @api.depends('estimated_stock','sales_quantity','sales_total')
    def _get_recommandation(self):
        if self.estimated_stock <= 0 and self.sales_total > 10 or \
            self.estimated_stock - self.sales_quantity <= 0 and self.sales_total > 50:
            self.restock_recommended = True
        else:
            self.restock_recommended = False

    def unlink(self):
        unlink_records = self.env['custom_reports.restock_report']
        unlink_lines = self.env['stock.inventory.line']
        for record in self:
            # Check if stock still exists, in case it has been unlinked by unlinking its template
            if not record.exists():
                continue
            unlink_records |= record
        res = super(RestockReport, unlink_records).unlink()
        unlink_lines.unlink()
        self.clear_caches()
        return res

    # def _compute_sales(self):
    #     for record in self:
    #         total_sale = 0.0
    #         product_sales = record.env['sale.order.line'].search([
    #             ('product_id', '=', record.product_id),
    #             ('order_id.date_order', '>=', fields.Date.today() - relativedelta(months=1)),
    #             ('order_id.date_order', '<=', fields.Date.today())
    #         ])
    #         for product_sale in product_sales:
    #             total_sale += product_sale.price_subtotal
    #         record.sales_total = total_sale