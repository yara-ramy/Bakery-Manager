from odoo import models, fields, api


class BakeryOrder(models.Model):
    _name = 'bakery.order'
    _description = 'Bakery Order'

    customer_id = fields.Many2one('res.partner',string='Customer', required=True)
    order_line_ids = fields.One2many('bakery.order.line', 'order_id', string="Order Lines")
    total_price = fields.Monetary(string='Total Price',currency_field="currency_id"
                                  ,compute='_compute_total_price', store=True)
    status = fields.Selection([
        ('cart','Cart'),
        ('confirmed','Confirmed'),
        ('shipped','Shipped'),
        ('in_transit','In Transit'),
        ('delivered','Delivered')
    ])
    currency_id = fields.Many2one('res.currency',string='Currency',
                                  default=lambda self: self.env.ref("base.EGP"))
    order_date = fields.Datetime(string='Order Date', required=True, default=fields.Datetime.now)

    phone = fields.Char(string='Phone Number')
    shipping_address = fields.Text(string='Shipping Address')
    payment_method = fields.Selection([
        ('cash','Cash on delivery'),
        ('credit','Credit card')
    ], string='Payment Method')

    @api.depends('order_line_ids.subtotal')
    def _compute_total_price(self):
        for order_line in self:
            order_line.total_price = sum(order_line.order_line_ids.mapped('subtotal'))

    def action_checkout(self):
        self.ensure_one()
        partner = self.customer_id
        self.phone = partner.phone
        self.shipping_address = ', '.join(filter(None, [
            partner.country_id.name,
            partner.city,
            partner.street,
        ]))
        return {
            "type": "ir.actions.act_window",
            "name": "Checkout",
            "res_model": "bakery.order",
            "res_id": self.id,
            "view_mode": "form",
            "view_id": self.env.ref('my_bakery.bakery_checkout_form_view').id,
            "target": "current",
        }

    def action_confirm_order(self):
        self.ensure_one()
        self.status = "confirmed"
        return{
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "name": "Order confirmed!",
                "message": "Your order has been placed successfully!",
                "type": "success",
                "sticky": False,
            }
        }