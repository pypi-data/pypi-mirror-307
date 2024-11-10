# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FingerspotMachineUser(models.Model):
    _name = "fingerspot.machine.user"
    _description = "Fingerspot Machine User"
    _rec_name = "employee_id"

    machine_id = fields.Many2one(
        comodel_name="fingerspot.data.machine", string="Machine", ondelete="cascade"
    )
    pin = fields.Char(
        required=True,
        string="PIN",
    )
    employee_id = fields.Many2one(
        comodel_name="hr.employee", string="Employee", required=False
    )
    employee_name = fields.Char(
        related="employee_id.name",
        string="Employee Name",
    )
    device_id = fields.Char(
        string="Device ID",
        related="machine_id.device_id",
        store=True,
    )
