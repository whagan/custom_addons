# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class reports(models.Model):
#     _name = 'reports.reports'
#     _description = 'reports.reports'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class Report(models.Model):
    _name = 'reports.report'
    _description = "Reports"
    name = fields.Char(string="Title", required=True)
    description = fields.Text()