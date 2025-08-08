import { useState, useEffect } from 'react'
import { 
  ClipboardList, 
  Plus, 
  ArrowLeft, 
  User, 
  Calendar,
  Clock,
  FileText,
  Stethoscope,
  Users,
  TrendingUp,
  BarChart3,
  Search,
  Filter,
  Edit,
  Trash2,
  Eye,
  X,
  CheckCircle,
  AlertCircle,
  Phone,
  MapPin
} from 'lucide-react'

const AnamnesesPage = () => {
  // Simulação de dados do usuário logado (na implementação real virá do contexto de auth)
  const [user] = useState({
    username: 'Recepção 808',
    role: 'recepcao',
    recepcao_nome: 'Recepção 808',
    recepcao_id: '808'
  })
  
  const [showForm, setShowForm] = useState(false)
  const [editingAnamnese, setEditingAnamnese] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterMes, setFilterMes] = useState('all')
  const [filterProfissional, setFilterProfissional] = useState('all')
  const [selectedAnamnese, setSelectedAnamnese] = useState(null)

  // Dados das Anamneses
  const [anamneses, setAnamneses] = useState([
    {
      id: 1,
      nome_pais: 'Carlos e Maria Silva',
      nome_paciente: 'Ana Clara Silva',
      data_anamnese: '2024-08-01',
      profissional: 'Dra. Patricia Santos',
      tipo_anamnese: 'Inicial',
      idade_paciente: '5 anos',
      motivo_consulta: 'Atraso na linguagem',
      observacoes: 'Criança comunicativa, mas com dificuldades articulatórias',
      contato_responsavel: '(11) 99999-9999',
      recepcao_id: '808',
      recepcao_nome: 'Recepção 808',
      status: 'agendada',
      created_at: '2024-07-28',
      created_by: 'recepcao808'
    },
    {
      id: 2,
      nome_pais: 'João e Ana Oliveira',
      nome_paciente: 'Pedro Oliveira',
      data_anamnese: '2024-08-02',
      profissional: 'Dr. Roberto Lima',
      tipo_anamnese: 'Reavaliação',
      idade_paciente: '8 anos',
      motivo_consulta: 'Acompanhamento terapêutico',
      observacoes: 'Paciente em tratamento há 6 meses',
      contato_responsavel: '(11) 88888-8888',
      recepcao_id: '808',
      recepcao_nome: 'Recepção 808',
      status: 'realizada',
      created_at: '2024-07-29',
      created_by: 'recepcao808'
    },
    {
      id: 3,
      nome_pais: 'Marcos e Lucia Costa',
      nome_paciente: 'Gabriel Costa',
      data_anamnese: '2024-08-03',
      profissional: 'Dra. Fernanda Mendes',
      tipo_anamnese: 'Inicial',
      idade_paciente: '3 anos',
      motivo_consulta: 'Avaliação comportamental',
      observacoes: 'Encaminhado pela escola',
      contato_responsavel: '(11) 77777-7777',
      recepcao_id: '808',
      recepcao_nome: 'Recepção 808',
      status: 'agendada',
      created_at: '2024-07-30',
      created_by: 'recepcao808'
    }
  ])

  const profissionais = [
    'Dra. Patricia Santos',
    'Dr. Roberto Lima', 
    'Dra. Fernanda Mendes',
    'Dr. Carlos Andrade',
    'Dra. Mariana Silva',
    'Dr. Paulo Rodrigues'
  ]

  const tiposAnamnese = [
    'Inicial',
    'Reavaliação',
    'Complementar',
    'Seguimento'
  ]

  // Verificar se o usuário pode acessar anamneses
  const canAccessAnamneses = () => {
    return ['808', '108'].includes(user?.recepcao_id || '') || 
           user?.role === 'admin' || 
           user?.role === 'admin_geral'
  }

  // Filtrar anamneses da recepção do usuário (ou todas se for admin)
  const anamnesesFiltradas = anamneses.filter(anamnese => {
    const pertenceRecepcao = user?.role === 'admin' || user?.role === 'admin_geral' || 
                            anamnese.recepcao_id === user?.recepcao_id
    
    const matchesSearch = anamnese.nome_paciente.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         anamnese.nome_pais.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         anamnese.profissional.toLowerCase().includes(searchTerm.toLowerCase())
    
    const dataAnamnese = new Date(anamnese.data_anamnese)
    const hoje = new Date()
    const matchesMes = filterMes === 'all' || 
                      (filterMes === 'current' && dataAnamnese.getMonth() === hoje.getMonth()) ||
                      (filterMes === 'next' && dataAnamnese.getMonth() === hoje.getMonth() + 1)
    
    const matchesProfissional = filterProfissional === 'all' || anamnese.profissional === filterProfissional
    
    return pertenceRecepcao && matchesSearch && matchesMes && matchesProfissional
  })

  // Estatísticas
  const stats = {
    totalAnamneses: anamnesesFiltradas.length,
    agendadas: anamnesesFiltradas.filter(a => a.status === 'agendada').length,
    realizadas: anamnesesFiltradas.filter(a => a.status === 'realizada').length,
    esteMes: anamnesesFiltradas.filter(a => {
      const dataAnamnese = new Date(a.data_anamnese)
      const hoje = new Date()
      return dataAnamnese.getMonth() === hoje.getMonth() && dataAnamnese.getFullYear() === hoje.getFullYear()
    }).length,
    proximoMes: anamnesesFiltradas.filter(a => {
      const dataAnamnese = new Date(a.data_anamnese)
      const proximoMes = new Date()
      proximoMes.setMonth(proximoMes.getMonth() + 1)
      return dataAnamnese.getMonth() === proximoMes.getMonth() && dataAnamnese.getFullYear() === proximoMes.getFullYear()
    }).length,
    profissionaisAtivos: [...new Set(anamnesesFiltradas.map(a => a.profissional))].length
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'agendada':
        return 'bg-blue-100 text-blue-800'
      case 'realizada':
        return 'bg-green-100 text-green-800'
      case 'cancelada':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getStatusText = (status) => {
    switch (status) {
      case 'agendada': return 'Agendada'
      case 'realizada': return 'Realizada'
      case 'cancelada': return 'Cancelada'
      default: return status
    }
  }

  const FormAnamnese = () => {
    const [formData, setFormData] = useState({
      nome_pais: '',
      nome_paciente: '',
      data_anamnese: '',
      profissional: '',
      tipo_anamnese: 'Inicial',
      idade_paciente: '',
      motivo_consulta: '',
      observacoes: '',
      contato_responsavel: ''
    })

    useEffect(() => {
      if (editingAnamnese) {
        setFormData(editingAnamnese)
      }
    }, [editingAnamnese])

    const handleSubmit = (e) => {
      e.preventDefault()
      
      if (editingAnamnese) {
        setAnamneses(anamneses.map(anamnese => 
          anamnese.id === editingAnamnese.id 
            ? { ...formData, id: editingAnamnese.id, updated_at: new Date().toISOString() }
            : anamnese
        ))
        setEditingAnamnese(null)
      } else {
        const novaAnamnese = {
          id: Date.now(),
          ...formData,
          recepcao_id: user?.recepcao_id || '808',
          recepcao_nome: user?.recepcao_nome || 'Recepção 808',
          status: 'agendada',
          created_at: new Date().toISOString(),
          created_by: user?.username || 'usuario'
        }
        setAnamneses([novaAnamnese, ...anamneses])
      }
      
      setShowForm(false)
      setFormData({
        nome_pais: '',
        nome_paciente: '',
        data_anamnese: '',
        profissional: '',
        tipo_anamnese: 'Inicial',
        idade_paciente: '',
        motivo_consulta: '',
        observacoes: '',
        contato_responsavel: ''
      })
    }

    return (
      <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 mb-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h3 className="text-lg font-bold text-gray-900">
              {editingAnamnese ? 'Editar Anamnese' : 'Registrar Nova Anamnese'}
            </h3>
            <p className="text-gray-600">Preencha os dados do solicitante da anamnese</p>
          </div>
          <button
            onClick={() => {
              setShowForm(false)
              setEditingAnamnese(null)
            }}
            className="text-gray-400 hover:text-gray-600 p-2"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Nome dos Pais</label>
              <input
                type="text"
                value={formData.nome_pais}
                onChange={(e) => setFormData({ ...formData, nome_pais: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Nome completo dos pais"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Nome do Paciente</label>
              <input
                type="text"
                value={formData.nome_paciente}
                onChange={(e) => setFormData({ ...formData, nome_paciente: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Nome completo do paciente"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Data da Anamnese</label>
              <input
                type="date"
                value={formData.data_anamnese}
                onChange={(e) => setFormData({ ...formData, data_anamnese: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Profissional</label>
              <select
                value={formData.profissional}
                onChange={(e) => setFormData({ ...formData, profissional: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="">Selecione o profissional</option>
                {profissionais.map(prof => (
                  <option key={prof} value={prof}>{prof}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Tipo de Anamnese</label>
              <select
                value={formData.tipo_anamnese}
                onChange={(e) => setFormData({ ...formData, tipo_anamnese: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {tiposAnamnese.map(tipo => (
                  <option key={tipo} value={tipo}>{tipo}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Idade do Paciente</label>
              <input
                type="text"
                value={formData.idade_paciente}
                onChange={(e) => setFormData({ ...formData, idade_paciente: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Ex: 5 anos, 18 meses"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Contato do Responsável</label>
              <input
                type="tel"
                value={formData.contato_responsavel}
                onChange={(e) => setFormData({ ...formData, contato_responsavel: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="(11) 99999-9999"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Motivo da Consulta</label>
              <input
                type="text"
                value={formData.motivo_consulta}
                onChange={(e) => setFormData({ ...formData, motivo_consulta: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Breve descrição do motivo"
                required
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Observações</label>
            <textarea
              value={formData.observacoes}
              onChange={(e) => setFormData({ ...formData, observacoes: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows="3"
              placeholder="Informações adicionais relevantes"
            />
          </div>
          <div className="flex gap-3 pt-4">
            <button
              onClick={handleSubmit}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center space-x-2"
            >
              <CheckCircle className="h-4 w-4" />
              <span>{editingAnamnese ? 'Atualizar' : 'Registrar'}</span>
            </button>
            <button
              onClick={() => {
                setShowForm(false)
                setEditingAnamnese(null)
              }}
              className="border border-gray-300 text-gray-700 px-6 py-2 rounded-lg font-medium hover:bg-gray-50 transition-colors"
            >
              Cancelar
            </button>
          </div>
        </div>
      </div>
    )
  }

  // Verificação de acesso
  if (!canAccessAnamneses()) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="bg-white rounded-xl p-8 shadow-lg border border-gray-100 text-center max-w-md">
          <AlertCircle className="h-16 w-16 mx-auto text-red-500 mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Acesso Negado</h3>
          <p className="text-gray-600 mb-4">
            O módulo de anamneses está disponível apenas para as recepções 808 e 108.
          </p>
          <button
            onClick={() => window.history.back()}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Voltar
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white shadow-lg border-b border-gray-200">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button className="flex items-center space-x-2 bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-lg transition-colors">
                <ArrowLeft className="h-4 w-4 text-gray-600" />
                <span className="text-sm font-medium text-gray-700">Voltar</span>
              </button>
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-gradient-to-br from-violet-600 to-purple-700 rounded-xl flex items-center justify-center shadow-lg">
                  <ClipboardList className="h-7 w-7 text-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">
                    Anamneses - {user?.recepcao_nome}
                  </h1>
                  <p className="text-gray-600">Lançamento de solicitantes de anamnese</p>
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setShowForm(!showForm)}
                className="flex items-center space-x-2 bg-violet-600 text-white px-4 py-2 rounded-lg hover:bg-violet-700 transition-colors shadow-lg"
              >
                <Plus className="h-4 w-4" />
                <span className="font-medium">Nova Anamnese</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto p-6">
        {/* Estatísticas */}
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
          <div className="bg-gradient-to-br from-violet-50 to-purple-100 rounded-xl p-4 shadow-lg border border-violet-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-violet-700 font-medium">Total</p>
                <p className="text-2xl font-bold text-violet-900">{stats.totalAnamneses}</p>
              </div>
              <ClipboardList className="h-8 w-8 text-violet-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-4 shadow-lg border border-blue-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-700 font-medium">Agendadas</p>
                <p className="text-2xl font-bold text-blue-900">{stats.agendadas}</p>
              </div>
              <Calendar className="h-8 w-8 text-blue-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-4 shadow-lg border border-green-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-700 font-medium">Realizadas</p>
                <p className="text-2xl font-bold text-green-900">{stats.realizadas}</p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl p-4 shadow-lg border border-orange-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-orange-700 font-medium">Este Mês</p>
                <p className="text-2xl font-bold text-orange-900">{stats.esteMes}</p>
              </div>
              <Clock className="h-8 w-8 text-orange-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-teal-50 to-teal-100 rounded-xl p-4 shadow-lg border border-teal-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-teal-700 font-medium">Próximo Mês</p>
                <p className="text-2xl font-bold text-teal-900">{stats.proximoMes}</p>
              </div>
              <TrendingUp className="h-8 w-8 text-teal-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-indigo-50 to-indigo-100 rounded-xl p-4 shadow-lg border border-indigo-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-indigo-700 font-medium">Profissionais</p>
                <p className="text-2xl font-bold text-indigo-900">{stats.profissionaisAtivos}</p>
              </div>
              <Stethoscope className="h-8 w-8 text-indigo-500" />
            </div>
          </div>
        </div>

        {/* Filtros */}
        <div className="bg-white rounded-xl p-4 shadow-lg border border-gray-100 mb-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
            <div className="flex items-center space-x-4">
              <div className="relative flex-1 md:w-80">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <input
                  type="text"
                  placeholder="Buscar pacientes, pais ou profissionais..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <div className="flex items-center space-x-2">
                <Filter className="h-4 w-4 text-gray-500" />
                <select
                  value={filterMes}
                  onChange={(e) => setFilterMes(e.target.value)}
                  className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="all">Todos os Meses</option>
                  <option value="current">Este Mês</option>
                  <option value="next">Próximo Mês</option>
                </select>
              </div>
              
              <div>
                <select
                  value={filterProfissional}
                  onChange={(e) => setFilterProfissional(e.target.value)}
                  className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="all">Todos Profissionais</option>
                  {profissionais.map(prof => (
                    <option key={prof} value={prof}>{prof}</option>
                  ))}
                </select>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-600">
                Exibindo {anamnesesFiltradas.length} anamnese{anamnesesFiltradas.length !== 1 ? 's' : ''}
              </span>
            </div>
          </div>
        </div>

        {/* Formulário */}
        {showForm && <FormAnamnese />}

        {/* Grid de Anamneses */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {anamnesesFiltradas.map((anamnese) => (
            <div key={anamnese.id} className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-violet-100 rounded-xl flex items-center justify-center">
                    <ClipboardList className="h-6 w-6 text-violet-600" />
                  </div>
                  <div>
                    <h3 className="font-bold text-gray-900">{anamnese.nome_paciente}</h3>
                    <p className="text-sm text-gray-600">{anamnese.idade_paciente}</p>
                  </div>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getStatusColor(anamnese.status)}`}>
                  {getStatusText(anamnese.status)}
                </span>
              </div>
              
              <div className="space-y-3 mb-4">
                <div className="bg-gray-50 rounded-lg p-3">
                  <p className="text-sm">
                    <strong className="text-gray-700">Pais:</strong> {anamnese.nome_pais}
                  </p>
                  <p className="text-sm mt-1">
                    <strong className="text-gray-700">Tipo:</strong> {anamnese.tipo_anamnese}
                  </p>
                </div>
                
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Data:</span>
                    <span className="font-medium">{new Date(anamnese.data_anamnese).toLocaleDateString('pt-BR')}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Profissional:</span>
                    <span className="font-medium">{anamnese.profissional}</span>
                  </div>
                  {anamnese.contato_responsavel && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Contato:</span>
                      <span className="font-medium">{anamnese.contato_responsavel}</span>
                    </div>
                  )}
                </div>
                
                <div className="bg-blue-50 rounded-lg p-3">
                  <p className="text-sm text-blue-800">
                    <strong>Motivo:</strong> {anamnese.motivo_consulta}
                  </p>
                </div>
                
                {anamnese.observacoes && (
                  <div className="bg-yellow-50 rounded-lg p-3">
                    <p className="text-xs text-yellow-800">
                      <strong>Obs:</strong> {anamnese.observacoes}
                    </p>
                  </div>
                )}
              </div>
              
              <div className="flex gap-2">
                <button
                  onClick={() => {
                    setEditingAnamnese(anamnese)
                    setShowForm(true)
                  }}
                  className="flex-1 bg-blue-100 text-blue-700 py-2 px-3 rounded-lg font-medium hover:bg-blue-200 transition-colors flex items-center justify-center space-x-1"
                >
                  <Edit className="h-4 w-4" />
                  <span>Editar</span>
                </button>
                <button
                  onClick={() => setSelectedAnamnese(anamnese)}
                  className="flex-1 bg-gray-100 text-gray-700 py-2 px-3 rounded-lg font-medium hover:bg-gray-200 transition-colors flex items-center justify-center space-x-1"
                >
                  <Eye className="h-4 w-4" />
                  <span>Ver</span>
                </button>
                <button className="bg-red-100 text-red-700 py-2 px-3 rounded-lg font-medium hover:bg-red-200 transition-colors">
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Estado vazio */}
        {anamnesesFiltradas.length === 0 && (
          <div className="bg-white rounded-xl p-12 shadow-lg border border-gray-100 text-center">
            <ClipboardList className="h-16 w-16 mx-auto text-gray-400 mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Nenhuma anamnese encontrada</h3>
            <p className="text-gray-600 mb-4">
              {searchTerm || filterMes !== 'all' || filterProfissional !== 'all'
                ? 'Tente ajustar os filtros de busca'
                : 'Ainda não há anamneses registradas'
              }
            </p>
            {!searchTerm && filterMes === 'all' && filterProfissional === 'all' && (
              <button
                onClick={() => setShowForm(true)}
                className="bg-violet-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-violet-700 transition-colors"
              >
                Registrar Primeira Anamnese
              </button>
            )}
          </div>
        )}
      </div>

      {/* Modal de Detalhes */}
      {selectedAnamnese && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-md w-full shadow-2xl">
            <div className="p-6">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-xl font-bold text-gray-900">{selectedAnamnese.nome_paciente}</h3>
                  <p className="text-gray-600">{selectedAnamnese.tipo_anamnese}</p>
                </div>
                <button 
                  onClick={() => setSelectedAnamnese(null)}
                  className="text-gray-400 hover:text-gray-600 p-1"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>
              
              <div className="space-y-4">
                <div className="bg-gray-50 rounded-lg p-4">
                  <h4 className="font-semibold text-gray-900 mb-3">Informações Gerais</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Pais:</span>
                      <span className="font-medium">{selectedAnamnese.nome_pais}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Idade:</span>
                      <span className="font-medium">{selectedAnamnese.idade_paciente}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Data:</span>
                      <span className="font-medium">{new Date(selectedAnamnese.data_anamnese).toLocaleDateString('pt-BR')}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Profissional:</span>
                      <span className="font-medium">{selectedAnamnese.profissional}</span>
                    </div>
                    {selectedAnamnese.contato_responsavel && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">Contato:</span>
                        <span className="font-medium">{selectedAnamnese.contato_responsavel}</span>
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="bg-blue-50 rounded-lg p-4">
                  <h4 className="font-semibold text-gray-900 mb-2">Motivo da Consulta</h4>
                  <p className="text-sm text-gray-700">{selectedAnamnese.motivo_consulta}</p>
                </div>
                
                {selectedAnamnese.observacoes && (
                  <div className="bg-yellow-50 rounded-lg p-4">
                    <h4 className="font-semibold text-gray-900 mb-2">Observações</h4>
                    <p className="text-sm text-gray-700">{selectedAnamnese.observacoes}</p>
                  </div>
                )}
              </div>
              
              <div className="mt-6 pt-4 border-t border-gray-200">
                <button
                  onClick={() => setSelectedAnamnese(null)}
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

export default AnamnesesPage