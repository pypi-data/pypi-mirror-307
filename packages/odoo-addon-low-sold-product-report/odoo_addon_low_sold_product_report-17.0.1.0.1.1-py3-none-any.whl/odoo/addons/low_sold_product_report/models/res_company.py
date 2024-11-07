# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    low_sales_report_default_product_type = fields.Selection(
        selection=[
            ("product_product", "By product variants"),
            ("product_template", "By product templates"),
        ],
        required=True,
        default="product_product",
    )
    low_sales_report_default_period = fields.Selection(
        selection=[
            ("1", "Last Month"),
            ("3", "Last 3 Months"),
            ("6", "Last 6 Months"),
            ("12", "Last 12 Month"),
        ],
        string="Default analyzed period",
        required=True,
        default="1",
    )
    low_sales_report_default_sold_quantity_limit = fields.Float(
        digits="Product Unit of Measure"
    )
    low_sales_report_default_sold_amount_limit = fields.Float(
        digits="Product Unit of Measure"
    )
