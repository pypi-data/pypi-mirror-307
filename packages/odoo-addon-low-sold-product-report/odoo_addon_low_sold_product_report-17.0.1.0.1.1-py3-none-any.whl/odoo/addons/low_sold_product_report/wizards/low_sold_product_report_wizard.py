# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

from dateutil.relativedelta import relativedelta

from odoo import fields, models


class LowSoldProductReportWizard(models.TransientModel):
    _name = "low_sold_product_report_wizard"
    _description = "Wizard to query low sold products"

    product_type = fields.Selection(
        selection=[
            ("product_product", "By product variants"),
            ("product_template", "By product templates"),
        ],
        default=lambda s: s.env.company.low_sales_report_default_product_type,
        required=True,
    )

    date_start = fields.Date(
        default=lambda self: (
            datetime.date.today()
            - relativedelta(
                months=int(self.env.company.low_sales_report_default_period)
            )
        ),
        required=True,
    )
    date_end = fields.Date(default=datetime.date.today(), required=True)

    sold_quantity_limit = fields.Float(
        default=lambda s: s.env.company.low_sales_report_default_sold_quantity_limit,
        digits="Product Unit of Measure",
    )
    sold_amount_limit = fields.Float(
        default=lambda s: s.env.company.low_sales_report_default_sold_amount_limit,
        digits="Product Unit of Measure",
    )

    team_ids = fields.Many2many(
        comodel_name="crm.team",
        string="Sales Teams",
        help="If not chosen, all sales teams would be analyzed",
    )
    country_ids = fields.Many2many(
        comodel_name="res.country",
        string="Partner Country",
        help="If not selected all countries would be taken into account",
    )

    def action_accept(self):
        self.ensure_one()
        context = {
            "date_from": self.date_start,
            "date_to": self.date_end,
            "sold_quantity_limit": self.sold_quantity_limit,
            "sold_amount_limit": self.sold_amount_limit,
            "product_type": self.product_type,
            "team_ids": self.team_ids.ids,
            "country_ids": self.country_ids.ids,
        }
        return {
            "type": "ir.actions.act_window",
            "name": ("TEST"),
            "view_mode": "tree,pivot",
            "res_model": "low.sold.product.report",
            "context": context,
        }
