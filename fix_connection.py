#!/usr/bin/env python3
"""
Script automático para diagnosticar e corrigir problemas de conexão
"""

import os
import sys
import socket
import requests
import subprocess
import time
from urllib.parse import urlparse

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔧 {title}")
    print('='*60)

def print_step(step, description):
    print(f"\n{step}. {description}")
    print("-" * 40)

def test_basic_connectivity():
    """Testa conectividade básica"""
    print_step("1", "TESTANDO CONECTIVIDADE BÁSICA")
    
    # Teste DNS
    try:
        socket.gethostbyname('google.com')
        print("✅ DNS funcionando")
    except Exception as e:
        print(f"❌ Problema com DNS: {e}")
        print("💡 Solução: Verificar conexão de internet ou usar DNS público (8.8.8.8)")
        return False
    
    # Teste HTTP
    try:
        response = requests.get('https://httpbin.org/status/200', timeout=10)
        print("✅ HTTP funcionando")
    except Exception as e:
        print(f"❌ Problema com HTTP: {e}")
        print("💡 Solução: Verificar firewall ou proxy")
        return False
    
    return True

def check_environment_variables():
    """Verifica e corrige variáveis de ambiente"""
    print_step("2", "VERIFICANDO VARIÁVEIS DE AMBIENTE")
    
    required_vars = {
        'SUPABASE_URL': 'URL do Supabase (https://xxx.supabase.co)',
        'SUPABASE_KEY': 'Chave do Supabase (eyJ...)'
    }
    
    missing_vars = []
    invalid_vars = []
    
    for var, description in required_vars.items():
        value = os.environ.get(var)
        
        if not value:
            missing_vars.append(var)
            print(f"❌ {var} não definida")
        else:
            print(f"✅ {var} definida: {value[:30]}...")
            
            # Validações específicas
            if var == 'SUPABASE_URL':
                if not value.startswith('https://') or '.supabase.co' not in value:
                    invalid_vars.append(var)
                    print(f"   ⚠️ URL inválida: deve ser https://xxx.supabase.co")
            
            elif var == 'SUPABASE_KEY':
                if len(value) < 50:
                    invalid_vars.append(var)
                    print(f"   ⚠️ Chave muito curta: deve ter pelo menos 50 caracteres")
    
    if missing_vars or invalid_vars:
        print(f"\n💡 AÇÃO NECESSÁRIA:")
        print("1. Crie/edite o arquivo .env na raiz do projeto")
        print("2. Adicione as variáveis corretas:")
        for var in missing_vars + invalid_vars:
            print(f"   {var}=sua_credencial_aqui")
        print("3. Reinicie o servidor")
        return False
    
    return True

def test_supabase_dns():
    """Testa DNS específico do Supabase"""
    print_step("3", "TESTANDO DNS DO SUPABASE")
    
    url = os.environ.get('SUPABASE_URL')
    if not url:
        print("❌ SUPABASE_URL não definida")
        return False
    
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        ip = socket.gethostbyname(hostname)
        print(f"✅ DNS resolvido: {hostname} -> {ip}")
        return True
    except Exception as e:
        print(f"❌ Erro DNS: {e}")
        print("💡 Soluções:")
        print("   - Tentar DNS público: 8.8.8.8 ou 1.1.1.1")
        print("   - Verificar firewall/proxy corporativo")
        print("   - Testar em rede diferente")
        return False

