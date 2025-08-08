#!/usr/bin/env python3
"""
Script de configuração inicial do sistema
Execute: python setup_system.py
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é adequada"""
    print("🐍 Verificando versão do Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ é necessário")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_env_file():
    """Verifica e cria arquivo .env se necessário"""
    print("\n📄 Verificando arquivo .env...")
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_file.exists():
        if env_example.exists():
            print("⚠️ Arquivo .env não encontrado, copiando de .env.example...")
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ Arquivo .env criado")
        else:
            print("❌ Nem .env nem .env.example encontrados")
            create_basic_env()
    else:
        print("✅ Arquivo .env existe")
    
    # Verificar se as variáveis essenciais estão definidas
    check_env_variables()

def create_basic_env():
    """Cria um arquivo .env básico"""
    print("🔧 Criando arquivo .env básico...")
    
    env_content = """# Configurações do Supabase
SUPABASE_URL=https://dzufdkejujyhvtlyvors.supabase.co
SUPABASE_KEY=SUA_CHAVE_AQUI

# Configurações do JWT
JWT_SECRET_KEY=sua-chave-secreta-aqui-mude-em-producao

# Configurações do Flask
FLASK_ENV=development
FLASK_DEBUG=True
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Arquivo .env criado")
    print("⚠️ IMPORTANTE: Configure suas chaves do Supabase no arquivo .env")

def check_env_variables():
    """Verifica se as variáveis de ambiente estão configuradas"""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['SUPABASE_URL', 'SUPABASE_KEY', 'JWT_SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value == 'SUA_CHAVE_AQUI' or 'sua-chave' in value.lower():
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Variáveis não configuradas: {', '.join(missing_vars)}")
        print("   Configure essas variáveis no arquivo .env")
        return False
    else:
        print("✅ Variáveis de ambiente configuradas")
        return True

def install_dependencies():
    """Instala dependências Python"""
    print("\n📦 Verificando dependências...")
    
    requirements_file = Path('requirements.txt')
    
    if not requirements_file.exists():
        print("⚠️ requirements.txt não encontrado, criando...")
        create_requirements_file()
    
    print("🔧 Instalando dependências...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependências instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        print("💡 Tente executar manualmente: pip install -r requirements.txt")
        return False

def create_requirements_file():
    """Cria arquivo requirements.txt"""
    requirements = """flask==2.3.3
flask-jwt-extended==4.5.3
flask-cors==4.0.0
supabase==1.0.4
python-dotenv==1.0.0
werkzeug==2.3.7
requests==2.31.0
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("✅ requirements.txt criado")

def test_database_connection():
    """Testa conexão com banco de dados"""
    print("\n🗄️ Testando conexão com banco...")
    
    try:
        from database import test_supabase_connection
        if test_supabase_connection():
            print("✅ Conexão com banco OK")
            return True
        else:
            print("❌ Falha na conexão com banco")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar banco: {str(e)}")
        return False

def create_test_users():
    """Cria usuários de teste"""
    print("\n👥 Criando usuários de teste...")
    
    try:
        from create_test_users import create_test_users as create_users
        create_users()
        return True
    except Exception as e:
        print(f"❌ Erro ao criar usuários: {str(e)}")
        return False

def run_debug_tests():
    """Executa testes de debug"""
    print("\n🔍 Executando testes de diagnóstico...")
    
    try:
        from debug_system import main as debug_main
        debug_main()
        return True
    except Exception as e:
        print(f"❌ Erro nos testes: {str(e)}")
        return False

def start_backend():
    """Inicia o backend Flask"""
    print("\n🚀 Iniciando backend...")
    print("💡 Para parar o servidor, pressione Ctrl+C")
    print("🌐 Frontend: Abra outro terminal e execute 'npm run dev'")
    print("=" * 50)
    
    try:
        import app
        app.app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Backend parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar backend: {str(e)}")

def main():
    print("🎯 CONFIGURAÇÃO INICIAL DO SISTEMA")
    print("=" * 50)
    
    steps_completed = 0
    total_steps = 6
    
    # 1. Verificar Python
    if check_python_version():
        steps_completed += 1
    else:
        print("❌ Configure Python 3.8+ e execute novamente")
        return
    
    # 2. Verificar arquivo .env
    check_env_file()
    steps_completed += 1
    
    # 3. Instalar dependências
    if install_dependencies():
        steps_completed += 1
    else:
        print("❌ Instale as dependências manualmente e execute novamente")
        return
    
    # 4. Testar banco
    if test_database_connection():
        steps_completed += 1
    else:
        print("❌ Configure as credenciais do Supabase no .env")
        return
    
    # 5. Criar usuários
    if create_test_users():
        steps_completed += 1
    
    # 6. Executar testes
    run_debug_tests()
    steps_completed += 1
    
    print(f"\n✅ Configuração completa! ({steps_completed}/{total_steps} etapas)")
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("1. Backend: python app.py")
    print("2. Frontend: npm run dev (em outro terminal)")
    print("3. Login: admin / 123456 ou gerencia@incentivar.com / 123456")
    
    # Perguntar se quer iniciar o backend
    response = input("\n🚀 Iniciar backend agora? (s/n): ")
    if response.lower() in ['s', 'sim', 'y', 'yes']:
        start_backend()

if __name__ == "__main__":
    main()