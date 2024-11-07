# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class LowSoldProductReport(models.Model):
    _name = "low.sold.product.report"
    _description = "Low Sold Products Report"
    _auto = False
    _rec_name = "product_id"
    _order = "product_id desc"

    product_id = fields.Many2one(
        comodel_name="product.product", string="Product Variant", readonly=True
    )
    product_tmpl_id = fields.Many2one(
        comodel_name="product.template", string="Product Template", readonly=True
    )
    product_uom_qty = fields.Float(
        string="Sold Qty",
        digits="Product Unit of Measure",
        readonly=True,
        help="Which sales level consider to be low in default units of measure",
    )
    price_subtotal = fields.Monetary(
        string="Sold Untaxed Amount",
        readonly=True,
        help="Which sales level consider to be low in default units of measure",
    )
    categ_id = fields.Many2one(
        comodel_name="product.category", string="Product Category", readonly=True
    )
    product_uom = fields.Many2one(
        comodel_name="uom.uom", string="Unit of Measure", readonly=True
    )
    detailed_type = fields.Selection(
        [("consu", "Consumable"), ("service", "Service")],
        string="Product Type",
        readonly=True,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency", compute="_compute_currency_id"
    )

    query_type = fields.Selection(
        selection=[
            ("product_product", "By product variants"),
            ("product_template", "By product templates"),
        ],
        compute="_compute_query_type",
    )
    name = fields.Char(compute="_compute_query_type")

    @api.depends_context("allowed_company_ids")
    def _compute_currency_id(self):
        for rec in self:
            rec.currency_id = self.env.company.currency_id

    @api.depends_context("product_type")
    def _compute_query_type(self):
        for rec in self:
            rec.query_type = self.env.context.get("product_type", "product_product")
            rec.name = (
                rec.product_id.name
                if rec.query_type == "product_product"
                else rec.product_tmpl_id.name
            )

    def _select(self):
        template_type = self.env.context.get("product_type") == "product_template"
        select_ = f"""
            {"l.product_id" if not template_type else "0"} as product_id,
            p.product_tmpl_id as product_tmpl_id,
            t.uom_id AS product_uom,
            CASE WHEN p.product_tmpl_id IS NOT NULL THEN
            SUM(l.product_uom_qty / u.factor * u2.factor) ELSE 0 END AS product_uom_qty,
            CASE WHEN p.product_tmpl_id IS NOT NULL THEN
            SUM(l.price_subtotal) ELSE 0 END AS price_subtotal,
            t.categ_id AS categ_id,
            t.detailed_type AS detailed_type
            """
        return select_

    def _case_value_or_one(self, value):
        return f"""CASE COALESCE({value}, 0) WHEN 0 THEN 1.0 ELSE {value} END"""

    def _from(self):
        return """
            sale_order_line l
            LEFT JOIN sale_order s ON s.id=l.order_id
            LEFT JOIN product_product p ON l.product_id=p.id
            LEFT JOIN product_template t ON p.product_tmpl_id=t.id
            LEFT JOIN uom_uom u ON u.id=l.product_uom
            LEFT JOIN uom_uom u2 ON u2.id=t.uom_id
            LEFT JOIN res_partner rp ON s.partner_id = rp.id
            """

    def _where(self):
        res = """
            l.display_type IS NULL AND
            l.state = 'sale'"""
        if self.env.context.get("date_from"):
            date_from = self.env.context.get("date_from")
            res += f" AND s.date_order >= '{str(date_from)}'"

        if self.env.context.get("date_to"):
            date_to = self.env.context.get("date_to")
            res += f" AND s.date_order <= '{str(date_to)}'"

        if self.env.context.get("team_ids"):
            team_ids = self.env.context.get("team_ids")
            team_str = ",".join(map(str, team_ids))
            res += f" AND s.team_id in ({team_str})"

        if self.env.context.get("country_ids"):
            country_ids = self.env.context.get("country_ids")
            country_str = ",".join(map(str, country_ids))
            res += f" AND rp.country_id in ({country_str})"

        return res

    def _group_by(self):
        template_type = self.env.context.get("product_type") == "product_template"
        return f"""
            {"l.product_id," if not template_type else ""}
            p.product_tmpl_id,
            t.uom_id,
            t.categ_id,
            t.detailed_type
        """

    def _query_zero_products(self):
        template_type = self.env.context.get("product_type") == "product_template"
        select = f"""
            SELECT
                {"p.id" if not template_type else "0"} as product_id,
                p.product_tmpl_id as product_tmpl_id,
                t.uom_id AS product_uom,
                0 AS product_uom_qty,
                0 AS price_subtotal,
                t.categ_id AS categ_id,
                t.detailed_type AS detailed_type
            FROM product_product p
                LEFT JOIN product_template t ON p.product_tmpl_id=t.id
            WHERE
                {"p" if not template_type else "t"}.active = TRUE
                AND t.sale_ok = TRUE
                AND {"p" if not template_type else "t"}.id NOT IN (
                    SELECT
                        {"l.product_id" if not template_type else "p.product_tmpl_id"}
                    FROM sale_order_line l
                        LEFT JOIN product_product p ON l.product_id=p.id
                        LEFT JOIN sale_order s ON s.id=l.order_id
                        LEFT JOIN res_partner rp ON s.partner_id = rp.id
                    WHERE {self._where()}
                    GROUP BY
                        {"l.product_id" if not template_type else "p.product_tmpl_id"}
                )
            GROUP BY {self._group_by().replace("l.product_id,", "p.id,")}
        """
        return select

    def _query(self):
        template_type = self.env.context.get("product_type") == "product_template"
        price_subtotal_limit = self.env.context.get("sold_quantity_limit", 0)
        product_uom_qty_limit = self.env.context.get("sold_amount_limit", 0)
        return f"""
            SELECT ROW_NUMBER () OVER (
                ORDER BY
                {"p.product_id" if not template_type else "p.product_tmpl_id"}
            ) as id , *
            FROM (
                SELECT * FROM (
                    SELECT {self._select()}
                    FROM {self._from()}
                    WHERE {self._where()}
                    GROUP BY {self._group_by()}
                ) s
                WHERE product_uom_qty <= {price_subtotal_limit} OR
                    price_subtotal <= {product_uom_qty_limit}
                UNION
                {self._query_zero_products()}
            ) p
        """

    @property
    def _table_query(self):
        return self._query()

    def view_product(self):
        self.ensure_one()
        template_type = self.env.context.get("product_type") == "product_template"
        return {
            "type": "ir.actions.act_window",
            "name": ("TEST2"),
            "res_id": self.product_id.id
            if not template_type
            else self.product_tmpl_id.id,
            "view_mode": "form",
            "res_model": "product.product" if not template_type else "product.template",
        }
