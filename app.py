from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurações
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'sua-chave-secreta-aqui-mude-em-producao')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Token não expira

# Inicializar extensões
jwt = JWTManager(app)
CORS(app)  # Permite requisições do frontend

# Lista de blueprints essenciais para tentar importar
essential_blueprints = [
    ('blueprints.auth', 'auth_bp', '/api/auth'),
    ('blueprints.dashboard', 'dashboard_bp', '/api/dashboard'),
    ('blueprints.recepcao', 'recepcao_bp', '/api/recepcao'),
]

# Lista de blueprints opcionais
optional_blueprints = [
    ('blueprints.admin', 'admin_bp', '/api/admin'),
    ('blueprints.salas', 'salas_bp', '/api/salas'),
    ('blueprints.estoque', 'estoque_bp', '/api/estoque'),
    ('blueprints.orcamentos', 'orcamentos_bp', '/api/orcamentos'),
    ('blueprints.brindes', 'brindes_bp', '/api/brindes'),
    ('blueprints.lista_espera', 'lista_espera_bp', '/api/lista-espera'),
    ('blueprints.visitas', 'visitas_bp', '/api/visitas'),
    ('blueprints.anamnese', 'anamnese_bp', '/api/anamnese'),
]

def register_blueprints():
    """Registra blueprints com tratamento de erro individual"""
    registered_count = 0
    failed_blueprints = []
    
    # Registrar blueprints essenciais primeiro
    print("🔧 Registrando blueprints essenciais...")
    for module_name, blueprint_name, url_prefix in essential_blueprints:
        try:
            module = __import__(module_name, fromlist=[blueprint_name])
            blueprint = getattr(module, blueprint_name)
            app.register_blueprint(blueprint, url_prefix=url_prefix)
            print(f"✅ {blueprint_name} registrado em {url_prefix}")
            registered_count += 1
        except Exception as e:
            print(f"❌ Erro ao registrar {blueprint_name}: {str(e)}")
            failed_blueprints.append((blueprint_name, str(e)))
    
    # Registrar blueprints opcionais
    print("🔧 Registrando blueprints opcionais...")
    for module_name, blueprint_name, url_prefix in optional_blueprints:
        try:
            module = __import__(module_name, fromlist=[blueprint_name])
            blueprint = getattr(module, blueprint_name)
            app.register_blueprint(blueprint, url_prefix=url_prefix)
            print(f"✅ {blueprint_name} registrado em {url_prefix}")
            registered_count += 1
        except Exception as e:
            print(f"⚠️ Blueprint opcional {blueprint_name} falhou: {str(e)}")
            failed_blueprints.append((blueprint_name, str(e)))
    
    print(f"\n📊 Resultado: {registered_count} blueprints registrados")
    
    if failed_blueprints:
        print("⚠️ Blueprints com problemas:")
        for bp_name, error in failed_blueprints:
            print(f"   - {bp_name}: {error}")
    else:
        print("✅ Todos os blueprints registrados com sucesso!")
    
    return len(failed_blueprints) == 0

# Registrar blueprints
register_blueprints()

# Rota de teste
@app.route('/')
def hello():
    return {'message': 'Reception Sync API está rodando!', 'status': 'online'}

@app.route('/api/test')
def test():
    return {'message': 'API funcionando!', 'endpoints': [
        '/api/auth/login',
        '/api/auth/me',
        '/api/dashboard/stats',
        '/api/salas/',
        '/api/orcamentos/',
    ]}

# Tratamento de erros
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Endpoint não encontrado'}, 404

@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Erro interno do servidor'}, 500

# Rota para listar todas as rotas registradas (debug)
@app.route('/api/debug/routes')
def list_routes():
    """Lista todas as rotas registradas para debug"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'url': str(rule)
        })
    return {'routes': routes}

# Configuração para desenvolvimento
if __name__ == '__main__':
    print("🚀 Iniciando Reception Sync API...")
    print("📍 Acesse: http://localhost:5001")  # Mudei para porta 5001
    print("🧪 Teste: http://localhost:5001/api/test")
    print("🔐 Login: POST http://localhost:5001/api/auth/login")
    print("🔍 Debug rotas: http://localhost:5001/api/debug/routes")
    print("=" * 50)
    
    app.run(
        host='0.0.0.0',  # Permite acesso externo
        port=5001,       # Mudei para porta 5001 para evitar conflito
        debug=True       # Modo debug ativado
    )