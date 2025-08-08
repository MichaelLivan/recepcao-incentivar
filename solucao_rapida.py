#!/usr/bin/env python3
"""
SOLUÇÃO RÁPIDA - Gera hash garantido que funciona
Execute: python solucao_rapida.py
"""

from werkzeug.security import generate_password_hash, check_password_hash

def gerar_hash_garantido():
    print("🔐 GERANDO HASH GARANTIDO")
    print("=" * 40)
    
    senha = "gerencia123"
    
    # Gerar múltiplos hashes para testar
    print(f"🔑 Senha: {senha}")
    print("\n📋 HASHES GERADOS:")
    
    for i in range(3):
        hash_gerado = generate_password_hash(senha)
        verificacao = check_password_hash(hash_gerado, senha)
        
        print(f"\nHash {i+1}:")
        print(f"Hash: {hash_gerado}")
        print(f"Funciona: {verificacao}")
        
        if verificacao:
            print(f"\n✅ HASH CONFIRMADO FUNCIONANDO:")
            print(f"📋 EXECUTE NO SUPABASE SQL EDITOR:")
            print(f"UPDATE usuarios SET password_hash = '{hash_gerado}' WHERE username = 'gerencia';")
            print(f"\n🧪 TESTE COM:")
            print(f"Username: gerencia")
            print(f"Password: {senha}")
            return hash_gerado
    
    print("❌ Nenhum hash funcionou!")
    return None

def teste_simples():
    print("\n🧪 TESTE SIMPLES")
    print("=" * 40)
    
    # Hash específico para teste
    senha = "123456"
    hash_simples = generate_password_hash(senha)
    
    print(f"🔑 Senha simples: {senha}")
    print(f"🔐 Hash simples: {hash_simples}")
    print(f"✅ Verificação: {check_password_hash(hash_simples, senha)}")
    
    print(f"\n📋 SQL ALTERNATIVO (senha: 123456):")
    print(f"UPDATE usuarios SET password_hash = '{hash_simples}' WHERE username = 'gerencia';")

if __name__ == "__main__":
    print("🚀 SOLUÇÃO RÁPIDA DE SENHA")
    print("=" * 50)
    
    try:
        # Tentar hash principal
        hash_principal = gerar_hash_garantido()
        
        if not hash_principal:
            # Hash alternativo
            teste_simples()
            
        print("\n🎯 APÓS EXECUTAR O SQL:")
        print("1. Teste o login no frontend")
        print("2. Ou teste via curl:")
        print("curl -X POST http://localhost:5000/api/auth/login -H 'Content-Type: application/json' -d '{\"username\": \"gerencia\", \"password\": \"gerencia123\"}'")
        
    except ImportError:
        print("❌ Werkzeug não instalado!")
        print("Execute: pip install werkzeug")
    except Exception as e:
        print(f"❌ Erro: {e}")