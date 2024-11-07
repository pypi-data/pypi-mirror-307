# Copyright 2023 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Message Connector Base",
    "summary": "Message Connector Base",
    "version": "15.0.1.0.0",
    "category": "Custom",
    "website": "https://github.com/sygel-technology/sy-social",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["base", "base_setup", "base_automation", "mass_editing", "queue_job"],
    "data": [
        "data/actions_server.xml",
        "data/message_connector_base_queue_job.xml",
        "security/message_connector_base_security.xml",
        "security/ir.model.access.csv",
        "wizard/wizard_send_test_message_views.xml",
        "wizard/wizard_test_response_views.xml",
        "views/message_connector_channel_views.xml",
        "views/res_config_settings_views.xml",
        "views/message_connector_connection_views.xml",
        "views/message_connector_field_builder_views.xml",
        "views/message_connector_message_builder_views.xml",
        "views/ir_actions_server_views.xml",
    ],
}
