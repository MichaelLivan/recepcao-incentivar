from flask import Blueprint, request, jsonify
from utils.permissions import require_recepcao, get_current_user
from database import get_supabase
from datetime import datetime

visitas_bp = Blueprint('visitas', __name__)

@visitas_bp.route('/', methods=['GET'])
@require_recepcao(['108'])
def get_visitas():
    user = get_current_user()
    supabase = get_supabase()
    
    result = supabase.table('visitas_externas').select('*').eq('recepcao_id', user.recepcao_id).order('created_at', desc=True).execute()
    return jsonify({'visitas': result.data}), 200

@visitas_bp.route('/', methods=['POST'])
@require_recepcao(['108'])
def registrar_visita():
    user = get_current_user()
    data = request.get_json()
    
    required_fields = ['visitante_nome', 'data_visita', 'tipo_visita']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} é obrigatório'}), 400
    
    supabase = get_supabase()
    
    visita_data = {
        'visitante_nome': data['visitante_nome'],
        'empresa': data.get('empresa', ''),
        'data_visita': data['data_visita'],
        'hora_entrada': data.get('hora_entrada'),
        'hora_saida': data.get('hora_saida'),
        'tipo_visita': data['tipo_visita'],
        'agendamento': data.get('agendamento', False),
        'observacoes': data.get('observacoes', ''),
        'recepcao_id': user.recepcao_id,
        'created_at': datetime.now().isoformat(),
        'created_by': user.username
    }
    
    result = supabase.table('visitas_externas').insert(visita_data).execute()
    
    if result.data:
        return jsonify({'message': 'Visita registrada com sucesso', 'visita': result.data[0]}), 201
    
    return jsonify({'error': 'Erro ao registrar visita'}), 500

@visitas_bp.route('/pacientes', methods=['GET'])
@require_recepcao(['108'])
def get_pacientes():
    user = get_current_user()
    supabase = get_supabase()
    
    result = supabase.table('entrada_saida_pacientes').select('*').eq('recepcao_id', user.recepcao_id).order('created_at', desc=True).execute()
    return jsonify({'pacientes': result.data}), 200

@visitas_bp.route('/pacientes/entrada', methods=['POST'])
@require_recepcao(['108'])
def registrar_entrada_paciente():
    user = get_current_user()
    data = request.get_json()
    
    required_fields = ['paciente_nome', 'hora_entrada']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} é obrigatório'}), 400
    
    supabase = get_supabase()
    
    entrada_data = {
        'paciente_nome': data['paciente_nome'],
        'responsavel': data.get('responsavel', ''),
        'hora_entrada': data['hora_entrada'],
        'tipo_atendimento': data.get('tipo_atendimento', ''),
        'profissional': data.get('profissional', ''),
        'observacoes': data.get('observacoes', ''),
        'status': 'presente',
        'recepcao_id': user.recepcao_id,
        'data_registro': datetime.now().date().isoformat(),
        'created_at': datetime.now().isoformat(),
        'created_by': user.username
    }
    
    result = supabase.table('entrada_saida_pacientes').insert(entrada_data).execute()
    
    if result.data:
        return jsonify({'message': 'Entrada registrada com sucesso', 'entrada': result.data[0]}), 201
    
    return jsonify({'error': 'Erro ao registrar entrada'}), 500

@visitas_bp.route('/pacientes/<int:paciente_id>/saida', methods=['PUT'])
@require_recepcao(['108'])
def registrar_saida_paciente(paciente_id):
    user = get_current_user()
    data = request.get_json()
    
    if not data.get('hora_saida'):
        return jsonify({'error': 'Hora de saída é obrigatória'}), 400
    
    supabase = get_supabase()
    
    update_data = {
        'hora_saida': data['hora_saida'],
        'status': 'finalizado',
        'observacoes_saida': data.get('observacoes_saida', ''),
        'updated_at': datetime.now().isoformat(),
        'updated_by': user.username
    }
    
    result = supabase.table('entrada_saida_pacientes').update(update_data).eq('id', paciente_id).eq('recepcao_id', user.recepcao_id).execute()
    
    if result.data:
        return jsonify({'message': 'Saída registrada com sucesso', 'paciente': result.data[0]}), 200
    
    return jsonify({'error': 'Erro ao registrar saída'}), 500