from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models.user import User

def is_admin(user_role):
    """Verifica se o role é de admin (qualquer tipo)"""
    return user_role in ['admin', 'admin_geral', 'admin_limitado']

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Token inválido'}), 401
    return decorated_function

def require_role(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                user = User.find_by_username(current_user_id)
                
                if not user:
                    return jsonify({'error': 'Usuário não encontrado'}), 404
                
                # Verificar se é admin (aceita qualquer tipo de admin)
                if 'admin' in allowed_roles and is_admin(user.role):
                    return f(*args, **kwargs)
                
                # Verificar role exato
                if user.role not in allowed_roles:
                    return jsonify({'error': 'Acesso negado'}), 403
                
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'Erro de autenticação'}), 401
        return decorated_function
    return decorator

def require_recepcao(allowed_recepcoes):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                user = User.find_by_username(current_user_id)
                
                if not user:
                    return jsonify({'error': 'Usuário não encontrado'}), 404
                
                # Admin tem acesso a tudo
                if is_admin(user.role):
                    return f(*args, **kwargs)
                
                if user.recepcao_id not in allowed_recepcoes:
                    return jsonify({'error': 'Acesso negado para esta recepção'}), 403
                
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'Erro de autenticação'}), 401
        return decorated_function
    return decorator

def get_current_user():
    try:
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        return User.find_by_username(current_user_id)
    except:
        return None