# Copyright 2023 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    unvalued_copy = fields.Boolean(
        "Unvalued Copy",
        help="Print an unvalued picking copy",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.update(
                {
                    "unvalued_copy": self.env["res.partner"]
                    .browse(vals["partner_id"])
                    .unvalued_picking_copy
                }
            )
        return super().create(vals_list)
