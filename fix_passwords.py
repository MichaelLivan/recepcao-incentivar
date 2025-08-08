#!/usr/bin/env python3
"""
Script para corrigir as senhas dos usuários no banco de dados
Execute este script depois de configurar o Supabase
"""

from werkzeug.security import generate_password_hash
from database import get_supabase

def fix_user_passwords():
    """Corrige as senhas dos usuários no banco"""
    
    # Usuários e suas senhas
    users_passwords = {
        'gerencia': '123456',
        'admpodd': '123456', 
        'admpdg': '123456',
        'admaba': '123456',
        'recepcao103': '123456',
        'recepcao108': '123456', 
        'recepcao203': '123456',
        'recepcao808': '123456',
        'recepcao1002': '123456',
        'recepcao1009': '123456',
        'recepcao1108': '123456'
    }
    
    print("🔐 Corrigindo senhas dos usuários...")
    print("=" * 50)
    
    try:
        supabase = get_supabase()
        
        # Primeiro, verificar se o usuário 'gerencia' existe, se não, criar
        try:
            existing_gerencia = supabase.table('usuarios').select('*').eq('username', 'gerencia').execute()
            if not existing_gerencia.data:
                print("👤 Criando usuário 'gerencia'...")
                gerencia_hash = generate_password_hash('123456')
                supabase.table('usuarios').insert({
                    'username': 'gerencia',
                    'email': 'gerencia@incentivar.com',
                    'password_hash': gerencia_hash,
                    'role': 'admin',
                    'ativo': True
                }).execute()
                print("✅ Usuário 'gerencia' criado")
        except Exception as e:
            print(f"⚠️ Erro ao verificar/criar gerencia: {e}")
        
        # Atualizar senhas de todos os usuários
        for username, password in users_passwords.items():
            try:
                # Gerar hash da senha
                password_hash = generate_password_hash(password)
                
                print(f"🔄 Atualizando senha para: {username}")
                
                # Verificar se usuário existe
                user_check = supabase.table('usuarios').select('id, username').eq('username', username).execute()
                
                if user_check.data:
                    # Atualizar senha
                    result = supabase.table('usuarios').update({
                        'password_hash': password_hash
                    }).eq('username', username).execute()
                    
                    if result.data:
                        print(f"✅ Senha atualizada para: {username}")
                    else:
                        print(f"❌ Erro ao atualizar senha para: {username}")
                else:
                    print(f"⚠️ Usuário não encontrado: {username}")
                    
            except Exception as e:
                print(f"❌ Erro ao processar {username}: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 Processo de correção de senhas concluído!")
        print("\n📋 Credenciais de teste:")
        print("Username: gerencia | Senha: 123456")
        print("Email: gerencia@incentivar.com | Senha: 123456")
        print("\nOutros usuários também têm senha: 123456")
        
        # Verificar usuários finais
        print("\n👥 Verificando usuários no banco:")
        all_users = supabase.table('usuarios').select('username, email, role, ativo').execute()
        for user in all_users.data:
            status = "🟢 Ativo" if user['ativo'] else "🔴 Inativo"
            print(f"  {status} {user['username']} ({user['email']}) - {user['role']}")
            
    except Exception as e:
        print(f"💥 ERRO GERAL: {e}")
        print("Verifique se o Supabase está configurado corretamente")

def test_login(username, password):
    """Testa o login de um usuário"""
    try:
        from models.user import User
        print(f"\n🧪 Testando login: {username}")
        
        user = User.find_by_username(username)
        if user:
            if user.check_password(password):
                print(f"✅ Login OK para {username}")
                return True
            else:
                print(f"❌ Senha incorreta para {username}")
        else:
            print(f"❌ Usuário {username} não encontrado")
        return False
    except Exception as e:
        print(f"❌ Erro no teste de login: {e}")
        return False

if __name__ == '__main__':
    # Corrigir senhas
    fix_user_passwords()
    
    # Testar alguns logins
    print("\n" + "=" * 50)
    print("🧪 Testando logins...")
    test_login('gerencia', '123456')
    test_login('recepcao103', '123456')
    test_login('admpodd', '123456')