# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class WizardSendTestMessage(models.TransientModel):
    _name = "wizard.send.test.message"
    _description = "Wizard Send Test Message"

    def _get_default_model_id(self):
        """Gets the model of the active message template."""
        res = None
        model_id = (
            self.env["message.connector.message.builder"]
            .browse(self._context.get("active_id"))
            .model_id
        )
        if model_id:
            res = model_id
        return res

    model_id = fields.Many2one(
        comodel_name="ir.model",
        string="Model",
        readonly=True,
        ondelete="cascade",
        default=_get_default_model_id,
    )
    record_selection = fields.Selection(
        string="Record",
        selection=lambda self: self._record_selection(),
    )

    def _record_selection(self):
        """Gets the list of records of the selected model in
        the message template.
        """
        res = []
        model_id = (
            self.env["message.connector.message.builder"]
            .browse(self._context.get("active_id"))
            .model_id
        )
        if model_id:
            record_list = self.env[model_id.model].search([]).mapped("name")
            for record in record_list:
                res.append((record, record))
        return res

    def action_send_test_message(self):
        """Gets the record and sends the message from the message template
        that called the wizard.
        Returns a view wizard with the test result.
        """
        record_id = self.env[self.model_id.model].search(
            [("name", "=", self.record_selection)], limit=1
        )
        response = (
            self.env["message.connector.message.builder"]
            .browse(self._context.get("active_id"))
            .with_context(send_directly=True)
            .action_send_message(record_id)
        )
        res = _("Message sent successfully")
        if response.error:
            res = _(
                "There was an error sending the message. "
                "See the message log for more information.\n"
                f"Api response: {response.error} \n"
            )
        view = self.env.ref(
            "message_connector_base.message_connector_base_wizard_test_response"
        )
        context = dict(self._context or {})
        context["message"] = res
        return {
            "name": _("Message Test"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "wizard.test.response",
            "views": [(view.id, "form")],
            "target": "new",
            "context": context,
        }
