#!/usr/bin/env python3
"""
Servidor simplificado para Railway
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS

# Criar app Flask
app = Flask(__name__)

# Configurar CORS
CORS(app, origins="*")

# Configurações básicas
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-for-testing')

# Health check para Railway
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'Reception Sync API is running',
        'port': os.environ.get('PORT', 'not_set'),
        'python_version': '3.11'
    }), 200

# Root endpoint
@app.route('/')
def root():
    return jsonify({
        'message': 'Reception Sync API',
        'status': 'online',
        'version': '1.0.0'
    }), 200

# Test endpoint
@app.route('/api/test')
def test():
    return jsonify({
        'message': 'API está funcionando!',
        'status': 'success'
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    print("🚀 Iniciando Reception Sync Backend (Versão Simplificada)...")
    
    # Configurações para Railway
    port = int(os.environ.get('PORT', 8000))
    host = '0.0.0.0'
    
    print(f"📡 Rodando em: {host}:{port}")
    print(f"🔗 Health check: http://{host}:{port}/api/health")
    print("-" * 50)
    
    app.run(host=host, port=port, debug=False)