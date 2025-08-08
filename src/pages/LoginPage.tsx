import { useState } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Label } from '../components/ui/label'
import { toast } from 'sonner'

const LoginPage = () => {
  const { user, login } = useAuth()
  const [loginInput, setLoginInput] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)

  if (user) {
    return <Navigate to="/dashboard" replace />
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    console.log('🔍 DEBUG: Dados do formulário')
    console.log('👤 Login input:', loginInput)
    console.log('🔑 Password length:', password.length)

    try {
      // Enviar o input como "username" para o backend
      // O backend agora vai buscar por username OU email
      await login(loginInput, password)
      toast.success('Login realizado com sucesso!')
    } catch (error) {
      console.log('❌ Erro no login:', error)
      toast.error(error instanceof Error ? error.message : 'Erro no login')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-center">Reception Sync</CardTitle>
          <CardDescription className="text-center">
            Sistema de Gestão de Recepções
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="loginInput">Usuário ou Email</Label>
              <Input
                id="loginInput"
                type="text"
                placeholder="Digite seu usuário ou email"
                value={loginInput}
                onChange={(e) => setLoginInput(e.target.value)}
                required
                disabled={loading}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Senha</Label>
              <Input
                id="password"
                type="password"
                placeholder="Digite sua senha"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading}
              />
            </div>
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Entrando...' : 'Entrar'}
            </Button>
          </form>
          
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <h3 className="font-semibold text-sm mb-2">🔑 Credenciais de Teste:</h3>
            <div className="text-xs space-y-1 text-gray-600">
              <div><strong>Username:</strong> gerencia | <strong>Senha:</strong> 123456</div>
              <div><strong>Email:</strong> gerencia@incentivar.com | <strong>Senha:</strong> 123456</div>
              <div><strong>Username:</strong> admin | <strong>Senha:</strong> 123456</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default LoginPage