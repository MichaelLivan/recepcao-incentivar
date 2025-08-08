# blueprints/anamneses.py - Sistema completo de anamneses
from flask import Blueprint, request, jsonify
from utils.permissions import require_recepcao, require_auth, get_current_user
from database import get_supabase
from datetime import datetime, date
import traceback

anamneses_bp = Blueprint('anamneses', __name__)

def can_access_anamneses(user):
    """Verifica se o usuário pode acessar o módulo de anamneses"""
    if not user:
        return False
    
    # Admins têm acesso total
    if user.role in ['admin', 'admin_geral', 'admin_limitado']:
        return True
    
    # Apenas recepções 808 e 108 têm acesso
    return user.recepcao_id in ['808', '108']

@anamneses_bp.route('/', methods=['GET'])
@require_auth
def get_anamneses():
    try:
        user = get_current_user()
        
        # Verificar se o usuário pode acessar anamneses
        if not can_access_anamneses(user):
            return jsonify({
                'error': 'Acesso negado. Módulo disponível apenas para recepções 808 e 108.'
            }), 403
        
        supabase = get_supabase()
        
        # Se for admin, busca todas as anamneses
        if user.role in ['admin', 'admin_geral', 'admin_limitado']:
            query = supabase.table('anamneses').select('*')
        else:
            # Se for recepção, busca apenas suas anamneses
            query = supabase.table('anamneses').select('*').eq('recepcao_id', user.recepcao_id)
        
        result = query.order('created_at', desc=True).execute()
        
        # Processar dados para incluir informações calculadas
        anamneses_processadas = []
        for anamnese in result.data:
            anamnese_data = dict(anamnese)
            
            # Calcular dias desde a criação
            if anamnese_data.get('created_at'):
                created_date = datetime.fromisoformat(anamnese_data['created_at'].replace('Z', '+00:00'))
                dias_desde_criacao = (datetime.now() - created_date.replace(tzinfo=None)).days
                anamnese_data['dias_desde_criacao'] = dias_desde_criacao
            
            anamneses_processadas.append(anamnese_data)
        
        print(f"✅ Anamneses carregadas: {len(anamneses_processadas)} para usuário {user.username}")
        
        return jsonify({
            'anamneses': anamneses_processadas,
            'total': len(anamneses_processadas),
            'user_recepcao': user.recepcao_nome
        }), 200
        
    except Exception as e:
        print(f"💥 ERRO ao buscar anamneses: {str(e)}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@anamneses_bp.route('/', methods=['POST'])
@require_auth
def registrar_anamnese():
    try:
        user = get_current_user()
        
        # Verificar se o usuário pode acessar anamneses
        if not can_access_anamneses(user):
            return jsonify({
                'error': 'Acesso negado. Módulo disponível apenas para recepções 808 e 108.'
            }), 403
        
        data = request.get_json()
        print(f"📝 Registrando nova anamnese: {data}")
        
        # Campos obrigatórios
        required_fields = ['nome_pais', 'nome_paciente', 'data_anamnese', 'profissional', 'motivo_consulta']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo "{field}" é obrigatório'}), 400
        
        # Validar data da anamnese
        try:
            data_anamnese = datetime.strptime(data['data_anamnese'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Data da anamnese deve estar no formato YYYY-MM-DD'}), 400
        
        supabase = get_supabase()
        
        # Preparar dados para inserção
        anamnese_data = {
            'nome_pais': data['nome_pais'].strip(),
            'nome_paciente': data['nome_paciente'].strip(),
            'data_anamnese': data['data_anamnese'],
            'profissional': data['profissional'].strip(),
            'tipo_anamnese': data.get('tipo_anamnese', 'Inicial'),
            'idade_paciente': data.get('idade_paciente', '').strip(),
            'motivo_consulta': data['motivo_consulta'].strip(),
            'observacoes': data.get('observacoes', '').strip(),
            'contato_responsavel': data.get('contato_responsavel', '').strip(),
            'recepcao_id': user.recepcao_id,
            'recepcao_nome': user.recepcao_nome,
            'status': 'agendada',  # Status padrão
            'created_at': datetime.now().isoformat(),
            'created_by': user.username
        }
        
        # Inserir no banco
        result = supabase.table('anamneses').insert(anamnese_data).execute()
        
        if result.data:
            anamnese_criada = result.data[0]
            print(f"✅ Anamnese criada com sucesso: ID {anamnese_criada['id']}")
            
            return jsonify({
                'message': 'Anamnese registrada com sucesso',
                'anamnese': anamnese_criada
            }), 201
        
        return jsonify({'error': 'Erro ao inserir anamnese no banco de dados'}), 500
        
    except Exception as e:
        print(f"💥 ERRO ao registrar anamnese: {str(e)}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@anamneses_bp.route('/<int:anamnese_id>', methods=['PUT'])
@require_auth
def atualizar_anamnese(anamnese_id):
    try:
        user = get_current_user()
        
        # Verificar se o usuário pode acessar anamneses
        if not can_access_anamneses(user):
            return jsonify({
                'error': 'Acesso negado. Módulo disponível apenas para recepções 808 e 108.'
            }), 403
        
        data = request.get_json()
        print(f"📝 Atualizando anamnese {anamnese_id}: {data}")
        
        supabase = get_supabase()
        
        # Verificar se a anamnese existe e pertence ao usuário
        if user.role not in ['admin', 'admin_geral', 'admin_limitado']:
            # Para recepções, verificar se a anamnese pertence a elas
            existing = supabase.table('anamneses').select('*').eq('id', anamnese_id).eq('recepcao_id', user.recepcao_id).execute()
        else:
            # Para admins, pode editar qualquer anamnese
            existing = supabase.table('anamneses').select('*').eq('id', anamnese_id).execute()
        
        if not existing.data:
            return jsonify({'error': 'Anamnese não encontrada ou sem permissão para editar'}), 404
        
        # Preparar dados para atualização
        update_data = {}
        updatable_fields = [
            'nome_pais', 'nome_paciente', 'data_anamnese', 'profissional', 
            'tipo_anamnese', 'idade_paciente', 'motivo_consulta', 
            'observacoes', 'contato_responsavel', 'status'
        ]
        
        for field in updatable_fields:
            if field in data:
                if field == 'data_anamnese':
                    # Validar formato da data
                    try:
                        datetime.strptime(data[field], '%Y-%m-%d')
                        update_data[field] = data[field]
                    except ValueError:
                        return jsonify({'error': f'Data da anamnese deve estar no formato YYYY-MM-DD'}), 400
                else:
                    update_data[field] = data[field].strip() if isinstance(data[field], str) else data[field]
        
        if update_data:
            update_data['updated_at'] = datetime.now().isoformat()
            update_data['updated_by'] = user.username
            
            result = supabase.table('anamneses').update(update_data).eq('id', anamnese_id).execute()
            
            if result.data:
                print(f"✅ Anamnese {anamnese_id} atualizada com sucesso")
                return jsonify({
                    'message': 'Anamnese atualizada com sucesso',
                    'anamnese': result.data[0]
                }), 200
        
        return jsonify({'error': 'Nenhum dado para atualizar ou erro no banco'}), 400
        
    except Exception as e:
        print(f"💥 ERRO ao atualizar anamnese: {str(e)}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@anamneses_bp.route('/<int:anamnese_id>', methods=['DELETE'])
@require_auth
def deletar_anamnese(anamnese_id):
    try:
        user = get_current_user()
        
        # Verificar se o usuário pode acessar anamneses
        if not can_access_anamneses(user):
            return jsonify({
                'error': 'Acesso negado. Módulo disponível apenas para recepções 808 e 108.'
            }), 403
        
        supabase = get_supabase()
        
        # Verificar se a anamnese existe e pertence ao usuário
        if user.role not in ['admin', 'admin_geral', 'admin_limitado']:
            # Para recepções, verificar se a anamnese pertence a elas
            existing = supabase.table('anamneses').select('*').eq('id', anamnese_id).eq('recepcao_id', user.recepcao_id).execute()
        else:
            # Para admins, pode deletar qualquer anamnese
            existing = supabase.table('anamneses').select('*').eq('id', anamnese_id).execute()
        
        if not existing.data:
            return jsonify({'error': 'Anamnese não encontrada ou sem permissão para deletar'}), 404
        
        # Deletar anamnese
        result = supabase.table('anamneses').delete().eq('id', anamnese_id).execute()
        
        if result.data:
            print(f"✅ Anamnese {anamnese_id} deletada com sucesso")
            return jsonify({'message': 'Anamnese deletada com sucesso'}), 200
        
        return jsonify({'error': 'Erro ao deletar anamnese'}), 500
        
    except Exception as e:
        print(f"💥 ERRO ao deletar anamnese: {str(e)}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@anamneses_bp.route('/estatisticas', methods=['GET'])
@require_auth
def get_estatisticas_anamneses():
    try:
        user = get_current_user()
        
        # Verificar se o usuário pode acessar anamneses
        if not can_access_anamneses(user):
            return jsonify({
                'error': 'Acesso negado. Módulo disponível apenas para recepções 808 e 108.'
            }), 403
        
        supabase = get_supabase()
        
        # Buscar anamneses para estatísticas
        if user.role in ['admin', 'admin_geral', 'admin_limitado']:
            result = supabase.table('anamneses').select('*').execute()
        else:
            result = supabase.table('anamneses').select('*').eq('recepcao_id', user.recepcao_id).execute()
        
        anamneses = result.data
        hoje = date.today()
        
        # Calcular estatísticas
        estatisticas = {
            'total_anamneses': len(anamneses),
            'agendadas': len([a for a in anamneses if a.get('status') == 'agendada']),
            'realizadas': len([a for a in anamneses if a.get('status') == 'realizada']),
            'canceladas': len([a for a in anamneses if a.get('status') == 'cancelada']),
            'este_mes': 0,
            'proximo_mes': 0,
            'por_profissional': {},
            'por_tipo': {},
            'por_mes': {}
        }
        
        for anamnese in anamneses:
            # Anamneses por mês
            data_anamnese = datetime.strptime(anamnese['data_anamnese'], '%Y-%m-%d').date()
            
            if data_anamnese.month == hoje.month and data_anamnese.year == hoje.year:
                estatisticas['este_mes'] += 1
            
            # Próximo mês
            proximo_mes = hoje.month + 1 if hoje.month < 12 else 1
            proximo_ano = hoje.year if hoje.month < 12 else hoje.year + 1
            if data_anamnese.month == proximo_mes and data_anamnese.year == proximo_ano:
                estatisticas['proximo_mes'] += 1
            
            # Por profissional
            profissional = anamnese.get('profissional', 'Não informado')
            estatisticas['por_profissional'][profissional] = estatisticas['por_profissional'].get(profissional, 0) + 1
            
            # Por tipo
            tipo = anamnese.get('tipo_anamnese', 'Não informado')
            estatisticas['por_tipo'][tipo] = estatisticas['por_tipo'].get(tipo, 0) + 1
            
            # Por mês (para gráficos)
            mes_ano = data_anamnese.strftime('%Y-%m')
            estatisticas['por_mes'][mes_ano] = estatisticas['por_mes'].get(mes_ano, 0) + 1
        
        # Profissionais mais ativos
        estatisticas['profissionais_ativos'] = len(estatisticas['por_profissional'])
        
        print(f"📊 Estatísticas calculadas para {user.username}: {estatisticas['total_anamneses']} anamneses")
        
        return jsonify({
            'estatisticas': estatisticas,
            'user_recepcao': user.recepcao_nome
        }), 200
        
    except Exception as e:
        print(f"💥 ERRO ao calcular estatísticas: {str(e)}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@anamneses_bp.route('/profissionais', methods=['GET'])
@require_auth
def get_profissionais():
    """Endpoint para buscar lista de profissionais únicos"""
    try:
        user = get_current_user()
        
        if not can_access_anamneses(user):
            return jsonify({
                'error': 'Acesso negado. Módulo disponível apenas para recepções 808 e 108.'
            }), 403
        
        supabase = get_supabase()
        
        # Buscar profissionais únicos
        if user.role in ['admin', 'admin_geral', 'admin_limitado']:
            result = supabase.table('anamneses').select('profissional').execute()
        else:
            result = supabase.table('anamneses').select('profissional').eq('recepcao_id', user.recepcao_id).execute()
        
        # Extrair profissionais únicos
        profissionais_set = set()
        for item in result.data:
            if item.get('profissional'):
                profissionais_set.add(item['profissional'])
        
        profissionais = sorted(list(profissionais_set))
        
        return jsonify({
            'profissionais': profissionais,
            'total': len(profissionais)
        }), 200
        
    except Exception as e:
        print(f"💥 ERRO ao buscar profissionais: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500