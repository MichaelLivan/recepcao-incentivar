#!/usr/bin/env python3
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