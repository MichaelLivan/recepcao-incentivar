import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'
import { Badge } from '../components/ui/badge'
import { toast } from 'sonner'
import { Users, Plus } from 'lucide-react'

interface Visita {
  id: number
  visitante_nome: string
  empresa: string
  data_visita: string
  hora_entrada: string
  hora_saida: string
  tipo_visita: string
  agendamento: boolean
  observacoes: string
}

interface Paciente {
  id: number
  paciente_nome: string
  responsavel: string
  hora_entrada: string
  hora_saida: string
  tipo_atendimento: string
  profissional: string
  status: 'presente' | 'finalizado'
}

const VisitasPage = () => {
  const [visitas, setVisitas] = useState<Visita[]>([])
  const [pacientes, setPacientes] = useState<Paciente[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'visitas' | 'pacientes'>('visitas')
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    visitante_nome: '',
    empresa: '',
    data_visita: '',
    hora_entrada: '',
    tipo_visita: '',
    agendamento: false,
    observacoes: ''
  })

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token')
      
      // Buscar visitas
      const visitasResponse = await fetch('/api/visitas/', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (visitasResponse.ok) {
        const visitasData = await visitasResponse.json()
        setVisitas(visitasData.visitas)
      }

      // Buscar pacientes
      const pacientesResponse = await fetch('/api/visitas/pacientes', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (pacientesResponse.ok) {
        const pacientesData = await pacientesResponse.json()
        setPacientes(pacientesData.pacientes)
      }
    } catch (error) {
      toast.error('Erro ao carregar dados')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmitVisita = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/visitas/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        toast.success('Visita registrada com sucesso!')
        setFormData({ visitante_nome: '', empresa: '', data_visita: '', hora_entrada: '', tipo_visita: '', agendamento: false, observacoes: '' })
        setShowForm(false)
        fetchData()
      } else {
        const error = await response.json()
        toast.error(error.error || 'Erro ao registrar visita')
      }
    } catch (error) {
      toast.error('Erro ao registrar visita')
    }
  }

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Carregando...</div>
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto p-6">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
              <Users className="h-8 w-8" />
              Visitas e Pacientes - Recepção 108
            </h1>
            <p className="text-gray-600">Controle de visitas externas e entrada/saída de pacientes</p>
          </div>
          <Button onClick={() => setShowForm(!showForm)}>
            <Plus className="h-4 w-4 mr-2" />
            Nova Visita
          </Button>
        </div>

        {/* Tabs */}
        <div className="flex space-x-1 mb-6">
          <Button
            variant={activeTab === 'visitas' ? 'default' : 'outline'}
            onClick={() => setActiveTab('visitas')}
          >
            Visitas Externas
          </Button>
          <Button
            variant={activeTab === 'pacientes' ? 'default' : 'outline'}
            onClick={() => setActiveTab('pacientes')}
          >
            Pacientes
          </Button>
        </div>

        {showForm && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Registrar Visita Externa</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmitVisita} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="visitante_nome">Nome do Visitante</Label>
                    <Input
                      id="visitante_nome"
                      value={formData.visitante_nome}
                      onChange={(e) => setFormData({ ...formData, visitante_nome: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="empresa">Empresa</Label>
                    <Input
                      id="empresa"
                      value={formData.empresa}
                      onChange={(e) => setFormData({ ...formData, empresa: e.target.value })}
                    />
                  </div>
                  <div>
                    <Label htmlFor="data_visita">Data da Visita</Label>
                    <Input
                      id="data_visita"
                      type="date"
                      value={formData.data_visita}
                      onChange={(e) => setFormData({ ...formData, data_visita: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="hora_entrada">Hora de Entrada</Label>
                    <Input
                      id="hora_entrada"
                      type="time"
                      value={formData.hora_entrada}
                      onChange={(e) => setFormData({ ...formData, hora_entrada: e.target.value })}
                    />
                  </div>
                  <div>
                    <Label htmlFor="tipo_visita">Tipo de Visita</Label>
                    <Input
                      id="tipo_visita"
                      value={formData.tipo_visita}
                      onChange={(e) => setFormData({ ...formData, tipo_visita: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="observacoes">Observações</Label>
                    <Input
                      id="observacoes"
                      value={formData.observacoes}
                      onChange={(e) => setFormData({ ...formData, observacoes: e.target.value })}
                    />
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="agendamento"
                    checked={formData.agendamento}
                    onChange={(e) => setFormData({ ...formData, agendamento: e.target.checked })}
                  />
                  <Label htmlFor="agendamento">Visita agendada</Label>
                </div>
                <div className="flex gap-2">
                  <Button type="submit">Registrar Visita</Button>
                  <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                    Cancelar
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        )}

        {/* Conteúdo das tabs */}
        {activeTab === 'visitas' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {visitas.map((visita) => (
              <Card key={visita.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle>{visita.visitante_nome}</CardTitle>
                      <CardDescription>{visita.empresa}</CardDescription>
                    </div>
                    {visita.agendamento && (
                      <Badge className="bg-blue-100 text-blue-800">
                        Agendada
                      </Badge>
                    )}
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <p className="text-sm">
                      <strong>Data:</strong> {new Date(visita.data_visita).toLocaleDateString()}
                    </p>
                    <p className="text-sm">
                      <strong>Tipo:</strong> {visita.tipo_visita}
                    </p>
                    {visita.hora_entrada && (
                      <p className="text-sm">
                        <strong>Entrada:</strong> {visita.hora_entrada}
                      </p>
                    )}
                    {visita.hora_saida && (
                      <p className="text-sm">
                        <strong>Saída:</strong> {visita.hora_saida}
                      </p>
                    )}
                    {visita.observacoes && (
                      <p className="text-sm text-gray-600">
                        <strong>Obs:</strong> {visita.observacoes}
                      </p>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {activeTab === 'pacientes' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {pacientes.map((paciente) => (
              <Card key={paciente.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle>{paciente.paciente_nome}</CardTitle>
                      <CardDescription>Responsável: {paciente.responsavel}</CardDescription>
                    </div>
                    <Badge className={paciente.status === 'presente' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}>
                      {paciente.status === 'presente' ? 'Presente' : 'Finalizado'}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <p className="text-sm">
                      <strong>Entrada:</strong> {paciente.hora_entrada}
                    </p>
                    {paciente.hora_saida && (
                      <p className="text-sm">
                        <strong>Saída:</strong> {paciente.hora_saida}
                      </p>
                    )}
                    <p className="text-sm">
                      <strong>Atendimento:</strong> {paciente.tipo_atendimento}
                    </p>
                    <p className="text-sm">
                      <strong>Profissional:</strong> {paciente.profissional}
                    </p>
                    {paciente.status === 'presente' && (
                      <Button className="w-full mt-4" size="sm">
                        Registrar Saída
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {((activeTab === 'visitas' && visitas.length === 0) || (activeTab === 'pacientes' && pacientes.length === 0)) && (
          <Card>
            <CardContent className="text-center py-8">
              <Users className="h-12 w-12 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-600">
                {activeTab === 'visitas' ? 'Nenhuma visita registrada' : 'Nenhum paciente registrado'}
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

export default VisitasPage