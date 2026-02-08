import { Evento } from '../services/api'
import dayjs from 'dayjs'

// Interface para as props do componente
interface EventCardProps {
    evento: Evento
    onEdit: (evento: Evento) => void
    onDelete: (id: number) => void
    isDeleting?: boolean
}

/**
 * Componente EventCard
 * Exibe um evento em um card com as informações principais
 * Permite editar e deletar o evento
 */
export function EventCard({ evento, onEdit, onDelete, isDeleting = false }: EventCardProps) {
    // Formata a data/hora para um formato mais legível
    const dataFormatada = dayjs(evento.data_horario).format('DD/MM/YYYY HH:mm')

    // Calcula quantos lembretes existem
    const totalLembretes = evento.lembretes.length

    return (
        <div className="card mb-4">
            {/* Header do card com título */}
            <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-800">{evento.titulo}</h3>
                    <p className="text-sm text-gray-500">{evento.email_usuario}</p>
                </div>
                {/* Botões de ação */}
                <div className="flex gap-2">
                    {/* Botão editar */}
                    <button
                        onClick={() => onEdit(evento)}
                        className="btn-secondary text-sm"
                    >
                        Editar
                    </button>
                    {/* Botão deletar */}
                    <button
                        onClick={() => onDelete(evento.id)}
                        disabled={isDeleting}
                        className="btn-danger text-sm disabled:opacity-50"
                    >
                        {isDeleting ? 'Deletando...' : 'Deletar'}
                    </button>
                </div>
            </div>

            {/* Informações do evento */}
            <div className="mb-3">
                {/* Data e hora */}
                <p className="text-gray-600 mb-2">
                    <span className="font-semibold">Data/Hora:</span> {dataFormatada}
                </p>

                {/* Descrição (se existir) */}
                {evento.descricao && (
                    <p className="text-gray-600 mb-2">
                        <span className="font-semibold">Descrição:</span> {evento.descricao}
                    </p>
                )}

                {/* Lembretes */}
                <p className="text-gray-600">
                    <span className="font-semibold">Lembretes:</span> {totalLembretes > 0 ? (
                        <span>
                            {evento.lembretes.map((r, i) => (
                                <span key={i}>
                                    {r.minutos_antecedencia} min{i < totalLembretes - 1 ? ', ' : ''}
                                </span>
                            ))}
                        </span>
                    ) : (
                        <span>Nenhum lembrete</span>
                    )}
                </p>
            </div>
        </div>
    )
}
