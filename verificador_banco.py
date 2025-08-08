#!/usr/bin/env python3
"""
Verificador do banco - mostra exatamente o que está no banco
Execute: python verificador_banco.py
"""

def verificar_banco():
    print("🔍 VERIFICANDO BANCO DE DADOS")
    print("=" * 50)
    
    try:
        from database import get_supabase
        supabase = get_supabase()
        
        # 1. Verificar se existe tabela usuarios
        print("📋 1. Verificando tabela usuarios...")
        
        # 2. Buscar todos os usuários
        result = supabase.table('usuarios').select('*').execute()
        
        print(f"👥 Total de usuários encontrados: {len(result.data)}")
        
        if not result.data:
            print("❌ NENHUM USUÁRIO ENCONTRADO!")
            print("🔧 A tabela está vazia - precisa criar usuários")
            return False
        
        # 3. Mostrar todos os usuários
        print("\n👤 USUÁRIOS NA TABELA:")
        for user in result.data:
            print(f"   ID: {user.get('id')}")
            print(f"   Username: {user.get('username')}")
            print(f"   Email: {user.get('email')}")
            print(f"   Role: {user.get('role')}")
            print(f"   Recepcao: {user.get('recepcao_id', 'NULL')}")
            print(f"   Ativo: {user.get('ativo')}")
            print(f"   Hash: {user.get('password_hash', '')[:50]}...")
            print("   " + "-" * 40)
        
        # 4. Verificar usuário específico 'gerencia'
        print("\n🔍 4. Verificando usuário 'gerencia'...")
        gerencia_result = supabase.table('usuarios').select('*').eq('username', 'gerencia').execute()
        
        if gerencia_result.data:
            user = gerencia_result.data[0]
            print("✅ Usuário 'gerencia' encontrado!")
            print(f"   ID: {user['id']}")
            print(f"   Email: {user['email']}")
            print(f"   Role: {user['role']}")
            print(f"   Ativo: {user['ativo']}")
            print(f"   Hash completo: {user['password_hash']}")
            
            # 5. Testar hash se werkzeug estiver disponível
            try:
                from werkzeug.security import check_password_hash
                
                senhas_teste = ['123456', 'gerencia123', 'admin', 'gerencia']
                print(f"\n🧪 5. Testando senhas contra o hash...")
                
                for senha in senhas_teste:
                    resultado = check_password_hash(user['password_hash'], senha)
                    status = "✅ FUNCIONA" if resultado else "❌ não funciona"
                    print(f"   Senha '{senha}': {status}")
                    
                    if resultado:
                        print(f"\n🎉 SENHA ENCONTRADA: '{senha}'")
                        print(f"🔑 CREDENCIAL CORRETA: gerencia / {senha}")
                        return True
                        
            except ImportError:
                print("⚠️ Werkzeug não disponível para testar hash")
                
        else:
            print("❌ Usuário 'gerencia' NÃO encontrado!")
            print("🔧 Precisa criar o usuário")
            
        return False
        
    except Exception as e:
        print(f"❌ ERRO ao verificar banco: {e}")
        import traceback
        traceback.print_exc()
        return False

def mostrar_solucoes():
    print("\n🔧 SOLUÇÕES DISPONÍVEIS:")
    print("=" * 50)
    
    print("1. 📋 EXECUTE O SQL DEFINITIVO no Supabase:")
    print("   - Vai deletar e recriar usuário com hash funcional")
    print("   - Credenciais: gerencia / 123456")
    
    print("\n2. 🐍 EXECUTE O SCRIPT PYTHON:")
    print("   python fix_definitivo.py")
    print("   - Cria usuário com hash gerado em tempo real")
    
    print("\n3. 🧪 TESTE DIRETO:")
    print("   curl -X POST http://localhost:5000/api/auth/login \\")
    print("   -H 'Content-Type: application/json' \\") 
    print("   -d '{\"username\": \"gerencia\", \"password\": \"123456\"}'")

def main():
    print("🔍 VERIFICADOR COMPLETO DO BANCO")
    print("=" * 60)
    
    sucesso = verificar_banco()
    
    if not sucesso:
        mostrar_solucoes()
    else:
        print("\n🎉 BANCO ESTÁ CORRETO!")
        print("🧪 Teste o login agora")

if __name__ == "__main__":
    main()