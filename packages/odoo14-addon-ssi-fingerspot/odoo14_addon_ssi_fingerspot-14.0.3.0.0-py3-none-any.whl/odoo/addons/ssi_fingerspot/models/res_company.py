# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    fingerspot_backend_id = fields.Many2one(
        string="Active Fingerspot Backend",
        comodel_name="fingerspot_backend",
        domain="[('state', '=', 'running')]",
    )
