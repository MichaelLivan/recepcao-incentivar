#!/usr/bin/env python3
"""
Servidor principal do Reception Sync
Execute este arquivo para iniciar o backend
"""

from flask import Flask
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
import os

def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Token não expira
    
    # Habilitar CORS para todas as rotas
    CORS(app, supports_credentials=True, origins=['http://localhost:3000'])
    
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
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'ok', 'message': 'Reception Sync API is running'}
    
    @app.route('/')
    def root():
        return {'message': 'Reception Sync API', 'version': '1.0.0'}
    
    return app

if __name__ == '__main__':
    print("🚀 Iniciando Reception Sync Backend...")
    print("📡 API será executada em: http://localhost:5001")
    print("🔗 Frontend deve estar em: http://localhost:3000")
    print("-" * 50)
    
    app = create_app()
    
    # Verificar conexão com banco na inicialização
    try:
        from models.user import test_database_connection
        if test_database_connection():
            print("✅ Conexão com banco de dados OK")
        else:
            print("❌ Erro na conexão com banco de dados")
    except Exception as e:
        print(f"⚠️ Erro ao testar banco: {e}")
    
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )