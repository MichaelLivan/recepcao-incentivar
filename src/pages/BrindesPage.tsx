import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'
import { Badge } from '../components/ui/badge'
import { toast } from 'sonner'
import { Gift, Plus, ArrowLeft, User, Calendar, Package, Send, Truck } from 'lucide-react'
import { Link } from 'react-router-dom'
// import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@radix-ui/react-select'

interface Brinde {
  id: number
  item_nome: string
  crianca_nome: string
  quantidade: number
  data_entrega: string
  observacoes: string
  recepcao_nome: string
  tipo: 'entrega' | 'solicitacao'
  status?: string
  created_at: string
}

interface EstoqueBrinde {
  id: number
  nome: string
  quantidade: number
  descricao: string
}

interface Distribuicao {
  id: number
  item_nome: string
  quantidade: number
  recepcao_destino: string
  created_at: string
}

const BrindesPage = () => {
  const { user } = useAuth()
  const [brindes, setBrindes] = useState<Brinde[]>([])
  const [estoque, setEstoque] = useState<EstoqueBrinde[]>([])
  const [distribuicoes, setDistribuicoes] = useState<Distribuicao[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'entregas' | 'estoque' | 'distribuicoes'>('entregas')
  const [showForm, setShowForm] = useState(false)
  const [formType, setFormType] = useState<'entrega' | 'solicitacao' | 'estoque' | 'distribuicao'>('entrega')
  
  // Formulário para entregas e solicitações
  const [formData, setFormData] = useState({
    item_nome: '',
    crianca_nome: '',
    quantidade: '',
    data_entrega: '',
    data_evento: '',
    observacoes: ''
  })

  // Formulário para estoque central
  const [estoqueFormData, setEstoqueFormData] = useState({
    nome: '',
    quantidade: '',
    descricao: ''
  })

  // Formulário para distribuição
  const [distribuicaoFormData, setDistribuicaoFormData] = useState({
    item_id: '',
    recepcao_destino: '',
    quantidade: '',
    observacoes: ''
  })

  const recepcoes = [
    { id: '103', nome: 'Recepção 103' },
    { id: '108', nome: 'Recepção 108' },
    { id: '203', nome: 'Recepção 203' },
    { id: '808', nome: 'Recepção 808' },
    { id: '1009', nome: 'Recepção 1009' },
    { id: '1108', nome: 'Recepção 1108' }
  ]

  // Verificar se é recepção central (1002)
  const isRecepcaoCentral = () => user?.recepcao_id === '1002'
  const isRecepcaoVisitantes = () => user?.recepcao_id === '108'

  useEffect(() => {
    fetchData()
  }, [activeTab])

  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token')
      
      // Buscar brindes/entregas
      if (activeTab === 'entregas') {
        const response = await fetch('/api/brindes/', {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        if (response.ok) {
          const data = await response.json()
          setBrindes(data.brindes)
        }
      }

      // Buscar estoque central (apenas 1002)
      if (activeTab === 'estoque' && isRecepcaoCentral()) {
        const response = await fetch('/api/brindes/estoque', {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        if (response.ok) {
          const data = await response.json()
          setEstoque(data.estoque)
        }
      }

      // Buscar distribuições (apenas 1002)
      if (activeTab === 'distribuicoes' && isRecepcaoCentral()) {
        const response = await fetch('/api/brindes/distribuicoes', {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        if (response.ok) {
          const data = await response.json()
          setDistribuicoes(data.distribuicoes)
        }
      }

    } catch (error) {
      toast.error('Erro ao carregar dados')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmitEntrega = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const token = localStorage.getItem('token')
      const endpoint = formType === 'entrega' ? '/api/brindes/entregas' : '/api/brindes/solicitar'
      
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        toast.success(formType === 'entrega' ? 'Entrega registrada!' : 'Solicitação enviada!')
        setFormData({ item_nome: '', crianca_nome: '', quantidade: '', data_entrega: '', data_evento: '', observacoes: '' })
        setShowForm(false)
        fetchData()
      } else {
        const error = await response.json()
        toast.error(error.error || 'Erro ao processar')
      }
    } catch (error) {
      toast.error('Erro ao processar')
    }
  }

  const handleSubmitEstoque = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/brindes/estoque/item', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(estoqueFormData)
      })

      if (response.ok) {
        toast.success('Item adicionado ao estoque!')
        setEstoqueFormData({ nome: '', quantidade: '', descricao: '' })
        setShowForm(false)
        fetchData()
      } else {
        const error = await response.json()
        toast.error(error.error || 'Erro ao adicionar item')
      }
    } catch (error) {
      toast.error('Erro ao adicionar item')
    }
  }

  const handleSubmitDistribuicao = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/brindes/distribuir', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(distribuicaoFormData)
      })

      if (response.ok) {
        toast.success('Distribuição realizada!')
        setDistribuicaoFormData({ item_id: '', recepcao_destino: '', quantidade: '', observacoes: '' })
        setShowForm(false)
        fetchData()
      } else {
        const error = await response.json()
        toast.error(error.error || 'Erro ao distribuir')
      }
    } catch (error) {
      toast.error('Erro ao distribuir')
    }
  }

  const openForm = (type: 'entrega' | 'solicitacao' | 'estoque' | 'distribuicao') => {
    setFormType(type)
    setShowForm(true)
  }

  const getTabs = () => {
    const tabs = [{ id: 'entregas', label: 'Entregas & Solicitações', icon: Gift }]
    
    if (isRecepcaoCentral()) {
      tabs.push(
        { id: 'estoque', label: 'Estoque Central', icon: Package },
        { id: 'distribuicoes', label: 'Distribuições', icon: Truck }
      )
    }
    
    return tabs
  }

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Carregando...</div>
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link to="/dashboard">
                <Button variant="outline" size="sm">
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Voltar
                </Button>
              </Link>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                  <Gift className="h-7 w-7 text-pink-600" />
                  Gestão de Brindes
                </h1>
                <p className="text-gray-600">
                  {isRecepcaoCentral() 
                    ? 'Estoque central e distribuição de brindes'
                    : 'Informar entregas e solicitar brindes'
                  }
                </p>
              </div>
            </div>
            
            <div className="flex gap-2">
              {activeTab === 'entregas' && (
                <>
                  <Button onClick={() => openForm('entrega')} className="bg-gradient-to-r from-pink-500 to-purple-600">
                    <Gift className="h-4 w-4 mr-2" />
                    Informar Entrega
                  </Button>
                  {!isRecepcaoCentral() && (
                    <Button variant="outline" onClick={() => openForm('solicitacao')}>
                      <Send className="h-4 w-4 mr-2" />
                      Solicitar Brindes
                    </Button>
                  )}
                </>
              )}
              
              {activeTab === 'estoque' && isRecepcaoCentral() && (
                <Button onClick={() => openForm('estoque')} className="bg-gradient-to-r from-blue-500 to-indigo-600">
                  <Package className="h-4 w-4 mr-2" />
                  Adicionar ao Estoque
                </Button>
              )}
              
              {activeTab === 'distribuicoes' && isRecepcaoCentral() && (
                <Button onClick={() => openForm('distribuicao')} className="bg-gradient-to-r from-green-500 to-teal-600">
                  <Truck className="h-4 w-4 mr-2" />
                  Nova Distribuição
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto p-6">
        {/* Tabs */}
        <div className="flex space-x-1 mb-6">
          {getTabs().map((tab) => {
            const Icon = tab.icon
            return (
              <Button
                key={tab.id}
                variant={activeTab === tab.id ? 'default' : 'outline'}
                onClick={() => setActiveTab(tab.id as any)}
                className="flex items-center gap-2"
              >
                <Icon className="h-4 w-4" />
                {tab.label}
              </Button>
            )
          })}
        </div>

        {/* Estatísticas */}
        {activeTab === 'entregas' && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
            <Card className="bg-gradient-to-br from-pink-50 to-pink-100 border-pink-200">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-pink-600 font-medium">Total Entregues</p>
                    <p className="text-3xl font-bold text-pink-900">
                      {brindes.filter(b => b.tipo === 'entrega').reduce((sum, b) => sum + b.quantidade, 0)}
                    </p>
                  </div>
                  <Gift className="h-10 w-10 text-pink-500" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-purple-600 font-medium">Crianças Atendidas</p>
                    <p className="text-3xl font-bold text-purple-900">
                      {brindes.filter(b => b.tipo === 'entrega').length}
                    </p>
                  </div>
                  <User className="h-10 w-10 text-purple-500" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-blue-600 font-medium">Solicitações</p>
                    <p className="text-3xl font-bold text-blue-900">
                      {brindes.filter(b => b.tipo === 'solicitacao').length}
                    </p>
                  </div>
                  <Send className="h-10 w-10 text-blue-500" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-50 to-green-100 border-green-200">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-green-600 font-medium">Hoje</p>
                    <p className="text-3xl font-bold text-green-900">
                      {brindes.filter(b => b.data_entrega === new Date().toISOString().split('T')[0]).length}
                    </p>
                  </div>
                  <Calendar className="h-10 w-10 text-green-500" />
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Formulários */}
        {showForm && (
          <Card className="mb-6 border-l-4 border-l-pink-500">
            <CardHeader>
              <CardTitle>
                {formType === 'entrega' && 'Informar Entrega de Brinde'}
                {formType === 'solicitacao' && 'Solicitar Brindes do Estoque Central'}
                {formType === 'estoque' && 'Adicionar Item ao Estoque Central'}
                {formType === 'distribuicao' && 'Distribuir Brindes para Recepção'}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {(formType === 'entrega' || formType === 'solicitacao') && (
                <form onSubmit={handleSubmitEntrega} className="space-y-4">
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <Label htmlFor="item_nome">Nome do Item</Label>
                      <Input
                        id="item_nome"
                        value={formData.item_nome}
                        onChange={(e) => setFormData({ ...formData, item_nome: e.target.value })}
                        required
                      />
                    </div>
                    {formType === 'entrega' && (
                      <div>
                        <Label htmlFor="crianca_nome">Nome da Criança</Label>
                        <Input
                          id="crianca_nome"
                          value={formData.crianca_nome}
                          onChange={(e) => setFormData({ ...formData, crianca_nome: e.target.value })}
                          required
                        />
                      </div>
                    )}
                    <div>
                      <Label htmlFor="quantidade">Quantidade</Label>
                      <Input
                        id="quantidade"
                        type="number"
                        value={formData.quantidade}
                        onChange={(e) => setFormData({ ...formData, quantidade: e.target.value })}
                        required
                      />
                    </div>
                    <div>
                      <Label htmlFor={formType === 'entrega' ? 'data_entrega' : 'data_evento'}>
                        {formType === 'entrega' ? 'Data da Entrega' : 'Data do Evento'}
                      </Label>
                      <Input
                        id={formType === 'entrega' ? 'data_entrega' : 'data_evento'}
                        type="date"
                        value={formType === 'entrega' ? formData.data_entrega : formData.data_evento}
                        onChange={(e) => setFormData({ 
                          ...formData, 
                          [formType === 'entrega' ? 'data_entrega' : 'data_evento']: e.target.value 
                        })}
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
                  <div className="flex gap-2">
                    <Button type="submit" className="bg-gradient-to-r from-pink-500 to-purple-600">
                      {formType === 'entrega' ? 'Registrar Entrega' : 'Enviar Solicitação'}
                    </Button>
                    <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                      Cancelar
                    </Button>
                  </div>
                </form>
              )}

              {formType === 'estoque' && (
                <form onSubmit={handleSubmitEstoque} className="space-y-4">
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <Label htmlFor="nome">Nome do Item</Label>
                      <Input
                        id="nome"
                        value={estoqueFormData.nome}
                        onChange={(e) => setEstoqueFormData({ ...estoqueFormData, nome: e.target.value })}
                        required
                      />
                    </div>
                    <div>
                      <Label htmlFor="quantidade_estoque">Quantidade</Label>
                      <Input
                        id="quantidade_estoque"
                        type="number"
                        value={estoqueFormData.quantidade}
                        onChange={(e) => setEstoqueFormData({ ...estoqueFormData, quantidade: e.target.value })}
                        required
                      />
                    </div>
                    <div>
                      <Label htmlFor="descricao">Descrição</Label>
                      <Input
                        id="descricao"
                        value={estoqueFormData.descricao}
                        onChange={(e) => setEstoqueFormData({ ...estoqueFormData, descricao: e.target.value })}
                      />
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button type="submit" className="bg-gradient-to-r from-blue-500 to-indigo-600">
                      Adicionar ao Estoque
                    </Button>
                    <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                      Cancelar
                    </Button>
                  </div>
                </form>
              )}

              {formType === 'distribuicao' && (
                <form onSubmit={handleSubmitDistribuicao} className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="item_id">Item do Estoque</Label>
                      <Select value={distribuicaoFormData.item_id} onValueChange={(value) => setDistribuicaoFormData({ ...distribuicaoFormData, item_id: value })}>
                        <SelectTrigger>
                          <SelectValue placeholder="Selecione o item" />
                        </SelectTrigger>
                        <SelectContent>
                          {estoque.map((item) => (
                            <SelectItem key={item.id} value={item.id.toString()}>
                              {item.nome} (Qtd: {item.quantidade})
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Label htmlFor="recepcao_destino">Recepção Destino</Label>
                      <Select value={distribuicaoFormData.recepcao_destino} onValueChange={(value) => setDistribuicaoFormData({ ...distribuicaoFormData, recepcao_destino: value })}>
                        <SelectTrigger>
                          <SelectValue placeholder="Selecione a recepção" />
                        </SelectTrigger>
                        <SelectContent>
                          {recepcoes.map((recepcao) => (
                            <SelectItem key={recepcao.id} value={recepcao.id}>
                              {recepcao.nome}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Label htmlFor="quantidade_dist">Quantidade</Label>
                      <Input
                        id="quantidade_dist"
                        type="number"
                        value={distribuicaoFormData.quantidade}
                        onChange={(e) => setDistribuicaoFormData({ ...distribuicaoFormData, quantidade: e.target.value })}
                        required
                      />
                    </div>
                    <div>
                      <Label htmlFor="observacoes_dist">Observações</Label>
                      <Input
                        id="observacoes_dist"
                        value={distribuicaoFormData.observacoes}
                        onChange={(e) => setDistribuicaoFormData({ ...distribuicaoFormData, observacoes: e.target.value })}
                      />
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button type="submit" className="bg-gradient-to-r from-green-500 to-teal-600">
                      Realizar Distribuição
                    </Button>
                    <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                      Cancelar
                    </Button>
                  </div>
                </form>
              )}
            </CardContent>
          </Card>
        )}

        {/* Conteúdo das Tabs */}
        {activeTab === 'entregas' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {brindes.map((brinde) => (
              <Card key={brinde.id} className="hover:shadow-xl transition-all duration-300 border-l-4 border-l-pink-500">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="flex items-center gap-2">
                        <Gift className="h-5 w-5 text-pink-600" />
                        {brinde.item_nome}
                      </CardTitle>
                      <CardDescription>
                        {brinde.tipo === 'entrega' 
                          ? `Para: ${brinde.crianca_nome}` 
                          : `Solicitação para evento`
                        }
                      </CardDescription>
                    </div>
                    <Badge className={brinde.tipo === 'entrega' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}>
                      {brinde.tipo === 'entrega' ? 'Entrega' : 'Solicitação'}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <p className="text-sm">
                      <strong>Quantidade:</strong> {brinde.quantidade}
                    </p>
                    <p className="text-sm">
                      <strong>Data:</strong> {new Date(brinde.data_entrega).toLocaleDateString('pt-BR')}
                    </p>
                    <p className="text-sm text-gray-600">
                      <strong>Recepção:</strong> {brinde.recepcao_nome}
                    </p>
                    {brinde.observacoes && (
                      <p className="text-sm text-gray-600">
                        <strong>Obs:</strong> {brinde.observacoes}
                      </p>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {activeTab === 'estoque' && isRecepcaoCentral() && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {estoque.map((item) => (
              <Card key={item.id} className="hover:shadow-xl transition-all duration-300 border-l-4 border-l-blue-500">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Package className="h-5 w-5 text-blue-600" />
                    {item.nome}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="text-center">
                      <p className="text-3xl font-bold text-blue-900">{item.quantidade}</p>
                      <p className="text-sm text-gray-600">unidades disponíveis</p>
                    </div>
                    {item.descricao && (
                      <p className="text-sm text-gray-600">{item.descricao}</p>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {activeTab === 'distribuicoes' && isRecepcaoCentral() && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {distribuicoes.map((dist) => (
              <Card key={dist.id} className="hover:shadow-xl transition-all duration-300 border-l-4 border-l-green-500">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Truck className="h-5 w-5 text-green-600" />
                    {dist.item_nome}
                  </CardTitle>
                  <CardDescription>
                    Para: Recepção {dist.recepcao_destino}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <p className="text-sm">
                      <strong>Quantidade:</strong> {dist.quantidade}
                    </p>
                    <p className="text-sm">
                      <strong>Data:</strong> {new Date(dist.created_at).toLocaleDateString('pt-BR')}
                    </p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {((activeTab === 'entregas' && brindes.length === 0) || 
          (activeTab === 'estoque' && estoque.length === 0) ||
          (activeTab === 'distribuicoes' && distribuicoes.length === 0)) && (
          <Card>
            <CardContent className="text-center py-8">
              <Gift className="h-12 w-12 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-600">
                {activeTab === 'entregas' && 'Nenhum brinde registrado'}
                {activeTab === 'estoque' && 'Estoque vazio'}
                {activeTab === 'distribuicoes' && 'Nenhuma distribuição realizada'}
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

export default BrindesPage