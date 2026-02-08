from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class LembreteSchema(BaseModel):
    """
    Schema Pydantic para representar um lembrete na API.

    Usado:
    - Em requisições: quando cliente envia lembretes para criar/atualizar evento
    - Em respostas: quando API retorna evento com seus lembretes

    Pydantic faz validação automática de tipos.
    """

    # Minutos antes do evento para enviar notificação
    minutos_antecedencia: int


class EventoCreateSchema(BaseModel):
    """
    Schema Pydantic para criar ou atualizar um evento via API.

    Usado em requisições:
    - POST /eventos/ (criar novo evento)
    - PUT /eventos/{id} (atualizar evento existente)

    Pydantic valida:
    - titulo: deve ser string (não-vazio)
    - data_horario: deve ser datetime válido (ISO 8601)
    - email_usuario: deve ser email válido (validado por EmailStr)
    - descricao: pode ser string ou None (opcional)
    - lembretes: deve ser lista de objetos com minutos_antecedencia
    """

    # Título/nome do compromisso (obrigatório)
    titulo: str

    # Data e hora do evento em formato ISO (obrigatório)
    data_horario: datetime

    # Email do usuário (validado como email real por EmailStr)
    email_usuario: EmailStr

    # Detalhes sobre o evento (opcional, padrão: None)
    descricao: Optional[str] = None

    # Array de lembretes (opcional, padrão: lista vazia)
    lembretes: List[LembreteSchema] = []


class EventoResponse(BaseModel):
    """
    Schema Pydantic para retornar um evento nas respostas da API.

    Usado em respostas de:
    - POST /eventos/ (retorna evento criado)
    - GET /eventos/ (lista de eventos)
    - GET /eventos/{id} (evento específico)
    - PUT /eventos/{id} (evento atualizado)
    - DELETE /eventos/{id} (confirmação com dados)

    Diferença de EventoCreateSchema:
    - Inclui campo 'id' que é preenchido pelo banco
    - Config 'from_attributes' permite converter SQLAlchemy Model para JSON
    """

    # ID único gerado pelo banco (obrigatório na resposta)
    id: int

    # Título do evento
    titulo: str

    # Data/hora do evento
    data_horario: datetime

    # Email do usuário
    email_usuario: EmailStr

    # Descrição opcional
    descricao: Optional[str] = None

    # Lista de lembretes do evento
    lembretes: List[LembreteSchema] = []

    class Config:
        """
        Configuração Pydantic para conversão de banco em JSON.

        'from_attributes=True' permite:
        - Ler atributos de objetos SQLAlchemy automaticamente
        - FastAPI converter model.attr para JSON sem DTO manual

        Sem isto, Pydantic não consegue extrair dados de modelos ORM.
        """

        from_attributes = True
