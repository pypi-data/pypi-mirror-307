# Copyright 2022 Angel Garcia de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    message_connector_active = fields.Boolean(
        string="Active Message Connector", default=False
    )
    log_msg_deletion_freq = fields.Integer(
        string="General Frequency of Log Message Deletion (days)", default=60
    )

    def get_message_services(self):
        """To add message services."""
        return []
