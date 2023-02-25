# Copyright 2021 openNova - Juan Pablo Garza <juanp@opennova.com.ar>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, tools

class ResPartner(models.Model):
    _inherit = 'res.partner'

    """ 
    Ejemplos tomados desde:
        \\ubudoc\public\odoo-dev\12\pronto2020\src\addons-adhoc\account-financial-tools\account_debt_management\models\res_partner.py >> _compute_debt_balance
    """

    debt_balance = fields.Monetary(compute='_compute_debt_balance', string="Saldo total")

    # total_invoiced = fields.Monetary(compute='_invoice_total', string="Total Invoiced",
    #     groups='account.group_account_invoice')

    def _compute_debt_balance(self):
        for rec in self:
            rec.debt_balance = rec.credit - rec.debit

    def action_view_debt_balance_detail(self):
        self.ensure_one()
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        action['domain'] = [
            ('type', 'in', ('in_invoice', 'in_refund', 'out_invoice', 'out_refund')),
            ('partner_id', 'child_of', self.id)
        ]
        action['context'] = {'search_default_unpaid': 1, 'default_type': 'out_invoice'}
        return action