# Sistema de Gestão de Recepções - Flask + Supabase

Sistema web completo para gerenciamento de múltiplas recepções com controle de acesso baseado em setores.

## 🏗️ **Arquitetura**

- **Backend:** Flask (Python) com Blueprints
- **Banco de Dados:** Supabase (PostgreSQL)
- **Autenticação:** JWT + Flask-JWT-Extended
- **Hospedagem:** Hostinger (Python)

## 👥 **Perfis de Usuário**

### **🔧 ADM (Gerência de Relacionamento)**
- Cadastro de usuários
- Visualização de gráficos e relatórios gerais
- Acesso total a todas as seções
- Dashboards com números totais

### **🏥 Recepções (por setor)**

#### **📍 Recepção 103:**
- Estoque exclusivo (incluir materiais/registrar retiradas)
- Lançamento de orçamentos
- Acesso à sessão de brindes

#### **📍 Recepção 1002:**
- Controle total da sessão de brindes
- Controle total da lista de espera
- Distribuição de brindes para outras recepções

#### **📍 Recepção 808:**
- Registrar quantidade de anamnese
- Lançamento de orçamento
- Acesso à sessão de brindes

#### **📍 Recepção 108:**
- Entrada/saída de pacientes
- Visitas externas com agendamento
- Controle exclusivo de brindes de visitantes
- Lançamento de orçamentos
- Alertas automáticos (24h após orçamento)

#### **📍 Recepções 203, 1009, 1108:**
- Acesso à sessão de brindes
- Lançamento de orçamento
- Mapa de salas

## 🔐 **Usuários Configurados**

### **Administradores:**
- `admpodd` / `admpodd@incentivar.com` (senha: 123456)
- `admpdg` / `admpdg@incentivar.com` (senha: 123456)
- `admaba` / `admaba@incentivar.com` (senha: 123456)

### **Recepções:**
- `recepcao103` / `recepcao103@incentivar.com` (senha: 123456)
- `recepcao108` / `recepcao108@incentivar.com` (senha: 123456)
- `recepcao203` / `recepcao203@incentivar.com` (senha: 123456)
- `recepcao808` / `recepcao808@incentivar.com` (senha: 123456)
- `recepcao1002` / `recepcao1002@incentivar.com` (senha: 123456)
- `recepcao1009` / `recepcao1009@incentivar.com` (senha: 123456)
- `recepcao1108` / `recepcao1108@incentivar.com` (senha: 123456)

## 🚀 **Instalação e Configuração**

### **1. Configurar Ambiente**
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações do Supabase
```

### **2. Configurar Supabase**
1. Crie um projeto no [Supabase](https://supabase.com)
2. Execute o script SQL em `sql/create_tables.sql`
3. Configure as variáveis no `.env`:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`

### **3. Inicializar Usuários**
```bash
python scripts/init_users.py
```

### **4. Executar Aplicação**
```bash
# Desenvolvimento
python app.py

# Produção
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

## 📊 **Funcionalidades por Módulo**

### **🏠 Salas**
- Cadastro e gerenciamento de salas
- Sistema de reservas
- Mapa visual de ocupação
- Controle de horários vagos

### **📦 Estoque (Recepção 103)**
- Controle de materiais
- Registro de retiradas
- Relatórios de consumo

### **💰 Orçamentos**
- Lançamento com dados dos pais/paciente
- Sistema de alertas (24h)
- Controle de feedback

### **🎁 Brindes**
- Controle centralizado (1002)
- Distribuição para recepções
- Controle especial para visitantes (108)

### **⏳ Lista de Espera (Recepção 1002)**
- Controle por especialidade
- Preferência de terapeuta
- Tempo de espera automático

### **👥 Visitas (Recepção 108)**
- Registro de visitas externas
- Controle de entrada/saída de pacientes
- Agendamentos

### **📋 Anamnese (Recepção 808)**
- Registro de quantidades
- Estatísticas por profissional
- Relatórios mensais

## 🔧 **API Endpoints**

### **Autenticação**
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Dados do usuário
- `POST /api/auth/change-password` - Alterar senha

### **Admin**
- `GET /api/admin/users` - Listar usuários
- `POST /api/admin/users` - Criar usuário
- `GET /api/admin/dashboard/overview` - Dashboard geral

### **Salas**
- `GET /api/salas/` - Listar salas
- `POST /api/salas/` - Criar sala
- `PUT /api/salas/<id>` - Atualizar sala
- `DELETE /api/salas/<id>` - Excluir sala
- `POST /api/salas/<id>/reservar` - Reservar sala

### **Outros Módulos**
- `/api/estoque/` - Gestão de estoque
- `/api/orcamentos/` - Gestão de orçamentos
- `/api/brindes/` - Gestão de brindes
- `/api/lista-espera/` - Lista de espera
- `/api/visitas/` - Visitas e pacientes
- `/api/anamnese/` - Anamneses
- `/api/dashboard/` - Dashboards e gráficos

## 🛡️ **Segurança**

- Autenticação JWT
- Controle de acesso por decorators
- Validação de permissões por recepção
- Senhas hasheadas com Werkzeug

## 📈 **Deploy na Hostinger**

1. **Upload dos arquivos** para o diretório público
2. **Configurar variáveis de ambiente** no painel
3. **Instalar dependências:** `pip install -r requirements.txt`
4. **Configurar WSGI:** Apontar para `app:create_app()`
5. **Configurar banco:** Executar scripts SQL no Supabase

## 🔄 **Estrutura de Arquivos**

```
├── app.py                 # Aplicação principal
├── config.py             # Configurações
├── database.py           # Conexão Supabase
├── requirements.txt      # Dependências
├── models/
│   └── user.py          # Model de usuário
├── blueprints/          # Módulos organizados
│   ├── auth.py         # Autenticação
│   ├── admin.py        # Administração
│   ├── salas.py        # Gestão de salas
│   ├── estoque.py      # Controle de estoque
│   ├── orcamentos.py   # Orçamentos
│   ├── brindes.py      # Gestão de brindes
│   ├── lista_espera.py # Lista de espera
│   ├── visitas.py      # Visitas e pacientes
│   ├── anamnese.py     # Anamneses
│   └── dashboard.py    # Dashboards
├── utils/
│   └── permissions.py   # Controle de acesso
├── scripts/
│   └── init_users.py   # Inicializar usuários
└── sql/
    └── create_tables.sql # Estrutura do banco
```

Sistema completo e pronto para produção! 🚀