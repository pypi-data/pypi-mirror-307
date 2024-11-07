# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Low Sold Product Report",
    "summary": "Adjustable Report of least sold product",
    "version": "17.0.1.0.1",
    "category": "Sales",
    "website": "https://github.com/sygel-technology/sy-sale-reporting",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
    ],
    "data": [
        "security/low_sold_product_report_security.xml",
        "security/ir.model.access.csv",
        "report/low_sold_product_report_views.xml",
        "views/res_config_settings_views.xml",
        "wizards/low_sold_product_report_wizard_views.xml",
    ],
}
