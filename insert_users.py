#!/usr/bin/env python3
"""
Script para inserir usuários iniciais no banco de dados
Execute este script para criar os usuários necessários
"""

from database import get_supabase
from werkzeug.security import generate_password_hash
import traceback

def insert_initial_users():
    """Insere os usuários iniciais no banco de dados"""
    
    print("👥 Inserindo usuários iniciais no banco...")
    print("=" * 50)
    
    # Lista de usuários para criar
    users_to_create = [
        {
            'username': 'gerencia',
            'email': 'gerencia@incentivar.com',
            'password': '123456',
            'role': 'admin',
            'recepcao_id': None,
            'recepcao_nome': None
        },
        {
            'username': 'admin',
            'email': 'admin@incentivar.com',
            'password': '123456',
            'role': 'admin',
            'recepcao_id': None,
            'recepcao_nome': None
        },
        {
            'username': 'admpodd',
            'email': 'admpodd@incentivar.com',
            'password': '123456',
            'role': 'admin',
            'recepcao_id': None,
            'recepcao_nome': None
        },
        {
            'username': 'admpdg',
            'email': 'admpdg@incentivar.com',
            'password': '123456',
            'role': 'admin',
            'recepcao_id': None,
            'recepcao_nome': None
        },
        {
            'username': 'recepcao103',
            'email': 'recepcao103@incentivar.com',
            'password': '123456',
            'role': 'recepcao',
            'recepcao_id': '103',
            'recepcao_nome': 'Recepção 103'
        },
        {
            'username': 'recepcao108',
            'email': 'recepcao108@incentivar.com',
            'password': '123456',
            'role': 'recepcao',
            'recepcao_id': '108',
            'recepcao_nome': 'Recepção 108'
        },
        {
            'username': 'recepcao203',
            'email': 'recepcao203@incentivar.com',
            'password': '123456',
            'role': 'recepcao',
            'recepcao_id': '203',
            'recepcao_nome': 'Recepção 203'
        },
        {
            'username': 'recepcao808',
            'email': 'recepcao808@incentivar.com',
            'password': '123456',
            'role': 'recepcao',
            'recepcao_id': '808',
            'recepcao_nome': 'Recepção 808'
        },
        {
            'username': 'recepcao1002',
            'email': 'recepcao1002@incentivar.com',
            'password': '123456',
            'role': 'recepcao',
            'recepcao_id': '1002',
            'recepcao_nome': 'Recepção 1002'
        },
        {
            'username': 'recepcao1009',
            'email': 'recepcao1009@incentivar.com',
            'password': '123456',
            'role': 'recepcao',
            'recepcao_id': '1009',
            'recepcao_nome': 'Recepção 1009'
        },
        {
            'username': 'recepcao1108',
            'email': 'recepcao1108@incentivar.com',
            'password': '123456',
            'role': 'recepcao',
            'recepcao_id': '1108',
            'recepcao_nome': 'Recepção 1108'
        }
    ]
    
    try:
        supabase = get_supabase()
        
        # Verificar se já existem usuários
        existing_users = supabase.table('usuarios').select('username').execute()
        existing_usernames = [user['username'] for user in existing_users.data]
        
        print(f"📊 Usuários existentes no banco: {len(existing_usernames)}")
        if existing_usernames:
            print(f"   Usuários: {', '.join(existing_usernames)}")
        
        created_count = 0
        skipped_count = 0
        
        for user_data in users_to_create:
            username = user_data['username']
            
            # Verificar se usuário já existe
            if username in existing_usernames:
                print(f"⏭️ Usuário '{username}' já existe - pulando")
                skipped_count += 1
                continue
            
            try:
                # Gerar hash da senha
                password_hash = generate_password_hash(user_data['password'])
                
                # Preparar dados para inserção
                insert_data = {
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'password_hash': password_hash,
                    'role': user_data['role'],
                    'recepcao_id': user_data['recepcao_id'],
                    'recepcao_nome': user_data['recepcao_nome'],
                    'ativo': True
                }
                
                # Inserir no banco
                result = supabase.table('usuarios').insert(insert_data).execute()
                
                if result.data:
                    print(f"✅ Usuário '{username}' criado com sucesso")
                    created_count += 1
                else:
                    print(f"❌ Erro ao criar usuário '{username}' - sem dados retornados")
                    
            except Exception as e:
                print(f"❌ Erro ao criar usuário '{username}': {e}")
        
        print("\n" + "=" * 50)
        print(f"📊 Resumo:")
        print(f"   ✅ Criados: {created_count}")
        print(f"   ⏭️ Já existiam: {skipped_count}")
        print(f"   📊 Total no banco: {len(existing_usernames) + created_count}")
        
        # Verificar usuários finais
        final_users = supabase.table('usuarios').select('username, email, role, ativo').execute()
        print(f"\n👥 Usuários no banco ({len(final_users.data)}):")
        for user in final_users.data:
            status = "🟢" if user['ativo'] else "🔴"
            role_emoji = "👑" if user['role'] == 'admin' else "📋"
            print(f"   {status} {role_emoji} {user['username']} ({user['email']})")
        
        print(f"\n🔑 Credenciais de teste:")
        print(f"   Username: gerencia | Senha: 123456")
        print(f"   Username: admin | Senha: 123456")
        print(f"   Username: recepcao103 | Senha: 123456")
        
        return True
        
    except Exception as e:
        print(f"💥 ERRO GERAL: {e}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        return False

def test_user_login(username, password):
    """Testa o login de um usuário específico"""
    try:
        print(f"\n🧪 Testando login: {username}")
        
        from models.user import User
        user = User.find_by_username(username)
        
        if user:
            print(f"   ✅ Usuário encontrado: {user.username}")
            print(f"   📧 Email: {user.email}")
            print(f"   👤 Role: {user.role}")
            print(f"   🏢 Recepção: {user.recepcao_nome or 'Admin'}")
            
            if user.check_password(password):
                print(f"   🔐 Senha correta!")
                return True
            else:
                print(f"   ❌ Senha incorreta")
                return False
        else:
            print(f"   ❌ Usuário não encontrado")
            return False
            
    except Exception as e:
        print(f"   💥 Erro no teste: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Reception Sync - Inserção de Usuários")
    print("=" * 50)
    
    # Testar conexão primeiro
    try:
        supabase = get_supabase()
        print("✅ Conexão com Supabase OK")
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        print("💡 Verifique o arquivo .env e as credenciais do Supabase")
        return False
    
    # Inserir usuários
    if insert_initial_users():
        print("\n🎉 Usuários inseridos com sucesso!")
        
        # Testar alguns logins
        print("\n" + "=" * 50)
        print("🧪 Testando logins...")
        
        test_users = ['gerencia', 'admin', 'recepcao103']
        success_count = 0
        
        for username in test_users:
            if test_user_login(username, '123456'):
                success_count += 1
        
        print(f"\n📊 Testes de login: {success_count}/{len(test_users)} sucessos")
        
        if success_count == len(test_users):
            print("🎉 Todos os logins funcionaram!")
            print("\n🚀 Sistema pronto para uso!")
            print("   Frontend: http://localhost:3000")
            print("   Backend: http://localhost:5001")
        else:
            print("⚠️ Alguns logins falharam - verifique os erros acima")
        
        return True
    else:
        print("❌ Erro ao inserir usuários")
        return False

if __name__ == '__main__':
    main()