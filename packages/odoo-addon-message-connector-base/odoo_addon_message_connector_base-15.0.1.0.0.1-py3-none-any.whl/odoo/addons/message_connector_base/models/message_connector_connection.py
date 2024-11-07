# Copyright 2023 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models


class MessageConnectorConnection(models.Model):
    """This model is in charge of sending the message and creating a log with
    the sent or failed messages.
    """

    _name = "message.connector.connection"
    _description = "Message Connector Connection"
    _order = "state asc, id desc"

    def _get_message_services(self):
        """Return the list of message service installed."""
        return self.env.company.get_message_services()

    display_name = fields.Char(
        string="Display Name", compute="_compute_display_name", store=True
    )
    channel = fields.Char(
        string="Channel",
    )
    date = fields.Datetime(
        string="Date",
        default=lambda self: fields.Datetime.now(),
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("progress", "In progress"),
            ("error", "Error"),
            ("sent", "Sent"),
        ],
        default="new",
    )
    model = fields.Char(string="Model")
    api_response = fields.Text(string="API Response")
    res_id = fields.Integer(string="Record id")
    user_id = fields.Many2one(comodel_name="res.users", string="User")
    message_template = fields.Integer(string="Message Template ID")
    messaging_service = fields.Selection(
        string="Message Service", selection="_get_message_services"
    )
    add_report = fields.Boolean(string="The Meessage Includes a PDF Report")
    message_report = fields.Char(string="Message PDF Report")
    data_file = fields.Text(string="Data PDF Report")
    error = fields.Char(string="Error")
    message_queue_job_ids = fields.Many2many(
        comodel_name="queue.job",
        string="Queue Jobs",
    )
    send_delay = fields.Integer(string="Send delay (seconds)")

    @api.depends("messaging_service", "date", "model")
    def _compute_display_name(self):
        """Compute display name:
        '<message_service> message <date_message_sent> from <model_name>'
        """
        for sel in self:
            sel.display_name = _(
                "{} message {:%d%m%Y-%H:%M} from {}".format(
                    sel.messaging_service, sel.date, sel.model
                )
            )

    def action_go_to_record_id(self):
        """URL to the record_id."""
        self.ensure_one()
        web_base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        url = f"{web_base_url}/web?#id={self.res_id}&view_type=form&model={self.model}"
        return {"type": "ir.actions.act_url", "url": url, "target": "current"}

    def action_go_to_message_template(self):
        """URL to the message template."""
        self.ensure_one()
        web_base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        url = "{}/web?#id={}&view_type=form&model=message.connector.message.builder".format(
            web_base_url,
            self.message_template,
        )
        return {"type": "ir.actions.act_url", "url": url, "target": "current"}

    def create(self, vals):
        res = super().create(vals)
        res._send_message()
        return res

    def _send_message(self):
        for sel in self:
            if hasattr(sel, f"_{sel.messaging_service}_send_message"):
                if sel.env.context.get("send_directly", False):
                    getattr(sel, f"_{sel.messaging_service}_send_message")()
                else:
                    queue_obj = self.env["queue.job"]
                    new_delay = getattr(
                        sel.with_delay(
                            eta=datetime.now() + timedelta(seconds=sel.send_delay)
                        ),
                        f"_{sel.messaging_service}_send_message",
                    )()
                    job = queue_obj.search([("uuid", "=", new_delay.uuid)], limit=1)
                    sel.message_queue_job_ids |= job

    def action_resend_messages(self):
        """Resend several failed messages."""
        self.message_queue_job_ids.filtered(lambda x: x.state == "failed").write(
            {"state": "cancelled"}
        )
        self.filtered(lambda x: x.state == "error")._send_message()

    def _decode_data_file(self, data_file):
        """Returns the decoded file."""
        self.ensure_one()
        return base64.b64decode(data_file)

    @api.autovacuum
    def _gc_messages(self):
        """Message log cleaning."""
        self.search(
            [
                (
                    "date",
                    "<",
                    fields.Datetime.now()
                    - relativedelta(days=self.env.company.log_msg_deletion_freq),
                )
            ]
        ).unlink()
