#!/usr/bin/env python3
"""
Script de diagnóstico para problemas de conexão com banco de dados
"""

import os
import socket
import requests
import time
from urllib.parse import urlparse

def test_network_connectivity():
    """Testa conectividade básica de rede"""
    print("🔍 DIAGNÓSTICO DE CONECTIVIDADE")
    print("=" * 50)
    
    # Teste 1: DNS básico
    try:
        print("1. Testando DNS para google.com...")
        socket.gethostbyname('google.com')
        print("   ✅ DNS funcionando")
    except socket.gaierror as e:
        print(f"   ❌ Erro de DNS: {e}")
        return False
    
    # Teste 2: Conectividade HTTP
    try:
        print("2. Testando HTTP para google.com...")
        response = requests.get('https://www.google.com', timeout=10)
        print(f"   ✅ HTTP funcionando (Status: {response.status_code})")
    except Exception as e:
        print(f"   ❌ Erro HTTP: {e}")
        return False
    
    return True

def test_supabase_connectivity():
    """Testa conectividade específica com Supabase"""
    print("\n🏗️ TESTE ESPECÍFICO SUPABASE")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    
    print(f"SUPABASE_URL: {supabase_url[:50]}..." if supabase_url else "❌ SUPABASE_URL não definida")
    print(f"SUPABASE_KEY: {supabase_key[:20]}..." if supabase_key else "❌ SUPABASE_KEY não definida")
    
    if not supabase_url or not supabase_key:
        print("\n❌ Variáveis de ambiente não configuradas!")
        return False
    
    # Teste de DNS para o Supabase
    try:
        parsed_url = urlparse(supabase_url)
        hostname = parsed_url.hostname
        print(f"\n3. Testando DNS para {hostname}...")
        ip = socket.gethostbyname(hostname)
        print(f"   ✅ DNS resolvido: {hostname} -> {ip}")
    except socket.gaierror as e:
        print(f"   ❌ Erro DNS Supabase: {e}")
        return False
    
    # Teste HTTP para Supabase
    try:
        print("4. Testando HTTP para Supabase...")
        headers = {
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}',
            'Content-Type': 'application/json'
        }
        
        # Teste simples de health check
        response = requests.get(f"{supabase_url}/rest/v1/", headers=headers, timeout=30)
        print(f"   ✅ Supabase respondeu (Status: {response.status_code})")
        
        if response.status_code == 200:
            print("   ✅ Autenticação com Supabase OK")
        else:
            print(f"   ⚠️ Status inesperado: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
        
    except requests.exceptions.Timeout:
        print("   ❌ Timeout na conexão com Supabase")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"   ❌ Erro de conexão: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Erro HTTP Supabase: {e}")
        return False
    
    return True

def test_supabase_table_access():
    """Testa acesso específico às tabelas"""
    print("\n📋 TESTE DE ACESSO ÀS TABELAS")
    print("=" * 50)
    
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Credenciais não disponíveis")
        return False
    
    headers = {
        'apikey': supabase_key,
        'Authorization': f'Bearer {supabase_key}',
        'Content-Type': 'application/json'
    }
    
    tables_to_test = ['usuarios', 'salas', 'orcamentos']
    
    for table in tables_to_test:
        try:
            print(f"5. Testando acesso à tabela '{table}'...")
            response = requests.get(
                f"{supabase_url}/rest/v1/{table}?select=*&limit=1",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Tabela '{table}' acessível ({len(data)} registros encontrados)")
            else:
                print(f"   ❌ Erro ao acessar '{table}': Status {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ Erro ao acessar tabela '{table}': {e}")
    
    return True

def suggest_solutions():
    """Sugere soluções baseadas nos testes"""
    print("\n💡 POSSÍVEIS SOLUÇÕES")
    print("=" * 50)
    
    print("1. Verificar variáveis de ambiente:")
    print("   - SUPABASE_URL deve estar no formato: https://xxx.supabase.co")
    print("   - SUPABASE_KEY deve ser a chave anon/service_role")
    
    print("\n2. Verificar conectividade:")
    print("   - Testar conexão em rede diferente")
    print("   - Verificar firewall/proxy corporativo")
    print("   - Testar VPN se disponível")
    
    print("\n3. Verificar configuração Supabase:")
    print("   - Confirmar URL no dashboard Supabase")
    print("   - Regenerar chaves se necessário")
    print("   - Verificar RLS (Row Level Security)")
    
    print("\n4. Configurações alternativas:")
    print("   - Aumentar timeout de conexão")
    print("   - Usar DNS público (8.8.8.8)")
    print("   - Testar em ambiente Docker")

if __name__ == "__main__":
    print("🚀 DIAGNÓSTICO DE CONEXÃO COM BANCO DE DADOS")
    print("=" * 60)
    
    # Execução dos testes
    network_ok = test_network_connectivity()
    
    if network_ok:
        supabase_ok = test_supabase_connectivity()
        if supabase_ok:
            test_supabase_table_access()
    
    # Sugestões
    suggest_solutions()
    
    print("\n" + "=" * 60)
    print("📝 Diagnóstico completo. Execute com as credenciais corretas.")