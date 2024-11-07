# Copyright 2023 Ángel García de la Chica <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "SO Product Set Report Hide Lines",
    "summary": "Hide sale order lines by product set",
    "version": "15.0.1.0.0",
    "category": "Sale",
    "website": "https://github.com/sygel-technology/sy-sale-reporting",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["so_report_hide_lines"],
    "data": ["views/product_set.xml", "wizard/product_set_add.xml"],
}
