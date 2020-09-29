# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CustomReport(models.Model):
    _name = 'custom_reports.custom_report'
    _description = 'Custom Reports'

    # basic fields
    name = fields.Char(string="Report Title", required=True)
    url = fields.Char(required=True)
    category = fields.Char()
    description = fields.Text()
    delete_date = fields.Datetime()

    # relational fields
    delete_uid = fields.Many2one(comodel_name="res.users")

    # auto
    # @api.multi
    # def action_url(self):
    #     return {
    #         'type' : 'ir.actions.act_url',
    #         'url' : '/custom_reports/go?model=custom_reports.custom_report&field=url&id=%s'%(self.id),
    #         'target' : 'new',
    #     }

# class CustomReport_History(models.Model):
#     _name = 'custom_reports.custom_report_history'
#     _description = 'Custom Reports History'

#     report_id = fields.Many2one(related='custom_reports.custom_report.id', required=True)
#     column_name = fields.Char(required=True)
#     old_value = fields.Text()
