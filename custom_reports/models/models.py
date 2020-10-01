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
    
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, ondelete='cascade', index=True)

    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    worked_hours = fields.Float(string="Worked Hours", compute="compute_worked_hours", readonly=False, store=True)
    total_sales = fields.Float(string="Total Sales", compute="compute_total_sales", readonly=False, store=True)

    @api.depends('employee_id', 'start_date', 'end_date')
    def compute_worked_hours(self):
        for record in self:
            w_hours = 0.0
            if record.employee_id:
                attendances = self.env['hr.attendance'].search([
                    ('employee_id', '=', self.employee_id.id),
                    ('check_in', '>=', self.start_date),
                    ('check_out', '<=', self.end_date)
                ])
                if attendances:
                    for attendance in attendances:
                        w_hours += attendance.worked_hours
                else:
                    record.worked_hours = w_hours
            else:
                record.worked_hours = w_hours
            record.worked_hours = w_hours
    

    
  

   #    ('state', 'in', ['sale', 'done']), 