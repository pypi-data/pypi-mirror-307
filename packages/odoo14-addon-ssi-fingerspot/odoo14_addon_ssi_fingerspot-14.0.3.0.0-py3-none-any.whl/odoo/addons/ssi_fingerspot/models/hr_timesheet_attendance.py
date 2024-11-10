# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HRTimesheetAttendance(models.Model):
    _inherit = "hr.timesheet_attendance"

    fingerspot_att_in = fields.Many2one(
        string="Fingespot In",
        comodel_name="fingerspot.attendance.machine",
    )
    fingerspot_att_out = fields.Many2one(
        string="Fingespot Out",
        comodel_name="fingerspot.attendance.machine",
    )
