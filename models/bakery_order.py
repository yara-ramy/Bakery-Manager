from odoo import models, fields, api


class BakeryOrder(models.Model):
    _name = 'bakery.order'
    _description = 'Bakery Order'

    name = fields.Char(string='Order Number', readonly=True, copy=False)
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
    ], required=True, default='cart', string='Status')
    currency_id = fields.Many2one('res.currency',string='Currency',
                                  default=lambda self: self.env.ref("base.EGP"))
    order_date = fields.Datetime(string='Order Date', required=True, default=fields.Datetime.now)
    status_changed_at = fields.Datetime(string='Status Changed At')

    phone = fields.Char(string='Phone Number')
    shipping_address = fields.Text(string='Shipping Address')
    payment_method = fields.Selection([
        ('cash','Cash on delivery'),
        ('credit','Credit card')
    ], string='Payment Method')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('status_changed_at'):
                vals['status_changed_at'] = fields.Datetime.now()
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('bakery.order')
        return super().create(vals_list)

    @api.depends('order_line_ids.subtotal')
    def _compute_total_price(self):
        for order_line in self:
            order_line.total_price = sum(order_line.order_line_ids.mapped('subtotal'))

    @staticmethod
    def _get_cron_interval_seconds(cron):
        interval = cron.interval_number
        if cron.interval_type == 'minutes':
            return interval * 60
        elif cron.interval_type == 'hours':
            return interval * 60 * 60
        elif cron.interval_type == 'days':
            return interval * 24 * 60 * 60
        elif cron.interval_type == 'weeks':
            return interval * 7 * 24 * 60 * 60
        elif cron.interval_type == 'months':
            return interval * 30 * 24 * 60 * 60
        else:
            return 0



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
        self.status_changed_at = fields.Datetime.now()
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

    def action_cancel(self):
        self.ensure_one()
        if self.status == "confirmed":
            self.status = "cart"
            self.status_changed_at = fields.Datetime.now()
            return{
                "type": "ir.actions.client",
                "tag": "reload",
            }
        elif self.status == "cart":
            self.unlink()
            return{
                "type": "ir.actions.act_window",
                "name": "Cart",
                "res_model": "bakery.order",
                "view_mode": "list,form",
                "target": "current",
            }

    def action_track(self):
        self.ensure_one()
        return{
            "type": "ir.actions.act_window",
            "name": "Track your order",
            "res_model": "bakery.order",
            "res_id": self.id,
            "view_mode": "form",
            "view_id": self.env.ref('my_bakery.track_order_form').id,
            "target": "current",
        }

    def cron_change_status(self):
        cron = self.env.ref('my_bakery.cron_change_status')
        interval_seconds = self._get_cron_interval_seconds(cron)
        orders = self.search([
            ("status", "in", ["confirmed", "shipped", "in_transit"])
        ])
        for order in orders:
            if not order.status_changed_at:
                continue
            elapsed_seconds = (
                    fields.Datetime.now() - order.status_changed_at
            ).total_seconds()
            if elapsed_seconds < interval_seconds:
                continue
            if order.status == "confirmed":
                order.status = "shipped"
            elif order.status == "shipped":
                order.status = "in_transit"
            elif order.status == "in_transit":
                order.status = "delivered"
            order.status_changed_at = fields.Datetime.now()