#!/usr/bin/env python3
"""
Servidor principal do Reception Sync para Railway
"""

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
import os

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')
    
    # Configuração baseada no ambiente
    config_name = os.environ.get('FLASK_ENV', 'production')
    app.config.from_object(config.get(config_name, config['production']))
    
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
        return {'status': 'ok', 'message': 'Reception Sync API is running'}
    
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
        if test_database_connection():
            print("✅ Conexão com banco de dados OK")
        else:
            print("❌ Erro na conexão com banco de dados")
    except Exception as e:
        print(f"⚠️ Erro ao testar banco: {e}")
    
    port = int(os.environ.get('PORT', 5001))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"📡 API será executada em: {host}:{port}")
    print(f"🔄 Debug mode: {debug}")
    print("-" * 50)
    
    app.run(host=host, port=port, debug=debug)