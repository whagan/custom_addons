# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
import datetime

# Custom Report DataModel
class CustomReport(models.Model):
    _name = 'custom_reports.custom_report'
    _description = 'Custom Reports'

    # basic properties
    name = fields.Char(string="Report Title", required=True)
    url = fields.Char() #required=True
    category = fields.Char()
    description = fields.Text()

    def click(self):
        return  {
            'name': self.name,
            'view_mode' : 'tree,form',
            'view_id': False,
            'res_model': self.url,
            'type':'ir.actions.act_window',
            'target': 'current',
        }
    
