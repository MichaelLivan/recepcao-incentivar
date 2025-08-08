#!/usr/bin/env python3
"""
Criar usuário 100% funcional do zero
Execute: python criar_usuario_funcional.py
"""

def criar_usuario_funcional():
    print("🚀 CRIANDO USUÁRIO 100% FUNCIONAL DO ZERO")
    print("=" * 60)
    
    try:
        from werkzeug.security import generate_password_hash, check_password_hash
        from database import get_supabase
        
        supabase = get_supabase()
        print("✅ Conectado ao Supabase")
        
        # Definir credenciais
        username = "gerencia"
        senha = "123456"
        
        print(f"👤 Username: {username}")
        print(f"🔑 Senha: {senha}")
        
        # Gerar hash funcional
        print("\n🔐 Gerando hash...")
        hash_senha = generate_password_hash(senha)
        print(f"Hash: {hash_senha}")
        
        # Testar hash ANTES de salvar
        print("\n🧪 Testando hash antes de salvar...")
        teste_hash = check_password_hash(hash_senha, senha)
        print(f"Resultado: {'✅ FUNCIONA' if teste_hash else '❌ NÃO FUNCIONA'}")
        
        if not teste_hash:
            print("❌ ERRO: Hash gerado não funciona!")
            return False
        
        # Deletar usuário existente
        print(f"\n🗑️ Removendo usuário '{username}' existente...")
        delete_result = supabase.table('usuarios').delete().eq('username', username).execute()
        print(f"Removido: {len(delete_result.data) if delete_result.data else 0} registros")
        
        # Criar usuário novo
        print(f"\n👤 Criando usuário '{username}'...")
        user_data = {
            'username': username,
            'email': f'{username}@incentivar.com',
            'password_hash': hash_senha,
            'role': 'admin_geral',
            'recepcao_id': None,
            'recepcao_nome': None,
            'ativo': True
        }
        
        insert_result = supabase.table('usuarios').insert(user_data).execute()
        
        if insert_result.data:
            user_criado = insert_result.data[0]
            print(f"✅ Usuário criado com sucesso!")
            print(f"   ID: {user_criado['id']}")
            print(f"   Username: {user_criado['username']}")
            print(f"   Role: {user_criado['role']}")
            
            # Verificar se foi salvo corretamente
            print(f"\n🔍 Verificando usuário salvo...")
            verify_result = supabase.table('usuarios').select('*').eq('username', username).execute()
            
            if verify_result.data:
                user_salvo = verify_result.data[0]
                hash_salvo = user_salvo['password_hash']
                
                print(f"Hash salvo: {hash_salvo[:60]}...")
                
                # Testar senha com hash salvo
                print(f"\n🧪 Testando senha com hash salvo...")
                teste_final = check_password_hash(hash_salvo, senha)
                print(f"Resultado: {'✅ FUNCIONA' if teste_final else '❌ NÃO FUNCIONA'}")
                
                if teste_final:
                    print(f"\n🎉 USUÁRIO CRIADO E FUNCIONANDO!")
                    print(f"🔑 CREDENCIAIS FINAIS:")
                    print(f"   Username: {username}")
                    print(f"   Password: {senha}")
                    print(f"\n🧪 TESTE AGORA:")
                    print(f"curl -X POST http://localhost:5000/api/auth/login \\")
                    print(f"-H 'Content-Type: application/json' \\")
                    print(f"-d '{{\"username\": \"{username}\", \"password\": \"{senha}\"}}'")
                    return True
                else:
                    print(f"❌ Hash salvo não funciona!")
                    return False
            else:
                print(f"❌ Usuário não foi encontrado após criação!")
                return False
        else:
            print(f"❌ Erro ao criar usuário!")
            return False
            
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

def testar_login_api(username="gerencia", senha="123456"):
    """Testa login via API"""
    print(f"\n🌐 TESTANDO LOGIN VIA API")
    print("=" * 40)
    
    try:
        import requests
        
        url = "http://localhost:5000/api/auth/login"
        data = {"username": username, "password": senha}
        
        print(f"📡 URL: {url}")
        print(f"📤 Dados: {data}")
        
        response = requests.post(url, json=data, timeout=10)
        
        print(f"📊 Status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("🎉 LOGIN FUNCIONOU PERFEITAMENTE!")
            print(f"👤 Username: {result.get('user', {}).get('username')}")
            print(f"💼 Role: {result.get('user', {}).get('role')}")
            print(f"🎫 Token: {result.get('access_token', '')[:50]}...")
            return True
        else:
            print("❌ Login ainda falha")
            return False
            
    except Exception as e:
        print(f"❌ ERRO no teste API: {e}")
        return False

def main():
    print("🚀 CRIADOR DE USUÁRIO FUNCIONAL - SOLUÇÃO DEFINITIVA")
    print("=" * 70)
    
    # Criar usuário funcional
    sucesso = criar_usuario_funcional()
    
    if sucesso:
        # Testar login via API
        login_ok = testar_login_api()
        
        if login_ok:
            print("\n🎉 PROBLEMA COMPLETAMENTE RESOLVIDO!")
            print("🌐 Teste agora no frontend:")
            print("   Username: gerencia")
            print("   Password: 123456")
        else:
            print("\n❌ Usuário criado mas login via API falha")
            print("🔧 Pode ser problema no backend")
    else:
        print("\n❌ Não conseguiu criar usuário funcional")

if __name__ == "__main__":
    main()