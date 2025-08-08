from flask import Blueprint, request, jsonify
from utils.permissions import require_recepcao, get_current_user
from database import get_supabase
from datetime import datetime

lista_espera_bp = Blueprint('lista_espera', __name__)

@lista_espera_bp.route('/', methods=['GET'])
@require_recepcao(['1002'])
def get_lista_espera():
    supabase = get_supabase()
    result = supabase.table('lista_espera').select('*').order('data_solicitacao', desc=False).execute()
    
    # Calcular tempo de espera
    for item in result.data:
        data_solicitacao = datetime.fromisoformat(item['data_solicitacao'])
        tempo_espera = datetime.now() - data_solicitacao
        item['tempo_espera_dias'] = tempo_espera.days
    
    return jsonify({'lista_espera': result.data}), 200

@lista_espera_bp.route('/', methods=['POST'])
@require_recepcao(['1002'])
def add_lista_espera():
    user = get_current_user()
    data = request.get_json()
    
    required_fields = ['especialidade', 'solicitante', 'data_solicitacao']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} é obrigatório'}), 400
    
    supabase = get_supabase()
    
    espera_data = {
        'especialidade': data['especialidade'],
        'solicitante': data['solicitante'],
        'terapeuta_preferencia': data.get('terapeuta_preferencia', ''),
        'data_solicitacao': data['data_solicitacao'],
        'observacoes': data.get('observacoes', ''),
        'status': 'aguardando',
        'created_at': datetime.now().isoformat(),
        'created_by': user.username
    }
    
    result = supabase.table('lista_espera').insert(espera_data).execute()
    
    if result.data:
        return jsonify({'message': 'Adicionado à lista de espera', 'item': result.data[0]}), 201
    
    return jsonify({'error': 'Erro ao adicionar à lista de espera'}), 500

@lista_espera_bp.route('/<int:item_id>', methods=['PUT'])
@require_recepcao(['1002'])
def update_lista_espera(item_id):
    user = get_current_user()
    data = request.get_json()
    
    supabase = get_supabase()
    
    update_data = {}
    allowed_fields = ['especialidade', 'solicitante', 'terapeuta_preferencia', 'status', 'observacoes']
    
    for field in allowed_fields:
        if field in data:
            update_data[field] = data[field]
    
    if update_data:
        update_data['updated_at'] = datetime.now().isoformat()
        update_data['updated_by'] = user.username
        
        result = supabase.table('lista_espera').update(update_data).eq('id', item_id).execute()
        
        if result.data:
            return jsonify({'message': 'Item atualizado com sucesso', 'item': result.data[0]}), 200
    
    return jsonify({'error': 'Erro ao atualizar item'}), 500

@lista_espera_bp.route('/<int:item_id>', methods=['DELETE'])
@require_recepcao(['1002'])
def delete_lista_espera(item_id):
    supabase = get_supabase()
    
    result = supabase.table('lista_espera').delete().eq('id', item_id).execute()
    
    if result.data:
        return jsonify({'message': 'Item removido da lista de espera'}), 200
    
    return jsonify({'error': 'Erro ao remover item'}), 500

@lista_espera_bp.route('/especialidades', methods=['GET'])
@require_recepcao(['1002'])
def get_especialidades():
    supabase = get_supabase()
    result = supabase.table('lista_espera').select('especialidade').execute()
    
    especialidades = list(set([item['especialidade'] for item in result.data]))
    return jsonify({'especialidades': especialidades}), 200