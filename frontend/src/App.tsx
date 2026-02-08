import { useState, useEffect } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { Evento, EventoCreatePayload, eventosAPI } from './services/api'
import { EventForm } from './components/EventForm'
import { EventList } from './components/EventList'

/**
 * Componente App
 * Componente raiz da aplicação
 * Gerencia:
 * - Estado de criação/edição de evento
 * - Chamadas à API para criar, atualizar e deletar eventos
 * - Refetch automático da lista após mutações
 */
function App() {
  // Estado para armazenar qual evento está sendo editado (null = criar novo)
  const [eventoEditando, setEventoEditando] = useState<Evento | null>(null)
  // Estado para armazenar qual evento está sendo deletado
  const [deletandoId, setDeletandoId] = useState<number | null>(null)

  // queryClient para fazer invalidar/refetch de queries do React Query
  const queryClient = useQueryClient()

  /**
   * Mutation para criar novo evento
   * Automaticamente chama os listeners após sucesso
   */
  const criarMutation = useMutation({
    mutationFn: (data: EventoCreatePayload) => eventosAPI.criar(data),
    onSuccess: () => {
      // Invalida a query de lista para que refetch automático aconteça
      queryClient.invalidateQueries({ queryKey: ['eventos'] })
      // Limpa o formulário
      setEventoEditando(null)
      // Mostra mensagem de sucesso
      alert('Evento criado com sucesso!')
    },
    onError: (error) => {
      // Mostra erro se houver
      alert('Erro ao criar evento: ' + (error instanceof Error ? error.message : 'Desconhecido'))
    }
  })

  /**
   * Mutation para atualizar evento
   * Similar à criação, mas com endpoint PUT
   */
  const atualizarMutation = useMutation({
    mutationFn: (data: { id: number; payload: EventoCreatePayload }) =>
      eventosAPI.atualizar(data.id, data.payload),
    onSuccess: () => {
      // Invalida a query de lista para refetch
      queryClient.invalidateQueries({ queryKey: ['eventos'] })
      // Limpa o formulário
      setEventoEditando(null)
      // Mostra mensagem de sucesso
      alert('Evento atualizado com sucesso!')
    },
    onError: (error) => {
      alert('Erro ao atualizar evento: ' + (error instanceof Error ? error.message : 'Desconhecido'))
    }
  })

  /**
   * Mutation para deletar evento
   */
  const deletarMutation = useMutation({
    mutationFn: (id: number) => eventosAPI.deletar(id),
    onSuccess: () => {
      // Invalida a query de lista para refetch
      queryClient.invalidateQueries({ queryKey: ['eventos'] })
      // Limpa o estado de deleção
      setDeletandoId(null)
      // Mostra mensagem de sucesso
      alert('Evento deletado com sucesso!')
    },
    onError: (error) => {
      setDeletandoId(null)
      alert('Erro ao deletar evento: ' + (error instanceof Error ? error.message : 'Desconhecido'))
    }
  })

  /**
   * Handler para salvar evento (criar ou atualizar)
   */
  const handleSalvarEvento = async (data: EventoCreatePayload) => {
    // Verifica se está editando ou criando
    if (eventoEditando) {
      // Atualizar
      atualizarMutation.mutate({ id: eventoEditando.id, payload: data })
    } else {
      // Criar
      criarMutation.mutate(data)
    }
  }

  /**
   * Handler para editar evento
   */
  const handleEditarEvento = (evento: Evento) => {
    // Define o evento como sendo editado
    setEventoEditando(evento)
    // Scroll para o formulário (opcional)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  /**
   * Handler para deletar evento
   */
  const handleDeletarEvento = async (id: number) => {
    // Pede confirmação ao usuário
    if (confirm('Tem certeza que deseja deletar este evento?')) {
      setDeletandoId(id)
      deletarMutation.mutate(id)
    }
  }

  /**
   * Handler para cancelar edição
   */
  const handleCancelarEdicao = () => {
    setEventoEditando(null)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header da aplicação */}
      <header className="bg-white shadow">
        <div className="container py-6">
          <h1 className="text-4xl font-bold text-gray-900">
            📅 Smart Agenda
          </h1>
          <p className="text-gray-600 mt-2">
            Gerenciador de eventos com lembretes automáticos
          </p>
        </div>
      </header>

      {/* Conteúdo principal */}
      <main className="container py-8">
        {/* Seção de formulário */}
        <EventForm
          evento={eventoEditando}
          onSubmit={handleSalvarEvento}
          isLoading={criarMutation.isPending || atualizarMutation.isPending}
          onCancel={eventoEditando ? handleCancelarEdicao : undefined}
        />

        {/* Seção de lista de eventos */}
        <EventList
          onEdit={handleEditarEvento}
          onDelete={handleDeletarEvento}
          deletingId={deletandoId}
        />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="container py-6 text-center text-gray-500">
          <p>
            Smart Agenda v0.1.0 | Desenvolvido com React + FastAPI
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
