from odoo.tests.common import TransactionCase

class TestMaterial(TransactionCase):
    
    def setUp(self):
        super(TestMaterial, self).setUp()
        self.Supplier = self.env['material.supplier']
        self.Material = self.env['material.registration']
        
        self.supplier = self.Supplier.create({
            'name': 'Test Supplier'
        })
    
    def test_create_material(self):
        material = self.Material.create({
            'material_code': 'MAT001',
            'material_name': 'Test Fabric',
            'material_type': 'fabric',
            'material_buy_price': 150,
            'supplier_id': self.supplier.id
        })
        self.assertEqual(material.material_code, 'MAT001')
        self.assertEqual(material.material_buy_price, 150)
    
    def test_price_validation(self):
        with self.assertRaises(ValidationError):
            self.Material.create({
                'material_code': 'MAT002',
                'material_name': 'Invalid Price',
                'material_type': 'jeans',
                'material_buy_price': 50,
                'supplier_id': self.supplier.id
            })
    
    def test_filter_by_type(self):
        self.Material.create({
            'material_code': 'MAT003',
            'material_name': 'Test Jeans',
            'material_type': 'jeans',
            'material_buy_price': 120,
            'supplier_id': self.supplier.id
        })
        jeans_materials = self.Material.search([('material_type', '=', 'jeans')])
        self.assertTrue(len(jeans_materials) > 0)
