# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductSetAdd(models.TransientModel):
    _inherit = "product.set.add"

    hide_set_lines = fields.Selection(
        string="Show Lines in Sales Report",
        selection=[
            ("by_set_config", "Depending on the set configuration"),
            ("hide_lines", "Hide All Lines"),
            ("show_lines", "Show All Lines"),
        ],
        help="'Depending on the set configuration': All lines that have been "
        "configured in the product set will be displayed in the sales report."
        "\n'Hide all lines': all lines of the product set will be hidden in "
        "the sales report.\n'Show all lines': all lines of the product set "
        "will be displayed in the sales report.\nYou can also modify the "
        "product set lines displayed in the sales report from the sales order.",
        default="by_set_config",
        required=True,
    )

    def prepare_sale_order_line_data(self, set_line, max_sequence=0):
        sol_data = super().prepare_sale_order_line_data(set_line, max_sequence)
        if self.hide_set_lines == "by_set_config" and not set_line.show_line_report:
            sol_data.update({"show_line_report": False})
        elif self.hide_set_lines == "hide_lines" and not set_line.display_type:
            sol_data.update({"show_line_report": False})
        return sol_data
