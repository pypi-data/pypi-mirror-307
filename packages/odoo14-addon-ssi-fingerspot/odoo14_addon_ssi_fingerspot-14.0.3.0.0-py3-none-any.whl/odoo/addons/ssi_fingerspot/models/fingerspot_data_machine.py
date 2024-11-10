# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FingerspotDataMachine(models.Model):
    _name = "fingerspot.data.machine"
    _inherit = ["mixin.master_data"]
    _description = "Fingerspot Data Machine"

    name = fields.Char(
        string="Machine",
    )
    device_id = fields.Char(
        string="Device ID",
        required=True,
    )
    user_ids = fields.One2many(
        comodel_name="fingerspot.machine.user",
        inverse_name="machine_id",
        string="Users",
        required=False,
    )

    def action_test_connection(self):
        pass
