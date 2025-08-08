#!/usr/bin/env python3
"""
Teste do login após correção do código
Execute: python teste_login_corrigido.py
"""

def testar_busca_usuario():
    print("🔍 TESTANDO BUSCA DE USUÁRIO")
    print("=" * 50)
    
    try:
        from models.user import User
        
        # Testar busca por username
        print("🧪 Teste 1: Buscar por username 'gerencia'")
        user1 = User.find_by_username('gerencia')
        print(f"Resultado: {'✅ ENCONTRADO' if user1 else '❌ NÃO ENCONTRADO'}")
        
        # Testar busca por email
        print("\n🧪 Teste 2: Buscar por email 'gerencia@incentivar.com'")
        user2 = User.find_by_username('gerencia@incentivar.com')
        print(f"Resultado: {'✅ ENCONTRADO' if user2 else '❌ NÃO ENCONTRADO'}")
        
        # Testar busca por email inexistente
        print("\n🧪 Teste 3: Buscar por email inexistente 'teste@teste.com'")
        user3 = User.find_by_username('teste@teste.com')
        print(f"Resultado: {'✅ ENCONTRADO' if user3 else '❌ NÃO ENCONTRADO (esperado)'}")
        
        return user1 or user2
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

def testar_verificacao_senha():
    print("\n🔐 TESTANDO VERIFICAÇÃO DE SENHA")
    print("=" * 50)
    
    try:
        from models.user import User
        
        # Buscar usuário
        user = User.find_by_username('gerencia@incentivar.com')
        
        if not user:
            print("❌ Usuário não encontrado para testar senha")
            return False
        
        # Testar senha correta
        print("🧪 Testando senha '123456'...")
        resultado = user.check_password('123456')
        print(f"Resultado: {'✅ SENHA CORRETA' if resultado else '❌ SENHA INCORRETA'}")
        
        return resultado
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False

def testar_login_api():
    print("\n🌐 TESTANDO LOGIN VIA API")
    print("=" * 50)
    
    credenciais = [
        ('gerencia', '123456', 'Username'),
        ('gerencia@incentivar.com', '123456', 'Email'),
        ('admin', '123456', 'Username'),
        ('admin@test.com', '123456', 'Email')
    ]
    
    try:
        import requests
        
        for login_input, senha, tipo in credenciais:
            print(f"\n🔐 Testando {tipo}: {login_input} / {senha}")
            
            try:
                response = requests.post(
                    'http://localhost:5000/api/auth/login',
                    json={'username': login_input, 'password': senha},
                    timeout=5
                )
                
                print(f"📊 Status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print("✅ LOGIN FUNCIONOU!")
                    print(f"👤 Username: {result.get('user', {}).get('username')}")
                    print(f"💼 Role: {result.get('user', {}).get('role')}")
                    print(f"🎫 Token: {result.get('access_token', '')[:30]}...")
                    
                    print(f"\n🎉 CREDENCIAL FUNCIONANDO:")
                    print(f"{tipo}: {login_input}")
                    print(f"Senha: {senha}")
                    return True
                else:
                    print(f"❌ Falhou: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                print("❌ Backend não responde! Execute: python app.py")
                return False
                
        print("\n❌ NENHUMA CREDENCIAL FUNCIONOU")
        return False
        
    except ImportError:
        print("❌ Requests não instalado: pip install requests")
        return False

def main():
    print("🧪 TESTE COMPLETO APÓS CORREÇÃO DO CÓDIGO")
    print("=" * 60)
    
    # Teste 1: Busca de usuário
    busca_ok = testar_busca_usuario()
    
    if not busca_ok:
        print("\n❌ ERRO: Usuário não foi encontrado")
        print("🔧 Verifique se o SQL foi executado no Supabase")
        return
    
    # Teste 2: Verificação de senha
    senha_ok = testar_verificacao_senha()
    
    if not senha_ok:
        print("\n❌ ERRO: Verificação de senha falhou")
        print("🔧 Problema no hash da senha")
        return
    
    # Teste 3: Login via API
    login_ok = testar_login_api()
    
    if login_ok:
        print("\n🎉 PROBLEMA COMPLETAMENTE RESOLVIDO!")
        print("🌐 Teste agora no frontend:")
        print("   - Acesse: http://localhost:8080")
        print("   - Use: gerencia@incentivar.com / 123456")
        print("   - Ou: gerencia / 123456")
    else:
        print("\n❌ Login via API ainda falha")
        print("🔧 Verifique se o backend foi atualizado")

if __name__ == "__main__":
    main()