from odoo import models, fields


class BakeryInfo(models.Model):
    _name = 'bakery.info'
    _description = 'Bakery information'

    def _compute_display_name(self):
        for record in self:
            record.display_name = 'Information'