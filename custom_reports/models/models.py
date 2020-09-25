# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomReport(models.Model):
    _name = 'custom_reports.custom_report'
    _description = "Custom Reports"

    name = fields.Char(string=_("Title"), required=True)
    description = fields.Text()