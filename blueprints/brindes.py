from flask import Blueprint, request, jsonify
from utils.permissions import require_recepcao, get_current_user
from database import get_supabase
from datetime import datetime

brindes_bp = Blueprint('brindes', __name__)

@brindes_bp.route('/', methods=['GET'])
@require_recepcao(['103', '808', '108', '203', '1009', '1108', '1002'])
def get_brindes():
    user = get_current_user()
    supabase = get_supabase()
    
    if user.recepcao_id == '1002' or user.role == 'admin':
        # 1002 e admin veem tudo
        result = supabase.table('brindes').select('*').order('created_at', desc=True).execute()
    else:
        # Outras recepções veem apenas seus registros
        result = supabase.table('brindes').select('*').eq('recepcao_id', user.recepcao_id).order('created_at', desc=True).execute()
    
    return jsonify({'brindes': result.data}), 200

@brindes_bp.route('/estoque', methods=['GET'])
@require_recepcao(['1002'])
def get_estoque_brindes():
    supabase = get_supabase()
    result = supabase.table('estoque_brindes').select('*').execute()
    return jsonify({'estoque': result.data}), 200

@brindes_bp.route('/distribuir', methods=['POST'])
@require_recepcao(['1002'])
def distribuir_brindes():
    user = get_current_user()
    data = request.get_json()
    
    required_fields = ['item_id', 'recepcao_destino', 'quantidade']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} é obrigatório'}), 400
    
    supabase = get_supabase()
    
    # Verificar estoque disponível
    item_result = supabase.table('estoque_brindes').select('*').eq('id', data['item_id']).execute()
    if not item_result.data:
        return jsonify({'error': 'Item não encontrado'}), 404
    
    item = item_result.data[0]
    if item['quantidade'] < data['quantidade']:
        return jsonify({'error': 'Quantidade insuficiente em estoque'}), 400
    
    # Registrar distribuição
    distribuicao_data = {
        'item_id': data['item_id'],
        'item_nome': item['nome'],
        'quantidade': data['quantidade'],
        'recepcao_origem': '1002',
        'recepcao_destino': data['recepcao_destino'],
        'observacoes': data.get('observacoes', ''),
        'created_at': datetime.now().isoformat(),
        'created_by': user.username
    }
    
    # Atualizar estoque
    nova_quantidade = item['quantidade'] - data['quantidade']
    supabase.table('estoque_brindes').update({'quantidade': nova_quantidade}).eq('id', data['item_id']).execute()
    
    # Inserir registro de distribuição
    result = supabase.table('distribuicao_brindes').insert(distribuicao_data).execute()
    
    if result.data:
        return jsonify({'message': 'Distribuição registrada com sucesso', 'distribuicao': result.data[0]}), 201
    
    return jsonify({'error': 'Erro ao registrar distribuição'}), 500

@brindes_bp.route('/solicitar', methods=['POST'])
@require_recepcao(['103', '808', '108', '203', '1009', '1108'])
def solicitar_brindes():
    user = get_current_user()
    data = request.get_json()
    
    required_fields = ['item_nome', 'quantidade', 'data_evento']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} é obrigatório'}), 400
    
    supabase = get_supabase()
    
    solicitacao_data = {
        'item_nome': data['item_nome'],
        'quantidade': data['quantidade'],
        'data_evento': data['data_evento'],
        'observacoes': data.get('observacoes', ''),
        'recepcao_id': user.recepcao_id,
        'recepcao_nome': user.recepcao_nome,
        'status': 'pendente',
        'created_at': datetime.now().isoformat(),
        'created_by': user.username
    }
    
    result = supabase.table('brindes').insert(solicitacao_data).execute()
    
    if result.data:
        return jsonify({'message': 'Solicitação de brindes criada com sucesso', 'brinde': result.data[0]}), 201
    
    return jsonify({'error': 'Erro ao criar solicitação'}), 500

@brindes_bp.route('/visitantes', methods=['GET'])
@require_recepcao(['108'])
def get_brindes_visitantes():
    user = get_current_user()
    supabase = get_supabase()
    
    result = supabase.table('brindes_visitantes').select('*').eq('recepcao_id', user.recepcao_id).order('created_at', desc=True).execute()
    return jsonify({'brindes_visitantes': result.data}), 200

@brindes_bp.route('/visitantes', methods=['POST'])
@require_recepcao(['108'])
def registrar_brinde_visitante():
    user = get_current_user()
    data = request.get_json()
    
    required_fields = ['visitante_nome', 'item_nome', 'quantidade']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} é obrigatório'}), 400
    
    supabase = get_supabase()
    
    brinde_data = {
        'visitante_nome': data['visitante_nome'],
        'item_nome': data['item_nome'],
        'quantidade': data['quantidade'],
        'observacoes': data.get('observacoes', ''),
        'recepcao_id': user.recepcao_id,
        'created_at': datetime.now().isoformat(),
        'created_by': user.username
    }
    
    result = supabase.table('brindes_visitantes').insert(brinde_data).execute()
    
    if result.data:
        return jsonify({'message': 'Brinde de visitante registrado com sucesso', 'brinde': result.data[0]}), 201
    
    return jsonify({'error': 'Erro ao registrar brinde'}), 500