import { useState, useEffect } from 'react'
import { 
  Clock, 
  Plus, 
  ArrowLeft, 
  Edit, 
  Trash2,
  Calendar,
  User,
  AlertCircle,
  CheckCircle,
  Search,
  Filter,
  Bell,
  TrendingUp,
  Users,
  Heart,
  Star,
  X,
  Eye,
  UserCheck,
  Zap
} from 'lucide-react'

const ListaEsperaPage = () => {
  const [userType, setUserType] = useState('1002') // '1002' para controle total, outras para visualização
  const [activeTab, setActiveTab] = useState('lista') // 'lista', 'horarios', 'matches'
  const [showForm, setShowForm] = useState(false)
  const [showHorarioForm, setShowHorarioForm] = useState(false)
  const [editingItem, setEditingItem] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterEspecialidade, setFilterEspecialidade] = useState('all')
  const [matches, setMatches] = useState([])

  // Dados da Lista de Espera
  const [listaEspera, setListaEspera] = useState([
    {
      id: 1,
      nome_paciente: 'Ana Clara Santos',
      especialidade: 'Fonoaudiologia',
      terapeuta_preferencia: 'Dra. Maria Silva',
      turno_preferencia: 'Manhã',
      data_solicitacao: '2024-07-15',
      quem_solicitou: 'Recepcao 103',
      observacoes: 'Criança com dificuldade na fala',
      status: 'aguardando',
      prioridade: 'alta',
      tempo_espera_dias: 15,
      contato_responsavel: '(11) 99999-9999'
    },
    {
      id: 2,
      nome_paciente: 'João Pedro Lima',
      especialidade: 'Fisioterapia',
      terapeuta_preferencia: 'Dr. Carlos Oliveira',
      turno_preferencia: 'Tarde',
      data_solicitacao: '2024-07-20',
      quem_solicitou: 'Recepcao 108',
      observacoes: 'Reabilitação pós-cirúrgica',
      status: 'aguardando',
      prioridade: 'media',
      tempo_espera_dias: 10,
      contato_responsavel: '(11) 88888-8888'
    },
    {
      id: 3,
      nome_paciente: 'Maria Eduarda Costa',
      especialidade: 'Terapia Ocupacional',
      terapeuta_preferencia: '',
      turno_preferencia: 'Qualquer horário',
      data_solicitacao: '2024-07-25',
      quem_solicitou: 'Recepcao 203',
      observacoes: 'Desenvolvimento motor',
      status: 'aguardando',
      prioridade: 'baixa',
      tempo_espera_dias: 5,
      contato_responsavel: '(11) 77777-7777'
    }
  ])

  // Dados de Horários Vagos
  const [horariosVagos, setHorariosVagos] = useState([
    {
      id: 1,
      especialidade: 'Fonoaudiologia',
      terapeuta: 'Dra. Maria Silva',
      data_disponivel: '2024-08-01',
      hora_inicio: '09:00',
      hora_fim: '10:00',
      sala: 'Sala Fono 01',
      turno: 'Manhã',
      observacoes: 'Horário liberado por cancelamento',
      created_by: 'recepcao103',
      status: 'disponivel'
    },
    {
      id: 2,
      especialidade: 'Fisioterapia',
      terapeuta: 'Dr. Carlos Oliveira',
      data_disponivel: '2024-08-02',
      hora_inicio: '14:00',
      hora_fim: '15:00',
      sala: 'Sala Fisio 02',
      turno: 'Tarde',
      observacoes: '',
      created_by: 'recepcao108',
      status: 'disponivel'
    }
  ])

  const especialidades = [
    'Fonoaudiologia',
    'Fisioterapia', 
    'Terapia Ocupacional',
    'Psicologia',
    'Psicopedagogia',
    'Neuropsicologia',
    'Musicoterapia'
  ]

  const turnos = ['Manhã', 'Tarde', 'Noite', 'Qualquer horário']

  const canEdit = () => userType === '1002' || userType === 'admin'

  // Calcular matches automaticamente
  useEffect(() => {
    const newMatches = []
    
    horariosVagos.forEach(horario => {
      const matchingPacientes = listaEspera.filter(paciente => 
        paciente.status === 'aguardando' &&
        paciente.especialidade === horario.especialidade &&
        (paciente.turno_preferencia === 'Qualquer horário' || 
         paciente.turno_preferencia === horario.turno) &&
        (!paciente.terapeuta_preferencia || 
         paciente.terapeuta_preferencia === horario.terapeuta)
      )
      
      if (matchingPacientes.length > 0) {
        newMatches.push({
          horario,
          pacientes: matchingPacientes.sort((a, b) => {
            // Ordenar por prioridade e tempo de espera
            const prioridadeOrder = { 'alta': 3, 'media': 2, 'baixa': 1 }
            if (prioridadeOrder[a.prioridade] !== prioridadeOrder[b.prioridade]) {
              return prioridadeOrder[b.prioridade] - prioridadeOrder[a.prioridade]
            }
            return b.tempo_espera_dias - a.tempo_espera_dias
          })
        })
      }
    })
    
    setMatches(newMatches)
  }, [listaEspera, horariosVagos])

  const filteredLista = listaEspera.filter(item => {
    const matchesSearch = item.nome_paciente.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.especialidade.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.terapeuta_preferencia.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesFilter = filterEspecialidade === 'all' || item.especialidade === filterEspecialidade
    return matchesSearch && matchesFilter
  })

  const stats = {
    totalAguardando: listaEspera.filter(i => i.status === 'aguardando').length,
    prioridadeAlta: listaEspera.filter(i => i.prioridade === 'alta').length,
    horariosDisponiveis: horariosVagos.filter(h => h.status === 'disponivel').length,
    matchesEncontrados: matches.length,
    tempoMedioEspera: Math.round(listaEspera.reduce((sum, i) => sum + i.tempo_espera_dias, 0) / listaEspera.length) || 0,
    especialidadesMaisRequisitadas: 3
  }

  const getPrioridadeColor = (prioridade) => {
    switch (prioridade) {
      case 'alta': return 'bg-red-100 text-red-800'
      case 'media': return 'bg-yellow-100 text-yellow-800'
      case 'baixa': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getTempoEsperaColor = (dias) => {
    if (dias >= 30) return 'text-red-600'
    if (dias >= 14) return 'text-yellow-600'
    return 'text-green-600'
  }

  const FormListaEspera = () => {
    const [formData, setFormData] = useState({
      nome_paciente: '',
      especialidade: '',
      terapeuta_preferencia: '',
      turno_preferencia: '',
      data_solicitacao: new Date().toISOString().split('T')[0],
      quem_solicitou: '',
      observacoes: '',
      prioridade: 'media',
      contato_responsavel: ''
    })

    useEffect(() => {
      if (editingItem) {
        setFormData(editingItem)
      }
    }, [editingItem])

    const handleSubmit = (e) => {
      e.preventDefault()
      if (editingItem) {
        setListaEspera(listaEspera.map(item => 
          item.id === editingItem.id ? { ...formData, id: editingItem.id } : item
        ))
        setEditingItem(null)
      } else {
        const novoItem = {
          id: Date.now(),
          ...formData,
          status: 'aguardando',
          tempo_espera_dias: Math.floor((new Date() - new Date(formData.data_solicitacao)) / (1000 * 60 * 60 * 24))
        }
        setListaEspera([novoItem, ...listaEspera])
      }
      setShowForm(false)
      setFormData({
        nome_paciente: '',
        especialidade: '',
        terapeuta_preferencia: '',
        turno_preferencia: '',
        data_solicitacao: new Date().toISOString().split('T')[0],
        quem_solicitou: '',
        observacoes: '',
        prioridade: 'media',
        contato_responsavel: ''
      })
    }

    return (
      <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 mb-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h3 className="text-lg font-bold text-gray-900">
              {editingItem ? 'Editar Paciente na Lista' : 'Adicionar à Lista de Espera'}
            </h3>
            <p className="text-gray-600">Preencha os dados do paciente</p>
          </div>
          <button
            onClick={() => {
              setShowForm(false)
              setEditingItem(null)
            }}
            className="text-gray-400 hover:text-gray-600 p-2"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Nome do Paciente</label>
              <input
                type="text"
                value={formData.nome_paciente}
                onChange={(e) => setFormData({ ...formData, nome_paciente: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Especialidade</label>
              <select
                value={formData.especialidade}
                onChange={(e) => setFormData({ ...formData, especialidade: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="">Selecione a especialidade</option>
                {especialidades.map(esp => (
                  <option key={esp} value={esp}>{esp}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Terapeuta de Preferência</label>
              <input
                type="text"
                value={formData.terapeuta_preferencia}
                onChange={(e) => setFormData({ ...formData, terapeuta_preferencia: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Opcional"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Turno de Preferência</label>
              <select
                value={formData.turno_preferencia}
                onChange={(e) => setFormData({ ...formData, turno_preferencia: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="">Selecione o turno</option>
                {turnos.map(turno => (
                  <option key={turno} value={turno}>{turno}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Data da Solicitação</label>
              <input
                type="date"
                value={formData.data_solicitacao}
                onChange={(e) => setFormData({ ...formData, data_solicitacao: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Quem Solicitou</label>
              <input
                type="text"
                value={formData.quem_solicitou}
                onChange={(e) => setFormData({ ...formData, quem_solicitou: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Prioridade</label>
              <select
                value={formData.prioridade}
                onChange={(e) => setFormData({ ...formData, prioridade: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="baixa">Baixa</option>
                <option value="media">Média</option>
                <option value="alta">Alta</option>
              </select>
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
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Observações</label>
            <textarea
              value={formData.observacoes}
              onChange={(e) => setFormData({ ...formData, observacoes: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows="3"
            />
          </div>
          <div className="flex gap-3 pt-4">
            <button
              onClick={handleSubmit}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center space-x-2"
            >
              <CheckCircle className="h-4 w-4" />
              <span>{editingItem ? 'Atualizar' : 'Adicionar'}</span>
            </button>
            <button
              onClick={() => {
                setShowForm(false)
                setEditingItem(null)
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

  const FormHorarioVago = () => {
    const [formData, setFormData] = useState({
      especialidade: '',
      terapeuta: '',
      data_disponivel: '',
      hora_inicio: '',
      hora_fim: '',
      sala: '',
      observacoes: ''
    })

    const handleSubmit = (e) => {
      e.preventDefault()
      const turno = formData.hora_inicio < '12:00' ? 'Manhã' : 
                   formData.hora_inicio < '18:00' ? 'Tarde' : 'Noite'
      
      const novoHorario = {
        id: Date.now(),
        ...formData,
        turno,
        status: 'disponivel',
        created_by: user?.username || 'usuario'
      }
      setHorariosVagos([novoHorario, ...horariosVagos])
      setShowHorarioForm(false)
      setFormData({
        especialidade: '',
        terapeuta: '',
        data_disponivel: '',
        hora_inicio: '',
        hora_fim: '',
        sala: '',
        observacoes: ''
      })
    }

    return (
      <div className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 mb-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h3 className="text-lg font-bold text-gray-900">Informar Horário Vago</h3>
            <p className="text-gray-600">Registre um horário disponível para atendimento</p>
          </div>
          <button
            onClick={() => setShowHorarioForm(false)}
            className="text-gray-400 hover:text-gray-600 p-2"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Especialidade</label>
              <select
                value={formData.especialidade}
                onChange={(e) => setFormData({ ...formData, especialidade: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="">Selecione a especialidade</option>
                {especialidades.map(esp => (
                  <option key={esp} value={esp}>{esp}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Terapeuta</label>
              <input
                type="text"
                value={formData.terapeuta}
                onChange={(e) => setFormData({ ...formData, terapeuta: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Data Disponível</label>
              <input
                type="date"
                value={formData.data_disponivel}
                onChange={(e) => setFormData({ ...formData, data_disponivel: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Sala</label>
              <input
                type="text"
                value={formData.sala}
                onChange={(e) => setFormData({ ...formData, sala: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Hora Início</label>
              <input
                type="time"
                value={formData.hora_inicio}
                onChange={(e) => setFormData({ ...formData, hora_inicio: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Hora Fim</label>
              <input
                type="time"
                value={formData.hora_fim}
                onChange={(e) => setFormData({ ...formData, hora_fim: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Observações</label>
            <input
              type="text"
              value={formData.observacoes}
              onChange={(e) => setFormData({ ...formData, observacoes: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div className="flex gap-3 pt-4">
            <button
              onClick={handleSubmit}
              className="bg-green-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-green-700 transition-colors flex items-center space-x-2"
            >
              <Calendar className="h-4 w-4" />
              <span>Registrar Horário</span>
            </button>
            <button
              onClick={() => setShowHorarioForm(false)}
              className="border border-gray-300 text-gray-700 px-6 py-2 rounded-lg font-medium hover:bg-gray-50 transition-colors"
            >
              Cancelar
            </button>
          </div>
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
                <div className="w-12 h-12 bg-gradient-to-br from-orange-600 to-red-700 rounded-xl flex items-center justify-center shadow-lg">
                  <Clock className="h-7 w-7 text-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">Lista de Espera & Horários Vagos</h1>
                  <p className="text-gray-600">
                    {canEdit() ? 'Gerenciar lista de espera e encontrar matches' : 'Visualizar lista de espera'}
                  </p>
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              {canEdit() && (
                <button
                  onClick={() => setShowForm(!showForm)}
                  className="flex items-center space-x-2 bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 transition-colors shadow-lg"
                >
                  <Plus className="h-4 w-4" />
                  <span className="font-medium">Adicionar Paciente</span>
                </button>
              )}
              
              <button
                onClick={() => setShowHorarioForm(!showHorarioForm)}
                className="flex items-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors shadow-lg"
              >
                <Calendar className="h-4 w-4" />
                <span className="font-medium">Horário Vago</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto p-6">
        {/* Estatísticas */}
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
          <div className="bg-gradient-to-br from-orange-50 to-red-100 rounded-xl p-4 shadow-lg border border-orange-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-orange-700 font-medium">Aguardando</p>
                <p className="text-2xl font-bold text-orange-900">{stats.totalAguardando}</p>
              </div>
              <Clock className="h-8 w-8 text-orange-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-red-50 to-red-100 rounded-xl p-4 shadow-lg border border-red-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-red-700 font-medium">Prioridade Alta</p>
                <p className="text-2xl font-bold text-red-900">{stats.prioridadeAlta}</p>
              </div>
              <AlertCircle className="h-8 w-8 text-red-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-4 shadow-lg border border-green-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-700 font-medium">Horários Vagos</p>
                <p className="text-2xl font-bold text-green-900">{stats.horariosDisponiveis}</p>
              </div>
              <Calendar className="h-8 w-8 text-green-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-4 shadow-lg border border-purple-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-purple-700 font-medium">Matches</p>
                <p className="text-2xl font-bold text-purple-900">{stats.matchesEncontrados}</p>
              </div>
              <Zap className="h-8 w-8 text-purple-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-4 shadow-lg border border-blue-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-700 font-medium">Tempo Médio</p>
                <p className="text-2xl font-bold text-blue-900">{stats.tempoMedioEspera}d</p>
              </div>
              <TrendingUp className="h-8 w-8 text-blue-500" />
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-indigo-50 to-indigo-100 rounded-xl p-4 shadow-lg border border-indigo-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-indigo-700 font-medium">Especialidades</p>
                <p className="text-2xl font-bold text-indigo-900">{stats.especialidadesMaisRequisitadas}</p>
              </div>
              <Heart className="h-8 w-8 text-indigo-500" />
            </div>
          </div>
        </div>

        {/* Matches Encontrados */}
        {matches.length > 0 && (
          <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl p-6 shadow-lg border border-purple-200 mb-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-purple-100 rounded-xl flex items-center justify-center">
                <Zap className="h-6 w-6 text-purple-600" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-purple-900">
                  🎉 {matches.length} Match{matches.length > 1 ? 'es' : ''} Encontrado{matches.length > 1 ? 's' : ''}!
                </h3>
                <p className="text-purple-700">Pacientes da lista que podem ser atendidos</p>
              </div>
            </div>
            
            <div className="space-y-4">
              {matches.map((match, index) => (
                <div key={index} className="bg-white rounded-lg p-4 border border-purple-200">
                  <div className="flex justify-between items-start mb-3">
                    <div>
                      <h4 className="font-bold text-gray-900">{match.horario.especialidade}</h4>
                      <p className="text-sm text-gray-600">
                        {match.horario.terapeuta} - {new Date(match.horario.data_disponivel).toLocaleDateString('pt-BR')} 
                        às {match.horario.hora_inicio}
                      </p>
                    </div>
                    <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-semibold">
                      {match.pacientes.length} candidato{match.pacientes.length > 1 ? 's' : ''}
                    </span>
                  </div>
                  
                  <div className="space-y-2">
                    {match.pacientes.slice(0, 3).map((paciente) => (
                      <div key={paciente.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <div className={`w-3 h-3 rounded-full ${
                            paciente.prioridade === 'alta' ? 'bg-red-400' :
                            paciente.prioridade === 'media' ? 'bg-yellow-400' : 'bg-green-400'
                          }`} />
                          <div>
                            <span className="font-medium">{paciente.nome_paciente}</span>
                            <span className="text-sm text-gray-600 ml-2">
                              (Aguardando {paciente.tempo_espera_dias} dias)
                            </span>
                          </div>
                        </div>
                        {canEdit() && (
                          <button className="bg-purple-600 text-white px-3 py-1 rounded-lg text-sm font-medium hover:bg-purple-700 transition-colors">
                            Agendar
                          </button>
                        )}
                      </div>
                    ))}
                    {match.pacientes.length > 3 && (
                      <p className="text-sm text-gray-500 text-center">
                        +{match.pacientes.length - 3} candidato{match.pacientes.length - 3 > 1 ? 's' : ''} adicional{match.pacientes.length - 3 > 1 ? 'is' : ''}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tabs */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 mb-6">
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setActiveTab('lista')}
              className={`px-6 py-4 font-medium transition-colors ${
                activeTab === 'lista'
                  ? 'text-orange-600 border-b-2 border-orange-600 bg-orange-50'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <div className="flex items-center space-x-2">
                <Users className="h-5 w-5" />
                <span>Lista de Espera ({stats.totalAguardando})</span>
              </div>
            </button>
            
            <button
              onClick={() => setActiveTab('horarios')}
              className={`px-6 py-4 font-medium transition-colors ${
                activeTab === 'horarios'
                  ? 'text-green-600 border-b-2 border-green-600 bg-green-50'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              <div className="flex items-center space-x-2">
                <Calendar className="h-5 w-5" />
                <span>Horários Vagos ({stats.horariosDisponiveis})</span>
              </div>
            </button>
          </div>
        </div>

        {/* Formulários */}
        {showForm && canEdit() && <FormListaEspera />}
        {showHorarioForm && <FormHorarioVago />}

        {/* Filtros */}
        {activeTab === 'lista' && (
          <div className="bg-white rounded-xl p-4 shadow-lg border border-gray-100 mb-6">
            <div className="flex items-center space-x-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <input
                  type="text"
                  placeholder="Buscar pacientes..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div className="flex items-center space-x-2">
                <Filter className="h-4 w-4 text-gray-500" />
                <select
                  value={filterEspecialidade}
                  onChange={(e) => setFilterEspecialidade(e.target.value)}
                  className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="all">Todas Especialidades</option>
                  {especialidades.map(esp => (
                    <option key={esp} value={esp}>{esp}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        )}

        {/* Conteúdo das Tabs */}
        {activeTab === 'lista' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredLista.map((item) => (
              <div key={item.id} className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-shadow">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="font-bold text-gray-900">{item.nome_paciente}</h3>
                    <p className="text-sm text-gray-600">{item.especialidade}</p>
                  </div>
                  <div className="flex flex-col items-end space-y-1">
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getPrioridadeColor(item.prioridade)}`}>
                      {item.prioridade.toUpperCase()}
                    </span>
                    <span className={`text-sm font-bold ${getTempoEsperaColor(item.tempo_espera_dias)}`}>
                      {item.tempo_espera_dias} dias
                    </span>
                  </div>
                </div>
                
                <div className="space-y-2 text-sm mb-4">
                  {item.terapeuta_preferencia && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Terapeuta:</span>
                      <span className="font-medium">{item.terapeuta_preferencia}</span>
                    </div>
                  )}
                  <div className="flex justify-between">
                    <span className="text-gray-600">Turno:</span>
                    <span className="font-medium">{item.turno_preferencia}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Solicitado:</span>
                    <span className="font-medium">{new Date(item.data_solicitacao).toLocaleDateString('pt-BR')}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Por:</span>
                    <span className="font-medium">{item.quem_solicitou}</span>
                  </div>
                  {item.contato_responsavel && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Contato:</span>
                      <span className="font-medium">{item.contato_responsavel}</span>
                    </div>
                  )}
                </div>
                
                {item.observacoes && (
                  <div className="bg-gray-50 rounded-lg p-3 mb-4">
                    <p className="text-xs text-gray-600">
                      <strong>Obs:</strong> {item.observacoes}
                    </p>
                  </div>
                )}
                
                {canEdit() && (
                  <div className="flex gap-2">
                    <button
                      onClick={() => {
                        setEditingItem(item)
                        setShowForm(true)
                      }}
                      className="flex-1 bg-blue-100 text-blue-700 py-2 px-3 rounded-lg font-medium hover:bg-blue-200 transition-colors flex items-center justify-center space-x-1"
                    >
                      <Edit className="h-4 w-4" />
                      <span>Editar</span>
                    </button>
                    <button className="flex-1 bg-red-100 text-red-700 py-2 px-3 rounded-lg font-medium hover:bg-red-200 transition-colors flex items-center justify-center space-x-1">
                      <Trash2 className="h-4 w-4" />
                      <span>Remover</span>
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {activeTab === 'horarios' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {horariosVagos.map((horario) => (
              <div key={horario.id} className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-shadow">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="font-bold text-gray-900">{horario.especialidade}</h3>
                    <p className="text-sm text-gray-600">{horario.terapeuta}</p>
                  </div>
                  <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-semibold">
                    Disponível
                  </span>
                </div>
                
                <div className="space-y-2 text-sm mb-4">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Data:</span>
                    <span className="font-medium">{new Date(horario.data_disponivel).toLocaleDateString('pt-BR')}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Horário:</span>
                    <span className="font-medium">{horario.hora_inicio} - {horario.hora_fim}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Turno:</span>
                    <span className="font-medium">{horario.turno}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Sala:</span>
                    <span className="font-medium">{horario.sala}</span>
                  </div>
                </div>
                
                {horario.observacoes && (
                  <div className="bg-gray-50 rounded-lg p-3 mb-4">
                    <p className="text-xs text-gray-600">
                      <strong>Obs:</strong> {horario.observacoes}
                    </p>
                  </div>
                )}
                
                <div className="flex gap-2">
                  <button className="flex-1 bg-green-100 text-green-700 py-2 px-3 rounded-lg font-medium hover:bg-green-200 transition-colors flex items-center justify-center space-x-1">
                    <UserCheck className="h-4 w-4" />
                    <span>Agendar</span>
                  </button>
                  <button className="flex-1 bg-gray-100 text-gray-700 py-2 px-3 rounded-lg font-medium hover:bg-gray-200 transition-colors flex items-center justify-center space-x-1">
                    <Eye className="h-4 w-4" />
                    <span>Detalhes</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Estado vazio */}
        {((activeTab === 'lista' && filteredLista.length === 0) || 
          (activeTab === 'horarios' && horariosVagos.length === 0)) && (
          <div className="bg-white rounded-xl p-12 shadow-lg border border-gray-100 text-center">
            {activeTab === 'lista' ? (
              <>
                <Users className="h-16 w-16 mx-auto text-gray-400 mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Lista de espera vazia</h3>
                <p className="text-gray-600 mb-4">
                  {searchTerm || filterEspecialidade !== 'all' 
                    ? 'Nenhum paciente encontrado com os filtros aplicados'
                    : 'Ainda não há pacientes na lista de espera'
                  }
                </p>
                {canEdit() && !searchTerm && filterEspecialidade === 'all' && (
                  <button
                    onClick={() => setShowForm(true)}
                    className="bg-orange-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-orange-700 transition-colors"
                  >
                    Adicionar Primeiro Paciente
                  </button>
                )}
              </>
            ) : (
              <>
                <Calendar className="h-16 w-16 mx-auto text-gray-400 mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Nenhum horário vago</h3>
                <p className="text-gray-600 mb-4">
                  Ainda não há horários vagos registrados
                </p>
                <button
                  onClick={() => setShowHorarioForm(true)}
                  className="bg-green-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-green-700 transition-colors"
                >
                  Registrar Primeiro Horário
                </button>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default ListaEsperaPage