#!/usr/bin/env python3
"""
Configuração da conexão com Supabase
"""

import os
from supabase import create_client, Client

# Configurações do Supabase
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://dzufdkejujyhvtlyvors.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'your-supabase-anon-key')

# Cliente global do Supabase
_supabase_client = None

def get_supabase() -> Client:
    """Retorna cliente do Supabase (singleton)"""
    global _supabase_client
    
    if _supabase_client is None:
        try:
            _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
            print(f"✅ Conectado ao Supabase: {SUPABASE_URL}")
        except Exception as e:
            print(f"❌ Erro ao conectar com Supabase: {e}")
            raise e
    
    return _supabase_client

def test_connection():
    """Testa a conexão com o banco"""
    try:
        supabase = get_supabase()
        result = supabase.table('usuarios').select('username').limit(1).execute()
        print(f"✅ Teste de conexão OK. Usuários encontrados: {len(result.data)}")
        return True
    except Exception as e:
        print(f"❌ Erro no teste de conexão: {e}")
        return False

if __name__ == '__main__':
    # Teste direto
    test_connection()