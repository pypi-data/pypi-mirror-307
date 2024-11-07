# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IrActionsServer(models.Model):
    _inherit = "ir.actions.server"

    message_template_id = fields.Many2one(
        comodel_name="message.connector.message.builder",
        string="Message Template",
        readonly=True,
    )
