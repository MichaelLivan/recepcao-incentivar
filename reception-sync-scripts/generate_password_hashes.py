#!/usr/bin/env python3
"""
Gerador de hashes de senha para o sistema Reception Sync
Execute este script para gerar os hashes corretos
"""

from werkzeug.security import generate_password_hash

def gerar_hashes():
    # Definir senhas padrão
    usuarios_senhas = {
      'gerencia': '123456',
    'admpodd': '123456', 
    'admpdg': '123456',
    'admaba': '123456',
    'recepcao103': '123456',
    'recepcao108': '123456', 
    'recepcao203': '123456',
    'recepcao808': '123456',
    'recepcao1002': '123456',
    'recepcao1009': '123456',
    'recepcao1108': '123456'
}
    
    print("🔐 Gerando hashes de senha...")
    print("=" * 60)
    
    # Gerar SQL UPDATE statements
    sql_statements = []
    
    for username, senha in usuarios_senhas.items():
        password_hash = generate_password_hash(senha)
        
        print(f"Usuário: {username}")
        print(f"Senha: {senha}")
        print(f"Hash: {password_hash}")
        
        # Gerar SQL UPDATE
        sql = f"UPDATE usuarios SET password_hash = '{password_hash}' WHERE username = '{username}';"
        sql_statements.append(sql)
        
        print("-" * 60)
    
    # Salvar SQL em arquivo
    with open('update_passwords.sql', 'w') as f:
        f.write("-- Atualização de senhas dos usuários\n")
        f.write("-- Execute este arquivo no Supabase SQL Editor\n\n")
        for sql in sql_statements:
            f.write(sql + "\n")
        
        f.write("\n-- Verificar atualizações\n")
        f.write("SELECT username, email, role, LEFT(password_hash, 20) || '...' as hash_preview FROM usuarios ORDER BY username;\n")
    
    print("\n✅ Arquivo 'update_passwords.sql' criado!")
    print("📁 Execute este arquivo no editor SQL do Supabase")
    
    return sql_statements

if __name__ == "__main__":
    gerar_hashes()