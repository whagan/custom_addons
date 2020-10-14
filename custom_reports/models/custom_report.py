# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
import datetime
import logging
_logger = logging.getLogger(__name__)

# Custom Report DataModel
class CustomReport(models.Model):
    _name = 'custom_reports.custom_report'
    _description = 'Custom Reports'

    # basic properties
    name = fields.Char(string="Report Title", required=True)
    url = fields.Char() #required=True
    category = fields.Char()
    description = fields.Text()
    # delete_date = fields.Datetime()

    # relational fields
    # delete_uid = fields.Many2one(comodel_name="res.users")

    def click(self):
        action = self.env['ir_actions'].search([
                    ('name', '=', self.name)])
        menu_id = self.env['ir_ui_menu'].search([
                    ('name', '=', "Custom Reports"),
                    ('parent_id', '=?', None)])
        urlString = "web#action=" + action + "&model=custom_reports." + self.name + "&view_type=list&cids=&menu_id=" + menu_id
        return {
            'name': 'View',
            'type': 'ir.actions.act_url',
            # 'url': self.url
            'url': urlString,
            'target': 'self',}

