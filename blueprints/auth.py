# blueprints/auth.py - Versão melhorada
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from utils.permissions import get_current_user
from werkzeug.security import generate_password_hash, check_password_hash
import traceback
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        print("🔍 DEBUG: Início do login")
        
        data = request.get_json()
        print(f"📥 Dados recebidos: {data}")
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            print("❌ Username ou password vazios")
            return jsonify({'error': 'Username e password são obrigatórios'}), 400
        
        print(f"🔍 Buscando usuário: {username}")
        user = User.find_by_username(username)
        
        if not user:
            print(f"❌ Usuário '{username}' não encontrado")
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        print(f"✅ Usuário encontrado: {user.username}")
        
        # Verificar se o usuário está ativo
        if not user.ativo:
            print(f"❌ Usuário '{username}' está inativo")
            return jsonify({'error': 'Usuário inativo. Entre em contato com o administrador.'}), 401
        
        print("🔐 Verificando senha...")
        password_check = user.check_password(password)
        
        if not password_check:
            print("❌ Senha incorreta")
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        print("🎫 Criando access token...")
        access_token = create_access_token(identity=username)
        
        user_dict = user.to_dict()
        print(f"✅ Login bem-sucedido para: {username}")
        
        return jsonify({
            'access_token': access_token,
            'user': user_dict,
            'message': 'Login realizado com sucesso'
        }), 200
        
    except Exception as e:
        print(f"💥 ERRO NO LOGIN: {str(e)}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user_info():
    try:
        print("🔍 DEBUG: Verificando usuário atual")
        user = get_current_user()
        if user:
            print(f"✅ Usuário autenticado: {user.username}")
            return jsonify({'user': user.to_dict()}), 200
        print("❌ Usuário não encontrado")
        return jsonify({'error': 'Usuário não encontrado'}), 404
    except Exception as e:
        print(f"💥 ERRO NO /me: {str(e)}")
        return jsonify({'error': 'Token inválido'}), 401

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        from database import get_supabase
        
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        print(f"🔑 Tentativa de mudança de senha")
        
        # Validações básicas
        if not current_password or not new_password:
            return jsonify({'error': 'Senha atual e nova senha são obrigatórias'}), 400
        
        # Validar força da nova senha
        if len(new_password) < 6:
            return jsonify({'error': 'Nova senha deve ter pelo menos 6 caracteres'}), 400
        
        if not re.search(r'\d', new_password):
            return jsonify({'error': 'Nova senha deve conter pelo menos 1 número'}), 400
        
        if not re.search(r'[a-zA-Z]', new_password):
            return jsonify({'error': 'Nova senha deve conter pelo menos 1 letra'}), 400
        
        # Buscar usuário atual
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        print(f"🔐 Verificando senha atual para: {user.username}")
        
        # Verificar senha atual
        if not user.check_password(current_password):
            print("❌ Senha atual incorreta")
            return jsonify({'error': 'Senha atual incorreta'}), 400
        
        # Verificar se a nova senha é diferente da atual
        if user.check_password(new_password):
            return jsonify({'error': 'A nova senha deve ser diferente da senha atual'}), 400
        
        print("🔒 Gerando nova hash de senha...")
        new_password_hash = generate_password_hash(new_password)
        
        # Atualizar senha no banco
        supabase = get_supabase()
        result = supabase.table('usuarios').update({
            'password_hash': new_password_hash,
            'updated_at': 'now()'
        }).eq('id', user.id).execute()
        
        if result.data:
            print(f"✅ Senha alterada com sucesso para: {user.username}")
            return jsonify({
                'message': 'Senha alterada com sucesso',
                'timestamp': result.data[0].get('updated_at')
            }), 200
        
        return jsonify({'error': 'Erro ao alterar senha no banco de dados'}), 500
        
    except Exception as e:
        print(f"💥 ERRO na mudança de senha: {str(e)}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/validate-password', methods=['POST'])
@jwt_required()
def validate_password():
    """Endpoint para validar se uma senha atende aos critérios"""
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        # Critérios de validação
        criteria = {
            'length': len(password) >= 6,
            'has_number': bool(re.search(r'\d', password)),
            'has_letter': bool(re.search(r'[a-zA-Z]', password)),
            'not_common': password.lower() not in ['123456', 'password', 'admin', 'qwerty', '123123']
        }
        
        # Calcular força da senha
        strength_score = sum(criteria.values())
        
        if strength_score == 0:
            strength = {'level': 0, 'text': '', 'color': 'gray'}
        elif strength_score <= 2:
            strength = {'level': 33, 'text': 'Fraca', 'color': 'red'}
        elif strength_score == 3:
            strength = {'level': 66, 'text': 'Média', 'color': 'yellow'}
        else:
            strength = {'level': 100, 'text': 'Forte', 'color': 'green'}
        
        return jsonify({
            'valid': all(criteria.values()),
            'criteria': criteria,
            'strength': strength
        }), 200
        
    except Exception as e:
        print(f"💥 ERRO na validação de senha: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Endpoint para logout (invalidar token no lado do cliente)"""
    try:
        user = get_current_user()
        if user:
            print(f"🚪 Logout realizado para: {user.username}")
        
        return jsonify({
            'message': 'Logout realizado com sucesso'
        }), 200
        
    except Exception as e:
        print(f"💥 ERRO no logout: {str(e)}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

# Rota adicional para debug
@auth_bp.route('/debug-user/<username>', methods=['GET'])
def debug_user(username):
    try:
        print(f"🔍 DEBUG: Buscando dados do usuário {username}")
        user = User.find_by_username(username)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        return jsonify({
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'recepcao_id': user.recepcao_id,
            'recepcao_nome': user.recepcao_nome,
            'ativo': user.ativo,
            'hash_preview': user.password_hash[:50] + '...' if user.password_hash else None
        })
        
    except Exception as e:
        print(f"💥 ERRO NO DEBUG: {str(e)}")
        return jsonify({'error': str(e)}), 500