import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def get_supabase() -> Client:
    """
    Retorna uma instância do cliente Supabase
    """
    try:
        # Obter credenciais das variáveis de ambiente
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            print("❌ ERRO: Variáveis SUPABASE_URL e SUPABASE_KEY não encontradas!")
            print("   Verifique se o arquivo .env está configurado corretamente")
            print("   Exemplo de .env:")
            print("   SUPABASE_URL=https://sua-instancia.supabase.co")
            print("   SUPABASE_KEY=sua-chave-aqui")
            raise ValueError("Credenciais do Supabase não configuradas")
        
        # Criar cliente Supabase
        supabase = create_client(supabase_url, supabase_key)
        
        return supabase
        
    except Exception as e:
        print(f"❌ Erro ao conectar com Supabase: {str(e)}")
        raise

def test_supabase_connection():
    """
    Testa a conexão com Supabase
    """
    try:
        print("🔍 Testando conexão com Supabase...")
        
        supabase = get_supabase()
        
        # Tentar fazer uma consulta simples
        result = supabase.table('usuarios').select('id, username').limit(1).execute()
        
        if result.data is not None:
            print("✅ Conexão com Supabase OK!")
            print(f"   📊 Banco encontrado com dados")
            return True
        else:
            print("⚠️ Conexão estabelecida mas sem dados")
            return True
            
    except Exception as e:
        print(f"❌ Erro na conexão: {str(e)}")
        return False

if __name__ == "__main__":
    # Teste direto do arquivo
    test_supabase_connection()