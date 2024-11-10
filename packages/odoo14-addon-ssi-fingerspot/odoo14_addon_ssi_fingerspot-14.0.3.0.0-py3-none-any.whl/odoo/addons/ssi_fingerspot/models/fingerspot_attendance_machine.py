# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import pytz

from odoo import _, api, fields, models


class FingerspotAttendanceMachine(models.Model):
    _name = "fingerspot.attendance.machine"
    _description = "Fingerspot Attendance Machine"
    _rec_name = "employee_id"
    _order = "scan_date"

    batch_id = fields.Many2one(
        string="# Batch",
        comodel_name="fingerspot.attendance.machine.batch",
        required=True,
        ondelete="cascade",
    )
    machine_id = fields.Many2one(
        string="# Machine",
        comodel_name="fingerspot.data.machine",
    )
    pin = fields.Char(
        required=True,
        string="PIN",
    )
    scan_date = fields.Datetime(
        string="Scan Date",
    )
    verify = fields.Selection(
        string="Verify",
        selection=[
            ("1", "Finger"),
            ("2", "Password"),
            ("3", "Card"),
            ("4", "Face"),
            ("5", "GPS"),
            ("6", "Vein"),
        ],
        default=False,
    )
    status_scan = fields.Selection(
        string="Status",
        selection=[
            ("0", "Scan In"),
            ("1", "Scan Out"),
            ("2", "Break In"),
            ("3", "Break Out"),
            ("4", "Overtime In"),
            ("5", "Overtime Out"),
            ("6", "Meeting In"),
            ("7", "Meeting Out"),
            ("8", "Customer In"),
            ("9", "Customer Out"),
        ],
        default=False,
    )

    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Employee",
    )
    is_transfer = fields.Boolean(
        string="Is Transfer?",
        required=False,
        copy=False,
        readonly=True,
    )
    is_skip = fields.Boolean(
        string="Is Skip?",
        required=False,
        copy=False,
        readonly=True,
    )
    err_msg = fields.Char(
        string="Error",
        default="-",
    )

    @api.onchange(
        "machine_id",
        "pin",
    )
    def onchange_employee_id(self):
        obj_machine_user = self.env["fingerspot.machine.user"]
        criteria = [
            ("machine_id", "=", self.machine_id.id),
            ("pin", "=", self.pin),
        ]
        machine_user_ids = obj_machine_user.search(criteria)
        self.employee_id = False
        if machine_user_ids:
            self.employee_id = (
                machine_user_ids and machine_user_ids.employee_id.id or False
            )

    def _check_attendance(self):
        self.ensure_one()
        result = False
        criteria = []
        obj_attendance = self.env["hr.timesheet_attendance"]
        if int(self.status_scan) % 2 == 0:
            criteria = [
                ("check_in", "=", self.scan_date),
                ("employee_id", "=", self.employee_id.id),
            ]
        else:
            criteria = [
                ("check_out", "=", self.scan_date),
                ("employee_id", "=", self.employee_id.id),
            ]
        attendance_ids = obj_attendance.search(criteria)
        if attendance_ids:
            result = True
        return result

    def _check_timesheet(self):
        self.ensure_one()
        result = False
        obj_timesheet = self.env["hr.timesheet"]
        tz = pytz.timezone(self.employee_id.tz or "Asia/Jakarta")
        conv_scan_date = pytz.utc.localize(self.scan_date).astimezone(tz)
        current_scan_date = conv_scan_date.date()
        criteria = [
            ("company_id", "=", self.employee_id.company_id.id),
            ("employee_id", "=", self.employee_id.id),
            ("state", "=", "open"),
            ("date_start", "<=", current_scan_date),
            ("date_end", ">=", current_scan_date),
        ]
        timesheet_ids = obj_timesheet.search(criteria, limit=1)
        if timesheet_ids:
            result = timesheet_ids
        return result

    def action_mark_is_transfer(self):
        for record in self:
            record.is_transfer = True

    def action_unmark_is_transfer(self):
        for record in self:
            record.is_transfer = False

    def action_mark_is_skip(self):
        for record in self:
            record.is_skip = True

    def action_unmark_is_skip(self):
        for record in self:
            record.is_skip = False

    def _get_latest_attendance(self):
        self.ensure_one()
        obj_attendance = self.env["hr.timesheet_attendance"]
        result = False

        criteria = [
            ("employee_id", "=", self.employee_id.id),
        ]
        attendance_ids = obj_attendance.search(criteria, limit=1)
        if attendance_ids:
            result = attendance_ids
        return result

    def _generate_attendance_by_system(self, attendance_vals):
        obj_attendance = self.env["hr.timesheet_attendance"]
        obj_attendance_reason = self.env["hr.attendance_reason"]

        reason_in_id = obj_attendance_reason.search([("code", "=", "SYS-IN")], limit=1)
        reason_out_id = obj_attendance_reason.search(
            [("code", "=", "SYS-OUT")], limit=1
        )
        attendance_vals.update(
            {
                "date": self.scan_date.date(),
                "check_in": self.scan_date,
                "check_out": self.scan_date,
                "reason_check_in_id": reason_in_id.id,
                "reason_check_out_id": reason_out_id.id,
                "fingerspot_att_out": self.id,
            }
        )
        return obj_attendance.create(attendance_vals)

    def _generate_attendances(self):
        obj_attendance = self.env["hr.timesheet_attendance"]
        latest = False
        for record in self:
            timesheet = record._check_timesheet()
            if not timesheet:
                msg_err = _("Timesheet for employee %s not found.") % (
                    record.employee_id.display_name,
                )
                record.write(
                    {
                        "err_msg": msg_err,
                    }
                )
                continue

            if record._check_attendance():
                tz = pytz.timezone(record.employee_id.tz or "Asia/Jakarta")
                current_datetime = pytz.utc.localize(record.scan_date).astimezone(tz)
                attendance_date = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
                msg_err = _("Attendance %s for employee %s already exists.") % (
                    attendance_date,
                    record.employee_id.display_name,
                )
                record.write(
                    {
                        "err_msg": msg_err,
                    }
                )
                continue

            attendance_vals = {
                "sheet_id": timesheet.id,
                "employee_id": record.employee_id.id,
            }
            if int(record.status_scan) % 2 == 0:
                # SCAN IN
                tz = pytz.timezone(record.employee_id.tz or "Asia/Jakarta")
                conv_scan_date = pytz.utc.localize(record.scan_date).astimezone(tz)
                current_scan_date = conv_scan_date.date()
                attendance_vals.update(
                    {
                        "date": current_scan_date,
                        "check_in": record.scan_date,
                        "fingerspot_att_in": record.id,
                    }
                )
                latest = obj_attendance.create(attendance_vals)
            else:
                # SCAN OUT
                latest_attendance_id = record._get_latest_attendance()
                _check = 0.0
                checkout_buffer = 0.0
                if latest_attendance_id:
                    company = self.env.company
                    checkout_buffer = company.checkout_buffer
                    latest_employee_id = latest_attendance_id.employee_id.id
                    if latest_employee_id == record.employee_id.id:
                        check_out = record.scan_date
                        if latest_attendance_id.date > record.scan_date.date():
                            if latest:
                                latest_attendance_id = latest
                        schedule = latest_attendance_id.schedule_id
                        schedule_check_out = schedule.date_end
                        if schedule_check_out:
                            _check = (
                                check_out - schedule_check_out
                            ).total_seconds() / 3600.0
                        else:
                            hours_per_day = timesheet.working_schedule_id.hours_per_day
                            checkout_buffer += hours_per_day
                            _check = (
                                check_out - latest_attendance_id.check_in
                            ).total_seconds() / 3600.0
                        if latest_attendance_id.check_out or (_check > checkout_buffer):
                            # Apabila latest_attendance tidak sesuai kriteria buffer
                            latest = record._generate_attendance_by_system(
                                attendance_vals
                            )
                        else:
                            attendance_vals.update(
                                {
                                    "check_out": record.scan_date,
                                    "fingerspot_att_out": record.id,
                                }
                            )
                            latest_attendance_id.write(attendance_vals)
                    else:
                        # Apabila tidak latest_attendance employee berbeda
                        latest = record._generate_attendance_by_system(attendance_vals)
                else:
                    # Apabila tidak ada latest_attendance
                    latest = record._generate_attendance_by_system(attendance_vals)

            record.write(
                {
                    "is_transfer": True,
                    "err_msg": "-",
                }
            )

    def action_generate_attendances(self):
        to_generate = self.filtered(
            lambda x: x.is_transfer is False and x.is_skip is False and x.employee_id
        ).sorted(lambda m: (m.pin))

        tz = pytz.timezone(self.env.user.tz or "Asia/Jakarta")
        time_now = fields.Datetime.now()
        current_datetime = pytz.utc.localize(time_now).astimezone(tz)
        attendance_date = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
        if to_generate:
            str_group = "Generate attendance Batch for %s" % (attendance_date)
            batch = self.env["queue.job.batch"].get_new_batch(str_group)
            description = "Generate attendance for %s" % (attendance_date)
            to_generate.with_context(job_batch=batch).with_delay(
                description=_(description)
            )._generate_attendances()
            batch.enqueue()

    def _cron_generate_attendances(self):
        attendance_machine_ids = self.search([])
        attendance_machine_ids.action_generate_attendances()
