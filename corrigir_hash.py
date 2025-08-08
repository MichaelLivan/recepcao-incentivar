from werkzeug.security import generate_password_hash, check_password_hash
from database import get_supabase

print("🔧 Corrigindo hash da senha...")

# Gerar hash correto
senha = "123456"
hash_correto = generate_password_hash(senha)
print(f"Hash gerado: {hash_correto}")

# Testar se funciona
teste = check_password_hash(hash_correto, senha)
print(f"Teste do hash: {'✅ FUNCIONA' if teste else '❌ NÃO FUNCIONA'}")

if teste:
    # Atualizar no banco
    supabase = get_supabase()
    result = supabase.table('usuarios').update({
        'password_hash': hash_correto
    }).eq('username', 'gerencia').execute()
    
    if result.data:
        print("✅ Hash atualizado no banco!")
        print(f"🔑 CREDENCIAL: gerencia@incentivar.com / {senha}")
    else:
        print("❌ Erro ao atualizar banco")
