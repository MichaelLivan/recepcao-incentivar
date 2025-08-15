#!/usr/bin/env python3
"""
Servidor principal do Reception Sync para Railway
VERSÃO CORRIGIDA - Carrega .env automaticamente
"""

# IMPORTANTE: Carregar variáveis de ambiente ANTES de qualquer outra importação
from dotenv import load_dotenv
import os

# Carregar .env do diretório atual
load_dotenv()

# Verificar se variáveis foram carregadas
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

print("🔍 DEBUG: Verificando variáveis de ambiente...")
print(f"SUPABASE_URL: {SUPABASE_URL[:50]}..." if SUPABASE_URL else "❌ SUPABASE_URL não carregada")
print(f"SUPABASE_KEY: {SUPABASE_KEY[:30]}..." if SUPABASE_KEY else "❌ SUPABASE_KEY não carregada")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ ERRO: Variáveis de ambiente não carregadas!")
    print("💡 Verifique se o arquivo .env existe e está no diretório correto")
    print(f"📁 Diretório atual: {os.getcwd()}")
    exit(1)

print("✅ Variáveis de ambiente carregadas com sucesso!")

# Agora importar o resto
from flask import Flask, send_from_directory, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp
from blueprints.salas import salas_bp
from blueprints.orcamentos import orcamentos_bp
from blueprints.estoque import estoque_bp
from blueprints.brindes import brindes_bp
from blueprints.lista_espera import lista_espera_bp
from blueprints.visitas import visitas_bp
from blueprints.anamnese import anamneses_bp
from blueprints.dashboard import dashboard_bp
from blueprints.recepcao import recepcao_bp
from config import config

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    
    # Configuração baseada no ambiente
    config_name = os.environ.get('FLASK_ENV', 'production')
    app.config.from_object(config.get(config_name, config['production']))
    
    # Debug das configurações
    print(f"🔧 Configuração: {config_name}")
    print(f"🔧 DEBUG: {app.config.get('DEBUG', False)}")
    print(f"🔧 CORS_ORIGINS: {app.config.get('CORS_ORIGINS', [])}")
    
    # Habilitar CORS
    CORS(app, 
         supports_credentials=True, 
         origins=app.config['CORS_ORIGINS'],
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # Inicializar JWT
    jwt = JWTManager(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(salas_bp, url_prefix='/api/salas')
    app.register_blueprint(orcamentos_bp, url_prefix='/api/orcamentos')
    app.register_blueprint(estoque_bp, url_prefix='/api/estoque')
    app.register_blueprint(brindes_bp, url_prefix='/api/brindes')
    app.register_blueprint(lista_espera_bp, url_prefix='/api/lista-espera')
    app.register_blueprint(visitas_bp, url_prefix='/api/visitas')
    app.register_blueprint(anamneses_bp, url_prefix='/api/anamneses')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(recepcao_bp, url_prefix='/api/recepcao')
    
    # Health check para Railway
    @app.route('/api/health')
    def health_check():
        # Incluir informações de debug
        return {
            'status': 'ok', 
            'message': 'Reception Sync API is running',
            'supabase_configured': bool(SUPABASE_URL and SUPABASE_KEY),
            'environment': config_name
        }
    
    # Endpoint de debug para variáveis de ambiente
    @app.route('/api/debug/env')
    def debug_env():
        return {
            'supabase_url_configured': bool(SUPABASE_URL),
            'supabase_key_configured': bool(SUPABASE_KEY),
            'flask_env': os.environ.get('FLASK_ENV', 'not_set'),
            'port': os.environ.get('PORT', 'not_set'),
            'working_directory': os.getcwd(),
            'env_file_exists': os.path.exists('.env')
        }
    
    # Servir arquivos estáticos do React
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react_app(path):
        # Se for uma requisição para a API, retorna 404
        if path.startswith('api/'):
            return {'error': 'API endpoint not found'}, 404
            
        # Se o arquivo existe na pasta static, serve ele
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        
        # Caso contrário, serve o index.html (SPA routing)
        return send_from_directory(app.static_folder, 'index.html')
    
    # Middleware para logs em produção
    if not app.config.get('DEBUG'):
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not os.path.exists('logs'):
            os.mkdir('logs')
            
        file_handler = RotatingFileHandler('logs/reception_sync.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Reception Sync startup')
    
    return app

# Para Railway
app = create_app()

if __name__ == '__main__':
    print("🚀 Iniciando Reception Sync Backend...")
    
    # Verificar conexão com banco na inicialização
    try:
        from models.user import test_database_connection
        print("🔍 Testando conexão com banco de dados...")
        if test_database_connection():
            print("✅ Conexão com banco de dados OK")
        else:
            print("❌ Erro na conexão com banco de dados")
            print("💡 Verifique as credenciais do Supabase")
    except Exception as e:
        print(f"⚠️ Erro ao testar banco: {e}")
        print("💡 Continuando mesmo assim...")
    
    port = int(os.environ.get('PORT', 5001))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"📡 API será executada em: {host}:{port}")
    print(f"🔄 Debug mode: {debug}")
    print(f"🌐 CORS origins: {os.environ.get('CORS_ORIGINS', 'localhost:3000')}")
    print("-" * 50)
    
    app.run(host=host, port=port, debug=debug)