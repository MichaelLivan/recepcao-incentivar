#!/usr/bin/env python3
"""
Script para corrigir o arquivo .env com as credenciais corretas do Supabase
"""

import os

def check_current_env():
    """Verifica o arquivo .env atual"""
    print("📁 Verificando arquivo .env atual...")
    
    if not os.path.exists('.env'):
        print("❌ Arquivo .env não encontrado")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
    
    print("📄 Conteúdo atual do .env:")
    print("-" * 30)
    print(content)
    print("-" * 30)
    
    return True

def fix_env_file():
    """Corrige o arquivo .env com as credenciais corretas"""
    print("\n🔧 Configurando arquivo .env...")
    
    # Como você está acessando o Supabase Dashboard, sabemos que a URL está correta
    SUPABASE_URL = "https://dzufdkejujyhvtlyvors.supabase.co"
    
    print(f"📡 URL do Supabase: {SUPABASE_URL}")
    print("\n🔑 Agora precisamos da sua chave de API:")
    print("1. Vá para: https://supabase.com/dashboard/project/dzufdkejujyhvtlyvors/settings/api")
    print("2. Copie a chave 'anon public'")
    print("3. Cole aqui:")
    
    supabase_key = input("\nSUPABASE_KEY: ").strip()
    
    if not supabase_key or supabase_key == "your-supabase-anon-key":
        print("❌ Chave inválida. Tente novamente.")
        return False
    
    # Criar novo arquivo .env
    env_content = f"""# Configurações do Supabase
SUPABASE_URL={SUPABASE_URL}
SUPABASE_KEY={supabase_key}

# JWT Secret (mude em produção)
JWT_SECRET_KEY=reception-sync-secret-key-{os.urandom(8).hex()}

# Configurações de desenvolvimento
FLASK_ENV=development
FLASK_DEBUG=True
"""
    
    # Backup do arquivo antigo
    if os.path.exists('.env'):
        with open('.env.backup', 'w') as f:
            with open('.env', 'r') as old_f:
                f.write(old_f.read())
        print("💾 Backup criado: .env.backup")
    
    # Escrever novo arquivo
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Arquivo .env atualizado!")
    return True

def test_new_connection():
    """Testa a nova conexão"""
    print("\n🧪 Testando nova conexão...")
    try:
        # Recarregar variáveis de ambiente
        from dotenv import load_dotenv
        load_dotenv(override=True)
        
        # Forçar recriação do cliente Supabase
        import database
        database._supabase_client = None
        
        # Testar conexão
        supabase = database.get_supabase()
        result = supabase.table('usuarios').select('username').execute()
        
        print(f"✅ Conexão funcionando! {len(result.data)} usuários encontrados")
        
        # Mostrar usuários
        for user in result.data:
            print(f"   👤 {user['username']}")
        
        return True
    except Exception as e:
        print(f"❌ Ainda com erro: {e}")
        return False

def main():
    """Função principal"""
    print("🔧 Correção do Arquivo .env - Reception Sync")
    print("=" * 50)
    
    # Verificar arquivo atual
    check_current_env()
    
    # Corrigir arquivo
    if fix_env_file():
        # Testar nova conexão
        if test_new_connection():
            print("\n🎉 SUCESSO! Configuração corrigida!")
            print("\n🚀 Próximos passos:")
            print("1. Execute: python app.py")
            print("2. Acesse: http://localhost:3000")
            print("3. Login: admin / 123456")
        else:
            print("\n⚠️ Conexão ainda não funciona")
            print("Verifique se a chave está correta")
    else:
        print("❌ Erro na configuração")

if __name__ == '__main__':
    main()