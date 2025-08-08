from flask import Blueprint, request, jsonify
from utils.permissions import require_auth, get_current_user
from database import get_supabase
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
@require_auth
def get_dashboard_stats():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    supabase = get_supabase()
    stats = {}
    
    if user.role == 'admin':
        # Admin vê estatísticas gerais
        stats = get_admin_stats(supabase)
    else:
        # Recepção vê estatísticas específicas
        stats = get_recepcao_stats(supabase, user)
    
    return jsonify({'stats': stats}), 200

def get_admin_stats(supabase):
    stats = {}
    
    # Total de usuários
    users_result = supabase.table('usuarios').select('id').execute()
    stats['total_usuarios'] = len(users_result.data)
    
    # Total de salas
    salas_result = supabase.table('salas').select('*').execute()
    stats['total_salas'] = len(salas_result.data)
    stats['salas_disponiveis'] = len([s for s in salas_result.data if s.get('status') == 'disponivel'])
    stats['salas_ocupadas'] = len([s for s in salas_result.data if s.get('status') == 'ocupada'])
    
    # Total de orçamentos
    orcamentos_result = supabase.table('orcamentos').select('*').execute()
    stats['total_orcamentos'] = len(orcamentos_result.data)
    stats['orcamentos_pendentes'] = len([o for o in orcamentos_result.data if o.get('status') == 'pendente'])
    
    # Salas por recepção
    salas_por_recepcao = {}
    for sala in salas_result.data:
        recepcao = sala.get('recepcao_id', 'Não definida')
        salas_por_recepcao[recepcao] = salas_por_recepcao.get(recepcao, 0) + 1
    
    stats['salas_por_recepcao'] = salas_por_recepcao
    
    # Orçamentos por recepção
    orcamentos_por_recepcao = {}
    for orcamento in orcamentos_result.data:
        recepcao = orcamento.get('recepcao_id', 'Não definida')
        orcamentos_por_recepcao[recepcao] = orcamentos_por_recepcao.get(recepcao, 0) + 1
    
    stats['orcamentos_por_recepcao'] = orcamentos_por_recepcao
    
    return stats

def get_recepcao_stats(supabase, user):
    stats = {
        'recepcao_id': user.recepcao_id,
        'recepcao_nome': user.recepcao_nome
    }
    
    # Salas da recepção
    salas_result = supabase.table('salas').select('*').eq('recepcao_id', user.recepcao_id).execute()
    stats['total_salas'] = len(salas_result.data)
    stats['salas_disponiveis'] = len([s for s in salas_result.data if s.get('status') == 'disponivel'])
    stats['salas_ocupadas'] = len([s for s in salas_result.data if s.get('status') == 'ocupada'])
    
    # Orçamentos da recepção
    orcamentos_result = supabase.table('orcamentos').select('*').eq('recepcao_id', user.recepcao_id).execute()
    stats['total_orcamentos'] = len(orcamentos_result.data)
    stats['orcamentos_pendentes'] = len([o for o in orcamentos_result.data if o.get('status') == 'pendente'])
    
    # Estatísticas específicas por recepção
    if user.recepcao_id == '103':
        # Estoque
        estoque_result = supabase.table('estoque').select('*').eq('recepcao_id', user.recepcao_id).execute()
        stats['total_itens_estoque'] = len(estoque_result.data)
        
        # Retiradas do mês
        inicio_mes = datetime.now().replace(day=1).isoformat()
        retiradas_result = supabase.table('retiradas_estoque').select('*').eq('recepcao_id', user.recepcao_id).gte('created_at', inicio_mes).execute()
        stats['retiradas_mes'] = len(retiradas_result.data)
    
    elif user.recepcao_id == '1002':
        # Lista de espera
        espera_result = supabase.table('lista_espera').select('*').execute()
        stats['total_lista_espera'] = len(espera_result.data)
        stats['aguardando'] = len([e for e in espera_result.data if e.get('status') == 'aguardando'])
        
        # Distribuição de brindes
        distribuicao_result = supabase.table('distribuicao_brindes').select('*').execute()
        stats['total_distribuicoes'] = len(distribuicao_result.data)
    
    elif user.recepcao_id == '808':
        # Anamneses
        anamneses_result = supabase.table('anamneses').select('quantidade').eq('recepcao_id', user.recepcao_id).execute()
        stats['total_anamneses'] = sum([a['quantidade'] for a in anamneses_result.data])
    
    elif user.recepcao_id == '108':
        # Visitas e pacientes
        visitas_result = supabase.table('visitas_externas').select('*').eq('recepcao_id', user.recepcao_id).execute()
        stats['total_visitas'] = len(visitas_result.data)
        
        pacientes_result = supabase.table('entrada_saida_pacientes').select('*').eq('recepcao_id', user.recepcao_id).execute()
        stats['total_pacientes'] = len(pacientes_result.data)
        stats['pacientes_presentes'] = len([p for p in pacientes_result.data if p.get('status') == 'presente'])
    
    return stats

@dashboard_bp.route('/graficos/<string:tipo>', methods=['GET'])
@require_auth
def get_grafico_data(tipo):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404
    
    supabase = get_supabase()
    
    if tipo == 'orcamentos_mes':
        return get_orcamentos_por_mes(supabase, user)
    elif tipo == 'salas_status':
        return get_salas_por_status(supabase, user)
    elif tipo == 'anamneses_mes' and user.recepcao_id == '808':
        return get_anamneses_por_mes(supabase, user)
    elif tipo == 'estoque_baixo' and user.recepcao_id == '103':
        return get_estoque_baixo(supabase, user)
    
    return jsonify({'error': 'Tipo de gráfico não encontrado'}), 404

def get_orcamentos_por_mes(supabase, user):
    if user.role == 'admin':
        result = supabase.table('orcamentos').select('created_at').execute()
    else:
        result = supabase.table('orcamentos').select('created_at').eq('recepcao_id', user.recepcao_id).execute()
    
    orcamentos_por_mes = {}
    for orcamento in result.data:
        mes = orcamento['created_at'][:7]  # YYYY-MM
        orcamentos_por_mes[mes] = orcamentos_por_mes.get(mes, 0) + 1
    
    return jsonify({'data': orcamentos_por_mes}), 200

def get_salas_por_status(supabase, user):
    if user.role == 'admin':
        result = supabase.table('salas').select('status').execute()
    else:
        result = supabase.table('salas').select('status').eq('recepcao_id', user.recepcao_id).execute()
    
    status_count = {}
    for sala in result.data:
        status = sala.get('status', 'indefinido')
        status_count[status] = status_count.get(status, 0) + 1
    
    return jsonify({'data': status_count}), 200

def get_anamneses_por_mes(supabase, user):
    result = supabase.table('anamneses').select('data_registro', 'quantidade').eq('recepcao_id', user.recepcao_id).execute()
    
    anamneses_por_mes = {}
    for anamnese in result.data:
        mes = anamnese['data_registro'][:7]  # YYYY-MM
        anamneses_por_mes[mes] = anamneses_por_mes.get(mes, 0) + anamnese['quantidade']
    
    return jsonify({'data': anamneses_por_mes}), 200

def get_estoque_baixo(supabase, user):
    result = supabase.table('estoque').select('nome', 'quantidade').eq('recepcao_id', user.recepcao_id).lt('quantidade', 10).execute()
    
    estoque_baixo = {item['nome']: item['quantidade'] for item in result.data}
    
    return jsonify({'data': estoque_baixo}), 200