import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'
import { Textarea } from '../components/ui/textarea'
import { Badge } from '../components/ui/badge'
import { toast } from 'sonner'
import { FileText, Plus, ArrowLeft, AlertCircle, DollarSign, Calendar, Clock, CheckCircle, XCircle, User, Building } from 'lucide-react'
import { Link } from 'react-router-dom'

interface Orcamento {
  id: number
  nome_pais: string
  nome_paciente: string
  terapias_solicitadas: string
  valor?: number
  observacoes: string
  status: 'pendente' | 'respondido' | 'aprovado' | 'rejeitado'
  recepcao_nome: string
  data_alerta?: string
  alerta_enviado: boolean
  feedback?: string
  data_feedback?: string
  feedback_by?: string
  created_at: string
}

const OrcamentosPage = () => {
  const { user } = useAuth()
  const [orcamentos, setOrcamentos] = useState<Orcamento[]>([])
  const [alertas, setAlertas] = useState<Orcamento[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [showFeedbackModal, setShowFeedbackModal] = useState<number | null>(null)
  const [feedbackText, setFeedbackText] = useState('')
  const [formData, setFormData] = useState({
    nome_pais: '',
    nome_paciente: '',
    terapias_solicitadas: '',
    valor: '',
    observacoes: ''
  })

  const isAdmin = () => {
    return user?.role === 'admin' || user?.role === 'admin_geral' || user?.role === 'admin_limitado'
  }

  useEffect(() => {
    fetchOrcamentos()
    fetchAlertas()
  }, [])

  const fetchOrcamentos = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/orcamentos/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        setOrcamentos(data.orcamentos)
      }
    } catch (error) {
      toast.error('Erro ao carregar orçamentos')
    } finally {
      setLoading(false)
    }
  }

  const fetchAlertas = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/orcamentos/alertas', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        setAlertas(data.alertas || [])
        if (data.alertas && data.alertas.length > 0) {
          toast.info(`${data.alertas.length} orçamento(s) precisam de feedback!`)
        }
      }
    } catch (error) {
      console.error('Erro ao carregar alertas:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/orcamentos/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          nome_pais: formData.nome_pais,
          nome_paciente: formData.nome_paciente,
          terapias_solicitadas: formData.terapias_solicitadas,
          valor: formData.valor ? parseFloat(formData.valor) : null,
          observacoes: formData.observacoes
        })
      })

      if (response.ok) {
        toast.success('Orçamento criado com sucesso!')
        setFormData({ nome_pais: '', nome_paciente: '', terapias_solicitadas: '', valor: '', observacoes: '' })
        setShowForm(false)
        fetchOrcamentos()
      } else {
        const error = await response.json()
        toast.error(error.error || 'Erro ao criar orçamento')
      }
    } catch (error) {
      toast.error('Erro ao criar orçamento')
    }
  }

  const adicionarFeedback = async (orcamentoId: number) => {
    if (!feedbackText.trim()) {
      toast.error('Digite um feedback válido')
      return
    }

    try {
      const token = localStorage.getItem('token')
      const response = await fetch(`/api/orcamentos/${orcamentoId}/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ feedback: feedbackText, status: 'respondido' })
      })

      if (response.ok) {
        toast.success('Feedback adicionado com sucesso!')
        setShowFeedbackModal(null)
        setFeedbackText('')
        fetchOrcamentos()
        fetchAlertas()
      }
    } catch (error) {
      toast.error('Erro ao adicionar feedback')
    }
  }

  const getStatusConfig = (status: string) => {
    switch (status) {
      case 'pendente':
        return {
          color: 'bg-gradient-to-r from-yellow-400 to-orange-500',
          textColor: 'text-yellow-800',
          bgColor: 'bg-yellow-50',
          icon: Clock,
          label: 'Pendente'
        }
      case 'respondido':
        return {
          color: 'bg-gradient-to-r from-blue-400 to-indigo-500',
          textColor: 'text-blue-800',
          bgColor: 'bg-blue-50',
          icon: FileText,
          label: 'Respondido'
        }
      case 'aprovado':
        return {
          color: 'bg-gradient-to-r from-green-400 to-emerald-500',
          textColor: 'text-green-800',
          bgColor: 'bg-green-50',
          icon: CheckCircle,
          label: 'Aprovado'
        }
      case 'rejeitado':
        return {
          color: 'bg-gradient-to-r from-red-400 to-pink-500',
          textColor: 'text-red-800',
          bgColor: 'bg-red-50',
          icon: XCircle,
          label: 'Rejeitado'
        }
      default:
        return {
          color: 'bg-gradient-to-r from-gray-400 to-gray-500',
          textColor: 'text-gray-800',
          bgColor: 'bg-gray-50',
          icon: FileText,
          label: status
        }
    }
  }

  const isAlertaVencido = (dataAlerta: string) => {
    return new Date(dataAlerta) <= new Date()
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando orçamentos...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-100">
      {/* Header */}
      <div className="bg-white shadow-lg border-b">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link to="/dashboard">
                <Button variant="outline" size="sm" className="hover:shadow-md transition-shadow">
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Voltar
                </Button>
              </Link>
              <div>
                <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent flex items-center gap-3">
                  <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-2 rounded-xl shadow-lg">
                    <FileText className="h-8 w-8 text-white" />
                  </div>
                  Gestão de Orçamentos
                </h1>
                <p className="text-gray-600 mt-1">
                  {isAdmin() ? 'Visualizar e gerenciar todos os orçamentos' : 'Criar e acompanhar orçamentos da recepção'}
                </p>
              </div>
            </div>
            {!isAdmin() && (
              <Button 
                onClick={() => setShowForm(!showForm)}
                className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 shadow-lg hover:shadow-xl transition-all duration-300"
              >
                <Plus className="h-4 w-4 mr-2" />
                Novo Orçamento
              </Button>
            )}
          </div>
        </div>
      </div>

      <div className="container mx-auto p-6">
        {/* Alertas de Feedback */}
        {alertas.length > 0 && (
          <Card className="mb-6 border-orange-200 bg-gradient-to-r from-orange-50 to-amber-50 shadow-xl">
            <CardHeader>
              <CardTitle className="flex items-center gap-3 text-orange-800">
                <div className="bg-gradient-to-r from-orange-400 to-amber-500 p-2 rounded-lg">
                  <AlertCircle className="h-6 w-6 text-white animate-pulse" />
                </div>
                Orçamentos Precisam de Feedback Urgente!
              </CardTitle>
              <CardDescription className="text-orange-700">
                Os seguintes orçamentos foram criados há mais de 24 horas e precisam de retorno imediato
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {alertas.map((orcamento) => (
                  <div key={orcamento.id} className="flex justify-between items-center p-4 bg-white rounded-xl border-l-4 border-l-orange-500 shadow-md hover:shadow-lg transition-shadow">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <User className="h-5 w-5 text-gray-500" />
                        <h4 className="font-bold text-gray-900">{orcamento.nome_paciente}</h4>
                        <Badge className="bg-red-100 text-red-800 animate-pulse">
                          URGENTE
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-600 flex items-center gap-2 mb-1">
                        <User className="h-4 w-4" />
                        Responsável: {orcamento.nome_pais}
                      </p>
                      <p className="text-sm text-gray-600 flex items-center gap-2">
                        <Building className="h-4 w-4" />
                        {orcamento.recepcao_nome}
                      </p>
                    </div>
                    <Button 
                      size="sm"
                      onClick={() => setShowFeedbackModal(orcamento.id)}
                      className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 shadow-md hover:shadow-lg transition-all"
                    >
                      <FileText className="h-4 w-4 mr-2" />
                      Dar Feedback
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Estatísticas */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-br from-blue-500 to-indigo-600 text-white shadow-xl hover:shadow-2xl transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-blue-100 font-medium">Total Orçamentos</p>
                  <p className="text-4xl font-bold">{orcamentos.length}</p>
                </div>
                <div className="bg-white bg-opacity-20 p-3 rounded-full">
                  <FileText className="h-8 w-8" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-yellow-500 to-orange-600 text-white shadow-xl hover:shadow-2xl transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-yellow-100 font-medium">Pendentes</p>
                  <p className="text-4xl font-bold">
                    {orcamentos.filter(o => o.status === 'pendente').length}
                  </p>
                </div>
                <div className="bg-white bg-opacity-20 p-3 rounded-full">
                  <Clock className="h-8 w-8" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-green-500 to-emerald-600 text-white shadow-xl hover:shadow-2xl transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-green-100 font-medium">Aprovados</p>
                  <p className="text-4xl font-bold">
                    {orcamentos.filter(o => o.status === 'aprovado').length}
                  </p>
                </div>
                <div className="bg-white bg-opacity-20 p-3 rounded-full">
                  <CheckCircle className="h-8 w-8" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-purple-500 to-pink-600 text-white shadow-xl hover:shadow-2xl transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-purple-100 font-medium">Valor Total</p>
                  <p className="text-2xl font-bold">
                    R$ {orcamentos.reduce((sum, o) => sum + (o.valor || 0), 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                  </p>
                </div>
                <div className="bg-white bg-opacity-20 p-3 rounded-full">
                  <DollarSign className="h-8 w-8" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Formulário */}
        {showForm && !isAdmin() && (
          <Card className="mb-8 border-l-4 border-l-indigo-500 shadow-xl">
            <CardHeader className="bg-gradient-to-r from-indigo-50 to-purple-50">
              <CardTitle className="flex items-center gap-3">
                <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-2 rounded-lg">
                  <Plus className="h-5 w-5 text-white" />
                </div>
                Novo Orçamento
              </CardTitle>
              <CardDescription>Preencha os dados para criar um novo orçamento</CardDescription>
            </CardHeader>
            <CardContent className="p-6">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-2 gap-6">
                  <div>
                    <Label htmlFor="nome_pais" className="text-sm font-semibold text-gray-700">Nome dos Pais/Responsáveis</Label>
                    <Input
                      id="nome_pais"
                      value={formData.nome_pais}
                      onChange={(e) => setFormData({ ...formData, nome_pais: e.target.value })}
                      className="mt-1 border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="nome_paciente" className="text-sm font-semibold text-gray-700">Nome do Paciente</Label>
                    <Input
                      id="nome_paciente"
                      value={formData.nome_paciente}
                      onChange={(e) => setFormData({ ...formData, nome_paciente: e.target.value })}
                      className="mt-1 border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
                      required
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="terapias_solicitadas" className="text-sm font-semibold text-gray-700">Terapias Solicitadas</Label>
                  <Textarea
                    id="terapias_solicitadas"
                    value={formData.terapias_solicitadas}
                    onChange={(e) => setFormData({ ...formData, terapias_solicitadas: e.target.value })}
                    className="mt-1 border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 min-h-[100px]"
                    placeholder="Descreva as terapias solicitadas..."
                    required
                  />
                </div>
                <div className="grid grid-cols-2 gap-6">
                  <div>
                    <Label htmlFor="valor" className="text-sm font-semibold text-gray-700">Valor Estimado (opcional)</Label>
                    <Input
                      id="valor"
                      type="number"
                      step="0.01"
                      value={formData.valor}
                      onChange={(e) => setFormData({ ...formData, valor: e.target.value })}
                      className="mt-1 border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
                      placeholder="0,00"
                    />
                  </div>
                  <div>
                    <Label htmlFor="observacoes" className="text-sm font-semibold text-gray-700">Observações</Label>
                    <Input
                      id="observacoes"
                      value={formData.observacoes}
                      onChange={(e) => setFormData({ ...formData, observacoes: e.target.value })}
                      className="mt-1 border-gray-300 focus:border-indigo-500 focus:ring-indigo-500"
                      placeholder="Informações adicionais..."
                    />
                  </div>
                </div>
                <div className="flex gap-3 pt-4">
                  <Button 
                    type="submit"
                    className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 shadow-lg hover:shadow-xl transition-all duration-300"
                  >
                    <FileText className="h-4 w-4 mr-2" />
                    Criar Orçamento
                  </Button>
                  <Button 
                    type="button" 
                    variant="outline" 
                    onClick={() => setShowForm(false)}
                    className="hover:shadow-md transition-shadow"
                  >
                    Cancelar
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        )}

        {/* Lista de Orçamentos */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {orcamentos.map((orcamento) => {
            const statusConfig = getStatusConfig(orcamento.status)
            const StatusIcon = statusConfig.icon
            const isUrgente = orcamento.data_alerta && isAlertaVencido(orcamento.data_alerta) && !orcamento.alerta_enviado

            return (
              <Card 
                key={orcamento.id} 
                className={`hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 ${
                  isUrgente ? 'border-l-4 border-l-red-500 bg-red-50' : 'border-l-4 border-l-indigo-500'
                }`}
              >
                <CardHeader className={`${statusConfig.bgColor} rounded-t-lg`}>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <CardTitle className="flex items-center gap-3 mb-2">
                        {isUrgente && <AlertCircle className="h-5 w-5 text-red-500 animate-pulse" />}
                        <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-1 rounded-lg">
                          <User className="h-4 w-4 text-white" />
                        </div>
                        <span className="text-gray-900">{orcamento.nome_paciente}</span>
                      </CardTitle>
                      <CardDescription className="flex items-center gap-2">
                        <User className="h-4 w-4" />
                        Responsável: {orcamento.nome_pais}
                      </CardDescription>
                    </div>
                    <div className="flex flex-col items-end gap-2">
                      <Badge className={`${statusConfig.color} text-white shadow-md`}>
                        <StatusIcon className="h-3 w-3 mr-1" />
                        {statusConfig.label}
                      </Badge>
                      {isUrgente && (
                        <Badge className="bg-red-500 text-white animate-pulse">
                          URGENTE
                        </Badge>
                      )}
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="p-6">
                  <div className="space-y-3">
                    <div className="bg-gray-50 p-3 rounded-lg">
                      <p className="text-sm font-semibold text-gray-700 mb-1">Terapias Solicitadas:</p>
                      <p className="text-sm text-gray-600">{orcamento.terapias_solicitadas}</p>
                    </div>
                    
                    {orcamento.valor && (
                      <div className="flex items-center gap-2 p-2 bg-green-50 rounded-lg">
                        <DollarSign className="h-4 w-4 text-green-600" />
                        <span className="font-bold text-green-800">
                          R$ {orcamento.valor.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                        </span>
                      </div>
                    )}

                    <div className="flex items-center gap-2 text-sm text-gray-500">
                      <Building className="h-4 w-4" />
                      <span>{orcamento.recepcao_nome}</span>
                    </div>

                    <div className="flex items-center gap-2 text-sm text-gray-500">
                      <Calendar className="h-4 w-4" />
                      <span>Criado em {new Date(orcamento.created_at).toLocaleDateString('pt-BR')}</span>
                    </div>

                    {orcamento.feedback && (
                      <div className="bg-blue-50 p-3 rounded-lg border-l-4 border-l-blue-400">
                        <p className="text-sm font-semibold text-blue-800 mb-1">Feedback:</p>
                        <p className="text-sm text-blue-700">{orcamento.feedback}</p>
                        {orcamento.feedback_by && (
                          <p className="text-xs text-blue-600 mt-1">Por: {orcamento.feedback_by}</p>
                        )}
                      </div>
                    )}

                    {orcamento.observacoes && (
                      <div className="bg-amber-50 p-3 rounded-lg border-l-4 border-l-amber-400">
                        <p className="text-sm font-semibold text-amber-800 mb-1">Observações:</p>
                        <p className="text-sm text-amber-700">{orcamento.observacoes}</p>
                      </div>
                    )}

                    {orcamento.status === 'pendente' && !isAdmin() && (
                      <Button 
                        className="w-full mt-4 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 shadow-md hover:shadow-lg transition-all"
                        size="sm"
                        onClick={() => setShowFeedbackModal(orcamento.id)}
                      >
                        <FileText className="h-4 w-4 mr-2" />
                        Adicionar Feedback
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {orcamentos.length === 0 && (
          <Card className="shadow-xl">
            <CardContent className="text-center py-16">
              <div className="bg-gradient-to-r from-indigo-500 to-purple-600 p-4 rounded-full w-20 h-20 mx-auto mb-6 flex items-center justify-center">
                <FileText className="h-10 w-10 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Nenhum orçamento encontrado</h3>
              <p className="text-gray-600">Comece criando seu primeiro orçamento</p>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Modal de Feedback */}
      {showFeedbackModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <Card className="w-full max-w-md shadow-2xl">
            <CardHeader className="bg-gradient-to-r from-green-50 to-emerald-50">
              <CardTitle className="flex items-center gap-3">
                <div className="bg-gradient-to-r from-green-500 to-emerald-600 p-2 rounded-lg">
                  <FileText className="h-5 w-5 text-white" />
                </div>
                Adicionar Feedback
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <div className="space-y-4">
                <div>
                  <Label htmlFor="feedback" className="text-sm font-semibold text-gray-700">Seu feedback sobre o orçamento:</Label>
                  <Textarea
                    id="feedback"
                    value={feedbackText}
                    onChange={(e) => setFeedbackText(e.target.value)}
                    className="mt-1 border-gray-300 focus:border-green-500 focus:ring-green-500 min-h-[120px]"
                    placeholder="Digite seu feedback detalhado..."
                  />
                </div>
                <div className="flex gap-3">
                  <Button 
                    onClick={() => adicionarFeedback(showFeedbackModal)}
                    className="flex-1 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 shadow-md hover:shadow-lg transition-all"
                  >
                    <CheckCircle className="h-4 w-4 mr-2" />
                    Enviar Feedback
                  </Button>
                  <Button 
                    variant="outline" 
                    onClick={() => {
                      setShowFeedbackModal(null)
                      setFeedbackText('')
                    }}
                    className="hover:shadow-md transition-shadow"
                  >
                    Cancelar
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}

export default OrcamentosPage