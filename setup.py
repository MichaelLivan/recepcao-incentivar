#!/usr/bin/env python3
"""
Script de configuração inicial do Reception Sync
Execute este script para configurar o sistema pela primeira vez
"""

import os
import sys
import subprocess

def check_python_version():
    """Verifica se a versão do Python é adequada"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        return False
    print(f"✅ Python {sys.version.split()[0]} OK")
    return True

def install_dependencies():
    """Instala as dependências Python"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def create_env_file():
    """Cria arquivo .env se não existir"""
    if not os.path.exists('.env'):
        print("📝 Criando arquivo .env...")
        
        # Perguntar dados do Supabase
        print("\n🔧 Configuração do Supabase:")
        supabase_url = input("URL do Supabase (ou ENTER para usar padrão): ").strip()
        if not supabase_url:
            supabase_url = "https://dzufdkejujyhvtlyvors.supabase.co"
        
        supabase_key = input("Chave anon do Supabase: ").strip()
        if not supabase_key:
            print("⚠️ Usando chave placeholder - configure depois!")
            supabase_key = "your-supabase-anon-key"
        
        env_content = f"""# Configurações do Supabase
SUPABASE_URL={supabase_url}
SUPABASE_KEY={supabase_key}

# JWT Secret (mude em produção)
JWT_SECRET_KEY=your-very-secret-jwt-key-change-in-production-{os.urandom(8).hex()}

# Configurações de desenvolvimento
FLASK_ENV=development
FLASK_DEBUG=True
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ Arquivo .env criado")
    else:
        print("✅ Arquivo .env já existe")

def test_supabase_connection():
    """Testa conexão com Supabase"""
    print("🔌 Testando conexão com Supabase...")
    try:
        from database import test_connection
        if test_connection():
            print("✅ Conexão com Supabase OK")
            return True
        else:
            print("❌ Erro na conexão com Supabase")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar Supabase: {e}")
        return False

def setup_database():
    """Configura o banco de dados"""
    print("🗄️ Configurando banco de dados...")
    try:
        from fix_passwords import fix_user_passwords
        fix_user_passwords()
        print("✅ Banco de dados configurado")
        return True
    except Exception as e:
        print(f"❌ Erro ao configurar banco: {e}")
        return False

def main():
    """Função principal de setup"""
    print("🚀 Reception Sync - Setup Inicial")
    print("=" * 40)
    
    steps = [
        ("Verificando Python", check_python_version),
        ("Instalando dependências", install_dependencies),
        ("Criando arquivo .env", create_env_file),
        ("Testando Supabase", test_supabase_connection),
        ("Configurando banco", setup_database)
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"❌ Falha em: {step_name}")
            print("🛑 Setup interrompido")
            return False
    
    print("\n" + "=" * 40)
    print("🎉 Setup concluído com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Configure o arquivo .env com suas credenciais do Supabase")
    print("2. Execute: python app.py")
    print("3. Execute o frontend: npm run dev")
    print("\n🔑 Credenciais de teste:")
    print("Username: gerencia | Senha: 123456")
    print("Email: gerencia@incentivar.com | Senha: 123456")
    
    return True

if __name__ == '__main__':
    main()