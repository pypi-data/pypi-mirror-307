# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductSetLine(models.Model):
    _inherit = "product.set.line"

    show_line_report = fields.Boolean(string="Line in Report", default=True)
