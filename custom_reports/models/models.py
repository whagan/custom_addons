# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
import datetime

class CustomReport(models.Model):
    _name = 'custom_reports.custom_report'
    _description = "Custom Reports"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()

class EmployeePerformanceReport(models.Model):
    _name = 'custom_reports.employee_performance_report'
    _description = "Employee Performance Reports"
   
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, ondelete='cascade', index=True, store=True)
    employee_user_id = fields.Many2one(related='employee_id.user_id', store=True, readonly=True)
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    worked_hours = fields.Float(string="Worked Hours", compute="compute_worked_hours", readonly=False, store=True)
    total_sales = fields.Float(string="Total Sales", compute="compute_total_sales", readonly=False, store=True)
    sales_hour = fields.Float(string="Sales / Hour", compute="compute_sales_hour", readonly=False, store=True)

    @api.depends('employee_id', 'start_date', 'end_date')
    def compute_worked_hours(self):
        for record in self:
            worked_hours = 0.0
            if record.employee_id and (self.start_date <= self.end_date):
                attendances = self.env['hr.attendance'].search([
                    ('employee_id', '=', self.employee_id.id),
                    ('check_in', '>=', self.start_date),
                    ('check_out', '<=', self.end_date)
                ])
                if attendances:
                    for attendance in attendances:
                        worked_hours += attendance.worked_hours
                else:
                    record.worked_hours = worked_hours
            else:
                record.worked_hours = worked_hours
            record.worked_hours = worked_hours
    
    @api.depends('employee_user_id', 'start_date', 'end_date')
    def compute_total_sales(self):
        for record in self:
            total_sales = 0.0
            if record.employee_id and (self.start_date <= self.end_date):
                orders = self.env['sale.order'].search([
                    ('state', 'in', ['sale', 'done']),
                    ('user_id', '=', self.employee_user_id.id),
                    ('date_order', '>=', self.start_date),
                    ('date_order', '<=', self.end_date)
                    ])
                if orders:
                    for sale in orders:
                        total_sales += sale.amount_total
                else:
                    record.total_sales = total_sales
            else:
                record.total_sales = total_sales
            record.total_sales = total_sales

    @api.depends('total_sales', 'worked_hours')
    def compute_sales_hour(self):
        for record in self:
            if(self.worked_hours != 0):
                record.sales_hour = self.total_sales / self.worked_hours
            else:
                record.sales_hour = 0
