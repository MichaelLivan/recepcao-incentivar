import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

interface ProtectedRouteProps {
  children: React.ReactNode
  requiredRole?: 'admin' | 'recepcao'
  requiredReception?: string
  requiredReceptions?: string[]
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  requiredRole, 
  requiredReception,
  requiredReceptions 
}) => {
  const { user, loading } = useAuth()

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Carregando...</div>
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  // Função para verificar se o usuário é admin
  const isAdmin = (userRole: string) => {
    return userRole === 'admin' || userRole === 'admin_geral' || userRole === 'admin_limitado'
  }

  // Verificar role se especificado
  if (requiredRole === 'admin' && !isAdmin(user.role)) {
    return <Navigate to="/dashboard" replace />
  }

  if (requiredRole === 'recepcao' && user.role !== 'recepcao') {
    return <Navigate to="/dashboard" replace />
  }

  // Admin tem acesso a tudo
  if (isAdmin(user.role)) {
    return <>{children}</>
  }

  // Verificar recepção específica
  if (requiredReception && user.recepcao_id !== requiredReception) {
    return <Navigate to="/dashboard" replace />
  }

  // Verificar múltiplas recepções
  if (requiredReceptions && !requiredReceptions.includes(user.recepcao_id || '')) {
    return <Navigate to="/dashboard" replace />
  }

  return <>{children}</>
}

export default ProtectedRoute