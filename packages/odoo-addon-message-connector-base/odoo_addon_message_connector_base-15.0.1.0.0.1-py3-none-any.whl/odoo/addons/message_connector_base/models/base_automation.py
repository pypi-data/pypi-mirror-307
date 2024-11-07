# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class BaseAutomation(models.Model):
    _inherit = "base.automation"

    def unlink(self):
        """Changes Message Template state before delete."""
        for sel in self.filtered(lambda x: x.message_template_id):
            sel.message_template_id.state = "draft"
        super().unlink()
