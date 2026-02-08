import axios from 'axios'

// Define a interface para os dados de um lembrete
interface Lembrete {
    minutos_antecedencia: number
}

// Define a interface para os dados de um evento retornado pela API
export interface Evento {
    id: number
    titulo: string
    data_horario: string // ISO 8601 datetime format
    email_usuario: string
    descricao?: string
    lembretes: Lembrete[]
}

// Define a interface para criação/atualização de evento
export interface EventoCreatePayload {
    titulo: string
    data_horario: string
    email_usuario: string
    descricao?: string
    lembretes: Lembrete[]
}

// URL base da API - pode ser configurada via variáveis de ambiente
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Cria uma instância do axios com a URL base configurada
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Exporta um objeto com todas as funções de chamadas à API
export const eventosAPI = {
    /**
     * Busca todos os eventos cadastrados
     * GET /eventos/
     */
    listar: async (): Promise<Evento[]> => {
        try {
            const response = await apiClient.get<Evento[]>('/eventos/')
            return response.data
        } catch (error) {
            console.error('Erro ao listar eventos:', error)
            throw error
        }
    },

    /**
     * Cria um novo evento
     * POST /eventos/
     */
    criar: async (payload: EventoCreatePayload): Promise<Evento> => {
        try {
            const response = await apiClient.post<Evento>('/eventos/', payload)
            return response.data
        } catch (error) {
            console.error('Erro ao criar evento:', error)
            throw error
        }
    },

    /**
     * Atualiza um evento existente
     * PUT /eventos/{id}
     */
    atualizar: async (id: number, payload: EventoCreatePayload): Promise<Evento> => {
        try {
            const response = await apiClient.put<Evento>(`/eventos/${id}`, payload)
            return response.data
        } catch (error) {
            console.error('Erro ao atualizar evento:', error)
            throw error
        }
    },

    /**
     * Deleta um evento
     * DELETE /eventos/{id}
     */
    deletar: async (id: number): Promise<void> => {
        try {
            await apiClient.delete(`/eventos/${id}`)
        } catch (error) {
            console.error('Erro ao deletar evento:', error)
            throw error
        }
    },

    /**
     * Verifica se a API está online
     * GET /health
     */
    health: async (): Promise<{ status: string }> => {
        try {
            const response = await apiClient.get<{ status: string }>('/health')
            return response.data
        } catch (error) {
            console.error('Erro ao verificar saúde da API:', error)
            throw error
        }
    },
}
