from flask import Blueprint, request, jsonify
from utils.permissions import require_auth, get_current_user
from database import get_supabase
from datetime import datetime

salas_bp = Blueprint('salas', __name__)

@salas_bp.route('/', methods=['GET'])
@require_auth
def get_salas():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    supabase = get_supabase()
    
    if user.role == 'admin':
        # Admin vê todas as salas
        result = supabase.table('salas').select('*').execute()
    else:
        # Recepção vê apenas suas salas
        result = supabase.table('salas').select('*').eq('recepcao_id', user.recepcao_id).execute()
    
    return jsonify({'salas': result.data}), 200

@salas_bp.route('/', methods=['POST'])
@require_auth
def create_sala():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    
    required_fields = ['nome', 'capacidade']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} é obrigatório'}), 400
    
    supabase = get_supabase()
    
    sala_data = {
        'nome': data['nome'],
        'capacidade': data['capacidade'],
        'recepcao_id': user.recepcao_id,
        'recepcao_nome': user.recepcao_nome,
        'status': 'disponivel',
        'created_at': datetime.now().isoformat(),
        'created_by': user.username
    }
    
    result = supabase.table('salas').insert(sala_data).execute()
    
    if result.data:
        return jsonify({'message': 'Sala criada com sucesso', 'sala': result.data[0]}), 201
    
    return jsonify({'error': 'Erro ao criar sala'}), 500

@salas_bp.route('/<int:sala_id>', methods=['PUT'])
@require_auth
def update_sala(sala_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    supabase = get_supabase()
    
    # Verificar se a sala pertence à recepção do usuário (exceto admin)
    if user.role != 'admin':
        sala_result = supabase.table('salas').select('*').eq('id', sala_id).eq('recepcao_id', user.recepcao_id).execute()
        if not sala_result.data:
            return jsonify({'error': 'Sala não encontrada ou sem permissão'}), 404
    
    update_data = {}
    allowed_fields = ['nome', 'capacidade', 'status', 'ocupado_por', 'ocupado_ate']
    
    for field in allowed_fields:
        if field in data:
            update_data[field] = data[field]
    
    if update_data:
        update_data['updated_at'] = datetime.now().isoformat()
        update_data['updated_by'] = user.username
        
        result = supabase.table('salas').update(update_data).eq('id', sala_id).execute()
        
        if result.data:
            return jsonify({'message': 'Sala atualizada com sucesso', 'sala': result.data[0]}), 200
    
    return jsonify({'error': 'Erro ao atualizar sala'}), 500

@salas_bp.route('/<int:sala_id>', methods=['DELETE'])
@require_auth
def delete_sala(sala_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    supabase = get_supabase()
    
    # Verificar se a sala pertence à recepção do usuário (exceto admin)
    if user.role != 'admin':
        sala_result = supabase.table('salas').select('*').eq('id', sala_id).eq('recepcao_id', user.recepcao_id).execute()
        if not sala_result.data:
            return jsonify({'error': 'Sala não encontrada ou sem permissão'}), 404
    
    result = supabase.table('salas').delete().eq('id', sala_id).execute()
    
    if result.data:
        return jsonify({'message': 'Sala excluída com sucesso'}), 200
    
    return jsonify({'error': 'Erro ao excluir sala'}), 500

@salas_bp.route('/<int:sala_id>/reservar', methods=['POST'])
@require_auth
def reservar_sala(sala_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    supabase = get_supabase()
    
    # Verificar se a sala existe e está disponível
    sala_result = supabase.table('salas').select('*').eq('id', sala_id).execute()
    if not sala_result.data:
        return jsonify({'error': 'Sala não encontrada'}), 404
    
    sala = sala_result.data[0]
    if sala['status'] != 'disponivel':
        return jsonify({'error': 'Sala não está disponível'}), 400
    
    # Criar reserva
    reserva_data = {
        'sala_id': sala_id,
        'usuario_id': user.id,
        'usuario_nome': user.username,
        'recepcao_id': sala['recepcao_id'],
        'data_inicio': data.get('data_inicio'),
        'data_fim': data.get('data_fim'),
        'observacoes': data.get('observacoes', ''),
        'status': 'ativa',
        'created_at': datetime.now().isoformat()
    }
    
    # Atualizar status da sala
    supabase.table('salas').update({
        'status': 'reservada',
        'ocupado_por': user.username,
        'ocupado_ate': data.get('data_fim')
    }).eq('id', sala_id).execute()
    
    # Inserir reserva
    result = supabase.table('reservas').insert(reserva_data).execute()
    
    if result.data:
        return jsonify({'message': 'Sala reservada com sucesso', 'reserva': result.data[0]}), 201
    
    return jsonify({'error': 'Erro ao reservar sala'}), 500