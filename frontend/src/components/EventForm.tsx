import React, { useState, useEffect } from 'react'
import { useForm, useFieldArray, Controller } from 'react-hook-form'
import { Evento, EventoCreatePayload } from '../services/api'
import dayjs from 'dayjs'

// Interface para as props do componente
interface EventFormProps {
  evento?: Evento | null // Se fornecido, está em modo edição
  onSubmit: (data: EventoCreatePayload) => void
  isLoading?: boolean
  onCancel?: () => void
}

/**
 * Componente EventForm
 * Formulário para criar ou editar eventos
 * Validação automática com react-hook-form
 */
export function EventForm({ evento, onSubmit, isLoading = false, onCancel }: EventFormProps) {
  // Usa react-hook-form para gerenciar o estado do formulário
  const { register, control, handleSubmit, formState: { errors }, reset } = useForm<EventoCreatePayload>({
    // Define valores padrão se estiver editando um evento existente
    defaultValues: evento ? {
      titulo: evento.titulo,
      data_horario: dayjs(evento.data_horario).format('YYYY-MM-DDTHH:mm'),
      email_usuario: evento.email_usuario,
      descricao: evento.descricao || '',
      lembretes: evento.lembretes,
    } : {
      titulo: '',
      data_horario: '',
      email_usuario: '',
      descricao: '',
      lembretes: [],
    }
  })

  // useFieldArray permite adicionar/remover lembretes dinamicamente
  const { fields, append, remove } = useFieldArray({
    control,
    name: 'lembretes',
  })

  // Função chamada quando o formulário é submetido
  const handleFormSubmit = (data: EventoCreatePayload) => {
    onSubmit(data)
  }

  // Função para adicionar um novo lembrete
  const adicionarLembrete = () => {
    append({ minutos_antecedencia: 15 })
  }

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="card mb-6">
      {/* Título do formulário */}
      <h2 className="text-2xl font-bold mb-6">
        {evento ? 'Editar Evento' : 'Criar Novo Evento'}
      </h2>

      {/* Campo Título */}
      <div className="mb-4">
        <label htmlFor="titulo" className="block text-sm font-medium text-gray-700 mb-2">
          Título *
        </label>
        <input
          id="titulo"
          {...register('titulo', { required: 'Título é obrigatório' })}
          type="text"
          placeholder="Digite o título do evento"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {errors.titulo && <span className="text-red-500 text-sm">{errors.titulo.message}</span>}
      </div>

      {/* Campo Email */}
      <div className="mb-4">
        <label htmlFor="email_usuario" className="block text-sm font-medium text-gray-700 mb-2">
          Email *
        </label>
        <input
          id="email_usuario"
          {...register('email_usuario', { 
            required: 'Email é obrigatório',
            pattern: {
              value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
              message: 'Email inválido'
            }
          })}
          type="email"
          placeholder="seu.email@example.com"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {errors.email_usuario && <span className="text-red-500 text-sm">{errors.email_usuario.message}</span>}
      </div>

      {/* Campo Data/Hora */}
      <div className="mb-4">
        <label htmlFor="data_horario" className="block text-sm font-medium text-gray-700 mb-2">
          Data e Hora *
        </label>
        <input
          id="data_horario"
          {...register('data_horario', { required: 'Data e hora são obrigatórias' })}
          type="datetime-local"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {errors.data_horario && <span className="text-red-500 text-sm">{errors.data_horario.message}</span>}
      </div>

      {/* Campo Descrição (opcional) */}
      <div className="mb-4">
        <label htmlFor="descricao" className="block text-sm font-medium text-gray-700 mb-2">
          Descrição
        </label>
        <textarea
          id="descricao"
          {...register('descricao')}
          placeholder="Descrição adicional (opcional)"
          rows={4}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Seção de Lembretes */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-lg font-semibold mb-4">Lembretes</h3>
        
        {/* Lista de lembretes existentes */}
        {fields.length > 0 ? (
          <div className="space-y-3 mb-4">
            {fields.map((field, index) => (
              <div key={field.id} className="flex gap-2 items-end">
                <div className="flex-1">
                  <label htmlFor={`lembrete-${index}`} className="block text-sm font-medium text-gray-700 mb-1">
                    Minutos de antecedência
                  </label>
                  <input
                    id={`lembrete-${index}`}
                    {...register(`lembretes.${index}.minutos_antecedencia`, { 
                      required: 'Campo obrigatório',
                      valueAsNumber: true
                    })}
                    type="number"
                    placeholder="Ex: 15"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                {/* Botão remover lembrete */}
                <button
                  type="button"
                  onClick={() => remove(index)}
                  className="btn-danger text-sm"
                >
                  Remover
                </button>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-sm mb-4">Nenhum lembrete adicionado ainda</p>
        )}

        {/* Botão adicionar lembrete */}
        <button
          type="button"
          onClick={adicionarLembrete}
          className="btn-secondary text-sm"
        >
          + Adicionar Lembrete
        </button>
      </div>

      {/* Botões de ação */}
      <div className="flex gap-3 justify-end">
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="btn-secondary"
          >
            Cancelar
          </button>
        )}
        <button
          type="submit"
          disabled={isLoading}
          className="btn-primary disabled:opacity-50"
        >
          {isLoading ? 'Salvando...' : (evento ? 'Atualizar' : 'Criar')}
        </button>
      </div>
    </form>
  )
}
