import React, { createContext, useContext, useState, useEffect } from 'react'

interface User {
  id: number
  username: string
  email: string
  role: 'admin' | 'admin_geral' | 'admin_limitado' | 'recepcao'
  recepcao_id?: string
  recepcao_nome?: string
  ativo: boolean
}

interface AuthContextType {
  user: User | null
  login: (username: string, password: string) => Promise<void>
  logout: () => void
  loading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    console.log('🔍 DEBUG: AuthProvider useEffect iniciado')
    
    // Verificar se há token salvo
    const token = localStorage.getItem('token')
    console.log('🎫 Token encontrado:', token ? `${token.substring(0, 20)}...` : 'null')
    
    if (token) {
      console.log('🔍 Verificando validade do token...')
      
      // Verificar se o token é válido
      fetch('/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then(response => {
        console.log('📡 Response /api/auth/me:', response.status, response.statusText)
        
        if (response.ok) {
          return response.json()
        }
        throw new Error(`Token inválido: ${response.status}`)
      })
      .then(data => {
        console.log('✅ Token válido, dados do usuário:', data)
        setUser(data.user)
      })
      .catch(error => {
        console.log('❌ Erro na verificação do token:', error)
        console.log('🗑️ Removendo token inválido...')
        localStorage.removeItem('token')
      })
      .finally(() => {
        console.log('🏁 Verificação de token finalizada')
        setLoading(false)
      })
    } else {
      console.log('📭 Nenhum token encontrado')
      setLoading(false)
    }
  }, [])

  const login = async (username: string, password: string) => {
    console.log('🚀 DEBUG: Iniciando processo de login')
    console.log('👤 Username:', username)
    console.log('🔑 Password length:', password.length)
    
    try {
      console.log('📡 Fazendo request para /api/auth/login...')
      
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
      })

      console.log('📡 Response status:', response.status)
      console.log('📡 Response headers:', Object.fromEntries(response.headers.entries()))

      if (!response.ok) {
        console.log('❌ Response não é OK, obtendo erro...')
        const errorText = await response.text()
        console.log('📄 Response text:', errorText)
        
        let error
        try {
          error = JSON.parse(errorText)
          console.log('📄 Error JSON:', error)
        } catch {
          error = { error: errorText || `Erro HTTP ${response.status}` }
        }
        
        throw new Error(error.error || 'Erro no login')
      }

      console.log('✅ Response OK, obtendo dados...')
      const data = await response.json()
      console.log('📄 Response data:', data)
      
      if (!data.access_token) {
        console.log('❌ Token não encontrado na resposta')
        throw new Error('Token não recebido do servidor')
      }
      
      if (!data.user) {
        console.log('❌ Dados do usuário não encontrados na resposta')
        throw new Error('Dados do usuário não recebidos')
      }

      console.log('💾 Salvando token no localStorage...')
      localStorage.setItem('token', data.access_token)
      
      console.log('👤 Definindo usuário no estado...')
      setUser(data.user)
      
      console.log('✅ Login bem-sucedido!')

    } catch (error) {
      console.log('💥 ERRO no login:', error)
      
      // Log adicional para debug de rede
      if (error instanceof TypeError && error.message.includes('fetch')) {
        console.log('🌐 Erro de rede - verificar se backend está rodando')
        console.log('🔗 URL tentada: /api/auth/login')
        console.log('🏃‍♂️ Backend rodando em: http://localhost:5000 ?')
      }
      
      throw error
    }
  }

  const logout = () => {
    console.log('🚪 DEBUG: Fazendo logout')
    localStorage.removeItem('token')
    setUser(null)
    console.log('✅ Logout concluído')
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}