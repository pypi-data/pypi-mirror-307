# Copyright 2023 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class QueueJob(models.Model):
    _inherit = "queue.job"

    def cancel_now(self):
        self.sudo().filtered(lambda x: x.state in ["pending", "enqueued"]).write(
            {"state": "cancelled"}
        )

    def requeue_sudo(self):
        self.sudo().requeue()
