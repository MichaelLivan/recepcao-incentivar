from flask import Blueprint, request, jsonify
from utils.permissions import require_recepcao, get_current_user
from database import get_supabase
from datetime import datetime, timedelta

orcamentos_bp = Blueprint('orcamentos', __name__)

@orcamentos_bp.route('/', methods=['GET'])
@require_recepcao(['103', '808', '108', '203', '1009', '1108'])
def get_orcamentos():
    user = get_current_user()
    supabase = get_supabase()
    
    if user.role == 'admin':
        result = supabase.table('orcamentos').select('*').order('created_at', desc=True).execute()
    else:
        result = supabase.table('orcamentos').select('*').eq('recepcao_id', user.recepcao_id).order('created_at', desc=True).execute()
    
    return jsonify({'orcamentos': result.data}), 200

@orcamentos_bp.route('/', methods=['POST'])
@require_recepcao(['103', '808', '108', '203', '1009', '1108'])
def create_orcamento():
    user = get_current_user()
    data = request.get_json()
    
    required_fields = ['nome_pais', 'nome_paciente', 'terapias_solicitadas']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} é obrigatório'}), 400
    
    supabase = get_supabase()
    
    # Calcular data de alerta (24 horas após criação)
    data_alerta = datetime.now() + timedelta(hours=24)
    
    orcamento_data = {
        'nome_pais': data['nome_pais'],
        'nome_paciente': data['nome_paciente'],
        'terapias_solicitadas': data['terapias_solicitadas'],
        'valor': data.get('valor'),
        'observacoes': data.get('observacoes', ''),
        'status': 'pendente',
        'recepcao_id': user.recepcao_id,
        'recepcao_nome': user.recepcao_nome,
        'data_alerta': data_alerta.isoformat(),
        'alerta_enviado': False,
        'created_at': datetime.now().isoformat(),
        'created_by': user.username
    }
    
    result = supabase.table('orcamentos').insert(orcamento_data).execute()
    
    if result.data:
        return jsonify({'message': 'Orçamento criado com sucesso', 'orcamento': result.data[0]}), 201
    
    return jsonify({'error': 'Erro ao criar orçamento'}), 500

@orcamentos_bp.route('/<int:orcamento_id>/feedback', methods=['POST'])
@require_recepcao(['103', '808', '108', '203', '1009', '1108'])
def add_feedback_orcamento(orcamento_id):
    user = get_current_user()
    data = request.get_json()
    
    if not data.get('feedback'):
        return jsonify({'error': 'Feedback é obrigatório'}), 400
    
    supabase = get_supabase()
    
    # Verificar se o orçamento pertence à recepção do usuário (exceto admin)
    if user.role != 'admin':
        orcamento_result = supabase.table('orcamentos').select('*').eq('id', orcamento_id).eq('recepcao_id', user.recepcao_id).execute()
        if not orcamento_result.data:
            return jsonify({'error': 'Orçamento não encontrado ou sem permissão'}), 404
    
    update_data = {
        'feedback': data['feedback'],
        'status': data.get('status', 'respondido'),
        'data_feedback': datetime.now().isoformat(),
        'feedback_by': user.username
    }
    
    result = supabase.table('orcamentos').update(update_data).eq('id', orcamento_id).execute()
    
    if result.data:
        return jsonify({'message': 'Feedback adicionado com sucesso', 'orcamento': result.data[0]}), 200
    
    return jsonify({'error': 'Erro ao adicionar feedback'}), 500

@orcamentos_bp.route('/alertas', methods=['GET'])
@require_recepcao(['103', '808', '108', '203', '1009', '1108'])
def get_alertas_orcamentos():
    user = get_current_user()
    supabase = get_supabase()
    
    # Buscar orçamentos que precisam de alerta (24h após criação)
    agora = datetime.now().isoformat()
    
    if user.role == 'admin':
        result = supabase.table('orcamentos').select('*').lt('data_alerta', agora).eq('alerta_enviado', False).execute()
    else:
        result = supabase.table('orcamentos').select('*').eq('recepcao_id', user.recepcao_id).lt('data_alerta', agora).eq('alerta_enviado', False).execute()
    
    # Marcar alertas como enviados
    if result.data:
        ids_para_atualizar = [item['id'] for item in result.data]
        supabase.table('orcamentos').update({'alerta_enviado': True}).in_('id', ids_para_atualizar).execute()
    
    return jsonify({'alertas': result.data}), 200