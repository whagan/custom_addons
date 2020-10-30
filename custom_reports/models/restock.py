from odoo import models, fields, api
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class RestockReport(models.Model):
    _name = 'custom_reports.restock_report'
    _description = 'Inventory Restock Report'
    # _inherits = {'product.product': 'product_id'}
    # _inherit = 'product.product'

    product_id = fields.Many2one('product.product', string='Product', ondelete="cascade", required=True)
    product_template_id = fields.Many2one('product.template', string='Template', related="product_id.product_tmpl_id")
    # stock_inventory_line_ids = fields.Many2many('stock.inventory.line', 'restock_line_rel', 'product_id', 'restock_id', string='Stocks')
    
    product_stock = fields.Integer(string="Stock", readonly=True, compute="_compute_stocks")
    sales_quantity = fields.Integer(string="Last Month Sales Quantity", readonly=True, compute="_compute_sales")
    estimated_stock = fields.Integer(string="Estimated", readonly=True, compute="_estimated_stock")
    sales_total = fields.Float(string="Last Month Sales Total", readonly=True, compute="_compute_sales")
    restock_recommended = fields.Boolean(string="Should Restock", readonly=True, compute="_get_recommandation")

    def _compute_stocks(self):
        for record in self:
            total_qty = 0.0
            lines = record.env['stock.inventory.line'].search([('product_id','=',record.product_id.id)])
            for line in lines:
                total_qty += line.product_qty
            record.product_stock = total_qty
        # for line_id in self.stock_inventory_line_ids:
        #     line = self.env['stock.inventory.line'].search([('id','=',line_id)])
        #     total_qty += line.product_qty
        # self.product_stock = total_qty

    def _compute_sales(self):
        for record in self:
            total_qty = 0.0
            total_sale = 0.0
            product_sales = record.env['sale.order.line'].search([
                ('product_id', '=', record.product_id.id),
                ('order_id.date_order', '>=', fields.Date.today() - timedelta(days=30)),
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
        for record in self:
            record.estimated_stock = record.product_stock - record.sales_quantity

    @api.depends('estimated_stock','sales_quantity','sales_total')
    def _get_recommandation(self):
        for record in self:
            if record.estimated_stock <= 0 and record.sales_total > 10 or \
                record.estimated_stock - record.sales_quantity <= 0 and record.sales_total > 50:
                record.restock_recommended = True
            else:
                record.restock_recommended = False

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