from odoo import models, fields, api


class BakeryItem(models.Model):
    _name = 'bakery.item'
    _description = 'Bakery Items'

    name = fields.Char(string='Name', required=True)
    item_type = fields.Selection([
        ('all','All'),
        ('cakes','Cakes'),
        ('cookies','Cookies'),
        ('croissants','Croissants')
    ], string='Type', required=True)
    price = fields.Monetary(string='Price', currency_field="currency_id",required=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.ref("base.EGP"))
    description = fields.Text(string='Description')
    is_available = fields.Boolean(string='Is Available')
    image_1920 = fields.Image(
        string="Item Image",
        max_width=1920,
        max_height=1920
    )

    def action_add_to_cart(self):
        self.ensure_one()
        return{
            "type": "ir.actions.act_window",
            "name": "Add To Cart",
            "res_model": "bakery.cart.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_item_id": self.id,
            },
        }