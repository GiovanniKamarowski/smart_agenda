import { useQuery } from '@tanstack/react-query'
import { Evento, eventosAPI } from '../services/api'
import { EventCard } from './EventCard'

// Interface para as props do componente
interface EventListProps {
    onEdit: (evento: Evento) => void
    deletingId?: number | null
    onDelete: (id: number) => void
}

/**
 * Componente EventList
 * Lista todos os eventos usando React Query para cache inteligente
 * Gerencia loading, erros e refetch automático
 */
export function EventList({ onEdit, deletingId, onDelete }: EventListProps) {
    // useQuery: hook do React Query que gerencia cache, loading, erro e refetch
    // Retorna os dados, status de loading, status de erro e função refetch
    const { data: eventos = [], isLoading, error, refetch } = useQuery({
        // Identificador único da query (importante para caching)
        queryKey: ['eventos'],
        // Função que busca os dados
        queryFn: () => eventosAPI.listar(),
        // Mantém os dados em cache por 5 minutos (300000ms)
        staleTime: 5 * 60 * 1000,
    })

    // Estado de carregamento
    if (isLoading) {
        return (
            <div className="text-center py-8">
                <p className="text-gray-500">Carregando eventos...</p>
            </div>
        )
    }

    // Estado de erro
    if (error) {
        return (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                <h3 className="text-red-800 font-semibold mb-2">Erro ao carregar eventos</h3>
                <p className="text-red-600 mb-4">
                    {error instanceof Error ? error.message : 'Erro desconhecido'}
                </p>
                {/* Botão para tentar novamente */}
                <button
                    onClick={() => refetch()}
                    className="btn-secondary"
                >
                    Tentar Novamente
                </button>
            </div>
        )
    }

    // Lista vazia
    if (eventos.length === 0) {
        return (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
                <p className="text-blue-800 text-lg">
                    Nenhum evento cadastrado ainda
                </p>
                <p className="text-blue-600">
                    Crie seu primeiro evento usando o formulário acima
                </p>
            </div>
        )
    }

    return (
        <div>
            {/* Título da seção */}
            <h2 className="text-2xl font-bold mb-6">Eventos</h2>

            {/* Lista de eventos */}
            <div>
                {eventos.map((evento) => (
                    <EventCard
                        key={evento.id}
                        evento={evento}
                        onEdit={onEdit}
                        onDelete={onDelete}
                        isDeleting={deletingId === evento.id}
                    />
                ))}
            </div>
        </div>
    )
}
