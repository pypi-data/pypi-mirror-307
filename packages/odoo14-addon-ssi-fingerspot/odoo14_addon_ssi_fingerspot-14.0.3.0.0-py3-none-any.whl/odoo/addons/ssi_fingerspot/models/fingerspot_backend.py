# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class FingerspotBackend(models.Model):
    _name = "fingerspot_backend"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Fingerspot Backend"
    _automatically_insert_print_button = False

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
        copy=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("running", "Running"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )

    # GENERAL
    base_url = fields.Char(
        string="Base URL",
        required=True,
    )
    api_token = fields.Char(
        string="API Token",
    )
    api_attlog = fields.Char(
        string="Attendance Log",
    )

    def action_running(self):
        for record in self:
            check_running_backend_ids = self.search(
                [
                    ("state", "=", "running"),
                    ("company_id", "=", self.env.user.company_id.id),
                    ("id", "!=", record.id),
                ]
            )
            if check_running_backend_ids:
                check_running_backend_ids.write({"state": "draft"})
            record.company_id.write({"fingerspot_backend_id": record.id})
            record.write({"state": "running"})

    def action_restart(self):
        for record in self:
            record.company_id.write({"fingerspot_backend_id": False})
            record.write({"state": "draft"})
