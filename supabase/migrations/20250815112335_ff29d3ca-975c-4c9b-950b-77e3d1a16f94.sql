-- Migration completa do sistema de recepção
-- Criação de todas as tabelas necessárias

-- 1. Tabela de usuários (já existe, mas garantindo estrutura correta)
CREATE TABLE IF NOT EXISTS public.usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    email VARCHAR NOT NULL UNIQUE,
    password_hash VARCHAR NOT NULL,
    role VARCHAR NOT NULL CHECK (role IN ('admin', 'gerencia', 'recepcao')),
    recepcao_id VARCHAR,
    recepcao_nome VARCHAR,
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- 2. Tabela de entrada e saída de pacientes
CREATE TABLE IF NOT EXISTS public.entrada_saida_pacientes (
    id SERIAL PRIMARY KEY,
    paciente_nome VARCHAR NOT NULL,
    idade_paciente INTEGER,
    responsavel VARCHAR,
    telefone_responsavel VARCHAR,
    tipo_atendimento VARCHAR,
    profissional VARCHAR,
    sala_atendimento VARCHAR,
    hora_entrada TIME WITHOUT TIME ZONE NOT NULL,
    hora_saida TIME WITHOUT TIME ZONE,
    data_registro DATE DEFAULT CURRENT_DATE,
    observacoes TEXT,
    observacoes_saida TEXT,
    status VARCHAR DEFAULT 'presente' CHECK (status IN ('presente', 'atendido', 'ausente')),
    recepcao_id VARCHAR NOT NULL,
    created_by VARCHAR,
    updated_by VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- 3. Tabela de anamneses
CREATE TABLE IF NOT EXISTS public.anamneses (
    id SERIAL PRIMARY KEY,
    paciente_nome VARCHAR NOT NULL,
    idade_paciente INTEGER,
    responsavel VARCHAR,
    tipo_anamnese VARCHAR,
    profissional VARCHAR,
    quantidade INTEGER NOT NULL DEFAULT 1,
    data_registro DATE DEFAULT CURRENT_DATE,
    observacoes TEXT,
    recepcao_id VARCHAR NOT NULL,
    created_by VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- 4. Tabela de orçamentos
CREATE TABLE IF NOT EXISTS public.orcamentos (
    id SERIAL PRIMARY KEY,
    nome_pais VARCHAR NOT NULL,
    nome_paciente VARCHAR NOT NULL,
    telefone_contato VARCHAR,
    email_contato VARCHAR,
    terapias_solicitadas TEXT NOT NULL,
    valor NUMERIC,
    observacoes TEXT,
    status VARCHAR DEFAULT 'pendente' CHECK (status IN ('pendente', 'em_analise', 'aprovado', 'rejeitado')),
    prioridade VARCHAR DEFAULT 'normal' CHECK (prioridade IN ('baixa', 'normal', 'alta', 'urgente')),
    data_alerta TIMESTAMP WITHOUT TIME ZONE,
    alerta_enviado BOOLEAN DEFAULT false,
    feedback TEXT,
    feedback_by VARCHAR,
    data_feedback TIMESTAMP WITHOUT TIME ZONE,
    recepcao_id VARCHAR NOT NULL,
    recepcao_nome VARCHAR,
    created_by VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- 5. Tabela de salas
CREATE TABLE IF NOT EXISTS public.salas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR NOT NULL,
    descricao TEXT,
    capacidade INTEGER,
    equipamentos TEXT,
    status VARCHAR DEFAULT 'disponivel' CHECK (status IN ('disponivel', 'ocupada', 'manutencao')),
    ocupado_por VARCHAR,
    ocupado_ate TIMESTAMP WITHOUT TIME ZONE,
    recepcao_id VARCHAR NOT NULL,
    recepcao_nome VARCHAR,
    created_by VARCHAR,
    updated_by VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- 6. Tabela de reservas de salas
CREATE TABLE IF NOT EXISTS public.reservas (
    id SERIAL PRIMARY KEY,
    sala_id INTEGER REFERENCES public.salas(id),
    usuario_id INTEGER,
    usuario_nome VARCHAR,
    data_inicio TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    data_fim TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    motivo VARCHAR,
    observacoes TEXT,
    status VARCHAR DEFAULT 'ativa' CHECK (status IN ('ativa', 'cancelada', 'finalizada')),
    recepcao_id VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- 7. Tabela de estoque
CREATE TABLE IF NOT EXISTS public.estoque (
    id SERIAL PRIMARY KEY,
    nome VARCHAR NOT NULL,
    descricao TEXT,
    categoria VARCHAR,
    unidade VARCHAR NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 0,
    quantidade_minima INTEGER DEFAULT 5,
    valor_unitario NUMERIC,
    localizacao VARCHAR,
    ativo BOOLEAN DEFAULT true,
    recepcao_id VARCHAR NOT NULL,
    created_by VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- 8. Tabela de retiradas de estoque
CREATE TABLE IF NOT EXISTS public.retiradas_estoque (
    id SERIAL PRIMARY KEY,
    item_id INTEGER REFERENCES public.estoque(id),
    item_nome VARCHAR,
    quantidade INTEGER NOT NULL,
    retirado_por VARCHAR NOT NULL,
    setor_destino VARCHAR,
    data_retirada DATE DEFAULT CURRENT_DATE,
    observacoes TEXT,
    recepcao_id VARCHAR NOT NULL,
    created_by VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- 9. Tabela de estoque de brindes
CREATE TABLE IF NOT EXISTS public.estoque_brindes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR NOT NULL,
    descricao TEXT,
    categoria VARCHAR,
    quantidade INTEGER NOT NULL DEFAULT 0,
    quantidade_minima INTEGER DEFAULT 10,
    valor_unitario NUMERIC,
    fornecedor VARCHAR,
    created_by VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- 10. Tabela de brindes para eventos
CREATE TABLE IF NOT EXISTS public.brindes (
    id SERIAL PRIMARY KEY,
    item_nome VARCHAR NOT NULL,
    quantidade INTEGER NOT NULL,
    tipo_evento VARCHAR,
    publico_alvo VARCHAR,
    data_evento DATE,
    observacoes TEXT,
    status VARCHAR DEFAULT 'pendente' CHECK (status IN ('pendente', 'aprovado', 'rejeitado', 'entregue')),
    aprovado_por VARCHAR,
    data_aprovacao TIMESTAMP WITHOUT TIME ZONE,
    recepcao_id VARCHAR NOT NULL,
    recepcao_nome VARCHAR,
    created_by VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- 11. Tabela de distribuição de brindes
CREATE TABLE IF NOT EXISTS public.distribuicao_brindes (
    id SERIAL PRIMARY KEY,
    item_id INTEGER REFERENCES public.estoque_brindes(id),
    item_nome VARCHAR,
    quantidade INTEGER NOT NULL,
    recepcao_origem VARCHAR,
    recepcao_destino VARCHAR NOT NULL,
    motivo VARCHAR,
    observacoes TEXT,
    status VARCHAR DEFAULT 'pendente' CHECK (status IN ('pendente', 'enviado', 'recebido')),
    created_by VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- 12. Tabela de brindes para visitantes
CREATE TABLE IF NOT EXISTS public.brindes_visitantes (
    id SERIAL PRIMARY KEY,
    visitante_nome VARCHAR NOT NULL,
    empresa VARCHAR,
    item_nome VARCHAR NOT NULL,
    quantidade INTEGER NOT NULL,
    tipo_visita VARCHAR,
    data_entrega DATE DEFAULT CURRENT_DATE,
    observacoes TEXT,
    recepcao_id VARCHAR NOT NULL,
    created_by VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- 13. Tabela de visitas externas
CREATE TABLE IF NOT EXISTS public.visitas_externas (
    id SERIAL PRIMARY KEY,
    visitante_nome VARCHAR NOT NULL,
    documento VARCHAR,
    empresa VARCHAR,
    cargo VARCHAR,
    telefone VARCHAR,
    tipo_visita VARCHAR,
    pessoa_visitada VARCHAR,
    data_visita DATE NOT NULL,
    hora_entrada TIME WITHOUT TIME ZONE,
    hora_saida TIME WITHOUT TIME ZONE,
    agendamento BOOLEAN DEFAULT false,
    observacoes TEXT,
    recepcao_id VARCHAR NOT NULL,
    created_by VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- 14. Tabela de lista de espera
CREATE TABLE IF NOT EXISTS public.lista_espera (
    id SERIAL PRIMARY KEY,
    especialidade VARCHAR NOT NULL,
    solicitante VARCHAR NOT NULL,
    idade_paciente INTEGER,
    telefone_contato VARCHAR,
    terapeuta_preferencia VARCHAR,
    data_solicitacao DATE NOT NULL,
    data_contato DATE,
    prioridade VARCHAR DEFAULT 'normal' CHECK (prioridade IN ('baixa', 'normal', 'alta', 'urgente')),
    status VARCHAR DEFAULT 'aguardando' CHECK (status IN ('aguardando', 'contatado', 'agendado', 'cancelado')),
    observacoes TEXT,
    observacoes_contato TEXT,
    created_by VARCHAR,
    updated_by VARCHAR,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- 15. Tabela de log de atividades
CREATE TABLE IF NOT EXISTS public.log_atividades (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER,
    usuario_nome VARCHAR,
    acao VARCHAR NOT NULL,
    tabela_afetada VARCHAR,
    registro_id INTEGER,
    detalhes JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

-- 16. Views para dashboard
CREATE OR REPLACE VIEW public.dashboard_geral AS
SELECT 
    'usuarios' as tabela,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE ativo = true) as ativos
FROM public.usuarios
UNION ALL
SELECT 
    'orcamentos' as tabela,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE status = 'pendente') as ativos
FROM public.orcamentos
UNION ALL
SELECT 
    'salas' as tabela,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE status = 'disponivel') as ativos
FROM public.salas
UNION ALL
SELECT 
    'pacientes_hoje' as tabela,
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE status = 'presente') as ativos
FROM public.entrada_saida_pacientes 
WHERE data_registro = CURRENT_DATE;

-- 17. View para estatísticas por recepção
CREATE OR REPLACE VIEW public.stats_recepcao AS
SELECT 
    s.recepcao_id,
    s.recepcao_nome,
    COUNT(o.*) as total_orcamentos,
    COUNT(o.*) FILTER (WHERE o.status = 'pendente') as orcamentos_pendentes,
    COUNT(sa.*) as total_salas,
    COUNT(sa.*) FILTER (WHERE sa.status = 'disponivel') as salas_disponiveis
FROM public.salas s
LEFT JOIN public.orcamentos o ON s.recepcao_id = o.recepcao_id
LEFT JOIN public.salas sa ON s.recepcao_id = sa.recepcao_id
GROUP BY s.recepcao_id, s.recepcao_nome;

-- Triggers para atualizar updated_at
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar triggers nas tabelas que precisam
DROP TRIGGER IF EXISTS update_usuarios_updated_at ON public.usuarios;
CREATE TRIGGER update_usuarios_updated_at
    BEFORE UPDATE ON public.usuarios
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

DROP TRIGGER IF EXISTS update_entrada_saida_pacientes_updated_at ON public.entrada_saida_pacientes;
CREATE TRIGGER update_entrada_saida_pacientes_updated_at
    BEFORE UPDATE ON public.entrada_saida_pacientes
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

DROP TRIGGER IF EXISTS update_salas_updated_at ON public.salas;
CREATE TRIGGER update_salas_updated_at
    BEFORE UPDATE ON public.salas
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

DROP TRIGGER IF EXISTS update_estoque_updated_at ON public.estoque;
CREATE TRIGGER update_estoque_updated_at
    BEFORE UPDATE ON public.estoque
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

DROP TRIGGER IF EXISTS update_estoque_brindes_updated_at ON public.estoque_brindes;
CREATE TRIGGER update_estoque_brindes_updated_at
    BEFORE UPDATE ON public.estoque_brindes
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

DROP TRIGGER IF EXISTS update_lista_espera_updated_at ON public.lista_espera;
CREATE TRIGGER update_lista_espera_updated_at
    BEFORE UPDATE ON public.lista_espera
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_usuarios_username ON public.usuarios(username);
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON public.usuarios(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_recepcao_id ON public.usuarios(recepcao_id);

CREATE INDEX IF NOT EXISTS idx_entrada_saida_data_registro ON public.entrada_saida_pacientes(data_registro);
CREATE INDEX IF NOT EXISTS idx_entrada_saida_recepcao_id ON public.entrada_saida_pacientes(recepcao_id);
CREATE INDEX IF NOT EXISTS idx_entrada_saida_status ON public.entrada_saida_pacientes(status);

CREATE INDEX IF NOT EXISTS idx_orcamentos_recepcao_id ON public.orcamentos(recepcao_id);
CREATE INDEX IF NOT EXISTS idx_orcamentos_status ON public.orcamentos(status);
CREATE INDEX IF NOT EXISTS idx_orcamentos_created_at ON public.orcamentos(created_at);

CREATE INDEX IF NOT EXISTS idx_salas_recepcao_id ON public.salas(recepcao_id);
CREATE INDEX IF NOT EXISTS idx_salas_status ON public.salas(status);

CREATE INDEX IF NOT EXISTS idx_estoque_recepcao_id ON public.estoque(recepcao_id);
CREATE INDEX IF NOT EXISTS idx_estoque_ativo ON public.estoque(ativo);

CREATE INDEX IF NOT EXISTS idx_brindes_recepcao_id ON public.brindes(recepcao_id);
CREATE INDEX IF NOT EXISTS idx_brindes_status ON public.brindes(status);

CREATE INDEX IF NOT EXISTS idx_visitas_recepcao_id ON public.visitas_externas(recepcao_id);
CREATE INDEX IF NOT EXISTS idx_visitas_data_visita ON public.visitas_externas(data_visita);

CREATE INDEX IF NOT EXISTS idx_lista_espera_status ON public.lista_espera(status);
CREATE INDEX IF NOT EXISTS idx_lista_espera_prioridade ON public.lista_espera(prioridade);

CREATE INDEX IF NOT EXISTS idx_log_atividades_usuario_id ON public.log_atividades(usuario_id);
CREATE INDEX IF NOT EXISTS idx_log_atividades_created_at ON public.log_atividades(created_at);

-- Inserir usuário gerência se não existir
INSERT INTO public.usuarios (username, email, password_hash, role, ativo)
SELECT 'gerencia', 'gerencia@incentivar.com', 'scrypt:32768:8:1$YC6FvybqZHeazQbk$433c842b28cb9de63a01db80ce8e0791fcabcb00272168b3b868d54ef0fb21b07a6241ddb733407a984fb3fe63a0311e596f15bc104b3ac69628e51172c9122f', 'gerencia', true
WHERE NOT EXISTS (
    SELECT 1 FROM public.usuarios WHERE username = 'gerencia'
);