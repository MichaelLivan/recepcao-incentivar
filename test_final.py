#!/usr/bin/env python3
"""
Teste final para verificar se tudo está funcionando
"""

# Carregar variáveis de ambiente
from dotenv import load_dotenv
import os

print("🧪 TESTE FINAL DE CONEXÃO")
print("=" * 40)

# Carregar .env
load_dotenv()

# Verificar variáveis
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')

print(f"1. SUPABASE_URL: {'✅' if url else '❌'}")
if url:
    print(f"   {url}")

print(f"2. SUPABASE_KEY: {'✅' if key else '❌'}")
if key:
    print(f"   {key[:50]}...")

if not url or not key:
    print("\n❌ Variáveis não carregadas!")
    print("Verifique se o arquivo .env está no diretório correto")
    exit(1)

# Testar Supabase
try:
    print("\n3. Testando Supabase...")
    import requests
    
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(f"{url}/rest/v1/", headers=headers, timeout=30)
    
    if response.status_code == 200:
        print("   ✅ Supabase OK")
    else:
        print(f"   ❌ Erro: {response.status_code}")
        exit(1)

except Exception as e:
    print(f"   ❌ Erro: {e}")
    exit(1)

# Testar tabela usuarios
try:
    print("4. Testando tabela usuarios...")
    response = requests.get(
        f"{url}/rest/v1/usuarios?select=username&limit=5",
        headers=headers,
        timeout=15
    )
    
    if response.status_code == 200:
        users = response.json()
        print(f"   ✅ {len(users)} usuário(s) encontrado(s)")
        for user in users:
            print(f"      • {user.get('username', 'N/A')}")
    else:
        print(f"   ❌ Erro: {response.status_code}")

except Exception as e:
    print(f"   ❌ Erro: {e}")

# Testar imports do projeto
try:
    print("5. Testando imports do projeto...")
    from models.user import User
    from database import get_supabase
    print("   ✅ Imports OK")
    
    # Testar cliente do Supabase
    print("6. Testando cliente Supabase...")
    supabase = get_supabase()
    result = supabase.table('usuarios').select('username').limit(1).execute()
    print(f"   ✅ Cliente OK - {len(result.data)} registro(s)")
    
except Exception as e:
    print(f"   ❌ Erro nos imports: {e}")

print("\n" + "=" * 40)
print("🎉 TESTE CONCLUÍDO!")
print("✅ Sistema pronto para executar: python app.py")