-- Criar tabela de usuários para o sistema de login
CREATE TABLE IF NOT EXISTS public.usuarios (
    id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'admin_geral', 'admin_limitado', 'recepcao')),
    recepcao_id TEXT,
    recepcao_nome TEXT,
    ativo BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Habilitar Row Level Security
ALTER TABLE public.usuarios ENABLE ROW LEVEL SECURITY;

-- Política para permitir que usuários vejam apenas seus próprios dados
CREATE POLICY "Usuários podem ver apenas seus próprios dados" 
ON public.usuarios 
FOR SELECT 
USING (auth.uid()::text = id::text);

-- Política para admin ver todos os usuários
CREATE POLICY "Admins podem ver todos os usuários" 
ON public.usuarios 
FOR SELECT 
USING (
    EXISTS (
        SELECT 1 FROM public.usuarios 
        WHERE id::text = auth.uid()::text 
        AND role IN ('admin', 'admin_geral')
    )
);

-- Inserir usuários de teste
INSERT INTO public.usuarios (username, email, password_hash, role, recepcao_id, recepcao_nome) VALUES
('admin', 'admin@incentivar.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/NcFNWM.jXX8K8aZSK', 'admin', null, null),
('gerencia', 'gerencia@incentivar.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/NcFNWM.jXX8K8aZSK', 'admin_geral', null, null),
('recepcao103', 'recepcao103@incentivar.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/NcFNWM.jXX8K8aZSK', 'recepcao', '103', 'Recepção 103')
ON CONFLICT (username) DO NOTHING;

-- Criar trigger para atualizar updated_at automaticamente
CREATE TRIGGER update_usuarios_updated_at
    BEFORE UPDATE ON public.usuarios
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();