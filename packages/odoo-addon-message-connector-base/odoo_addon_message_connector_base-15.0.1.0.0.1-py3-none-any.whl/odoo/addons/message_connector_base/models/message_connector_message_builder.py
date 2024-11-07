# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MessageConnectorMessageBuilder(models.Model):
    """This model allows to create templates with the messages to be sent."""

    _name = "message.connector.message.builder"
    _check_company_auto = True
    _order = "state asc"
    _description = "Message Template Builder"

    def _get_message_services(self):
        """Return the list of message service installed."""
        return self.env.company.get_message_services()

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    message_connector_active = fields.Boolean(
        string="Message Connector Active", compute="_compute_message_connector_active"
    )
    name = fields.Char(
        string="Name",
        states={"active": [("readonly", True)], "canceled": [("readonly", True)]},
        required=True,
    )
    state = fields.Selection(
        string="State",
        selection=[("draft", "Draft"), ("active", "Active"), ("canceled", "Canceled")],
        default="draft",
        compute="_compute_state",
        store=True,
        readonly=False,
    )
    messaging_service = fields.Selection(
        string="Message Service",
        states={"active": [("readonly", True)], "canceled": [("readonly", True)]},
        selection="_get_message_services",
        required=True,
    )
    channel_id = fields.Many2one(
        comodel_name="message.connector.channel",
        string="Channel",
        states={"active": [("readonly", True)], "canceled": [("readonly", True)]},
        domain=lambda self: "[\
            ('messaging_service', '=', messaging_service),\
            ('state', '=', 'validated')\
        ]",
        required=True,
    )
    model_id = fields.Many2one(
        comodel_name="ir.model",
        string="Model",
        states={"active": [("readonly", True)], "canceled": [("readonly", True)]},
        ondelete="cascade",
        domain=[("transient", "=", False)],
    )
    message_field_ids = fields.One2many(
        comodel_name="message.connector.field.builder",
        inverse_name="message_template_id",
        string="Fields",
        states={"active": [("readonly", True)], "canceled": [("readonly", True)]},
        copy=True,
    )
    automation_id = fields.Many2one(
        comodel_name="base.automation", string="Automated Action"
    )
    add_report = fields.Boolean(
        string="Add Report to Message",
        states={"active": [("readonly", True)], "canceled": [("readonly", True)]},
        default=False,
    )
    message_report = fields.Char(
        string="File Introduction Message",
        states={"active": [("readonly", True)], "canceled": [("readonly", True)]},
    )
    report_id = fields.Many2one(
        string="Report",
        comodel_name="ir.actions.report",
        states={"active": [("readonly", True)], "canceled": [("readonly", True)]},
        domain="[('model_id', '=', model_id), \
        ('report_type', '=', 'qweb-pdf')]",
    )
    creation_delay = fields.Integer(
        string="Creation delay (seconds)",
        default=60,
        states={"active": [("readonly", True)], "canceled": [("readonly", True)]},
    )
    send_delay = fields.Integer(
        string="Send delay (seconds)",
        default=60,
        states={"active": [("readonly", True)], "canceled": [("readonly", True)]},
    )

    def action_delete_automated_action(self):
        """Removes the automatic action and the related server action."""
        for sel in self.filtered(lambda x: x.automation_id):
            server_action_id = sel.automation_id.action_server_id
            sel.automation_id.unlink()
            server_action_id.unlink()

    def action_cancel(self):
        """To cancel message template.
        This action will remove the automatic action if it exists.
        """
        self.filtered(
            lambda x: x.message_connector_active and x.automation_id
        ).action_delete_automated_action()
        self.filtered(lambda x: x.message_connector_active).write({"state": "canceled"})

    def action_draft(self):
        """To return the message template to draft state."""
        msg = ""
        for sel in self.filtered(lambda x: x.message_connector_active):
            if sel.channel_id.state == "validated":
                sel.write({"state": "draft"})
                sel.automation_id.action_archive()
            else:
                msg = _(
                    "The selected channel is not validated. To move the "
                    "message to draft state, first validate the channel "
                    "or select another validated channel."
                )
        if msg:
            raise ValidationError(msg)

    def action_activate(self):
        """To activate message template.
        This action will also activate the automatic action.
        """
        msg = ""
        for sel in self.filtered(lambda x: x.message_connector_active):
            if sel.automation_id:
                if sel.channel_id.state == "validated":
                    sel.write({"state": "active"})
                    sel.automation_id.action_unarchive()
                else:
                    msg = _(
                        "The selected channel is not validated. To "
                        "activate the message, first validate the channel "
                        "or select another validated channel."
                    )
            else:
                msg = _(
                    "It is necessary to create an automatic action before "
                    "activating the message."
                )
        if msg:
            raise ValidationError(msg)

    @api.depends("automation_id.active")
    def _compute_state(self):
        """Depending on the status of the automatic action, the status of
        the message changes. In the event that the channel is in 'draft'
        state, this also changes.
        """
        self.mapped("channel_id").filtered(
            lambda x: x.state == "draft"
        ).action_validate()
        self.filtered(
            lambda x: x.automation_id.active and x.state == "draft"
        ).action_activate()
        self.filtered(
            lambda x: not x.automation_id.active and x.state == "active"
        ).action_draft()

    def _get_data_file(self, record_id):
        """Return the data_file with the selected report template."""
        self.ensure_one()
        xml_id = self.report_id.xml_id
        report = self.env.ref(xml_id)
        report_template_id = report._render_qweb_pdf(record_id.id)
        data_file = base64.b64encode(report_template_id[0])
        return data_file

    def _compute_message_connector_active(self):
        """Compute if the connector is active."""
        for sel in self:
            sel.message_connector_active = sel._message_connector_is_active()

    def _message_connector_is_active(self):
        """Returns the status of the connector in the company.
        Create <messaging_service>_active field to check the messaging
        service state.
        """
        self.ensure_one()
        res = self.company_id.message_connector_active
        if self.messaging_service:
            res = getattr(self.company_id, f"{self.messaging_service}_active")
        return res

    def unlink(self):
        """Clear automation and server action before delete message."""
        for sel in self:
            server_action_id = sel.automation_id.action_server_id
            sel.automation_id.unlink()
            server_action_id.unlink()
        super().unlink()

    def _get_fields(self, record_id):
        """Gets the fields."""
        fields = []
        for field in self.message_field_ids:
            value = field.get_value(record_id)
            field_vals = self._get_field_vals(field, value)
            fields.append(field_vals)
        return fields

    def _get_field_vals(self, field, value):
        """To add more vals to the fields inherit from this function."""
        res = {
            "title": field.name,
            "value": value if value else field.default_value,
        }
        return res

    def _get_url(self, record_id):
        """Gets the record url."""
        web_base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        url = "{}/web?#id={}&view_type=form&model={}".format(
            web_base_url, record_id.id, self.model_id.model
        )
        return url

    def _get_message_vals(self, record_id):
        """Message fields. To add more fields inherit from this fucnion."""
        self.ensure_one()
        vals = {
            "messaging_service": self.messaging_service,
            "model": self.model_id.model,
            "res_id": record_id.id,
            "user_id": self._uid,
            "message_template": self.id,
            "send_delay": self.send_delay,
        }
        if self.add_report:
            vals.update(
                {
                    "add_report": self.add_report,
                    "message_report": self.message_report,
                    "data_file": self._get_data_file(record_id),
                }
            )
        return vals

    def action_send_message(self, record_id):
        """Send a message by creating an instance of
        message.connector.connection
        To add more fields to the message inheriting from _get_message_vals
        """
        self.ensure_one()
        if self.message_connector_active:
            res = None
            if self.env.context.get("send_directly", False):
                res = self._action_send_message(record_id)
            else:
                res = self.with_delay(
                    eta=datetime.now() + timedelta(seconds=self.creation_delay)
                )._action_send_message(record_id)
            return res

    def _action_send_message(self, record_id):
        res = self.env["message.connector.connection"].create(
            self._get_message_vals(record_id)
        )
        return res

    def action_create_automated_action(self):
        """To create an automatic action for sending
        the message automatically.
        """
        self.ensure_one()
        res = None
        if self.message_connector_active:
            code = """model.env['message.connector.message.builder'].browse([{}]).action_send_message(model.browse(model._context.get('active_ids', model._context.get('active_id'))))
            """.format(self.id)
            self.automation_id = self.env["base.automation"].create(
                {
                    "name": f"Message Connector {self.messaging_service}: {self.name}",
                    "active": self.state == "active",
                    "message_template_id": self.id,
                    "model_id": self.model_id.id,
                    "trigger": "on_write",
                    "state": "code",
                    "code": code,
                }
            )
            res = {
                "view_type": "form",
                "view_mode": "form",
                "view_id": self.env.ref("base_automation.view_base_automation_form").id,
                "res_model": "base.automation",
                "res_id": self.automation_id.id,
                "type": "ir.actions.act_window",
                "context": {
                    "form_view_initial_mode": "edit",
                    "force_detailed_view": "true",
                },
                "target": "current",
            }
        return res

    @api.onchange("model_id")
    def _onchange_model_id(self):
        """Removes all fields if model_id is changed."""
        self.mapped("message_field_ids").unlink()

    def copy(self, default=None):
        """Copy the record with another name."""
        default = dict(
            default or {}, name=_("{} (copy)").format(self.name), automation_id=None
        )
        return super(MessageConnectorMessageBuilder, self).copy(default=default)

    @api.constrains("name")
    def _check_name(self):
        """Checks that there are not two message templates
        with the same name.
        """
        for sel in self:
            res = self.search_count([("id", "!=", sel.id), ("name", "=", sel.name)])
            if res:
                raise ValidationError(
                    _("There cannot be two Messages with the same name: '{}'.").format(
                        sel.name
                    )
                )

    @api.constrains("model_id")
    def _check_model(self):
        """Checks that the model is not changed after the utomatic action
        is created.
        """
        for sel in self.filtered(lambda x: x.automation_id):
            if sel.automation_id.model_id != sel.model_id:
                raise ValidationError(
                    _(
                        "The model cannot be changed once the auto action is "
                        "created. If you want to change the model, first remove "
                        "the automatic action.\n"
                        "Automatic Action Model: '{}'\n"
                        "Message Model: '{}'"
                    ).format(sel.automation_id.model_id.name, sel.model_id.name)
                )
