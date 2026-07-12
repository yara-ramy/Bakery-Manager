# from odoo import models, fields, api


# class my_bakery(models.Model):
#     _name = 'my_bakery.my_bakery'
#     _description = 'my_bakery.my_bakery'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

