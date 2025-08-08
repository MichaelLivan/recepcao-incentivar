-- Tabela de usuários
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'recepcao')),
    recepcao_id VARCHAR(10),
    recepcao_nome VARCHAR(100),
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de salas
CREATE TABLE salas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    capacidade INTEGER,
    recepcao_id VARCHAR(10) NOT NULL,
    recepcao_nome VARCHAR(100),
    status VARCHAR(20) DEFAULT 'disponivel' CHECK (status IN ('disponivel', 'ocupada', 'reservada')),
    ocupado_por VARCHAR(100),
    ocupado_ate TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(50),
    updated_at TIMESTAMP DEFAULT NOW(),
    updated_by VARCHAR(50)
);

-- Tabela de reservas
CREATE TABLE reservas (
    id SERIAL PRIMARY KEY,
    sala_id INTEGER REFERENCES salas(id) ON DELETE CASCADE,
    usuario_id INTEGER REFERENCES usuarios(id),
    usuario_nome VARCHAR(100),
    recepcao_id VARCHAR(10),
    data_inicio TIMESTAMP NOT NULL,
    data_fim TIMESTAMP NOT NULL,
    observacoes TEXT,
    status VARCHAR(20) DEFAULT 'ativa' CHECK (status IN ('ativa', 'cancelada', 'finalizada')),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de orçamentos
CREATE TABLE orcamentos (
    id SERIAL PRIMARY KEY,
    nome_pais VARCHAR(200) NOT NULL,
    nome_paciente VARCHAR(200) NOT NULL,
    terapias_solicitadas TEXT NOT NULL,
    valor DECIMAL(10,2),
    observacoes TEXT,
    status VARCHAR(20) DEFAULT 'pendente' CHECK (status IN ('pendente', 'respondido', 'aprovado', 'rejeitado')),
    recepcao_id VARCHAR(10) NOT NULL,
    recepcao_nome VARCHAR(100),
    data_alerta TIMESTAMP,
    alerta_enviado BOOLEAN DEFAULT FALSE,
    feedback TEXT,
    data_feedback TIMESTAMP,
    feedback_by VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(50)
);

-- Tabela de estoque (Recepção 103)
CREATE TABLE estoque (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 0,
    unidade VARCHAR(20) NOT NULL,
    descricao TEXT,
    recepcao_id VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(50),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de retiradas de estoque
CREATE TABLE retiradas_estoque (
    id SERIAL PRIMARY KEY,
    item_id INTEGER REFERENCES estoque(id),
    item_nome VARCHAR(200),
    quantidade INTEGER NOT NULL,
    retirado_por VARCHAR(100) NOT NULL,
    observacoes TEXT,
    recepcao_id VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(50)
);

-- Tabela de brindes
CREATE TABLE brindes (
    id SERIAL PRIMARY KEY,
    item_nome VARCHAR(200) NOT NULL,
    quantidade INTEGER NOT NULL,
    data_evento DATE,
    observacoes TEXT,
    recepcao_id VARCHAR(10) NOT NULL,
    recepcao_nome VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pendente' CHECK (status IN ('pendente', 'aprovado', 'entregue')),
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(50)
);

-- Tabela de estoque de brindes (Recepção 1002)
CREATE TABLE estoque_brindes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 0,
    descricao TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de distribuição de brindes
CREATE TABLE distribuicao_brindes (
    id SERIAL PRIMARY KEY,
    item_id INTEGER REFERENCES estoque_brindes(id),
    item_nome VARCHAR(200),
    quantidade INTEGER NOT NULL,
    recepcao_origem VARCHAR(10),
    recepcao_destino VARCHAR(10) NOT NULL,
    observacoes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(50)
);

-- Tabela de brindes para visitantes (Recepção 108)
CREATE TABLE brindes_visitantes (
    id SERIAL PRIMARY KEY,
    visitante_nome VARCHAR(200) NOT NULL,
    item_nome VARCHAR(200) NOT NULL,
    quantidade INTEGER NOT NULL,
    observacoes TEXT,
    recepcao_id VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(50)
);

-- Tabela de lista de espera (Recepção 1002)
CREATE TABLE lista_espera (
    id SERIAL PRIMARY KEY,
    especialidade VARCHAR(100) NOT NULL,
    solicitante VARCHAR(200) NOT NULL,
    terapeuta_preferencia VARCHAR(100),
    data_solicitacao DATE NOT NULL,
    observacoes TEXT,
    status VARCHAR(20) DEFAULT 'aguardando' CHECK (status IN ('aguardando', 'atendido', 'cancelado')),
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(50),
    updated_at TIMESTAMP DEFAULT NOW(),
    updated_by VARCHAR(50)
);

-- Tabela de visitas externas (Recepção 108)
CREATE TABLE visitas_externas (
    id SERIAL PRIMARY KEY,
    visitante_nome VARCHAR(200) NOT NULL,
    empresa VARCHAR(200),
    data_visita DATE NOT NULL,
    hora_entrada TIME,
    hora_saida TIME,
    tipo_visita VARCHAR(50),
    agendamento BOOLEAN DEFAULT FALSE,
    observacoes TEXT,
    recepcao_id VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(50)
);

-- Tabela de entrada e saída de pacientes (Recepção 108)
CREATE TABLE entrada_saida_pacientes (
    id SERIAL PRIMARY KEY,
    paciente_nome VARCHAR(200) NOT NULL,
    responsavel VARCHAR(200),
    hora_entrada TIME NOT NULL,
    hora_saida TIME,
    tipo_atendimento VARCHAR(100),
    profissional VARCHAR(100),
    observacoes TEXT,
    observacoes_saida TEXT,
    status VARCHAR(20) DEFAULT 'presente' CHECK (status IN ('presente', 'finalizado')),
    recepcao_id VARCHAR(10) NOT NULL,
    data_registro DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(50),
    updated_at TIMESTAMP DEFAULT NOW(),
    updated_by VARCHAR(50)
);

-- Tabela de anamneses (Recepção 808)
CREATE TABLE anamneses (
    id SERIAL PRIMARY KEY,
    paciente_nome VARCHAR(200) NOT NULL,
    responsavel VARCHAR(200),
    quantidade INTEGER NOT NULL DEFAULT 1,
    tipo_anamnese VARCHAR(100),
    profissional VARCHAR(100),
    observacoes TEXT,
    recepcao_id VARCHAR(10) NOT NULL,
    data_registro DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(50)
);

-- Inserir usuários iniciais
INSERT INTO usuarios (username, email, password_hash, role, recepcao_id, recepcao_nome) VALUES
-- Admins
('admpodd', 'admpodd@incentivar.com', 'pbkdf2:sha256:260000$salt$hash', 'admin', NULL, NULL),
('admpdg', 'admpdg@incentivar.com', 'pbkdf2:sha256:260000$salt$hash', 'admin', NULL, NULL),
('admaba', 'admaba@incentivar.com', 'pbkdf2:sha256:260000$salt$hash', 'admin', NULL, NULL),
-- Recepções
('recepcao103', 'recepcao103@incentivar.com', 'pbkdf2:sha256:260000$salt$hash', 'recepcao', '103', 'Recepção 103'),
('recepcao108', 'recepcao108@incentivar.com', 'pbkdf2:sha256:260000$salt$hash', 'recepcao', '108', 'Recepção 108'),
('recepcao203', 'recepcao203@incentivar.com', 'pbkdf2:sha256:260000$salt$hash', 'recepcao', '203', 'Recepção 203'),
('recepcao808', 'recepcao808@incentivar.com', 'pbkdf2:sha256:260000$salt$hash', 'recepcao', '808', 'Recepção 808'),
('recepcao1002', 'recepcao1002@incentivar.com', 'pbkdf2:sha256:260000$salt$hash', 'recepcao', '1002', 'Recepção 1002'),
('recepcao1009', 'recepcao1009@incentivar.com', 'pbkdf2:sha256:260000$salt$hash', 'recepcao', '1009', 'Recepção 1009'),
('recepcao1108', 'recepcao1108@incentivar.com', 'pbkdf2:sha256:260000$salt$hash', 'recepcao', '1108', 'Recepção 1108');

-- Criar índices para performance
CREATE INDEX idx_salas_recepcao ON salas(recepcao_id);
CREATE INDEX idx_orcamentos_recepcao ON orcamentos(recepcao_id);
CREATE INDEX idx_orcamentos_alerta ON orcamentos(data_alerta, alerta_enviado);
CREATE INDEX idx_estoque_recepcao ON estoque(recepcao_id);
CREATE INDEX idx_usuarios_username ON usuarios(username);
CREATE INDEX idx_reservas_sala ON reservas(sala_id);
CREATE INDEX idx_lista_espera_status ON lista_espera(status);