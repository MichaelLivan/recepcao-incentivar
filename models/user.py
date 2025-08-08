from database import get_supabase
from werkzeug.security import generate_password_hash, check_password_hash
import traceback

class User:
    def __init__(self, id=None, username=None, email=None, password_hash=None, 
                 role=None, recepcao_id=None, recepcao_nome=None, ativo=True):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.recepcao_id = recepcao_id
        self.recepcao_nome = recepcao_nome
        self.ativo = ativo
    
    @staticmethod
    def create_user(username, email, password, role, recepcao_id=None, recepcao_nome=None):
        try:
            print(f"🔍 DEBUG: Criando usuário {username}")
            supabase = get_supabase()
            password_hash = generate_password_hash(password)
            
            data = {
                'username': username,
                'email': email,
                'password_hash': password_hash,
                'role': role,
                'recepcao_id': recepcao_id,
                'recepcao_nome': recepcao_nome,
                'ativo': True
            }
            
            result = supabase.table('usuarios').insert(data).execute()
            print(f"✅ Usuário criado: {result.data}")
            return result.data[0] if result.data else None
            
        except Exception as e:
            print(f"💥 ERRO ao criar usuário: {str(e)}")
            return None
    
    @staticmethod
    def find_by_username(login_input):
        try:
            print(f"🔍 DEBUG: Buscando usuário com input '{login_input}' no banco")
            supabase = get_supabase()
            
            # Primeiro, tentar buscar por username
            print(f"🔍 Tentativa 1: Buscar por username = '{login_input}'")
            result = supabase.table('usuarios').select('*').eq('username', login_input).eq('ativo', True).execute()
            
            print(f"📊 Resultado busca por username: {len(result.data) if result.data else 0} registros")
            
            # Se não encontrou por username, tentar por email
            if not result.data:
                print(f"🔍 Tentativa 2: Buscar por email = '{login_input}'")
                result = supabase.table('usuarios').select('*').eq('email', login_input).eq('ativo', True).execute()
                print(f"📊 Resultado busca por email: {len(result.data) if result.data else 0} registros")
            
            # Se ainda não encontrou, mostrar todos os usuários para debug
            if not result.data:
                print(f"🔍 DEBUG: Nenhum usuário encontrado. Listando todos os usuários:")
                all_users = supabase.table('usuarios').select('username, email, ativo').execute()
                for user in all_users.data:
                    print(f"   👤 Username: '{user['username']}' | Email: '{user['email']}' | Ativo: {user['ativo']}")
                print(f"❌ Usuário '{login_input}' não encontrado no banco")
                return None
            
            if result.data:
                user_data = result.data[0]
                print(f"✅ Usuário encontrado: {user_data['username']}")
                print(f"📧 Email: {user_data['email']}")
                print(f"👥 Role: {user_data['role']}")
                print(f"🏢 Recepcao: {user_data.get('recepcao_id', 'N/A')}")
                print(f"🔐 Hash existe: {'Sim' if user_data.get('password_hash') else 'Não'}")
                print(f"🔐 Hash preview: {user_data.get('password_hash', '')[:50]}...")
                
                return User(
                    id=user_data['id'],
                    username=user_data['username'],
                    email=user_data['email'],
                    password_hash=user_data['password_hash'],
                    role=user_data['role'],
                    recepcao_id=user_data['recepcao_id'],
                    recepcao_nome=user_data['recepcao_nome'],
                    ativo=user_data['ativo']
                )
            else:
                print(f"❌ Usuário '{login_input}' não encontrado no banco")
                return None
                
        except Exception as e:
            print(f"💥 ERRO ao buscar usuário: {str(e)}")
            print(f"📋 Traceback: {traceback.format_exc()}")
            return None
    
    def check_password(self, password):
        try:
            print(f"🔐 DEBUG: Verificando senha para {self.username}")
            print(f"🔐 Password recebida: '{password}' (length: {len(password)})")
            print(f"🔐 Hash salvo: {self.password_hash[:50]}...")
            
            # Verificar se hash existe
            if not self.password_hash:
                print("❌ Hash de senha não existe!")
                return False
            
            # Verificar formato do hash
            if not (self.password_hash.startswith('pbkdf2:') or self.password_hash.startswith('scrypt:')):
                print(f"⚠️ Hash não está no formato conhecido! Formato atual: {self.password_hash[:20]}...")
                
            # Tentar verificar senha
            result = check_password_hash(self.password_hash, password)
            print(f"🔐 Resultado check_password_hash: {result}")
            
            return result
            
        except Exception as e:
            print(f"💥 ERRO ao verificar senha: {str(e)}")
            print(f"📋 Traceback: {traceback.format_exc()}")
            return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'recepcao_id': self.recepcao_id,
            'recepcao_nome': self.recepcao_nome,
            'ativo': self.ativo
        }

# Função auxiliar para testar conexão com banco
def test_database_connection():
    try:
        print("🔍 DEBUG: Testando conexão com banco...")
        supabase = get_supabase()
        result = supabase.table('usuarios').select('username').limit(1).execute()
        print(f"✅ Conexão OK. Usuarios encontrados: {len(result.data)}")
        return True
    except Exception as e:
        print(f"💥 ERRO na conexão: {str(e)}")
        return False

# Função para testar hash específico
def test_password_hash(stored_hash, password):
    try:
        print(f"🧪 TESTE: Hash '{stored_hash[:50]}...' com senha '{password}'")
        result = check_password_hash(stored_hash, password)
        print(f"🧪 Resultado: {result}")
        return result
    except Exception as e:
        print(f"💥 ERRO no teste de hash: {str(e)}")
        return False