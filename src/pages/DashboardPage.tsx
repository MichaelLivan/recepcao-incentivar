import { useAuth } from '../contexts/AuthContext'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Link } from 'react-router-dom'
import { useState } from 'react'
import { 
  Building2, 
  Package, 
  FileText, 
  Gift, 
  Clock, 
  Users, 
  ClipboardList,
  BarChart3,
  UserPlus,
  Calendar,
  LogOut,
  Settings,
  Bell,
  Home,
  Activity,
  TrendingUp,
  Star,
  ArrowRight,
  User
} from 'lucide-react'

const DashboardPage = () => {
  const { user, logout } = useAuth()
  const [showPasswordModal, setShowPasswordModal] = useState(false)

  // Função para verificar se é admin
  const isAdmin = () => {
    return user?.role === 'admin' || user?.role === 'admin_geral' || user?.role === 'admin_limitado'
  }

  const getAvailableModules = () => {
    if (!user) return []

    const modules = []

    if (isAdmin()) {
      modules.push(
        {
          title: 'Cadastrar Usuários',
          description: 'Gerenciar usuários do sistema',
          icon: UserPlus,
          path: '/admin/users',
          color: 'from-purple-500 to-purple-600',
          bgColor: 'bg-purple-50',
          borderColor: 'border-purple-200'
        },
        {
          title: 'Relatórios',
          description: 'Relatórios de orçamentos e estatísticas',
          icon: BarChart3,
          path: '/admin/reports',
          color: 'from-green-500 to-green-600',
          bgColor: 'bg-green-50',
          borderColor: 'border-green-200'
        },
        {
          title: 'Mapa de Salas',
          description: 'Visualizar e reservar salas',
          icon: Building2,
          path: '/salas',
          color: 'from-blue-500 to-blue-600',
          bgColor: 'bg-blue-50',
          borderColor: 'border-blue-200'
        },
        {
          title: 'Controle de Pacientes',
          description: 'Entradas e saídas da clínica',
          icon: Users,
          path: '/pacientes',
          color: 'from-teal-500 to-teal-600',
          bgColor: 'bg-teal-50',
          borderColor: 'border-teal-200'
        }
      )
    } else {
      // Módulos para recepções
      modules.push(
        {
          title: 'Mapa de Salas',
          description: 'Gerenciar salas da recepção',
          icon: Building2,
          path: '/salas',
          color: 'from-blue-500 to-blue-600',
          bgColor: 'bg-blue-50',
          borderColor: 'border-blue-200'
        },
        {
          title: 'Controle de Pacientes',
          description: 'Entrada e saída de pacientes',
          icon: Users,
          path: '/pacientes',
          color: 'from-teal-500 to-teal-600',
          bgColor: 'bg-teal-50',
          borderColor: 'border-teal-200'
        },
        {
          title: 'Orçamentos',
          description: 'Lançar e acompanhar orçamentos',
          icon: FileText,
          path: '/orcamentos',
          color: 'from-indigo-500 to-indigo-600',
          bgColor: 'bg-indigo-50',
          borderColor: 'border-indigo-200'
        },
        {
          title: 'Brindes Entregues',
          description: 'Informar brindes entregues',
          icon: Gift,
          path: '/brindes',
          color: 'from-pink-500 to-pink-600',
          bgColor: 'bg-pink-50',
          borderColor: 'border-pink-200'
        },
        {
          title: 'Lista de Espera',
          description: user?.recepcao_id === '1002' ? 'Gerenciar lista de espera' : 'Visualizar lista de espera',
          icon: Clock,
          path: '/lista-espera',
          color: 'from-orange-500 to-orange-600',
          bgColor: 'bg-orange-50',
          borderColor: 'border-orange-200'
        },
        {
          title: 'Horários Vagos',
          description: 'Informar horários disponíveis',
          icon: Calendar,
          path: '/horarios-vagos',
          color: 'from-yellow-500 to-yellow-600',
          bgColor: 'bg-yellow-50',
          borderColor: 'border-yellow-200'
        }
      )

      // Módulos específicos por recepção
      if (user.recepcao_id === '103') {
        modules.push({
          title: 'Controle de Estoque',
          description: 'Controle de materiais',
          icon: Package,
          path: '/estoque',
          color: 'from-emerald-500 to-emerald-600',
          bgColor: 'bg-emerald-50',
          borderColor: 'border-emerald-200'
        })
      }

      if (['808', '108'].includes(user.recepcao_id || '')) {
        modules.push({
          title: 'Anamneses',
          description: 'Registro de anamneses',
          icon: ClipboardList,
          path: '/anamneses',
          color: 'from-violet-500 to-violet-600',
          bgColor: 'bg-violet-50',
          borderColor: 'border-violet-200'
        })
      }

      if (user.recepcao_id === '108') {
        modules.push({
          title: 'Visitas Externas',
          description: 'Controle de visitas externas',
          icon: Users,
          path: '/visitas',
          color: 'from-cyan-500 to-cyan-600',
          bgColor: 'bg-cyan-50',
          borderColor: 'border-cyan-200'
        })
      }
    }

    return modules
  }

  const modules = getAvailableModules()

  const getUserTypeDisplay = () => {
    if (isAdmin()) {
      return 'Administrador Geral'
    }
    return user?.recepcao_nome || 'Recepção'
  }

  const changePassword = () => {
    setShowPasswordModal(true)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Header estilo moderno */}
      <div className="bg-white shadow-lg border-b border-gray-200">
        <div className="container mx-auto px-6 py-6">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl flex items-center justify-center shadow-lg">
                <Home className="h-7 w-7 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Reception Sync</h1>
                <p className="text-gray-600 font-medium mt-1">{getUserTypeDisplay()}</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 bg-gray-100 rounded-full px-4 py-2">
                <User className="h-5 w-5 text-gray-600" />
                <span className="font-medium text-gray-700">{user?.username}</span>
              </div>
              <Button variant="outline" size="sm" onClick={changePassword} className="shadow-sm">
                <Settings className="h-4 w-4 mr-2" />
                Alterar Senha
              </Button>
              <Button variant="outline" size="sm" onClick={logout} className="shadow-sm">
                <LogOut className="h-4 w-4 mr-2" />
                Sair
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto p-6">
        {/* Welcome Section Melhorada */}
        <div className="mb-8">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-2xl shadow-xl p-8 text-white relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-white bg-opacity-10 rounded-full -mr-16 -mt-16"></div>
            <div className="absolute bottom-0 left-0 w-24 h-24 bg-white bg-opacity-10 rounded-full -ml-12 -mb-12"></div>
            <div className="relative z-10">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-3xl font-bold mb-3">
                    Bem-vindo, {user?.username}! 
                    <span className="inline-block ml-2">👋</span>
                  </h2>
                  <p className="text-blue-100 text-lg leading-relaxed">
                    {isAdmin() 
                      ? 'Painel administrativo com acesso completo ao sistema de gestão'
                      : `Painel da ${user?.recepcao_nome} - Gerencie suas atividades diárias`
                    }
                  </p>
                  <div className="flex items-center mt-4 space-x-6">
                    <div className="flex items-center space-x-2">
                      <Activity className="h-5 w-5 text-green-300" />
                      <span className="text-blue-100">Online</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Star className="h-5 w-5 text-yellow-300" />
                      <span className="text-blue-100">Sistema Ativo</span>
                    </div>
                  </div>
                </div>
                <div className="hidden md:block">
                  <div className="w-24 h-24 bg-white bg-opacity-20 rounded-2xl flex items-center justify-center backdrop-blur-sm">
                    <TrendingUp className="h-12 w-12 text-white" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Modules Grid Melhorado */}
        <div className="mb-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <Bell className="h-6 w-6 mr-3 text-blue-600" />
            Módulos Disponíveis
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {modules.map((module) => {
              const Icon = module.icon
              return (
                <Card key={module.path} className={`group hover:shadow-2xl transition-all duration-300 border-0 overflow-hidden ${module.bgColor} ${module.borderColor} border-2`}>
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <div className={`p-3 rounded-xl bg-gradient-to-r ${module.color} shadow-lg`}>
                        <Icon className="h-7 w-7 text-white" />
                      </div>
                      <ArrowRight className="h-5 w-5 text-gray-400 group-hover:text-gray-600 group-hover:translate-x-1 transition-all duration-300" />
                    </div>
                    <CardTitle className="text-xl group-hover:text-blue-700 transition-colors mt-4">
                      {module.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <CardDescription className="mb-4 text-gray-600 leading-relaxed">
                      {module.description}
                    </CardDescription>
                    <Link to={module.path}>
                      <Button className="w-full group-hover:scale-105 transition-all duration-300 shadow-md">
                        Acessar Módulo
                      </Button>
                    </Link>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </div>

        {/* Quick Stats para Recepções */}
        {!isAdmin() && (
          <div>
            <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <BarChart3 className="h-6 w-6 mr-3 text-green-600" />
              Resumo de Hoje
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200 border-2">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-blue-700 font-semibold mb-1">Salas Ativas</p>
                      <p className="text-3xl font-bold text-blue-900">--</p>
                      <p className="text-xs text-blue-600 mt-1">Em uso agora</p>
                    </div>
                    <div className="p-3 bg-blue-200 rounded-xl">
                      <Building2 className="h-8 w-8 text-blue-700" />
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="bg-gradient-to-br from-green-50 to-green-100 border-green-200 border-2">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-green-700 font-semibold mb-1">Orçamentos</p>
                      <p className="text-3xl font-bold text-green-900">--</p>
                      <p className="text-xs text-green-600 mt-1">Este mês</p>
                    </div>
                    <div className="p-3 bg-green-200 rounded-xl">
                      <FileText className="h-8 w-8 text-green-700" />
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200 border-2">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-purple-700 font-semibold mb-1">Pacientes</p>
                      <p className="text-3xl font-bold text-purple-900">--</p>
                      <p className="text-xs text-purple-600 mt-1">Hoje</p>
                    </div>
                    <div className="p-3 bg-purple-200 rounded-xl">
                      <Users className="h-8 w-8 text-purple-700" />
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200 border-2">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-orange-700 font-semibold mb-1">Lista Espera</p>
                      <p className="text-3xl font-bold text-orange-900">--</p>
                      <p className="text-xs text-orange-600 mt-1">Aguardando</p>
                    </div>
                    <div className="p-3 bg-orange-200 rounded-xl">
                      <Clock className="h-8 w-8 text-orange-700" />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}

        {/* Estatísticas para Admin */}
        {isAdmin() && (
          <div>
            <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <BarChart3 className="h-6 w-6 mr-3 text-green-600" />
              Visão Geral do Sistema
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card className="bg-gradient-to-br from-indigo-50 to-indigo-100 border-indigo-200 border-2">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-indigo-700 font-semibold mb-1">Total Usuários</p>
                      <p className="text-3xl font-bold text-indigo-900">--</p>
                      <p className="text-xs text-indigo-600 mt-1">Ativos no sistema</p>
                    </div>
                    <div className="p-3 bg-indigo-200 rounded-xl">
                      <UserPlus className="h-8 w-8 text-indigo-700" />
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="bg-gradient-to-br from-emerald-50 to-emerald-100 border-emerald-200 border-2">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-emerald-700 font-semibold mb-1">Salas Sistema</p>
                      <p className="text-3xl font-bold text-emerald-900">--</p>
                      <p className="text-xs text-emerald-600 mt-1">Todas as recepções</p>
                    </div>
                    <div className="p-3 bg-emerald-200 rounded-xl">
                      <Building2 className="h-8 w-8 text-emerald-700" />
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="bg-gradient-to-br from-rose-50 to-rose-100 border-rose-200 border-2">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-rose-700 font-semibold mb-1">Orçamentos</p>
                      <p className="text-3xl font-bold text-rose-900">--</p>
                      <p className="text-xs text-rose-600 mt-1">Todos os períodos</p>
                    </div>
                    <div className="p-3 bg-rose-200 rounded-xl">
                      <FileText className="h-8 w-8 text-rose-700" />
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="bg-gradient-to-br from-amber-50 to-amber-100 border-amber-200 border-2">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-amber-700 font-semibold mb-1">Recepções</p>
                      <p className="text-3xl font-bold text-amber-900">7</p>
                      <p className="text-xs text-amber-600 mt-1">Ativas</p>
                    </div>
                    <div className="p-3 bg-amber-200 rounded-xl">
                      <Users className="h-8 w-8 text-amber-700" />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </div>

      {/* Modal de Mudança de Senha */}
      {showPasswordModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-full max-w-md mx-4 shadow-2xl">
            <h3 className="text-xl font-bold mb-4 text-gray-900">Alterar Senha</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Nova Senha</label>
                <input 
                  type="password" 
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Digite sua nova senha"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Confirmar Senha</label>
                <input 
                  type="password" 
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Confirme sua nova senha"
                />
              </div>
              <div className="flex gap-3 pt-4">
                <Button className="flex-1">
                  Alterar Senha
                </Button>
                <Button 
                  variant="outline" 
                  className="flex-1"
                  onClick={() => setShowPasswordModal(false)}
                >
                  Cancelar
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default DashboardPage