#!/usr/bin/env python3
"""
Script para corrigir o carregamento das variáveis de ambiente
"""

import os
import sys

def fix_env_loading():
    """Corrige o carregamento do arquivo .env"""
    print("🔧 CORRIGINDO CARREGAMENTO DO ARQUIVO .env")
    print("=" * 50)
    
    # Verificar se arquivo .env existe
    env_file_path = '.env'
    if not os.path.exists(env_file_path):
        print("❌ Arquivo .env não encontrado no diretório atual")
        print(f"📁 Diretório atual: {os.getcwd()}")
        return False
    
    print(f"✅ Arquivo .env encontrado: {os.path.abspath(env_file_path)}")
    
    # Verificar conteúdo do arquivo .env
    try:
        with open(env_file_path, 'r') as f:
            content = f.read()
        
        print(f"📄 Tamanho do arquivo: {len(content)} caracteres")
        
        # Verificar se contém as variáveis necessárias
        has_url = 'SUPABASE_URL' in content
        has_key = 'SUPABASE_KEY' in content
        
        print(f"🔍 SUPABASE_URL presente: {'✅' if has_url else '❌'}")
        print(f"🔍 SUPABASE_KEY presente: {'✅' if has_key else '❌'}")
        
        if not has_url or not has_key:
            print("❌ Variáveis necessárias não encontradas no .env")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao ler arquivo .env: {e}")
        return False
    
    # Instalar python-dotenv se necessário
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv já instalado")
    except ImportError:
        print("📦 Instalando python-dotenv...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
        from dotenv import load_dotenv
        print("✅ python-dotenv instalado com sucesso")
    
    # Carregar variáveis de ambiente
    print("\n🔄 Carregando variáveis de ambiente...")
    load_dotenv(override=True)
    
    # Verificar se as variáveis foram carregadas
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_KEY')
    
    print(f"🔍 SUPABASE_URL carregada: {'✅' if url else '❌'}")
    if url:
        print(f"   Valor: {url}")
    
    print(f"🔍 SUPABASE_KEY carregada: {'✅' if key else '❌'}")
    if key:
        print(f"   Valor: {key[:50]}...")
    
    if url and key:
        print("\n🎉 VARIÁVEIS CARREGADAS COM SUCESSO!")
        return True
    else:
        print("\n❌ Falha ao carregar variáveis")
        return False

def test_supabase_connection():
    """Testa a conexão com Supabase após carregar variáveis"""
    print("\n🧪 TESTANDO CONEXÃO COM SUPABASE")
    print("=" * 50)
    
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_KEY')
    
    if not url or not key:
        print("❌ Variáveis não carregadas")
        return False
    
    try:
        import requests
        
        headers = {
            'apikey': key,
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        
        print(f"🔗 Testando conexão com {url}...")
        response = requests.get(f"{url}/rest/v1/", headers=headers, timeout=30)
        
        if response.status_code == 200:
            print("✅ Conexão com Supabase OK!")
            
            # Testar tabela específica
            print("📋 Testando acesso à tabela 'usuarios'...")
            users_response = requests.get(
                f"{url}/rest/v1/usuarios?select=username&limit=1",
                headers=headers,
                timeout=15
            )
            
            if users_response.status_code == 200:
                users = users_response.json()
                print(f"✅ Tabela 'usuarios' acessível - {len(users)} registro(s)")
                return True
            else:
                print(f"❌ Erro ao acessar tabela: {users_response.status_code}")
                return False
                
        else:
            print(f"❌ Erro na conexão: Status {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar conexão: {e}")
        return False

def update_app_py():
    """Atualiza app.py para garantir que .env seja carregado"""
    print("\n📝 ATUALIZANDO APP.PY")
    print("=" * 50)
    
    app_py_path = 'app.py'
    if not os.path.exists(app_py_path):
        print("❌ app.py não encontrado")
        return False
    
    try:
        with open(app_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar se já tem load_dotenv
        if 'load_dotenv' in content:
            print("✅ load_dotenv já presente no app.py")
            return True
        
        # Adicionar load_dotenv no início
        lines = content.split('\n')
        
        # Encontrar onde inserir
        insert_index = 0
        for i, line in enumerate(lines):
            if line.startswith('from') or line.startswith('import'):
                continue
            else:
                insert_index = i
                break
        
        # Inserir as linhas necessárias
        new_lines = (
            lines[:insert_index] +
            ['# Carregar variáveis de ambiente'] +
            ['from dotenv import load_dotenv'] +
            ['load_dotenv()'] +
            [''] +
            lines[insert_index:]
        )
        
        # Salvar arquivo
        new_content = '\n'.join(new_lines)
        with open(app_py_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ app.py atualizado com load_dotenv()")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar app.py: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 CORREÇÃO DO CARREGAMENTO DE VARIÁVEIS DE AMBIENTE")
    print("=" * 60)
    
    # Etapa 1: Corrigir carregamento do .env
    if not fix_env_loading():
        print("\n❌ Falha ao corrigir carregamento do .env")
        return
    
    # Etapa 2: Testar conexão
    if not test_supabase_connection():
        print("\n❌ Falha no teste de conexão")
        return
    
    # Etapa 3: Atualizar app.py
    update_app_py()
    
    print("\n" + "=" * 60)
    print("🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    
    print("\n✅ PRÓXIMOS PASSOS:")
    print("1. Execute: python app.py")
    print("2. Acesse: http://localhost:5001/api/health")
    print("3. Teste o login na aplicação")
    
    print("\n📋 CREDENCIAIS DE TESTE:")
    print("Username: gerencia")
    print("Password: 123456")

if __name__ == "__main__":
    main()