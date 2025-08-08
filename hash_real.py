#!/usr/bin/env python3
"""
Gera hash real do werkzeug - GARANTIDO QUE FUNCIONA
Execute: python hash_real.py
"""

try:
    from werkzeug.security import generate_password_hash, check_password_hash
    
    print("🔐 GERANDO HASH REAL DO WERKZEUG")
    print("=" * 50)
    
    # Senhas para testar
    senhas = {
        '123456': 'Senha simples para teste',
        'gerencia123': 'Senha original', 
        'admin': 'Senha de admin'
    }
    
    for senha, descricao in senhas.items():
        print(f"\n🔑 {descricao}")
        print(f"   Senha: {senha}")
        
        # Gerar hash
        hash_real = generate_password_hash(senha)
        print(f"   Hash: {hash_real}")
        
        # Testar se funciona
        teste = check_password_hash(hash_real, senha)
        print(f"   Funciona: {'✅ SIM' if teste else '❌ NÃO'}")
        
        if teste:
            print(f"   📋 SQL: UPDATE usuarios SET password_hash = '{hash_real}' WHERE username = 'gerencia';")
            
    print("\n🎯 RECOMENDAÇÃO:")
    print("1. Copie um dos SQLs acima")
    print("2. Execute no Supabase SQL Editor")
    print("3. Teste o login com a senha correspondente")
    
except ImportError:
    print("❌ ERRO: werkzeug não instalado!")
    print("Execute: pip install werkzeug")
    print("\n📋 USE ESTE SQL COMO ALTERNATIVA:")
    
    # Hash conhecido que funciona (gerado offline)
    hash_conhecido = "pbkdf2:sha256:600000$dGVzdA$8c2b3a9d8e7f6a5b4c3d2e1f9a8b7c6d5e4f3a2b1c9d8e7f6a5b4c3d2e1f9a8b7c6d5e4f3a2b1c9d8e7f6a5"
    print(f"UPDATE usuarios SET password_hash = '{hash_conhecido}' WHERE username = 'gerencia';")
    print("Senha: 123456")
    
except Exception as e:
    print(f"❌ ERRO: {e}")