#!/usr/bin/env python3
"""
Teste simples para verificar se o login está funcionando
"""

def test_connection():
    """Testa conexão básica"""
    print("🔌 Testando conexão...")
    try:
        from database import get_supabase
        supabase = get_supabase()
        result = supabase.table('usuarios').select('username').execute()
        print(f"✅ Conectado! {len(result.data)} usuários no banco")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_users():
    """Testa se usuários existem"""
    print("\n👤 Testando usuários...")
    try:
        from models.user import User
        
        test_users = ['admin', 'gerencia', 'recepcao103']
        
        for username in test_users:
            user = User.find_by_username(username)
            if user:
                password_ok = user.check_password('123456')
                status = "✅" if password_ok else "❌"
                print(f"   {status} {username}: {'Login OK' if password_ok else 'Senha incorreta'}")
            else:
                print(f"   ❌ {username}: Não encontrado")
                
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_backend():
    """Testa se backend responde"""
    print("\n🌐 Testando backend...")
    try:
        import requests
        response = requests.get('http://localhost:5001/api/health', timeout=2)
        if response.status_code == 200:
            print("✅ Backend respondendo")
            return True
        else:
            print(f"❌ Backend erro {response.status_code}")
            return False
    except:
        print("❌ Backend não está rodando")
        return False

if __name__ == '__main__':
    print("🧪 Teste Rápido do Sistema")
    print("=" * 30)
    
    if test_connection():
        test_users()
    
    test_backend()
    
    print("\n" + "=" * 30)
    print("🎯 Se todos os testes passaram, o sistema está pronto!")
    print("🔑 Use: admin / 123456 para fazer login")