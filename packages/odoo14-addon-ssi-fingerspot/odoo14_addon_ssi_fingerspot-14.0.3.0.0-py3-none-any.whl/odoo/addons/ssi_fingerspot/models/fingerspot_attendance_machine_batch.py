# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json
import logging
from datetime import datetime, timedelta

import pytz
import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator

_logger = logging.getLogger(__name__)

try:
    import pandas as pd
except (ImportError, IOError) as err:
    _logger.debug(err)


class FingerspotAttendanceMachineBatch(models.Model):
    _name = "fingerspot.attendance.machine.batch"
    _description = "Fingerspot Attendance Batch"
    _inherit = [
        "mixin.transaction_queue_cancel",
        "mixin.transaction_queue_done",
        "mixin.transaction_confirm",
        "mixin.transaction_date_duration",
        "mixin.many2one_configurator",
    ]

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "action_queue_done"
    _approval_state = "confirm"
    _after_approved_method = "action_queue_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_cancel_policy_fields = False
    _automatically_insert_cancel_button = False
    _automatically_insert_cancel_reason = False
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False
    _automatically_insert_queue_done_button = False
    _automatically_insert_queue_cancel_button = False

    _queue_processing_create_page = True
    _queue_to_done_insert_form_element_ok = True
    _queue_to_done_form_xpath = "//group[@name='queue_processing']"

    _queue_to_cancel_insert_form_element_ok = True
    _queue_to_cancel_form_xpath = "//group[@name='queue_processing']"

    _method_to_run_from_wizard = "action_queue_cancel"

    _statusbar_visible_label = "draft,confirm,queue_done,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "queue_cancel_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "queue_done_ok",
        "manual_number_ok",
    ]

    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_queue_done",
        "dom_done",
        "dom_terminate",
        "dom_queue_cancel",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    _auto_enqueue_done = True

    @api.model
    def _get_policy_field(self):
        res = super(FingerspotAttendanceMachineBatch, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "cancel_ok",
            "queue_cancel_ok",
            "done_ok",
            "queue_done_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.model
    def _get_fingerspot_backend_id(self):
        company = self.env.company
        backend = company.fingerspot_backend_id
        return backend and backend.id or False

    fingerspot_backend_id = fields.Many2one(
        string="Backend",
        comodel_name="fingerspot_backend",
        default=lambda self: self._get_fingerspot_backend_id(),
        required=True,
    )

    @api.model
    def _get_is_admin(self):
        result = False
        if self.env.user.has_group("base.group_system"):
            result = True
        return result

    is_admin = fields.Boolean(
        string="Is Admin?",
        default=lambda self: self._get_is_admin(),
    )

    machine_id = fields.Many2one(
        string="# Machine",
        comodel_name="fingerspot.data.machine",
        required=True,
    )
    attendance_machine_ids = fields.One2many(
        string="Attendance Machines",
        comodel_name="fingerspot.attendance.machine",
        inverse_name="batch_id",
        readonly=True,
    )

    @api.constrains("date_start", "date_end")
    def _check_date_start_end(self):
        for record in self:
            if record.date_start and record.date_end:
                strWarning = _("Date end must be greater than date start")
                if record.date_end < record.date_start:
                    raise UserError(strWarning)

    def _convert_datetime_utc(self, dt):
        if dt:
            user = self.env.user
            convert_dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            if user.tz:
                tz = pytz.timezone(user.tz)
            else:
                tz = pytz.utc
            convert_utc = tz.localize(convert_dt).astimezone(pytz.utc)
            format_utc = convert_utc.strftime("%Y-%m-%d %H:%M:%S")
            return format_utc
        else:
            return "-"

    def _import_attendance(self, date):
        self.ensure_one()
        description = "Import attendance for %s" % (date)
        self.with_context(job_batch=self.done_queue_job_batch_id).with_delay(
            description=_(description)
        )._get_attlog(date)

    def _get_attlog(self, date):
        self.ensure_one()
        backend = self.fingerspot_backend_id
        url = backend.base_url + backend.api_attlog
        api_token = backend.api_token
        headers = {
            "Authorization": "Bearer %s" % api_token,
        }
        payload = json.dumps(
            {
                "trans_id": "1",
                "cloud_id": self.machine_id.device_id,
                "start_date": date,
                "end_date": date,
            }
        )

        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            result = response.json()
            self._get_result(result)
        except Exception as e:
            raise UserError(str(e))

    def _prepare_att_machine_data(self, data):
        self.ensure_one()
        return {
            "machine_id": self.machine_id.id,
            "batch_id": self.id,
            "scan_date": self._convert_datetime_utc(data["scan_date"]),
            "pin": data["pin"],
            "verify": str(data["verify"]),
            "status_scan": str(data["status_scan"]),
        }

    def _get_result(self, result):
        self.ensure_one()
        obj_att_machine = self.env["fingerspot.attendance.machine"]
        if result["success"]:
            result_data = result["data"]
            if result_data:
                for data in result_data:
                    criteria = [
                        ("pin", "=", data["pin"]),
                        (
                            "scan_date",
                            "=",
                            self._convert_datetime_utc(data["scan_date"]),
                        ),
                    ]
                    att_machine_ids = obj_att_machine.search(criteria)
                    if len(att_machine_ids) == 0:
                        att_machine = obj_att_machine.create(
                            self._prepare_att_machine_data(data)
                        )
                        att_machine.onchange_employee_id()

    def _cron_import_attendance(self):
        obj_data_machine = self.env["fingerspot.data.machine"]
        company = self.env.company
        fingerspot_backend_id = company.fingerspot_backend_id.id
        utc_date_now = datetime.now()
        tz = pytz.timezone(self.env.user.tz or "Asia/Jakarta")
        user_date_now = utc_date_now.astimezone(tz).date()
        date_start = user_date_now - timedelta(days=2)

        machine_ids = obj_data_machine.search([])
        if machine_ids:
            for machine in machine_ids:
                fs_batch = self.create(
                    {
                        "fingerspot_backend_id": fingerspot_backend_id,
                        "machine_id": machine.id,
                        "date_start": date_start,
                        "date_end": user_date_now,
                    }
                )
                try:
                    fs_batch.action_confirm()
                except Exception as e:
                    raise UserError(str(e))

                try:
                    fs_batch.with_context(
                        {"bypass_policy_check": True}
                    ).action_approve_approval()
                except Exception as e:
                    raise UserError(str(e))

    @ssi_decorator.post_queue_done_action()
    def _fingerspot_get_attendance(self):
        self.ensure_one()
        date_start = self.date_start
        date_list = pd.date_range(date_start, self.date_end, freq="D")
        for index in date_list.strftime("%Y-%m-%d"):
            self._import_attendance(index)
