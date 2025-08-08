#!/usr/bin/env python3
"""
Script para inicializar usuários no sistema
Execute: python scripts/init_users.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User

def init_users():
    users_data = [
        # Admins
        {'username': 'admpodd', 'email': 'admpodd@incentivar.com', 'password': '123456', 'role': 'admin'},
        {'username': 'admpdg', 'email': 'admpdg@incentivar.com', 'password': '123456', 'role': 'admin'},
        {'username': 'admaba', 'email': 'admaba@incentivar.com', 'password': '123456', 'role': 'admin'},
        
        # Recepções
        {'username': 'recepcao103', 'email': 'recepcao103@incentivar.com', 'password': '123456', 'role': 'recepcao', 'recepcao_id': '103', 'recepcao_nome': 'Recepção 103'},
        {'username': 'recepcao108', 'email': 'recepcao108@incentivar.com', 'password': '123456', 'role': 'recepcao', 'recepcao_id': '108', 'recepcao_nome': 'Recepção 108'},
        {'username': 'recepcao203', 'email': 'recepcao203@incentivar.com', 'password': '123456', 'role': 'recepcao', 'recepcao_id': '203', 'recepcao_nome': 'Recepção 203'},
        {'username': 'recepcao808', 'email': 'recepcao808@incentivar.com', 'password': '123456', 'role': 'recepcao', 'recepcao_id': '808', 'recepcao_nome': 'Recepção 808'},
        {'username': 'recepcao1002', 'email': 'recepcao1002@incentivar.com', 'password': '123456', 'role': 'recepcao', 'recepcao_id': '1002', 'recepcao_nome': 'Recepção 1002'},
        {'username': 'recepcao1009', 'email': 'recepcao1009@incentivar.com', 'password': '123456', 'role': 'recepcao', 'recepcao_id': '1009', 'recepcao_nome': 'Recepção 1009'},
        {'username': 'recepcao1108', 'email': 'recepcao1108@incentivar.com', 'password': '123456', 'role': 'recepcao', 'recepcao_id': '1108', 'recepcao_nome': 'Recepção 1108'},
    ]
    
    print("Inicializando usuários...")
    
    for user_data in users_data:
        try:
            # Verificar se usuário já existe
            existing_user = User.find_by_username(user_data['username'])
            if existing_user:
                print(f"✓ Usuário {user_data['username']} já existe")
                continue
            
            # Criar usuário
            user = User.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                role=user_data['role'],
                recepcao_id=user_data.get('recepcao_id'),
                recepcao_nome=user_data.get('recepcao_nome')
            )
            
            if user:
                print(f"✓ Usuário {user_data['username']} criado com sucesso")
            else:
                print(f"✗ Erro ao criar usuário {user_data['username']}")
                
        except Exception as e:
            print(f"✗ Erro ao criar usuário {user_data['username']}: {str(e)}")
    
    print("\nInicialização concluída!")
    print("\nCredenciais de acesso:")
    print("Admins: admpodd, admpdg, admaba")
    print("Recepções: recepcao103, recepcao108, recepcao203, recepcao808, recepcao1002, recepcao1009, recepcao1108")
    print("Senha padrão para todos: 123456")

if __name__ == '__main__':
    init_users()