from flask import Blueprint, request, jsonify
from utils.permissions import require_recepcao, get_current_user
from database import get_supabase
from datetime import datetime

estoque_bp = Blueprint('estoque', __name__)

@estoque_bp.route('/', methods=['GET'])
@require_recepcao(['103'])
def get_estoque():
    user = get_current_user()
    supabase = get_supabase()
    
    result = supabase.table('estoque').select('*').eq('recepcao_id', user.recepcao_id).execute()
    return jsonify({'estoque': result.data}), 200

@estoque_bp.route('/item', methods=['POST'])
@require_recepcao(['103'])
def add_item_estoque():
    user = get_current_user()
    data = request.get_json()
    
    required_fields = ['nome', 'quantidade', 'unidade']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} é obrigatório'}), 400
    
    supabase = get_supabase()
    
    item_data = {
        'nome': data['nome'],
        'quantidade': data['quantidade'],
        'unidade': data['unidade'],
        'descricao': data.get('descricao', ''),
        'recepcao_id': user.recepcao_id,
        'created_at': datetime.now().isoformat(),
        'created_by': user.username
    }
    
    result = supabase.table('estoque').insert(item_data).execute()
    
    if result.data:
        return jsonify({'message': 'Item adicionado ao estoque', 'item': result.data[0]}), 201
    
    return jsonify({'error': 'Erro ao adicionar item'}), 500

@estoque_bp.route('/retirada', methods=['POST'])
@require_recepcao(['103'])
def registrar_retirada():
    user = get_current_user()
    data = request.get_json()
    
    required_fields = ['item_id', 'quantidade', 'retirado_por']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} é obrigatório'}), 400
    
    supabase = get_supabase()
    
    # Verificar se o item existe e tem quantidade suficiente
    item_result = supabase.table('estoque').select('*').eq('id', data['item_id']).execute()
    if not item_result.data:
        return jsonify({'error': 'Item não encontrado'}), 404
    
    item = item_result.data[0]
    if item['quantidade'] < data['quantidade']:
        return jsonify({'error': 'Quantidade insuficiente em estoque'}), 400
    
    # Registrar retirada
    retirada_data = {
        'item_id': data['item_id'],
        'item_nome': item['nome'],
        'quantidade': data['quantidade'],
        'retirado_por': data['retirado_por'],
        'observacoes': data.get('observacoes', ''),
        'recepcao_id': user.recepcao_id,
        'created_at': datetime.now().isoformat(),
        'created_by': user.username
    }
    
    # Atualizar quantidade no estoque
    nova_quantidade = item['quantidade'] - data['quantidade']
    supabase.table('estoque').update({'quantidade': nova_quantidade}).eq('id', data['item_id']).execute()
    
    # Inserir registro de retirada
    result = supabase.table('retiradas_estoque').insert(retirada_data).execute()
    
    if result.data:
        return jsonify({'message': 'Retirada registrada com sucesso', 'retirada': result.data[0]}), 201
    
    return jsonify({'error': 'Erro ao registrar retirada'}), 500

@estoque_bp.route('/retiradas', methods=['GET'])
@require_recepcao(['103'])
def get_retiradas():
    user = get_current_user()
    supabase = get_supabase()
    
    result = supabase.table('retiradas_estoque').select('*').eq('recepcao_id', user.recepcao_id).order('created_at', desc=True).execute()
    return jsonify({'retiradas': result.data}), 200