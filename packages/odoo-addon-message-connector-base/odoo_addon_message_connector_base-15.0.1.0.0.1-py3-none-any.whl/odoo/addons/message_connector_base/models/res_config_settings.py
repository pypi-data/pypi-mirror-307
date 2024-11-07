# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    message_connector_active = fields.Boolean(
        string="Active Message Connector",
        related="company_id.message_connector_active",
        store=True,
        readonly=False,
    )
    log_msg_deletion_freq = fields.Integer(
        string="General Frequency of Log Message Deletion (days)",
        related="company_id.log_msg_deletion_freq",
        default=60,
        store=True,
        readonly=False,
    )

    @api.constrains("log_msg_deletion_freq")
    def _check_log_msg_deletion_freq(self):
        """Checks that the deletion frequency is greater than zero."""
        if self.filtered(lambda x: x.log_msg_deletion_freq < 0):
            raise ValidationError(
                _("The frequency of message log " "deletion must be greater than zero.")
            )

    def set_values(self):
        """Sets all validated channels and active message templates to draft status.
        Consequently, it also disables their automatic actions.
        """
        res = super(ResConfigSettings, self).set_values()
        if not self.message_connector_active:
            self.env["message.connector.channel"].search(
                [("state", "=", "validated")]
            ).action_draft()
            self.env["message.connector.message.builder"].search(
                [("state", "=", "active")]
            ).action_draft()
        return res

    def _get_test_message_vals(self, messaging_service=False):
        """To add the message fields"""
        self.ensure_one()
        vals = {
            "messaging_service": messaging_service,
            "model": self._name,
            "user_id": self._uid,
        }
        return vals

    def _send_test_message(self, messaging_service=False):
        """To send a test message.
        Inherit from the _get_message_vals function to
        add the fields of the message.
        Returns a view wizard with the test result.
        """
        self.ensure_one()
        message_vals = self._get_test_message_vals(messaging_service)
        response = (
            self.env["message.connector.connection"]
            .with_context(send_directly=True)
            .create(message_vals)
        )
        res = _("Connection Test Succeeded!")
        if response.error:
            res = _(
                "There was an error sending the message. "
                "See the message log for more information.\n"
                f"Api response: {response.error} \n"
            )
        view = self.env.ref(
            "message_connector_base.message_connector_base_wizard_test_response"
        )
        return {
            "name": _("Connection Test"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "wizard.test.response",
            "views": [(view.id, "form")],
            "target": "new",
            "context": {**{"message": res}, **dict(self._context or {})},
        }
