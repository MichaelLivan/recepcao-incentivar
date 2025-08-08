# Salve como: hash_generator.py
# Execute: python hash_generator.py

from werkzeug.security import generate_password_hash

# Definir senhas
senhas = {
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

print("-- Comandos SQL gerados automaticamente")
print("-- Cole no Supabase SQL Editor\n")

for usuario, senha in senhas.items():
    hash_senha = generate_password_hash(senha)
    print(f"UPDATE usuarios SET password_hash = '{hash_senha}' WHERE username = '{usuario}';")

print("\n-- Verificar:")
print("SELECT username, LEFT(password_hash, 30) || '...' FROM usuarios;")