def test_supabase_connection():
    """Testa conexão completa com Supabase"""
    print_step("4", "TESTANDO CONEXÃO COM SUPABASE")
    
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_KEY')
    
    if not url or not key:
        print("❌ Credenciais incompletas")
        return False
    
    try:
        headers = {
            'apikey': key,
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
        
        print(f"🔗 Conectando a {url}...")
        response = requests.get(f"{url}/rest/v1/", headers=headers, timeout=30)
        
        if response.status_code == 200:
            print("✅ Conexão com Supabase OK")
            return True
        else:
            print(f"❌ Status inesperado: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
            if response.status_code == 401:
                print("💡 Erro de autenticação - verificar SUPABASE_KEY")
            elif response.status_code == 404:
                print("💡 Projeto não encontrado - verificar SUPABASE_URL")
            
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout na conexão")
        print("💡 Soluções:")
        print("   - Verificar conexão de internet")
        print("   - Tentar VPN")
        print("   - Aumentar timeout")
        return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def test_database_tables():
    """Testa acesso às tabelas do banco"""
    print_step("5", "TESTANDO ACESSO ÀS TABELAS")
    
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_KEY')
    
    if not url or not key:
        print("❌ Credenciais não disponíveis")
        return False
    
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }
    
    critical_tables = ['usuarios', 'salas', 'orcamentos']
    
    for table in critical_tables:
        try:
            print(f"📋 Testando tabela '{table}'...")
            response = requests.get(
                f"{url}/rest/v1/{table}?select=*&limit=1",
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ OK - {len(data)} registro(s)")
            else:
                print(f"   ❌ Erro {response.status_code}: {response.text[:100]}")
                
                if 'permission denied' in response.text.lower():
                    print("   💡 Problema de permissão - verificar RLS")
                
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    return True

def create_env_file():
    """Cria arquivo .env se não existir"""
    if not os.path.exists('.env'):
        print("\n📝 Criando arquivo .env...")
        
        env_content = """# Configurações do Reception Sync
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_anon_aqui
SECRET_KEY=chave-secreta-forte
JWT_SECRET_KEY=jwt-chave-secreta-forte
FLASK_ENV=development
PORT=5001
HOST=0.0.0.0
CORS_ORIGINS=http://localhost:3000
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ Arquivo .env criado!")
        print("⚠️ EDITE O ARQUIVO COM SUAS CREDENCIAIS REAIS")
        return False
    
    return True

def suggest_solutions():
    """Sugere soluções baseadas nos problemas encontrados"""
    print_step("6", "SOLUÇÕES RECOMENDADAS")
    
    print("🏥 SOLUÇÕES GERAIS:")
    print()
    print("1. PROBLEMAS DE REDE:")
    print("   • Tentar em rede diferente (dados móveis)")
    print("   • Usar VPN se disponível")
    print("   • Configurar DNS público: 8.8.8.8")
    print()
    print("2. PROBLEMAS DE FIREWALL:")
    print("   • Permitir conexões HTTPS na porta 443")
    print("   • Whitelist: *.supabase.co")
    print("   • Verificar proxy corporativo")
    print()
    print("3. PROBLEMAS DE CREDENCIAIS:")
    print("   • Regenerar chaves no dashboard Supabase")
    print("   • Verificar se projeto está ativo")
    print("   • Confirmar URL do projeto")
    print()
    print("4. PROBLEMAS DE CONFIGURAÇÃO:")
    print("   • Verificar RLS (Row Level Security)")
    print("   • Confirmar políticas de acesso")
    print("   • Testar com service_role_key temporariamente")

def run_fixes():
    """Executa correções automáticas"""
    print_step("7", "EXECUTANDO CORREÇÕES AUTOMÁTICAS")
    
    fixes_applied = []
    
    # Fix 1: Criar .env se não existir
    if create_env_file():
        fixes_applied.append("Arquivo .env verificado")
    else:
        fixes_applied.append("Arquivo .env criado (EDITAR NECESSÁRIO)")
    
    # Fix 2: Instalar dependências se necessário
    try:
        import supabase
        fixes_applied.append("Biblioteca supabase disponível")
    except ImportError:
        print("📦 Instalando biblioteca supabase...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "supabase"])
        fixes_applied.append("Biblioteca supabase instalada")
    
    # Fix 3: Testar variáveis após load
    try:
        from dotenv import load_dotenv
        load_dotenv()
        fixes_applied.append("Variáveis de ambiente carregadas")
    except:
        print("📦 Instalando python-dotenv...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
        fixes_applied.append("python-dotenv instalado")
    
    print("\n✅ CORREÇÕES APLICADAS:")
    for fix in fixes_applied:
        print(f"   • {fix}")

def main():
    """Função principal de diagnóstico"""
    print_header("DIAGNÓSTICO E CORREÇÃO DE PROBLEMAS DE CONEXÃO")
    
    print("🚀 Iniciando diagnóstico completo...")
    print("⏱️ Este processo pode levar alguns minutos...")
    
    # Executar testes em sequência
    tests = [
        ("Conectividade Básica", test_basic_connectivity),
        ("Variáveis de Ambiente", check_environment_variables),
        ("DNS do Supabase", test_supabase_dns),
        ("Conexão Supabase", test_supabase_connection),
        ("Acesso às Tabelas", test_database_tables)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Executando: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            results.append((test_name, False))
    
    # Resumo dos resultados
    print_header("RESUMO DOS TESTES")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"📊 Resultados: {passed}/{total} testes passaram")
    print()
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"   {status} - {test_name}")
    
    # Aplicar correções se necessário
    if passed < total:
        print(f"\n🔧 {total - passed} problema(s) detectado(s)")
        run_fixes()
        suggest_solutions()
    else:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema está pronto para uso")
    
    print_header("PRÓXIMOS PASSOS")
    
    if passed < total:
        print("1. Revisar e aplicar as soluções sugeridas")
        print("2. Editar o arquivo .env com credenciais corretas")
        print("3. Executar este script novamente")
        print("4. Reiniciar o servidor após as correções")
    else:
        print("1. Executar: python app.py")
        print("2. Acessar: http://localhost:5001/api/health")
        print("3. Testar login na aplicação")
    
    print("\n📞 Se problemas persistirem:")
    print("   • Verificar logs do Supabase")
    print("   • Testar em ambiente/rede diferente")
    print("   • Contatar suporte técnico")

if __name__ == "__main__":
    main()