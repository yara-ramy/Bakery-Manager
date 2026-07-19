from odoo import models, fields, api


class BakeryOrderLine(models.Model):
    _name = 'bakery.order.line'
    _description = 'Bakery Order Line'

    item_id = fields.Many2one('bakery.item')
    order_id = fields.Many2one('bakery.order')
    quantity = fields.Integer(string='Quantity', default=1)
    unit_price = fields.Monetary(
        string="Unit Price",
        currency_field="currency_id"
    )
    subtotal = fields.Monetary(
        string="Subtotal",
        currency_field="currency_id",
        compute="_compute_subtotal",
        store=True
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="order_id.currency_id",
        store=True
    )

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for order in self:
            order.subtotal = order.quantity * order.unit_price