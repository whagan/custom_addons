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
    _order = "category, name, description"

    # basic properties
    name = fields.Char(string="Report Title", required=True)
    url = fields.Char() #required=True
    category = fields.Char()
    description = fields.Text()

    def click(self):
        return {
            'name': self.name,
            'view_mode' : 'tree,form',
            'view_id': False,
            'res_model': self.url,
            'type':'ir.actions.act_window',
            'target': 'current',
            }
    #     # action = ir.actions.search([
    #     #             ('name', '=', self.name)]).id
    #     # menu_id = ir.ui.menu.search([
    #     #             ('name', '=', "Custom Reports"),
    #     #             ('parent_id', '=?', None)]).id
    #     # urlString = "web#action=" + action + "&model=" + self._name + "&view_type=list&cids=1&menu_id=" + menu_id
    #     return {
    #         # 'name': 'View',
    #         # 'type': 'ir.actions.act_url',
    #         # # 'url': self.url
    #         # 'url': urlString,
    #         # 'target': 'self',
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'tree',
    #         'view_type': 'tree',
    #         'res_model': self.url
    #         }


