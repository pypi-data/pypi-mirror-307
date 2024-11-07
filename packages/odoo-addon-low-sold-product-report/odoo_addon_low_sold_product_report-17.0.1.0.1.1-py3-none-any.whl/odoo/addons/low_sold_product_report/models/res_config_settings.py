# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    low_sales_report_default_product_type = fields.Selection(
        selection=[
            ("product_product", "By product variants"),
            ("product_template", "By product templates"),
        ],
        related="company_id.low_sales_report_default_product_type",
        readonly=False,
        required=True,
    )
    low_sales_report_default_period = fields.Selection(
        selection=[
            ("1", "Last Month"),
            ("3", "Last 3 Months"),
            ("6", "Last 6 Months"),
            ("12", "Last 12 Month"),
        ],
        related="company_id.low_sales_report_default_period",
        readonly=False,
        required=True,
    )
    low_sales_report_default_sold_quantity_limit = fields.Float(
        related="company_id.low_sales_report_default_sold_quantity_limit",
        digits="Product Unit of Measure",
        readonly=False,
    )
    low_sales_report_default_sold_amount_limit = fields.Float(
        related="company_id.low_sales_report_default_sold_amount_limit",
        digits="Product Unit of Measure",
        readonly=False,
    )
