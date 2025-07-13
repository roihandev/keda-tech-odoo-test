from odoo import http
import json
from odoo.http import request, Response

class MaterialAPI(http.Controller):
    
    @http.route('/api/materials', auth='public', methods=['GET'], csrf=False)
    def get_materials(self, **kwargs):
        domain = []
        if kwargs.get('material_type'):
            domain.append(('material_type', '=', kwargs.get('material_type')))
        
        materials = request.env['material.registration'].search(domain)
        result = []
        for material in materials:
            result.append({
                'id': material.id,
                'material_code': material.material_code,
                'material_name': material.material_name,
                'material_type': material.material_type,
                'material_buy_price': material.material_buy_price,
                'supplier': material.supplier_id.name
            })
        return Response(json.dumps(result), content_type='application/json')
    
    @http.route('/api/materials', auth='public', methods=['POST'], csrf=False)
    def create_material(self, **kwargs):
        data = json.loads(request.httprequest.data)
        try:
            new_material = request.env['material.registration'].create({
                'material_code': data.get('material_code'),
                'material_name': data.get('material_name'),
                'material_type': data.get('material_type'),
                'material_buy_price': float(data.get('material_buy_price')),
                'supplier_id': int(data.get('supplier_id'))
            })
            return Response(json.dumps({'id': new_material.id}), status=201)
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), status=400)
    
    @http.route('/api/materials/<int:material_id>', auth='public', methods=['PUT'], csrf=False)
    def update_material(self, material_id, **kwargs):
        data = json.loads(request.httprequest.data)
        material = request.env['material.registration'].browse(material_id)
        if not material.exists():
            return Response(json.dumps({'error': 'Material not found'}), status=404)
        try:
            material.write(data)
            return Response(json.dumps({'success': True}), status=200)
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), status=400)
    
    @http.route('/api/materials/<int:material_id>', auth='public', methods=['DELETE'], csrf=False)
    def delete_material(self, material_id, **kwargs):
        material = request.env['material.registration'].browse(material_id)
        if not material.exists():
            return Response(json.dumps({'error': 'Material not found'}), status=404)
        try:
            material.unlink()
            return Response(json.dumps({'success': True}), status=200)
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), status=400)
