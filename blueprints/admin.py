from flask import Blueprint, request, jsonify
from utils.permissions import require_role, get_current_user
from models.user import User
from database import get_supabase

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@require_role(['admin'])
def get_all_users():
    supabase = get_supabase()
    result = supabase.table('usuarios').select('*').execute()
    
    users = []
    for user_data in result.data:
        users.append({
            'id': user_data['id'],
            'username': user_data['username'],
            'email': user_data['email'],
            'role': user_data['role'],
            'recepcao_id': user_data['recepcao_id'],
            'recepcao_nome': user_data['recepcao_nome'],
            'ativo': user_data['ativo']
        })
    
    return jsonify({'users': users}), 200

@admin_bp.route('/users', methods=['POST'])
@require_role(['admin'])
def create_user():
    data = request.get_json()
    
    required_fields = ['username', 'email', 'password', 'role']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} é obrigatório'}), 400
    
    # Verificar se usuário já existe
    existing_user = User.find_by_username(data['username'])
    if existing_user:
        return jsonify({'error': 'Username já existe'}), 400
    
    user = User.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data['role'],
        recepcao_id=data.get('recepcao_id'),
        recepcao_nome=data.get('recepcao_nome')
    )
    
    if user:
        return jsonify({'message': 'Usuário criado com sucesso', 'user': user}), 201
    
    return jsonify({'error': 'Erro ao criar usuário'}), 500

@admin_bp.route('/dashboard/overview', methods=['GET'])
@require_role(['admin'])
def dashboard_overview():
    supabase = get_supabase()
    
    # Buscar estatísticas gerais
    stats = {}
    
    # Total de usuários
    users_result = supabase.table('usuarios').select('id').execute()
    stats['total_usuarios'] = len(users_result.data)
    
    # Total de salas
    salas_result = supabase.table('salas').select('id').execute()
    stats['total_salas'] = len(salas_result.data)
    
    # Total de orçamentos
    orcamentos_result = supabase.table('orcamentos').select('id').execute()
    stats['total_orcamentos'] = len(orcamentos_result.data)
    
    # Salas por recepção
    salas_por_recepcao = {}
    for sala in salas_result.data:
        recepcao = sala.get('recepcao_id', 'Não definida')
        salas_por_recepcao[recepcao] = salas_por_recepcao.get(recepcao, 0) + 1
    
    stats['salas_por_recepcao'] = salas_por_recepcao
    
    return jsonify({'stats': stats}), 200