# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MessageConnectorChannel(models.Model):
    """This model contains the fields to define the channels through which
    the messages will be sent.
    """

    _name = "message.connector.channel"
    _check_company_auto = True
    _description = "Message Connector Channel"

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
    name = fields.Char(string="Name", required=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("validated", "Validated"),
            ("canceled", "Canceled"),
        ],
        help="Draft: If the channel has messages, all messages will go to "
        "draft status and their automatic actions will be disabled.\n"
        "Validated: The channel can be selected in the messages.\n"
        "Canceled: If the channel has messages, all messages will be canceled "
        "and their automatic actions will be deleted.",
        default="draft",
    )
    messaging_service = fields.Selection(
        string="Message Service", selection="_get_message_services", required=True
    )
    description = fields.Html(string="Description")
    message_template_ids = fields.One2many(
        comodel_name="message.connector.message.builder",
        inverse_name="channel_id",
        string="Message Templates",
    )

    def _compute_message_connector_active(self):
        """Compute if the connector in company is active."""
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

    def action_cancel(self):
        """To cancel the channel.
        This action will cancel the channel message templates.
        """
        self.filtered(lambda x: x.message_connector_active).mapped(
            "message_template_ids"
        ).action_cancel()
        self.filtered(lambda x: x.message_connector_active).write({"state": "canceled"})

    def action_draft(self):
        """To return the channel to draft state.
        This action will return the channel message templates
        back to draft only if it was in a validated status.
        """
        self.filtered(
            lambda x: x.message_connector_active and x.state == "validated"
        ).mapped("message_template_ids").filtered(
            lambda x: x.state == "active"
        ).action_draft()
        self.filtered(lambda x: x.message_connector_active).write({"state": "draft"})

    def action_validate(self):
        """To validate the channel."""
        self.write({"state": "validated"})

    @api.constrains("name")
    def _check_name(self):
        """Checks that there are not two channels
        with the same name.
        """
        for sel in self:
            res = self.search_count([("id", "!=", sel.id), ("name", "=", sel.name)])
            if res:
                raise ValidationError(
                    _("There cannot be two Channels with the same name: '{}'.").format(
                        sel.name
                    )
                )
