import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Input } from '../components/ui/input'
import { Label } from '../components/ui/label'
import { toast } from 'sonner'
import { Package, Plus } from 'lucide-react'

interface ItemEstoque {
  id: number
  nome: string
  quantidade: number
  unidade: string
  descricao: string
}

const EstoquePage = () => {
  const [itens, setItens] = useState<ItemEstoque[]>([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    nome: '',
    quantidade: '',
    unidade: '',
    descricao: ''
  })

  useEffect(() => {
    fetchEstoque()
  }, [])

  const fetchEstoque = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/estoque/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        setItens(data.estoque)
      }
    } catch (error) {
      toast.error('Erro ao carregar estoque')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const token = localStorage.getItem('token')
      const response = await fetch('/api/estoque/item', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          nome: formData.nome,
          quantidade: parseInt(formData.quantidade),
          unidade: formData.unidade,
          descricao: formData.descricao
        })
      })

      if (response.ok) {
        toast.success('Item adicionado ao estoque!')
        setFormData({ nome: '', quantidade: '', unidade: '', descricao: '' })
        setShowForm(false)
        fetchEstoque()
      } else {
        const error = await response.json()
        toast.error(error.error || 'Erro ao adicionar item')
      }
    } catch (error) {
      toast.error('Erro ao adicionar item')
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
              <Package className="h-8 w-8" />
              Estoque - Recepção 103
            </h1>
            <p className="text-gray-600">Controle de materiais e retiradas</p>
          </div>
          <Button onClick={() => setShowForm(!showForm)}>
            <Plus className="h-4 w-4 mr-2" />
            Novo Item
          </Button>
        </div>

        {showForm && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Novo Item</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="nome">Nome do Item</Label>
                    <Input
                      id="nome"
                      value={formData.nome}
                      onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                      required
                    />
                  </div>
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
                    <Label htmlFor="unidade">Unidade</Label>
                    <Input
                      id="unidade"
                      value={formData.unidade}
                      onChange={(e) => setFormData({ ...formData, unidade: e.target.value })}
                      placeholder="ex: unidades, kg, litros"
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="descricao">Descrição</Label>
                    <Input
                      id="descricao"
                      value={formData.descricao}
                      onChange={(e) => setFormData({ ...formData, descricao: e.target.value })}
                    />
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button type="submit">Adicionar Item</Button>
                  <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                    Cancelar
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {itens.map((item) => (
            <Card key={item.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle>{item.nome}</CardTitle>
                <CardDescription>{item.descricao}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <p className="text-lg font-semibold">
                    {item.quantidade} {item.unidade}
                  </p>
                  <Button className="w-full" variant="outline">
                    Registrar Retirada
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {itens.length === 0 && (
          <Card>
            <CardContent className="text-center py-8">
              <Package className="h-12 w-12 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-600">Nenhum item no estoque</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

export default EstoquePage