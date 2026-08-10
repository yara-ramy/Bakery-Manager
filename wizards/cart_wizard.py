from odoo import fields, models

class CartWizard(models.TransientModel):
    _name = 'bakery.cart.wizard'
    _description = 'Add items to cart'

    item_id = fields.Many2one(
        'bakery.item',
        string='Item',
        required=True,
    )
    quantity = fields.Integer(
        string='Quantity',
        default=1,
    )

    def action_confirm(self):
        self.ensure_one()
        customer = self.env.user.partner_id
        cart = self.env['bakery.order'].search([
            ("customer_id","=",customer.id),
            ("status", "=", "cart"),
        ], limit=1)
        if not cart:
            cart = self.env['bakery.order'].create({
                "customer_id": self.env.user.partner_id.id,
            })
        existing_line = self.env['bakery.order.line'].search([
            ("order_id","=",cart.id),
            ("item_id","=",self.item_id.id),
        ], limit=1)
        if existing_line:
            existing_line.quantity += self.quantity
        else:
            existing_line = self.env['bakery.order.line'].create({
                "order_id": cart.id,
                "item_id": self.item_id.id,
                "quantity": self.quantity,
                "unit_price": self.item_id.price,
            })
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Success",
                "message": "Added to cart successfully!",
                "type": "success",
                "sticky": False,
                "next": {
                    "type": "ir.actions.act_window_close",
                }
            }
        }
