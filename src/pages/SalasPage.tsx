import { useState, useEffect } from 'react'
import { 
  Building2, 
  Plus, 
  ArrowLeft, 
  Calendar, 
  Clock, 
  User, 
  Trash2, 
  Edit,
  MapPin,
  Users,
  CheckCircle,
  XCircle,
  AlertCircle,
  Filter,
  Search,
  Zap,
  Star,
  Settings,
  Eye
} from 'lucide-react'

const SalasPage = () => {
  const [userType, setUserType] = useState('admin') // 'admin' ou 'recepcao'
  const [viewMode, setViewMode] = useState('grid') // 'grid' ou 'calendar'
  const [filterStatus, setFilterStatus] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [editingSala, setEditingSala] = useState(null)
  const [selectedSala, setSelectedSala] = useState(null)
  const [formData, setFormData] = useState({
    nome: '',
    capacidade: '',
    terapeuta: '',
    periodo_inicio: '',
    periodo_fim: '',
    status: 'disponivel'
  })

  // Dados simulados das salas
  const [salas, setSalas] = useState([
    {
      id: 1,
      nome: 'Sala Fono 01',
      capacidade: 2,
      status: 'disponivel',
      recepcao_id: '103',
      recepcao_nome: 'Recepção 103',
      terapeuta: 'Dra. Maria Silva',
      periodo_inicio: '08:00',
      periodo_fim: '12:00',
      proxima_sessao: '14:00',
      tipo_terapia: 'Fonoaudiologia',
      equipamentos: ['Microfone', 'Espelho']
    },
    {
      id: 2,
      nome: 'Sala Fisio 02',
      capacidade: 4,
      status: 'ocupada',
      recepcao_id: '108',
      recepcao_nome: 'Recepção 108',
      terapeuta: 'Dr. João Santos',
      periodo_inicio: '09:00',
      periodo_fim: '18:00',
      ocupado_por: 'Pedro Oliveira',
      ocupado_ate: '16:30',
      tipo_terapia: 'Fisioterapia',
      equipamentos: ['Maca', 'Aparelhos']
    },
    {
      id: 3,
      nome: 'Sala TO 03',
      capacidade: 3,
      status: 'reservada',
      recepcao_id: '203',
      recepcao_nome: 'Recepção 203',
      terapeuta: 'Dra. Ana Costa',
      periodo_inicio: '13:00',
      periodo_fim: '17:00',
      proxima_sessao: '13:30',
      tipo_terapia: 'Terapia Ocupacional',
      equipamentos: ['Mesa adaptada', 'Jogos']
    },
    {
      id: 4,
      nome: 'Sala Psico 04',
      capacidade: 2,
      status: 'disponivel',
      recepcao_id: '808',
      recepcao_nome: 'Recepção 808',
      terapeuta: 'Dr. Carlos Lima',
      periodo_inicio: '10:00',
      periodo_fim: '16:00',
      tipo_terapia: 'Psicologia',
      equipamentos: ['Sofá', 'Mesa infantil']
    },
    {
      id: 5,
      nome: 'Sala Multi 05',
      capacidade: 6,
      status: 'manutencao',
      recepcao_id: '1002',
      recepcao_nome: 'Recepção 1002',
      tipo_terapia: 'Multidisciplinar',
      equipamentos: ['Projetor', 'Cadeiras']
    },
    {
      id: 6,
      nome: 'Sala Neuro 06',
      capacidade: 2,
      status: 'disponivel',
      recepcao_id: '1009',
      recepcao_nome: 'Recepção 1009',
      terapeuta: 'Dra. Lucia Fernandes',
      periodo_inicio: '08:30',
      periodo_fim: '12:30',
      tipo_terapia: 'Neuropsicologia',
      equipamentos: ['Computador', 'Testes']
    }
  ])

  const isAdmin = () => userType === 'admin'

  const getStatusColor = (status) => {
    switch (status) {
      case 'disponivel':
        return {
          bg: 'from-green-50 to-emerald-100',
          border: 'border-green-200',
          badge: 'bg-green-100 text-green-800',
          icon: CheckCircle,
          iconColor: 'text-green-500'
        }
      case 'ocupada':
        return {
          bg: 'from-red-50 to-rose-100',
          border: 'border-red-200',
          badge: 'bg-red-100 text-red-800',
          icon: XCircle,
          iconColor: 'text-red-500'
        }
      case 'reservada':
        return {
          bg: 'from-yellow-50 to-amber-100',
          border: 'border-yellow-200',
          badge: 'bg-yellow-100 text-yellow-800',
          icon: Clock,
          iconColor: 'text-yellow-500'
        }
      case 'manutencao':
        return {
          bg: 'from-gray-50 to-slate-100',
          border: 'border-gray-200',
          badge: 'bg-gray-100 text-gray-800',
          icon: Settings,
          iconColor: 'text-gray-500'
        }
      default:
        return {
          bg: 'from-blue-50 to-blue-100',
          border: 'border-blue-200',
          badge: 'bg-blue-100 text-blue-800',
          icon: Building2,
          iconColor: 'text-blue-500'
        }
    }
  }

  const getStatusText = (status) => {
    switch (status) {
      case 'disponivel': return 'Disponível'
      case 'ocupada': return 'Ocupada'
      case 'reservada': return 'Reservada'
      case 'manutencao': return 'Manutenção'
      default: return status
    }
  }

  const filteredSalas = salas.filter(sala => {
    const matchesStatus = filterStatus === 'all' || sala.status === filterStatus
    const matchesSearch = sala.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         sala.terapeuta?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         sala.tipo_terapia?.toLowerCase().includes(searchTerm.toLowerCase())
    return matchesStatus && matchesSearch
  })

  const handleReservar = (salaId) => {
    setSalas(salas.map(sala => 
      sala.id === salaId 
        ? { ...sala, status: 'reservada', ocupado_por: 'Admin Sistema' }
        : sala
    ))
  }

  const handleLiberar = (salaId) => {
    setSalas(salas.map(sala => 
      sala.id === salaId 
        ? { ...sala, status: 'disponivel', ocupado_por: null, ocupado_ate: null }
        : sala
    ))
  }

  const stats = {
    total: salas.length,
    disponivel: salas.filter(s => s.status === 'disponivel').length,
    ocupada: salas.filter(s => s.status === 'ocupada').length,
    reservada: salas.filter(s => s.status === 'reservada').length,
    manutencao: salas.filter(s => s.status === 'manutencao').length
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Header Moderno */}
      <div className="bg-white shadow-xl border-b border-gray-200">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button className="flex items-center space-x-2 bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-lg transition-colors">
                <ArrowLeft className="h-4 w-4 text-gray-600" />
                <span className="text-sm font-medium text-gray-700">Voltar</span>
              </button>
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl flex items-center justify-center shadow-lg">
                  <Building2 className="h-7 w-7 text-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">
                    {isAdmin() ? 'Sistema de Agendamento de Salas' : 'Gerenciar Salas'}
                  </h1>
                  <p className="text-gray-600">
                    {isAdmin() ? 'Visualize e reserve salas disponíveis' : 'Cadastre e gerencie salas da recepção'}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              {!isAdmin() && (
                <button
                  onClick={() => setShowForm(!showForm)}
                  className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors shadow-lg"
                >
                  <Plus className="h-4 w-4" />
                  <span className="font-medium">Nova Sala</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto p-6">
        {/* Estatísticas em Cards Modernos */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          <div className="bg-white rounded-xl p-4 shadow-lg border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 font-medium">Total</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
              </div>
              <Building2 className="h-8 w-8 text-blue-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-green-50 to-emerald-100 rounded-xl p-4 shadow-lg border border-green-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-700 font-medium">Disponíveis</p>
                <p className="text-2xl font-bold text-green-900">{stats.disponivel}</p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-red-50 to-rose-100 rounded-xl p-4 shadow-lg border border-red-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-red-700 font-medium">Ocupadas</p>
                <p className="text-2xl font-bold text-red-900">{stats.ocupada}</p>
              </div>
              <XCircle className="h-8 w-8 text-red-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-yellow-50 to-amber-100 rounded-xl p-4 shadow-lg border border-yellow-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-yellow-700 font-medium">Reservadas</p>
                <p className="text-2xl font-bold text-yellow-900">{stats.reservada}</p>
              </div>
              <Clock className="h-8 w-8 text-yellow-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-gray-50 to-slate-100 rounded-xl p-4 shadow-lg border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-700 font-medium">Manutenção</p>
                <p className="text-2xl font-bold text-gray-900">{stats.manutencao}</p>
              </div>
              <Settings className="h-8 w-8 text-gray-500" />
            </div>
          </div>
        </div>

        {/* Filtros e Busca */}
        <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 mb-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
            <div className="flex items-center space-x-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <input
                  type="text"
                  placeholder="Buscar salas, terapeutas..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <div className="flex items-center space-x-2">
                <Filter className="h-4 w-4 text-gray-500" />
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="all">Todos os Status</option>
                  <option value="disponivel">Disponível</option>
                  <option value="ocupada">Ocupada</option>
                  <option value="reservada">Reservada</option>
                  <option value="manutencao">Manutenção</option>
                </select>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-600">Exibindo {filteredSalas.length} de {salas.length} salas</span>
            </div>
          </div>
        </div>

        {/* Grid de Salas - Estilo Sistema de Agendamento */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredSalas.map((sala) => {
            const statusConfig = getStatusColor(sala.status)
            const StatusIcon = statusConfig.icon
            
            return (
              <div
                key={sala.id}
                className={`group relative overflow-hidden rounded-2xl shadow-xl transition-all duration-300 hover:shadow-2xl hover:scale-105 bg-gradient-to-br ${statusConfig.bg} border-2 ${statusConfig.border}`}
              >
                <div className="p-6">
                  {/* Header da Sala */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className={`p-2 rounded-xl bg-white shadow-sm`}>
                        <StatusIcon className={`h-6 w-6 ${statusConfig.iconColor}`} />
                      </div>
                      <div>
                        <h3 className="text-lg font-bold text-gray-900">{sala.nome}</h3>
                        <p className="text-sm text-gray-600">{sala.tipo_terapia}</p>
                      </div>
                    </div>
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${statusConfig.badge}`}>
                      {getStatusText(sala.status)}
                    </span>
                  </div>

                  {/* Informações da Sala */}
                  <div className="space-y-3 mb-4">
                    <div className="flex items-center text-sm text-gray-700">
                      <Users className="h-4 w-4 mr-2 text-gray-500" />
                      <span>Capacidade: <strong>{sala.capacidade} pessoas</strong></span>
                    </div>
                    
                    {sala.terapeuta && (
                      <div className="flex items-center text-sm text-gray-700">
                        <User className="h-4 w-4 mr-2 text-gray-500" />
                        <span>{sala.terapeuta}</span>
                      </div>
                    )}
                    
                    {sala.periodo_inicio && sala.periodo_fim && (
                      <div className="flex items-center text-sm text-gray-700">
                        <Clock className="h-4 w-4 mr-2 text-gray-500" />
                        <span>{sala.periodo_inicio} - {sala.periodo_fim}</span>
                      </div>
                    )}
                    
                    <div className="flex items-center text-sm text-gray-600">
                      <MapPin className="h-4 w-4 mr-2 text-gray-500" />
                      <span>{sala.recepcao_nome}</span>
                    </div>
                  </div>

                  {/* Status específico */}
                  {sala.status === 'ocupada' && sala.ocupado_por && (
                    <div className="bg-red-50 rounded-lg p-3 mb-4 border border-red-100">
                      <p className="text-sm text-red-800">
                        <strong>Ocupado por:</strong> {sala.ocupado_por}
                      </p>
                      {sala.ocupado_ate && (
                        <p className="text-xs text-red-600 mt-1">
                          Até {sala.ocupado_ate}
                        </p>
                      )}
                    </div>
                  )}

                  {sala.status === 'disponivel' && sala.proxima_sessao && (
                    <div className="bg-green-50 rounded-lg p-3 mb-4 border border-green-100">
                      <p className="text-sm text-green-800">
                        <strong>Próxima sessão:</strong> {sala.proxima_sessao}
                      </p>
                    </div>
                  )}

                  {/* Equipamentos */}
                  {sala.equipamentos && sala.equipamentos.length > 0 && (
                    <div className="mb-4">
                      <p className="text-xs text-gray-600 mb-2">Equipamentos:</p>
                      <div className="flex flex-wrap gap-1">
                        {sala.equipamentos.map((equip, index) => (
                          <span
                            key={index}
                            className="px-2 py-1 bg-white bg-opacity-60 rounded-full text-xs text-gray-700 border border-gray-200"
                          >
                            {equip}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Ações */}
                  <div className="space-y-2">
                    {isAdmin() && (
                      <>
                        {sala.status === 'disponivel' && (
                          <button
                            onClick={() => handleReservar(sala.id)}
                            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center justify-center space-x-2"
                          >
                            <Calendar className="h-4 w-4" />
                            <span>Reservar Sala</span>
                          </button>
                        )}
                        
                        {sala.status === 'reservada' && (
                          <button
                            onClick={() => handleLiberar(sala.id)}
                            className="w-full bg-green-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-green-700 transition-colors flex items-center justify-center space-x-2"
                          >
                            <CheckCircle className="h-4 w-4" />
                            <span>Liberar Sala</span>
                          </button>
                        )}
                        
                        <button
                          onClick={() => setSelectedSala(sala)}
                          className="w-full bg-gray-100 text-gray-700 py-2 px-4 rounded-lg font-medium hover:bg-gray-200 transition-colors flex items-center justify-center space-x-2"
                        >
                          <Eye className="h-4 w-4" />
                          <span>Ver Detalhes</span>
                        </button>
                      </>
                    )}
                    
                    {!isAdmin() && (
                      <div className="flex gap-2">
                        <button
                          onClick={() => setEditingSala(sala)}
                          className="flex-1 bg-blue-100 text-blue-700 py-2 px-3 rounded-lg font-medium hover:bg-blue-200 transition-colors flex items-center justify-center space-x-1"
                        >
                          <Edit className="h-4 w-4" />
                          <span>Editar</span>
                        </button>
                        <button className="flex-1 bg-red-100 text-red-700 py-2 px-3 rounded-lg font-medium hover:bg-red-200 transition-colors flex items-center justify-center space-x-1">
                          <Trash2 className="h-4 w-4" />
                          <span>Excluir</span>
                        </button>
                      </div>
                    )}
                  </div>
                </div>

                {/* Indicador de destaque para salas em destaque */}
                {sala.status === 'disponivel' && (
                  <div className="absolute top-2 right-2">
                    <Star className="h-5 w-5 text-yellow-400 fill-current" />
                  </div>
                )}
              </div>
            )
          })}
        </div>

        {filteredSalas.length === 0 && (
          <div className="bg-white rounded-xl p-12 shadow-lg border border-gray-100 text-center">
            <Building2 className="h-16 w-16 mx-auto text-gray-400 mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Nenhuma sala encontrada</h3>
            <p className="text-gray-600 mb-4">
              {searchTerm || filterStatus !== 'all' 
                ? 'Tente ajustar os filtros de busca'
                : 'Ainda não há salas cadastradas no sistema'
              }
            </p>
            {!isAdmin() && (
              <button
                onClick={() => setShowForm(true)}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors"
              >
                Cadastrar Primeira Sala
              </button>
            )}
          </div>
        )}
      </div>

      {/* Modal de Detalhes da Sala */}
      {selectedSala && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-md w-full shadow-2xl">
            <div className="p-6">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-xl font-bold text-gray-900">{selectedSala.nome}</h3>
                  <p className="text-gray-600">{selectedSala.tipo_terapia}</p>
                </div>
                <button 
                  onClick={() => setSelectedSala(null)}
                  className="text-gray-400 hover:text-gray-600 p-1"
                >
                  <XCircle className="h-6 w-6" />
                </button>
              </div>
              
              <div className="space-y-4">
                <div className="bg-gray-50 rounded-lg p-4">
                  <h4 className="font-semibold text-gray-900 mb-2">Informações da Sala</h4>
                  <div className="space-y-2 text-sm">
                    <div>
                      <span className="text-gray-600">Status:</span>
                      <span className={`ml-2 px-2 py-1 rounded-full text-xs font-semibold ${getStatusColor(selectedSala.status).badge}`}>
                        {getStatusText(selectedSala.status)}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-600">Capacidade:</span>
                      <span className="ml-2 font-medium">{selectedSala.capacidade} pessoas</span>
                    </div>
                    {selectedSala.terapeuta && (
                      <div>
                        <span className="text-gray-600">Terapeuta:</span>
                        <span className="ml-2 font-medium">{selectedSala.terapeuta}</span>
                      </div>
                    )}
                    <div>
                      <span className="text-gray-600">Recepção:</span>
                      <span className="ml-2 font-medium">{selectedSala.recepcao_nome}</span>
                    </div>
                  </div>
                </div>
                
                {selectedSala.equipamentos && selectedSala.equipamentos.length > 0 && (
                  <div className="bg-blue-50 rounded-lg p-4">
                    <h4 className="font-semibold text-gray-900 mb-2">Equipamentos</h4>
                    <div className="flex flex-wrap gap-2">
                      {selectedSala.equipamentos.map((equip, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
                        >
                          {equip}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
              
              <div className="mt-6 pt-4 border-t border-gray-200">
                <button
                  onClick={() => setSelectedSala(null)}
                  className="w-full bg-gray-100 text-gray-700 py-2 px-4 rounded-lg font-medium hover:bg-gray-200 transition-colors"
                >
                  Fechar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default SalasPage