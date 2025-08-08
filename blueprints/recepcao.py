from flask import Blueprint, request, jsonify
from utils.permissions import require_auth, get_current_user
from database import get_supabase

recepcao_bp = Blueprint('recepcao', __name__)

@recepcao_bp.route('/dashboard', methods=['GET'])
@require_auth
def dashboard_recepcao():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    supabase = get_supabase()
    stats = {}
    
    if user.role == 'admin':
        # Admin vê tudo
        salas_result = supabase.table('salas').select('*').execute()
        orcamentos_result = supabase.table('orcamentos').select('*').execute()
    else:
        # Recepção vê apenas seus dados
        salas_result = supabase.table('salas').select('*').eq('recepcao_id', user.recepcao_id).execute()
        orcamentos_result = supabase.table('orcamentos').select('*').eq('recepcao_id', user.recepcao_id).execute()
    
    stats['total_salas'] = len(salas_result.data)
    stats['total_orcamentos'] = len(orcamentos_result.data)
    stats['recepcao_nome'] = user.recepcao_nome
    stats['recepcao_id'] = user.recepcao_id
    
    # Salas disponíveis/ocupadas
    salas_disponiveis = len([s for s in salas_result.data if s.get('status') == 'disponivel'])
    salas_ocupadas = len([s for s in salas_result.data if s.get('status') == 'ocupada'])
    
    stats['salas_disponiveis'] = salas_disponiveis
    stats['salas_ocupadas'] = salas_ocupadas
    
    return jsonify({'stats': stats, 'user': user.to_dict()}), 200

@recepcao_bp.route('/permissions', methods=['GET'])
@require_auth
def get_user_permissions():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    permissions = {
        'can_manage_users': user.role == 'admin',
        'can_view_all_data': user.role == 'admin',
        'can_manage_salas': True,
        'can_manage_estoque': user.recepcao_id in ['103'],
        'can_manage_orcamentos': user.recepcao_id in ['103', '808', '108', '203', '1009', '1108'],
        'can_manage_brindes': user.recepcao_id in ['103', '808', '108', '203', '1009', '1108'],
        'can_control_brindes': user.recepcao_id == '1002',
        'can_manage_lista_espera': user.recepcao_id == '1002',
        'can_manage_anamnese': user.recepcao_id == '808',
        'can_manage_visitas': user.recepcao_id == '108',
        'can_manage_pacientes': user.recepcao_id == '108'
    }
    
    return jsonify({'permissions': permissions}), 200