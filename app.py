#!/usr/bin/env python3
"""
Servidor principal do Reception Sync para Railway
VERSÃO OTIMIZADA - Corrigida para deployment
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
    print("💡 Continuando mesmo assim para Railway...")

print("✅ Continuando inicialização...")

# Agora importar o resto
from flask import Flask, send_from_directory, send_file, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    
    # Configuração para Railway
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    
    # Configuração de CORS para Railway
    cors_origins = os.environ.get('CORS_ORIGINS', '*').split(',')
    app.config['CORS_ORIGINS'] = cors_origins
    
    # Debug das configurações
    config_name = os.environ.get('FLASK_ENV', 'production')
    print(f"🔧 Configuração: {config_name}")
    print(f"🔧 DEBUG: {config_name != 'production'}")
    print(f"🔧 CORS_ORIGINS: {cors_origins}")
    
    # Habilitar CORS
    CORS(app, 
         supports_credentials=True, 
         origins=cors_origins,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # Inicializar JWT
    jwt = JWTManager(app)
    
    # Health check SIMPLES para Railway
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'ok', 
            'message': 'Reception Sync API is running',
            'environment': config_name,
            'port': os.environ.get('PORT', 'not_set'),
            'supabase_configured': bool(SUPABASE_URL and SUPABASE_KEY)
        }), 200
    
    # Root endpoint
    @app.route('/')
    def root():
        return jsonify({
            'status': 'ok',
            'message': 'Reception Sync API',
            'version': '1.0.0'
        })
    
    # Endpoint básico de teste
    @app.route('/api/test')
    def test():
        return jsonify({'message': 'API funcionando!', 'status': 'success'})
    
    # Importar e registrar blueprints apenas se as variáveis estiverem disponíveis
    if SUPABASE_URL and SUPABASE_KEY:
        try:
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
            
            print("✅ Todos os blueprints registrados com sucesso")
            
        except Exception as e:
            print(f"⚠️ Erro ao registrar blueprints: {e}")
            print("💡 Continuando com endpoints básicos...")
    
    # Servir arquivos estáticos do React (se existirem)
    @app.route('/<path:path>')
    def serve_react_app(path):
        # Se for uma requisição para a API, retorna 404
        if path.startswith('api/'):
            return jsonify({'error': 'API endpoint not found'}), 404
            
        # Se o arquivo existe na pasta static, serve ele
        if path and app.static_folder and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        
        # Caso contrário, retorna info da API
        return jsonify({
            'message': 'Reception Sync API',
            'status': 'ok',
            'frontend': 'not_built'
        })
    
    return app

# Para Railway
app = create_app()

if __name__ == '__main__':
    print("🚀 Iniciando Reception Sync Backend para Railway...")
    
    # Configurações para Railway
    port = int(os.environ.get('PORT', 8000))
    host = '0.0.0.0'  # Importante para Railway
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"📡 API será executada em: {host}:{port}")
    print(f"🔄 Debug mode: {debug}")
    print(f"🌐 CORS origins: {os.environ.get('CORS_ORIGINS', '*')}")
    print("-" * 50)
    
    # Testar conexão com banco (não crítico para inicialização)
    try:
        if SUPABASE_URL and SUPABASE_KEY:
            from models.user import test_database_connection
            print("🔍 Testando conexão com banco de dados...")
            if test_database_connection():
                print("✅ Conexão com banco de dados OK")
            else:
                print("⚠️ Problema na conexão com banco, mas continuando...")
    except Exception as e:
        print(f"⚠️ Erro ao testar banco: {e}")
        print("💡 Continuando mesmo assim...")
    
    app.run(host=host, port=port, debug=debug)