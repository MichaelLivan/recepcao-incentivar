#!/usr/bin/env python3
"""
Configuração da conexão com Supabase para Railway
"""

import os
from supabase import create_client, Client
import logging

# Configurações do Supabase
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')

# Validação de variáveis obrigatórias
if not SUPABASE_URL or not SUPABASE_KEY:
    error_msg = "SUPABASE_URL e SUPABASE_KEY devem estar configurados nas variáveis de ambiente"
    logging.error(error_msg)
    if os.environ.get('FLASK_ENV') == 'production':
        raise ValueError(error_msg)
    else:
        print(f"⚠️ AVISO: {error_msg}")

# Cliente global do Supabase
_supabase_client = None

def get_supabase() -> Client:
    """Retorna cliente do Supabase (singleton) com tratamento de erro"""
    global _supabase_client
    
    if _supabase_client is None:
        try:
            if not SUPABASE_URL or not SUPABASE_KEY:
                raise ValueError("Credenciais do Supabase não configuradas")
                
            _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
            
            # Log apenas em desenvolvimento
            if os.environ.get('FLASK_ENV') != 'production':
                print(f"✅ Conectado ao Supabase: {SUPABASE_URL}")
            else:
                logging.info(f"Conectado ao Supabase: {SUPABASE_URL}")
                
        except Exception as e:
            error_msg = f"Erro ao conectar com Supabase: {e}"
            
            if os.environ.get('FLASK_ENV') == 'production':
                logging.error(error_msg)
            else:
                print(f"❌ {error_msg}")
            
            raise e
    
    return _supabase_client

def test_connection():
    """Testa a conexão com o banco com melhor tratamento de erro"""
    try:
        supabase = get_supabase()
        
        # Teste simples de conexão
        result = supabase.table('usuarios').select('username').limit(1).execute()
        
        user_count = len(result.data) if result.data else 0
        
        if os.environ.get('FLASK_ENV') != 'production':
            print(f"✅ Teste de conexão OK. Usuários encontrados: {user_count}")
        else:
            logging.info(f"Teste de conexão OK. Usuários: {user_count}")
            
        return True
        
    except Exception as e:
        error_msg = f"Erro no teste de conexão: {e}"
        
        if os.environ.get('FLASK_ENV') == 'production':
            logging.error(error_msg)
        else:
            print(f"❌ {error_msg}")
            
        return False

def health_check():
    """Health check específico para Railway"""
    try:
        supabase = get_supabase()
        
        # Teste básico de ping
        result = supabase.table('usuarios').select('count').limit(0).execute()
        
        return {
            'database': 'connected',
            'supabase_url': SUPABASE_URL[:50] + '...' if SUPABASE_URL else 'not_configured',
            'status': 'healthy'
        }
        
    except Exception as e:
        return {
            'database': 'error',
            'error': str(e),
            'status': 'unhealthy'
        }

# Auto-configuração para Railway
if __name__ == '__main__':
    print("🔍 Testando conexão com Supabase...")
    
    if test_connection():
        print("🎉 Conexão OK!")
    else:
        print("💥 Falha na conexão!")
        exit(1)