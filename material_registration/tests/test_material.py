from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestMaterial(TransactionCase):
    def setUp(self):
        super(TestMaterial, self).setUp()
        self.Supplier = self.env['material.supplier']
        self.Material = self.env['material.registration']
        
        # Create test supplier
        self.supplier = self.Supplier.create({'name': 'Test Supplier'})
        
        # Create valid test material
        self.valid_material = self.Material.create({
            'material_code': 'MAT001',
            'material_name': 'Test Fabric',
            'material_type': 'fabric',
            'material_buy_price': 150,
            'supplier_id': self.supplier.id
        })

    def test_01_material_creation(self):
        """Test valid material creation"""
        self.assertEqual(self.valid_material.material_code, 'MAT001')
        self.assertEqual(self.valid_material.supplier_id.name, 'Test Supplier')

    def test_02_price_validation(self):
        """Test price validation (<100 should fail)"""
        with self.assertRaises(ValidationError):
            self.Material.create({
                'material_code': 'MAT002',
                'material_name': 'Invalid Material',
                'material_type': 'cotton',
                'material_buy_price': 50,  # Invalid price
                'supplier_id': self.supplier.id
            })

    def test_03_required_fields(self):
        """Test all required fields"""
        with self.assertRaises(ValidationError):
            self.Material.create({})  # Empty dict should fail

    def test_04_api_operations(self):
        """Test API endpoints through controller"""
        # Test search
        materials = self.Material.search([('material_type', '=', 'fabric')])
        self.assertIn(self.valid_material, materials)
        
        # Test unlink
        material_id = self.valid_material.id
        self.valid_material.unlink()
        self.assertFalse(self.Material.browse(material_id).exists())
