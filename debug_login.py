#!/usr/bin/env python3
"""
Debug específico para o problema de login
Execute este script para diagnosticar por que o login não funciona
"""

def test_supabase_users():
    """Testa se consegue buscar usuários do Supabase"""
    print("🗄️ Testando busca de usuários no Supabase...")
    try:
        from database import get_supabase
        supabase = get_supabase()
        
        # Buscar todos os usuários
        result = supabase.table('usuarios').select('*').execute()
        users = result.data
        
        print(f"✅ Encontrados {len(users)} usuários:")
        for user in users:
            print(f"   👤 {user['username']} ({user['email']}) - {user['role']}")
            print(f"      Hash: {user['password_hash'][:50]}...")
            print(f"      Ativo: {user['ativo']}")
        
        return users
    except Exception as e:
        print(f"❌ Erro ao buscar usuários: {e}")
        import traceback
        traceback.print_exc()
        return []

def test_user_model():
    """Testa o modelo User diretamente"""
    print("\n👤 Testando modelo User...")
    try:
        from models.user import User
        
        # Testar usuários específicos
        test_usernames = ['admin', 'gerencia', 'recepcao103']
        
        for username in test_usernames:
            print(f"\n🔍 Testando usuário: {username}")
            
            # Buscar usuário
            user = User.find_by_username(username)
            
            if user:
                print(f"   ✅ Usuário encontrado")
                print(f"   📧 Email: {user.email}")
                print(f"   👤 Role: {user.role}")
                print(f"   🔐 Hash: {user.password_hash[:50]}...")
                print(f"   ✅ Ativo: {user.ativo}")
                
                # Testar senha
                password_test = user.check_password('123456')
                print(f"   🔑 Senha '123456': {'✅ OK' if password_test else '❌ FALHOU'}")
                
                if not password_test:
                    # Testar outras senhas possíveis
                    other_passwords = ['admin', username, 'password']
                    for pwd in other_passwords:
                        test_result = user.check_password(pwd)
                        if test_result:
                            print(f"   🎯 Senha correta é: '{pwd}'")
                            break
                    else:
                        print(f"   ⚠️ Nenhuma senha testada funcionou")
            else:
                print(f"   ❌ Usuário '{username}' não encontrado")
                
        return True
    except Exception as e:
        print(f"❌ Erro no modelo User: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_password_hash():
    """Testa geração e verificação de hash"""
    print("\n🔐 Testando sistema de hash...")
    try:
        from werkzeug.security import generate_password_hash, check_password_hash
        
        test_password = '123456'
        
        # Gerar novo hash
        new_hash = generate_password_hash(test_password)
        print(f"   Hash gerado: {new_hash}")
        
        # Verificar se funciona
        verify_result = check_password_hash(new_hash, test_password)
        print(f"   Verificação: {'✅ OK' if verify_result else '❌ FALHOU'}")
        
        # Testar hash do banco (exemplo)
        banco_hash = "scrypt:32768:8:1$akaGxzfS2OBDN9VB$0"  # Exemplo do que vi na imagem
        try:
            banco_test = check_password_hash(banco_hash, test_password)
            print(f"   Hash do banco: {'✅ OK' if banco_test else '❌ FALHOU'}")
        except Exception as e:
            print(f"   Hash do banco: ❌ ERRO - {e}")
        
        return True
    except Exception as e:
        print(f"❌ Erro no sistema de hash: {e}")
        return False

def test_login_endpoint():
    """Testa o endpoint de login diretamente"""
    print("\n🌐 Testando endpoint de login...")
    try:
        import requests
        
        # Dados de teste
        login_data = {
            'username': 'admin',
            'password': '123456'
        }
        
        # Fazer requisição
        response = requests.post(
            'http://localhost:5001/api/auth/login',
            json=login_data,
            timeout=5
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Login bem-sucedido!")
            print(f"   Token: {data.get('access_token', 'N/A')[:50]}...")
            print(f"   User: {data.get('user', {}).get('username', 'N/A')}")
        else:
            try:
                error_data = response.json()
                print(f"   ❌ Erro: {error_data}")
            except:
                print(f"   ❌ Erro: {response.text}")
        
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("   ❌ Backend não está rodando")
        return False
    except Exception as e:
        print(f"   ❌ Erro na requisição: {e}")
        return False

def test_direct_supabase_query():
    """Testa query direta no Supabase"""
    print("\n🔍 Testando query direta no Supabase...")
    try:
        from database import get_supabase
        supabase = get_supabase()
        
        # Buscar usuário admin especificamente
        result = supabase.table('usuarios').select('*').eq('username', 'admin').execute()
        
        if result.data:
            user = result.data[0]
            print(f"   ✅ Usuário 'admin' encontrado diretamente")
            print(f"   ID: {user['id']}")
            print(f"   Username: {user['username']}")
            print(f"   Email: {user['email']}")
            print(f"   Ativo: {user['ativo']}")
            print(f"   Hash completo: {user['password_hash']}")
            return user
        else:
            print(f"   ❌ Usuário 'admin' não encontrado")
            return None
    except Exception as e:
        print(f"   ❌ Erro na query: {e}")
        return None

def main():
    """Função principal de debug"""
    print("🔬 Debug Específico do Login")
    print("=" * 50)
    
    # Executar todos os testes
    supabase_users = test_supabase_users()
    
    if supabase_users:
        test_user_model()
        test_password_hash()
        test_direct_supabase_query()
        test_login_endpoint()
    
    print("\n" + "=" * 50)
    print("🎯 Resultado do diagnóstico:")
    
    if supabase_users:
        print("✅ Usuários existem no banco")
        print("💡 Se o login ainda não funcionar, o problema está na verificação de senha")
        print("🔧 Soluções possíveis:")
        print("   1. As senhas podem ter sido hasheadas com algoritmo diferente")
        print("   2. Pode ter algum caractere especial ou encoding diferente")
        print("   3. O hash pode estar truncado ou corrompido")
        print("\n🚀 Próximo passo: Execute este script e veja qual teste falha")
    else:
        print("❌ Problema na conexão com Supabase")

if __name__ == '__main__':
    main()