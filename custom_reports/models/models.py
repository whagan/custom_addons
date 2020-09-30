# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CustomReport(models.Model):
    _name = 'custom_reports.custom_report'
    _description = "Custom Reports"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()

class EmployeePerformanceReport(models.Model):
    _name = 'custom_reports.employee_performance_report'
    _description = "Employee Performance Reports"
    
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, ondelete='cascade', index=True)

    

class EmployeePerformance(models.Model):
    _name = 'custom_reports.employee_performance'
    _description = 'Employee Performance'

    #employee_performance_report_id = fields.Many2one('custom_report.employee_performance_report', string="Employee Performance Report")
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, ondelete='cascade', index=True)
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    worked_hours = fields.Float = fields.Float(string="Worked Hours", compute="worked_hours", store=True)
    total_sales = fields.Float(string="Sales", compute="sales", store=True)

    def worked_hours(self):
        for employee in self:
            worked_hours = 0
            if employee.employee_id:
                attendances = self.env['hr.attendance'].search([('employee_id', '=', employee.employee_id)])
                if attendances:
                    for attendance in attendances:
                        worked_hours += attendance.worked_hours
                else:
                    employee.worked_hours = worked_hours
            else:
                employee.worked_hours = worked_hours 
            employee.worked_hours = worked_hours
    
    def sales(self):
        for employee in self:
            if employee.employee_id:
                total_sales = 0
                orders = self.env['sale.order'].search([('state', 'in', ['sale', 'done']), ('user_id', '=', employee.employee_id)])
                if orders:
                    for sale in sales:
                        total_sales += sale.amount_total
                else:
                    employee.total_sales = total_sales
            else:
                employee.total_sales = total_sales
            employee.total_sales = total_sales

                
    
    
        

class Employee(models.Model):
    _inherit = 'hr.employee'

    worked_hours_total = fields.Float(string="Worked Hours", compute="worked_hours", store=True)

    def worked_hours(self):
        for employee in self:
            worked_hours_total = 0
            if employee.id:
                attendances = self.env['hr.attendance'].search([('employee_id', '=', employee.id)])   
                if attendances:
                    for attendance in attendances:
                        worked_hours_total += attendance.worked_hours
                else:
                    employee.worked_hours_total = worked_hours_total
            else:
                employee.worked_hours_total = worked_hours_total
            employee.worked_hours_total = worked_hours_total


