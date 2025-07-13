from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Supplier(models.Model):
    _name = 'material.supplier'
    _description = 'Supplier Information'

    name = fields.Char(string='Supplier Name', required=True)


class Material(models.Model):
    _name = 'material.registration'
    _description = 'Material Registration'

    material_code = fields.Char(string='Material Code', required=True)
    material_name = fields.Char(string='Material Name', required=True)
    material_type = fields.Selection(
        selection=[
            ('fabric', 'Fabric'),
            ('jeans', 'Jeans'),
            ('cotton', 'Cotton')
        ],
        string='Material Type',
        required=True
    )
    material_buy_price = fields.Float(string='Buy Price', required=True)
    supplier_id = fields.Many2one(
        'material.supplier',
        string='Supplier',
        required=True
    )

    @api.constrains('material_buy_price')
    def _check_buy_price(self):
        for record in self:
            if record.material_buy_price < 100:
                raise ValidationError("Material buy price must be at least 100.")
