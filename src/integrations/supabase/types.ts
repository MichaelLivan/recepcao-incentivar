export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "13.0.4"
  }
  public: {
    Tables: {
      anamneses: {
        Row: {
          created_at: string | null
          created_by: string | null
          data_registro: string | null
          id: number
          idade_paciente: number | null
          observacoes: string | null
          paciente_nome: string
          profissional: string | null
          quantidade: number
          recepcao_id: string
          responsavel: string | null
          tipo_anamnese: string | null
        }
        Insert: {
          created_at?: string | null
          created_by?: string | null
          data_registro?: string | null
          id?: number
          idade_paciente?: number | null
          observacoes?: string | null
          paciente_nome: string
          profissional?: string | null
          quantidade?: number
          recepcao_id: string
          responsavel?: string | null
          tipo_anamnese?: string | null
        }
        Update: {
          created_at?: string | null
          created_by?: string | null
          data_registro?: string | null
          id?: number
          idade_paciente?: number | null
          observacoes?: string | null
          paciente_nome?: string
          profissional?: string | null
          quantidade?: number
          recepcao_id?: string
          responsavel?: string | null
          tipo_anamnese?: string | null
        }
        Relationships: []
      }
      brindes: {
        Row: {
          aprovado_por: string | null
          created_at: string | null
          created_by: string | null
          data_aprovacao: string | null
          data_evento: string | null
          id: number
          item_nome: string
          observacoes: string | null
          publico_alvo: string | null
          quantidade: number
          recepcao_id: string
          recepcao_nome: string | null
          status: string | null
          tipo_evento: string | null
        }
        Insert: {
          aprovado_por?: string | null
          created_at?: string | null
          created_by?: string | null
          data_aprovacao?: string | null
          data_evento?: string | null
          id?: number
          item_nome: string
          observacoes?: string | null
          publico_alvo?: string | null
          quantidade: number
          recepcao_id: string
          recepcao_nome?: string | null
          status?: string | null
          tipo_evento?: string | null
        }
        Update: {
          aprovado_por?: string | null
          created_at?: string | null
          created_by?: string | null
          data_aprovacao?: string | null
          data_evento?: string | null
          id?: number
          item_nome?: string
          observacoes?: string | null
          publico_alvo?: string | null
          quantidade?: number
          recepcao_id?: string
          recepcao_nome?: string | null
          status?: string | null
          tipo_evento?: string | null
        }
        Relationships: []
      }
      brindes_visitantes: {
        Row: {
          created_at: string | null
          created_by: string | null
          data_entrega: string | null
          empresa: string | null
          id: number
          item_nome: string
          observacoes: string | null
          quantidade: number
          recepcao_id: string
          tipo_visita: string | null
          visitante_nome: string
        }
        Insert: {
          created_at?: string | null
          created_by?: string | null
          data_entrega?: string | null
          empresa?: string | null
          id?: number
          item_nome: string
          observacoes?: string | null
          quantidade: number
          recepcao_id: string
          tipo_visita?: string | null
          visitante_nome: string
        }
        Update: {
          created_at?: string | null
          created_by?: string | null
          data_entrega?: string | null
          empresa?: string | null
          id?: number
          item_nome?: string
          observacoes?: string | null
          quantidade?: number
          recepcao_id?: string
          tipo_visita?: string | null
          visitante_nome?: string
        }
        Relationships: []
      }
      distribuicao_brindes: {
        Row: {
          created_at: string | null
          created_by: string | null
          id: number
          item_id: number | null
          item_nome: string | null
          motivo: string | null
          observacoes: string | null
          quantidade: number
          recepcao_destino: string
          recepcao_origem: string | null
          status: string | null
        }
        Insert: {
          created_at?: string | null
          created_by?: string | null
          id?: number
          item_id?: number | null
          item_nome?: string | null
          motivo?: string | null
          observacoes?: string | null
          quantidade: number
          recepcao_destino: string
          recepcao_origem?: string | null
          status?: string | null
        }
        Update: {
          created_at?: string | null
          created_by?: string | null
          id?: number
          item_id?: number | null
          item_nome?: string | null
          motivo?: string | null
          observacoes?: string | null
          quantidade?: number
          recepcao_destino?: string
          recepcao_origem?: string | null
          status?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "distribuicao_brindes_item_id_fkey"
            columns: ["item_id"]
            isOneToOne: false
            referencedRelation: "estoque_brindes"
            referencedColumns: ["id"]
          },
        ]
      }
      entrada_saida_pacientes: {
        Row: {
          created_at: string | null
          created_by: string | null
          data_registro: string | null
          hora_entrada: string
          hora_saida: string | null
          id: number
          idade_paciente: number | null
          observacoes: string | null
          observacoes_saida: string | null
          paciente_nome: string
          profissional: string | null
          recepcao_id: string
          responsavel: string | null
          sala_atendimento: string | null
          status: string | null
          telefone_responsavel: string | null
          tipo_atendimento: string | null
          updated_at: string | null
          updated_by: string | null
        }
        Insert: {
          created_at?: string | null
          created_by?: string | null
          data_registro?: string | null
          hora_entrada: string
          hora_saida?: string | null
          id?: number
          idade_paciente?: number | null
          observacoes?: string | null
          observacoes_saida?: string | null
          paciente_nome: string
          profissional?: string | null
          recepcao_id: string
          responsavel?: string | null
          sala_atendimento?: string | null
          status?: string | null
          telefone_responsavel?: string | null
          tipo_atendimento?: string | null
          updated_at?: string | null
          updated_by?: string | null
        }
        Update: {
          created_at?: string | null
          created_by?: string | null
          data_registro?: string | null
          hora_entrada?: string
          hora_saida?: string | null
          id?: number
          idade_paciente?: number | null
          observacoes?: string | null
          observacoes_saida?: string | null
          paciente_nome?: string
          profissional?: string | null
          recepcao_id?: string
          responsavel?: string | null
          sala_atendimento?: string | null
          status?: string | null
          telefone_responsavel?: string | null
          tipo_atendimento?: string | null
          updated_at?: string | null
          updated_by?: string | null
        }
        Relationships: []
      }
      estoque: {
        Row: {
          ativo: boolean | null
          categoria: string | null
          created_at: string | null
          created_by: string | null
          descricao: string | null
          id: number
          localizacao: string | null
          nome: string
          quantidade: number
          quantidade_minima: number | null
          recepcao_id: string
          unidade: string
          updated_at: string | null
          valor_unitario: number | null
        }
        Insert: {
          ativo?: boolean | null
          categoria?: string | null
          created_at?: string | null
          created_by?: string | null
          descricao?: string | null
          id?: number
          localizacao?: string | null
          nome: string
          quantidade?: number
          quantidade_minima?: number | null
          recepcao_id: string
          unidade: string
          updated_at?: string | null
          valor_unitario?: number | null
        }
        Update: {
          ativo?: boolean | null
          categoria?: string | null
          created_at?: string | null
          created_by?: string | null
          descricao?: string | null
          id?: number
          localizacao?: string | null
          nome?: string
          quantidade?: number
          quantidade_minima?: number | null
          recepcao_id?: string
          unidade?: string
          updated_at?: string | null
          valor_unitario?: number | null
        }
        Relationships: []
      }
      estoque_brindes: {
        Row: {
          categoria: string | null
          created_at: string | null
          created_by: string | null
          descricao: string | null
          fornecedor: string | null
          id: number
          nome: string
          quantidade: number
          quantidade_minima: number | null
          updated_at: string | null
          valor_unitario: number | null
        }
        Insert: {
          categoria?: string | null
          created_at?: string | null
          created_by?: string | null
          descricao?: string | null
          fornecedor?: string | null
          id?: number
          nome: string
          quantidade?: number
          quantidade_minima?: number | null
          updated_at?: string | null
          valor_unitario?: number | null
        }
        Update: {
          categoria?: string | null
          created_at?: string | null
          created_by?: string | null
          descricao?: string | null
          fornecedor?: string | null
          id?: number
          nome?: string
          quantidade?: number
          quantidade_minima?: number | null
          updated_at?: string | null
          valor_unitario?: number | null
        }
        Relationships: []
      }
      lista_espera: {
        Row: {
          created_at: string | null
          created_by: string | null
          data_contato: string | null
          data_solicitacao: string
          especialidade: string
          id: number
          idade_paciente: number | null
          observacoes: string | null
          observacoes_contato: string | null
          prioridade: string | null
          solicitante: string
          status: string | null
          telefone_contato: string | null
          terapeuta_preferencia: string | null
          updated_at: string | null
          updated_by: string | null
        }
        Insert: {
          created_at?: string | null
          created_by?: string | null
          data_contato?: string | null
          data_solicitacao: string
          especialidade: string
          id?: number
          idade_paciente?: number | null
          observacoes?: string | null
          observacoes_contato?: string | null
          prioridade?: string | null
          solicitante: string
          status?: string | null
          telefone_contato?: string | null
          terapeuta_preferencia?: string | null
          updated_at?: string | null
          updated_by?: string | null
        }
        Update: {
          created_at?: string | null
          created_by?: string | null
          data_contato?: string | null
          data_solicitacao?: string
          especialidade?: string
          id?: number
          idade_paciente?: number | null
          observacoes?: string | null
          observacoes_contato?: string | null
          prioridade?: string | null
          solicitante?: string
          status?: string | null
          telefone_contato?: string | null
          terapeuta_preferencia?: string | null
          updated_at?: string | null
          updated_by?: string | null
        }
        Relationships: []
      }
      log_atividades: {
        Row: {
          acao: string
          created_at: string | null
          detalhes: Json | null
          id: number
          ip_address: unknown | null
          registro_id: number | null
          tabela_afetada: string | null
          user_agent: string | null
          usuario_id: number | null
          usuario_nome: string | null
        }
        Insert: {
          acao: string
          created_at?: string | null
          detalhes?: Json | null
          id?: number
          ip_address?: unknown | null
          registro_id?: number | null
          tabela_afetada?: string | null
          user_agent?: string | null
          usuario_id?: number | null
          usuario_nome?: string | null
        }
        Update: {
          acao?: string
          created_at?: string | null
          detalhes?: Json | null
          id?: number
          ip_address?: unknown | null
          registro_id?: number | null
          tabela_afetada?: string | null
          user_agent?: string | null
          usuario_id?: number | null
          usuario_nome?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "log_atividades_usuario_id_fkey"
            columns: ["usuario_id"]
            isOneToOne: false
            referencedRelation: "usuarios"
            referencedColumns: ["id"]
          },
        ]
      }
      orcamentos: {
        Row: {
          alerta_enviado: boolean | null
          created_at: string | null
          created_by: string | null
          data_alerta: string | null
          data_feedback: string | null
          email_contato: string | null
          feedback: string | null
          feedback_by: string | null
          id: number
          nome_paciente: string
          nome_pais: string
          observacoes: string | null
          prioridade: string | null
          recepcao_id: string
          recepcao_nome: string | null
          status: string | null
          telefone_contato: string | null
          terapias_solicitadas: string
          valor: number | null
        }
        Insert: {
          alerta_enviado?: boolean | null
          created_at?: string | null
          created_by?: string | null
          data_alerta?: string | null
          data_feedback?: string | null
          email_contato?: string | null
          feedback?: string | null
          feedback_by?: string | null
          id?: number
          nome_paciente: string
          nome_pais: string
          observacoes?: string | null
          prioridade?: string | null
          recepcao_id: string
          recepcao_nome?: string | null
          status?: string | null
          telefone_contato?: string | null
          terapias_solicitadas: string
          valor?: number | null
        }
        Update: {
          alerta_enviado?: boolean | null
          created_at?: string | null
          created_by?: string | null
          data_alerta?: string | null
          data_feedback?: string | null
          email_contato?: string | null
          feedback?: string | null
          feedback_by?: string | null
          id?: number
          nome_paciente?: string
          nome_pais?: string
          observacoes?: string | null
          prioridade?: string | null
          recepcao_id?: string
          recepcao_nome?: string | null
          status?: string | null
          telefone_contato?: string | null
          terapias_solicitadas?: string
          valor?: number | null
        }
        Relationships: []
      }
      reservas: {
        Row: {
          created_at: string | null
          data_fim: string
          data_inicio: string
          id: number
          motivo: string | null
          observacoes: string | null
          recepcao_id: string | null
          sala_id: number | null
          status: string | null
          usuario_id: number | null
          usuario_nome: string | null
        }
        Insert: {
          created_at?: string | null
          data_fim: string
          data_inicio: string
          id?: number
          motivo?: string | null
          observacoes?: string | null
          recepcao_id?: string | null
          sala_id?: number | null
          status?: string | null
          usuario_id?: number | null
          usuario_nome?: string | null
        }
        Update: {
          created_at?: string | null
          data_fim?: string
          data_inicio?: string
          id?: number
          motivo?: string | null
          observacoes?: string | null
          recepcao_id?: string | null
          sala_id?: number | null
          status?: string | null
          usuario_id?: number | null
          usuario_nome?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "reservas_sala_id_fkey"
            columns: ["sala_id"]
            isOneToOne: false
            referencedRelation: "salas"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "reservas_usuario_id_fkey"
            columns: ["usuario_id"]
            isOneToOne: false
            referencedRelation: "usuarios"
            referencedColumns: ["id"]
          },
        ]
      }
      retiradas_estoque: {
        Row: {
          created_at: string | null
          created_by: string | null
          data_retirada: string | null
          id: number
          item_id: number | null
          item_nome: string | null
          observacoes: string | null
          quantidade: number
          recepcao_id: string
          retirado_por: string
          setor_destino: string | null
        }
        Insert: {
          created_at?: string | null
          created_by?: string | null
          data_retirada?: string | null
          id?: number
          item_id?: number | null
          item_nome?: string | null
          observacoes?: string | null
          quantidade: number
          recepcao_id: string
          retirado_por: string
          setor_destino?: string | null
        }
        Update: {
          created_at?: string | null
          created_by?: string | null
          data_retirada?: string | null
          id?: number
          item_id?: number | null
          item_nome?: string | null
          observacoes?: string | null
          quantidade?: number
          recepcao_id?: string
          retirado_por?: string
          setor_destino?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "retiradas_estoque_item_id_fkey"
            columns: ["item_id"]
            isOneToOne: false
            referencedRelation: "estoque"
            referencedColumns: ["id"]
          },
        ]
      }
      salas: {
        Row: {
          capacidade: number | null
          created_at: string | null
          created_by: string | null
          descricao: string | null
          equipamentos: string | null
          id: number
          nome: string
          ocupado_ate: string | null
          ocupado_por: string | null
          recepcao_id: string
          recepcao_nome: string | null
          status: string | null
          updated_at: string | null
          updated_by: string | null
        }
        Insert: {
          capacidade?: number | null
          created_at?: string | null
          created_by?: string | null
          descricao?: string | null
          equipamentos?: string | null
          id?: number
          nome: string
          ocupado_ate?: string | null
          ocupado_por?: string | null
          recepcao_id: string
          recepcao_nome?: string | null
          status?: string | null
          updated_at?: string | null
          updated_by?: string | null
        }
        Update: {
          capacidade?: number | null
          created_at?: string | null
          created_by?: string | null
          descricao?: string | null
          equipamentos?: string | null
          id?: number
          nome?: string
          ocupado_ate?: string | null
          ocupado_por?: string | null
          recepcao_id?: string
          recepcao_nome?: string | null
          status?: string | null
          updated_at?: string | null
          updated_by?: string | null
        }
        Relationships: []
      }
      usuarios: {
        Row: {
          ativo: boolean | null
          created_at: string | null
          email: string
          id: number
          password_hash: string
          recepcao_id: string | null
          recepcao_nome: string | null
          role: string
          updated_at: string | null
          username: string
        }
        Insert: {
          ativo?: boolean | null
          created_at?: string | null
          email: string
          id?: number
          password_hash: string
          recepcao_id?: string | null
          recepcao_nome?: string | null
          role: string
          updated_at?: string | null
          username: string
        }
        Update: {
          ativo?: boolean | null
          created_at?: string | null
          email?: string
          id?: number
          password_hash?: string
          recepcao_id?: string | null
          recepcao_nome?: string | null
          role?: string
          updated_at?: string | null
          username?: string
        }
        Relationships: []
      }
      visitas_externas: {
        Row: {
          agendamento: boolean | null
          cargo: string | null
          created_at: string | null
          created_by: string | null
          data_visita: string
          documento: string | null
          empresa: string | null
          hora_entrada: string | null
          hora_saida: string | null
          id: number
          observacoes: string | null
          pessoa_visitada: string | null
          recepcao_id: string
          telefone: string | null
          tipo_visita: string | null
          visitante_nome: string
        }
        Insert: {
          agendamento?: boolean | null
          cargo?: string | null
          created_at?: string | null
          created_by?: string | null
          data_visita: string
          documento?: string | null
          empresa?: string | null
          hora_entrada?: string | null
          hora_saida?: string | null
          id?: number
          observacoes?: string | null
          pessoa_visitada?: string | null
          recepcao_id: string
          telefone?: string | null
          tipo_visita?: string | null
          visitante_nome: string
        }
        Update: {
          agendamento?: boolean | null
          cargo?: string | null
          created_at?: string | null
          created_by?: string | null
          data_visita?: string
          documento?: string | null
          empresa?: string | null
          hora_entrada?: string | null
          hora_saida?: string | null
          id?: number
          observacoes?: string | null
          pessoa_visitada?: string | null
          recepcao_id?: string
          telefone?: string | null
          tipo_visita?: string | null
          visitante_nome?: string
        }
        Relationships: []
      }
    }
    Views: {
      dashboard_geral: {
        Row: {
          ativos: number | null
          tabela: string | null
          total: number | null
        }
        Relationships: []
      }
      stats_recepcao: {
        Row: {
          orcamentos_pendentes: number | null
          recepcao_id: string | null
          recepcao_nome: string | null
          salas_disponiveis: number | null
          total_orcamentos: number | null
          total_salas: number | null
        }
        Relationships: []
      }
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {},
  },
} as const
