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
    
    employee_performance_id = fields.One2many('custom_reports.employee_performance', 'employee_performance_report_id', string="Employee Performances")


class EmployeePerformance(models.Model):
    _name = 'custom_reports.employee_performance'
    _description = 'Employee Performance'

    worked_hours_sum = fields.Float(string="Worked Hours", compute='worked_hours')
    employee_performance_report_id = fields.Many2one('custom_report.employee_performance_report', string="Employee Performance Report")

    def worked_hours(self):
        total = 0
        for attendance in self:
            recordset = self.env['hr.attendance'].search_read([('employee_id', '=', attendance.employee_id.id)])
            for record in recordset:
                total = total + record.worked_hours
        worked_hours_sum = total
        
                
