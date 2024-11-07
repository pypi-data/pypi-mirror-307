# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WizardTestResponse(models.TransientModel):
    _name = "wizard.test.response"
    _description = "Wizard Test Response"

    def _get_default(self):
        """Gets the message that will be displayed in the wizard with the
        test result.
        """
        res = False
        if self.env.context.get("message", False):
            res = self.env.context.get("message")
        return res

    message = fields.Text(
        string="Test Message Result", readonly=True, default=_get_default
    )
