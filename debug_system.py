#!/usr/bin/env python3
"""
Script de debug para testar o sistema
Execute: python debug_system.py
"""

import requests
import json
from models.user import User, test_database_connection, test_password_hash
from werkzeug.security import generate_password_hash, check_password_hash

def test_backend_connection():
    """Testa se o backend está rodando"""
    print("🔍 Testando conexão com backend...")
    
    try:
        # Testar endpoint básico
        response = requests.get('http://localhost:5000/')
        print(f"✅ Backend respondendo na porta 5000: {response.status_code}")
        print(f"📄 Resposta: {response.json()}")
        
        # Testar endpoint de teste
        response = requests.get('http://localhost:5000/api/test')
        print(f"✅ Endpoint /api/test: {response.status_code}")
        print(f"📄 Resposta: {response.json()}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Backend não está rodando na porta 5000")
        return False
    except Exception as e:
        print(f"❌ Erro ao conectar: {str(e)}")
        return False

def test_login_endpoint():
    """Testa o endpoint de login"""
    print("\n🔍 Testando endpoint de login...")
    
    test_credentials = [
        {'username': 'admin', 'password': '123456'},
        {'username': 'gerencia', 'password': '123456'},
        {'email': 'gerencia@incentivar.com', 'password': '123456'},
        {'username': 'recepcao808', 'password': '123456'},
        {'email': 'recepcao808@incentivar.com', 'password': '123456'}
    ]
    
    for cred in test_credentials:
        try:
            # Usar username ou email como login
            login_field = cred.get('username') or cred.get('email')
            
            response = requests.post('http://localhost:5000/api/auth/login', 
                json={'username': login_field, 'password': cred['password']})
            
            print(f"🔐 Teste login '{login_field}': {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ Login bem-sucedido!")
                data = response.json()
                print(f"   👤 Usuário: {data['user']['username']}")
                print(f"   🏢 Recepção: {data['user'].get('recepcao_nome', 'Admin')}")
            else:
                print(f"❌ Erro: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro na requisição: {str(e)}")

def test_user_model():
    """Testa o modelo de usuário"""
    print("\n🔍 Testando modelo de usuário...")
    
    # Testar conexão com banco
    if test_database_connection():
        print("✅ Conexão com banco OK")
    else:
        print("❌ Problema na conexão com banco")
        return
    
    # Testar busca de usuário
    test_usernames = ['admin', 'gerencia', 'recepcao808']
    
    for username in test_usernames:
        print(f"\n🔍 Buscando usuário: {username}")
        user = User.find_by_username(username)
        
        if user:
            print(f"✅ Usuário encontrado: {user.username}")
            print(f"   📧 Email: {user.email}")
            print(f"   👥 Role: {user.role}")
            print(f"   🏢 Recepção: {user.recepcao_nome}")
            
            # Testar senha
            if user.password_hash:
                password_check = user.check_password('123456')
                print(f"   🔐 Teste senha '123456': {password_check}")
                
                if not password_check:
                    print(f"   ⚠️ Hash atual: {user.password_hash[:50]}...")
                    # Testar se é um hash válido
                    try:
                        new_hash = generate_password_hash('123456')
                        test_result = check_password_hash(new_hash, '123456')
                        print(f"   🧪 Teste hash novo: {test_result}")
                    except Exception as e:
                        print(f"   ❌ Erro no hash: {str(e)}")
            else:
                print(f"   ❌ Hash de senha não encontrado!")
        else:
            print(f"❌ Usuário não encontrado: {username}")

def test_email_login():
    """Testa login por email"""
    print("\n🔍 Testando busca por email...")
    
    test_emails = ['gerencia@incentivar.com', 'recepcao808@incentivar.com']
    
    for email in test_emails:
        print(f"\n📧 Buscando por email: {email}")
        user = User.find_by_username(email)  # A função find_by_username também busca por email
        
        if user:
            print(f"✅ Usuário encontrado por email: {user.username}")
        else:
            print(f"❌ Usuário não encontrado por email: {email}")

def main():
    print("🚀 DIAGNÓSTICO DO SISTEMA DE LOGIN")
    print("=" * 50)
    
    # 1. Testar backend
    backend_ok = test_backend_connection()
    
    if not backend_ok:
        print("\n❌ PROBLEMA: Backend não está rodando!")
        print("   Solução: Execute 'python app.py' em outro terminal")
        return
    
    # 2. Testar modelo de usuário
    test_user_model()
    
    # 3. Testar login por email
    test_email_login()
    
    # 4. Testar endpoint de login
    test_login_endpoint()
    
    print("\n" + "=" * 50)
    print("🎯 PRÓXIMOS PASSOS:")
    print("1. Se usuários não existem: execute 'python create_test_users.py'")
    print("2. Se backend não responde: execute 'python app.py'") 
    print("3. Se senhas não funcionam: verifique os hashes no banco")

if __name__ == "__main__":
    main()