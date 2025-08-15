#!/usr/bin/env python3
"""
CORREÇÃO RÁPIDA - Execute este script para resolver o problema imediatamente
"""

from dotenv import load_dotenv
load_dotenv()

import os
import subprocess
import sys

def fix_supabase_library():
    """Corrige problemas na biblioteca Supabase"""
    print("🔧 CORREÇÃO RÁPIDA DA BIBLIOTECA SUPABASE")
    print("=" * 50)
    
    # Passo 1: Reinstalar supabase com versão específica
    print("1. Reinstalando biblioteca supabase...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "uninstall", "supabase", "-y"
        ])
        print("   ✅ Versão antiga removida")
        
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "supabase==1.0.4"
        ])
        print("   ✅ Versão 1.0.4 instalada")
        
    except Exception as e:
        print(f"   ⚠️ Erro na reinstalação: {e}")
        print("   🔄 Continuando mesmo assim...")

def create_simple_database():
    """Cria um database.py simplificado"""
    print("\n2. Criando database.py simplificado...")
    
    database_content = '''#!/usr/bin/env python3
"""
Database simplificado para resolver problema de headers
"""

from dotenv import load_dotenv
load_dotenv()

import os
import requests

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
_supabase_client = None

class SimpleSupabaseClient:
    def __init__(self, url, key):
        self.url = url.rstrip('/')
        self.headers = {
            'apikey': key,
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }
    
    def table(self, table_name):
        return SimpleTable(self.url, self.headers, table_name)

class SimpleTable:
    def __init__(self, url, headers, table_name):
        self.endpoint = f"{url}/rest/v1/{table_name}"
        self.headers = headers
    
    def select(self, columns='*'):
        return SimpleQuery(self.endpoint, self.headers, 'GET', columns)
    
    def insert(self, data):
        return SimpleQuery(self.endpoint, self.headers, 'POST', data)
    
    def update(self, data):
        return SimpleQuery(self.endpoint, self.headers, 'PATCH', data)

class SimpleQuery:
    def __init__(self, endpoint, headers, method, data=None):
        self.endpoint = endpoint
        self.headers = headers
        self.method = method
        self.data = data
        self.params = {}
    
    def eq(self, column, value):
        self.params[column] = f'eq.{value}'
        return self
    
    def limit(self, count):
        self.params['limit'] = count
        return self
    
    def order(self, column, desc=False):
        order_str = f"{column}.desc" if desc else column
        self.params['order'] = order_str
        return self
    
    def execute(self):
        if self.method == 'GET':
            if self.data != '*':
                self.params['select'] = self.data
            response = requests.get(self.endpoint, headers=self.headers, params=self.params, timeout=30)
        elif self.method == 'POST':
            response = requests.post(self.endpoint, headers=self.headers, json=self.data, timeout=30)
        elif self.method == 'PATCH':
            response = requests.patch(self.endpoint, headers=self.headers, json=self.data, params=self.params, timeout=30)
        
        if response.status_code in [200, 201]:
            data = response.json() if response.content else []
            return SimpleResult(data)
        else:
            raise Exception(f"Erro {response.status_code}: {response.text}")

class SimpleResult:
    def __init__(self, data):
        self.data = data if isinstance(data, list) else [data] if data else []

def get_supabase():
    global _supabase_client
    if _supabase_client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Credenciais do Supabase não configuradas")
        
        try:
            from supabase import create_client
            _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
            # Teste rápido
            _supabase_client.table('usuarios').select('username').limit(1).execute()
            print("✅ Cliente oficial funcionou")
        except:
            print("🔄 Usando cliente simplificado")
            _supabase_client = SimpleSupabaseClient(SUPABASE_URL, SUPABASE_KEY)
    
    return _supabase_client

def test_database_connection():
    try:
        supabase = get_supabase()
        result = supabase.table('usuarios').select('username').limit(1).execute()
        return True
    except:
        return False

def health_check():
    try:
        supabase = get_supabase()
        supabase.table('usuarios').select('username').limit(1).execute()
        return {'status': 'healthy', 'database': 'connected'}
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}
'''
    
    try:
        with open('database.py', 'w', encoding='utf-8') as f:
            f.write(database_content)
        print("   ✅ database.py criado")
        return True
    except Exception as e:
        print(f"   ❌ Erro ao criar database.py: {e}")
        return False

def test_fix():
    """Testa se a correção funcionou"""
    print("\n3. Testando correção...")
    
    try:
        # Importar e testar
        import importlib
        import sys
        
        # Recarregar módulo se já importado
        if 'database' in sys.modules:
            importlib.reload(sys.modules['database'])
        
        from database import get_supabase, test_database_connection
        
        print("   ✅ Import OK")
        
        # Testar conexão
        if test_database_connection():
            print("   ✅ Conexão OK")
            
            # Testar query
            supabase = get_supabase()
            result = supabase.table('usuarios').select('username').limit(3).execute()
            print(f"   ✅ Query OK - {len(result.data)} usuário(s)")
            
            for user in result.data:
                print(f"      • {user.get('username', 'N/A')}")
            
            return True
        else:
            print("   ❌ Falha na conexão")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro no teste: {e}")
        return False

def main():
    """Executa correção completa"""
    print("🚀 EXECUTANDO CORREÇÃO RÁPIDA...")
    
    # Verificar variáveis de ambiente
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_KEY')
    
    if not url or not key:
        print("❌ Variáveis de ambiente não carregadas!")
        print("💡 Execute: python fix_env_loading.py primeiro")
        return False
    
    print(f"✅ Variáveis OK: {url[:50]}...")
    
    # Executar correções
    fix_supabase_library()
    
    if create_simple_database():
        if test_fix():
            print("\n" + "="*50)
            print("🎉 CORREÇÃO CONCLUÍDA COM SUCESSO!")
            print("="*50)
            print("\n✅ PRÓXIMOS PASSOS:")
            print("1. Execute: python app.py")
            print("2. Acesse: http://localhost:5001/api/health")
            print("3. Teste o login na aplicação")
            return True
    
    print("\n❌ Correção falhou")
    return False

if __name__ == "__main__":
    main()