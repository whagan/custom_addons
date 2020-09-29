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
    
    employee_performance_ids = fields.Many2many('custom_reports.employee_performance', string="Employee Performances")


class EmployeePerformance(models.Model):
    _name = 'custom_reports.employee_performance'
    _description = 'Employee Performance'

    #employee_performance_report_id = fields.Many2one('custom_report.employee_performance_report', string="Employee Performance Report")
    employee_id = fields.Many2one('custom_reports.employee', string="Employee", required=True, ondelete='cascade', index=True)
    
    
        

class Employee(models.Model):
    _name = 'custom_reports.employee'
    _inherit = 'hr.employee'
    _description = 'Custom Reports Employee'

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


