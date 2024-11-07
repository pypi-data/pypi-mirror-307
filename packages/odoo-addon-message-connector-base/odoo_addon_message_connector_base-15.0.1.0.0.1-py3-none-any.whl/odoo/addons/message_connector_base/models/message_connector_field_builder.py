# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from bs4 import BeautifulSoup

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval


class MessageConnectorFieldBuilder(models.Model):
    """This model allows to configure the different fields that will
    appear in the messages. In addition, it contains all functions that
    will be called from the MessageConnectorMessageBuilder to display the
    values based on the record_id.
    """

    _name = "message.connector.field.builder"
    _description = "Message Connector Field Builder"
    _order = "sequence asc"

    sequence = fields.Integer(string="Sequence", default=30)
    name = fields.Char(string="Name", required=True)
    field_origin = fields.Selection(
        string="Field Origin",
        selection=[
            ("field", "Field"),
            ("rel_field", "Relational Field"),
            ("python", "Python Relation"),
        ],
        required=True,
        default="field",
    )
    field_type = fields.Selection(
        string="Field Type",
        selection=lambda self: self._get_odoo_fields_types(),
        compute="_get_field_type",
        readonly=False,
        store=True,
    )
    field_decimals = fields.Integer(string="Number of Decimals", default=2)
    message_template_id = fields.Many2one(
        comodel_name="message.connector.message.builder", string="Message Template"
    )
    model_id = fields.Many2one(
        comodel_name="ir.model", string="Model", related="message_template_id.model_id"
    )
    field_python = fields.Char(string="Python Expression")
    field_domain_ids = fields.Many2many(
        comodel_name="ir.model.fields",
        string="Field Domain",
        compute="_compute_field_domain",
    )
    field_id = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Field",
        ondelete="cascade",
        domain="[('id', 'in', field_domain_ids)]",
    )
    subfield_domain_ids = fields.Many2many(
        comodel_name="ir.model.fields",
        string="Domain subfield",
        compute="_compute_subfield_domain",
        ondelete="cascade",
    )
    subfield_ids = fields.Many2many(
        comodel_name="ir.model.fields",
        string="Subfields",
        ondelete="cascade",
        domain="[('id', 'in', subfield_domain_ids)]",
    )
    field_expression = fields.Char(
        string="Field Expression", compute="_compute_field_expression"
    )
    default_value = fields.Char(string="Default Value", required=True)
    eval_expression = fields.Boolean(string="Evaluate Expression")
    select_several_fields = fields.Boolean(
        string="Select Several Subfields",
        compute="_compute_select_several_fields",
        store=True,
        readonly=False,
    )
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency")
    truncate = fields.Boolean(
        string="Truncate",
        default=True,
    )

    def _get_odoo_fields_types(self):
        """Returns the allowed field types."""
        return [
            ("boolean", "boolean"),
            ("char", "char"),
            ("date", "date"),
            ("datetime", "datetime"),
            ("float", "float"),
            ("html", "html"),
            ("integer", "integer"),
            ("many2many", "many2many"),
            ("many2one", "many2one"),
            ("monetary", "monetary"),
            ("one2many", "one2many"),
            ("selection", "selection"),
            ("text", "text"),
        ]

    @api.depends("field_origin", "field_id")
    def _get_field_type(self):
        """Gets the field type automatically if it is of type
        field or rel_field.
        """
        for sel in self.filtered(lambda x: x.field_origin != "python"):
            sel.field_type = sel.field_id.ttype
        self.filtered(lambda x: x.field_origin == "python").write({"field_type": False})

    @api.depends("field_origin")
    def _compute_field_domain(self):
        """Computes the domain of the relational fields."""
        for sel in self:
            res = sel.env["ir.model.fields"].search(
                [("model_id", "=", sel.model_id.id)]
            )
            if sel.field_origin == "rel_field":
                res = sel.env["ir.model.fields"].search(
                    [
                        ("model_id", "=", sel.model_id.id),
                        ("ttype", "in", ["one2many", "many2many", "many2one"]),
                    ]
                )
            sel.field_domain_ids = res

    @api.depends("field_origin", "field_id")
    def _compute_subfield_domain(self):
        """Computes the domain of the final subfields of a relation."""
        for sel in self:
            res = []
            if sel.field_origin in ["rel_field", "python"] and sel.field_id:
                model = sel.env["ir.model"].search(
                    [("model", "=", sel.field_id.relation)]
                )
                res = sel.env["ir.model.fields"].search(
                    [
                        ("model_id", "=", model.id),
                        ("ttype", "not in", ["one2many", "many2many", "many2one"]),
                    ]
                )
            sel.subfield_domain_ids = res

    @api.depends("field_id", "field_python")
    def _compute_field_expression(self):
        """Computes the relational expression."""
        for sel in self:
            res = ""
            if sel.field_origin in ["field", "rel_field"]:
                res = f"{sel.field_id.name}"
            else:
                res = sel.field_python
            sel.field_expression = res

    @api.depends("field_origin", "field_id", "field_python")
    def _compute_select_several_fields(self):
        """Sets the select_several_fields field to true if the source is a
        relational field.
        """
        self.filtered(lambda x: x.field_origin == "rel_field").write(
            {"select_several_fields": True}
        )
        self.filtered(lambda x: x.field_origin != "rel_field").write(
            {"select_several_fields": False}
        )

    @api.onchange("field_origin")
    def _onchange_field_origin(self):
        """Clear field_id, field_python, default_value and
        eval_expression if field_origin changes.
        """
        self.write(
            {
                "field_id": None,
                "field_python": None,
                "default_value": None,
                "eval_expression": False,
            }
        )

    @api.onchange("field_id")
    def _onchange_field(self):
        """Clear subfield_ids if field_id changes."""
        self.write({"subfield_ids": None})

    @api.onchange("field_python")
    def _onchange_field_python(self):
        """Clear subfield_ids and field_type if field_python changes."""
        self.write({"subfield_ids": None})
        self.filtered(lambda x: x.eval_expression).write({"field_type": None})

    @api.onchange("select_several_fields")
    def _onchange_select_several_fields(self):
        """Clear  subfield_ids if select_several_fields changes."""
        self.write({"subfield_ids": None})

    @api.onchange("eval_expression")
    def _onchange_eval_expression(self):
        """Clear field_type if eval_expression changes."""
        self.write({"field_type": None})

    def action_eval_expression(self):
        """Evaluates the python expression field by field, if there is a
        field that does not exist it returns an error.
        """

        def _message_error(field):
            raise ValidationError(
                _(
                    "ERROR when evaluating the message. "
                    f"Check if the {field} field exists."
                )
            )

        for sel in self:
            fields = sel.field_python.split(".")
            sel.subfield_ids = None
            sel.select_several_fields = False
            model_id = sel.model_id
            for field in fields[:-1]:
                field_id = self.env["ir.model.fields"].search(
                    [("model_id", "=", model_id.id), ("name", "=", field)]
                )
                model_id = self.env["ir.model"].search(
                    [("model", "=", field_id.relation)]
                )
                if not model_id:
                    _message_error(field)
            field_id = self.env["ir.model.fields"].search(
                [("model_id", "=", model_id.id), ("name", "=", fields[-1])]
            )
            if not field_id:
                _message_error(fields[-1])
            sel.field_id = field_id
            sel.field_type = field_id.ttype

    """
        --------------------------------------------------
        Functions to display the values based on record_id
        --------------------------------------------------
    """

    def _get_field_value(self, field_expression, record_id, map_names=False):
        """Returns the field value.
        If you want to mapped one2many or many2many names set
        map_names to True.
        """
        self.ensure_one()
        expression = f"self.{field_expression}"
        if map_names:
            expression = f"self.{field_expression}.mapped('name')"
        try:
            value = safe_eval(expression, {"self": record_id})
        except Exception:
            value = ""
        if map_names and value:
            value = ", ".join(value)
        return value

    """
        The following functions are called depending on the field type.
        If you need to change the format depending on the type of functions,
        inherit from any of these functions.
    """

    def _boolean_field(self, field_expression, record_id):
        """Returns the field of type boolean."""
        self.ensure_one()
        res = _("False")
        value = self._get_field_value(field_expression, record_id)
        if value:
            res = _("True")
        return res

    def _char_field(self, field_expression, record_id):
        """Returns the field of type char."""
        self.ensure_one()
        return self._get_field_value(field_expression, record_id)

    def _date_field(self, field_expression, record_id):
        """Returns the field of type date."""
        self.ensure_one()
        value = self._get_field_value(field_expression, record_id)
        if value:
            value = self.env["ir.qweb.field.date"].value_to_html(value, {})
        return value

    def _datetime_field(self, field_expression, record_id):
        """Returns the field of type datetime."""
        self.ensure_one()
        value = self._get_field_value(field_expression, record_id)
        if value:
            value = self.env["ir.qweb.field.datetime"].value_to_html(value, {})
        return value

    def _float_field(self, field_expression, record_id):
        """Returns fields of type float:
        1. Extracts the value.
        2. Format the value by calling the value_to_html function.
        """
        self.ensure_one()
        value = self._get_field_value(field_expression, record_id)
        if value:
            decimal_precision_id = None
            if self.field_type == "python" and not self.eval_expression:
                decimal_precision_id = self.decimal_precision_id
            value = self.env["ir.qweb.field.float"].value_to_html(
                value, {"decimal_precision": decimal_precision_id}
            )
        return value

    def _html_field(self, field_expression, record_id):
        """Returns fields of type html:
        1. Extracts the value.
        2. Converts html value to text.
        """
        self.ensure_one()
        value = self._get_field_value(field_expression, record_id)
        value = BeautifulSoup(value, "html.parser").get_text(strip=True)
        return value

    def _integer_field(self, field_expression, record_id):
        """Returns the field of type char."""
        self.ensure_one()
        return self._get_field_value(field_expression, record_id)

    def _many2many_field(self, field_expression, record_id):
        """Returns the field of type many2many."""
        self.ensure_one()
        return self._get_field_value(field_expression, record_id, True)

    def _many2one_field(self, field_expression, record_id):
        """Returns the field of type many2one."""
        self.ensure_one()
        return self._get_field_value(field_expression, record_id, True)

    def _monetary_field(self, field_expression, record_id):
        """Returns fields of type monetary."""
        self.ensure_one()
        value = self._get_field_value(field_expression, record_id)
        if value:
            currency_id = self.env.company.currency_id
            if self.field_type == "python" and not self.eval_expression:
                currency_id == self.currency_id
            elif record_id._fields["currency_id"] and record_id.currency_id:
                currency_id = record_id.currency_id
            value = self.env["ir.qweb.field.monetary"].value_to_html(
                value, {"display_currency": currency_id}
            )
            value = BeautifulSoup(value, "html.parser").get_text(strip=True)
        return value

    def _one2many_field(self, field_expression, record_id):
        """Returns the field of type one2many."""
        self.ensure_one()
        return self._get_field_value(field_expression, record_id, True)

    def _selection_field(self, field_expression, record_id):
        """Returns the field of type selection."""
        self.ensure_one()
        return self._get_field_value(field_expression, record_id)

    def _text_field(self, field_expression, record_id):
        """Returns the field of type text."""
        self.ensure_one()
        return self._get_field_value(field_expression, record_id)

    def _get_value(self, field_expression, field_type, record_id):
        """Identifies the field type and calls the appropriate function."""
        self.ensure_one()
        value = ""
        if hasattr(self, f"_{field_type}_field"):
            value = getattr(self, f"_{field_type}_field")(field_expression, record_id)
        return value

    def _table_formatter(self, table):
        """Function for each messaging service to format the tables."""
        self.ensure_one()
        return table

    def _get_value_table(self, record_ids):
        """Returns all the subfields of the relation in a table.
        If the table has only one field, returns only the field.
        """
        self.ensure_one()
        res = ""
        if len(record_ids) == 1 and len(self.subfield_ids) == 1:
            value = self._get_value(
                self.subfield_ids[0].name, self.subfield_ids[0].ttype, record_ids[0]
            )
            res = value
        else:
            table = []
            for record in record_ids:
                line = []
                for subfield in self.subfield_ids:
                    value = self._get_value(subfield.name, subfield.ttype, record)
                    line.append(value if value else "")
                table.append(line)
            res = self._table_formatter(table)
        return res

    def get_value(self, record_id):
        """Identifies whether it is a single field or multiple fields and
        retrieves the field(s).
        """
        self.ensure_one()
        value = ""
        if self.field_origin in ["rel_field", "python"] and self.select_several_fields:
            record_ids = self._get_field_value(self.field_expression, record_id)
            if record_ids:
                value = self._get_value_table(record_ids)
        else:
            value = self._get_value(self.field_expression, self.field_type, record_id)
        return value
