from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.interfaces.api.schemas import EventoCreateSchema, EventoResponse
from app.infrastructure.db.database import get_db
from app.infrastructure.db.repositories import SQLAlchemyEventoRepository
from app.application.services.services import AgendaService

# Cria roteador que agrupa endpoints de eventos
router = APIRouter()


@router.get("/health")
def health_check():
    """
    Endpoint de health check.

    Verifica se a API está online respondendo rapidamente.

    Retorno: {"status": "ok"}
    """
    return {"status": "ok"}


@router.post("/eventos/", response_model=EventoResponse)
def criar_evento_endpoint(payload: EventoCreateSchema, db: Session = Depends(get_db)):
    """
    Cria um novo evento no sistema.

    Procedimento:
    1. Recebe dados JSON via payload (EventoCreateSchema)
    2. Obtém sessão de banco via dependency injection (Depends)
    3. Instancia repositório com sessão
    4. Instancia serviço com repositório
    5. Chama criar_novo_evento() passando dados dedisbrigados
    6. Se sucesso: retorna evento com ID (EventoResponse)
    7. Se falha: retorna HTTP 400 com mensagem de erro

    Payload necessário:
    - titulo: string (obrigatório)
    - data_horario: datetime ISO (obrigatório)
    - email_usuario: email válido (obrigatório)
    - descricao: string (opcional)
    - lembretes: array de {minutos_antecedencia: int} (opcional)
    """

    # Instancia repositório para acesso ao banco
    repo = SQLAlchemyEventoRepository(db)
    # Instancia serviço de negócio com repositório
    service = AgendaService(repo)

    try:
        # Chama método do serviço desagregando dados do payload
        evento = service.criar_novo_evento(
            titulo=payload.titulo,
            data=payload.data_horario,
            email_usuario=payload.email_usuario,
            descricao=payload.descricao,
            lembretes=[l.minutos_antecedencia for l in payload.lembretes],
        )

        # Retorna evento criado (FastAPI serializa automaticamente para JSON)
        return evento

    except ValueError as e:
        # Se houver erro de validação, retorna HTTP 400
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/eventos/", response_model=list[EventoResponse])
def listar_eventos(db: Session = Depends(get_db)):
    """
    Lista todos os eventos cadastrados.

    Procedimento:
    1. Obtém sessão de banco via dependency injection
    2. Instancia repositório
    3. Chama listar() para buscar todos os eventos
    4. Retorna lista em formato EventoResponse

    Retorno: array de EventoResponse
    """

    # Instancia repositório para acesso ao banco
    repo = SQLAlchemyEventoRepository(db)
    # Busca todos os eventos da tabela
    eventos = repo.listar()

    # Retorna lista (FastAPI serializa automaticamente)
    return eventos


@router.put("/eventos/{evento_id}", response_model=EventoResponse)
def atualizar_evento_endpoint(
    evento_id: int, payload: EventoCreateSchema, db: Session = Depends(get_db)
):
    """
    Atualiza um evento existente substituindo todos seus dados.

    Procedimento:
    1. Recebe ID do evento na URL
    2. Recebe dados novos no payload JSON
    3. Obtém sessão de banco
    4. Instancia repositório e serviço
    5. Chama atualizar_evento() passando ID e dados novos
    6. Repositório remove lembretes antigos e insere novos
    7. Se sucesso: retorna evento atualizado
    8. Se evento não existe: retorna HTTP 404

    Parâmetro URL:
    - evento_id: ID do evento a atualizar

    Payload: mesmo formato do POST (EventoCreateSchema)
    """

    # Instancia repositório para acesso ao banco
    repo = SQLAlchemyEventoRepository(db)
    # Instancia serviço de negócio
    service = AgendaService(repo)

    try:
        # Chama método de atualização do serviço
        evento = service.atualizar_evento(
            evento_id=evento_id,
            titulo=payload.titulo,
            data=payload.data_horario,
            email_usuario=payload.email_usuario,
            descricao=payload.descricao,
            lembretes=[l.minutos_antecedencia for l in payload.lembretes],
        )

        # Retorna evento atualizado
        return evento

    except ValueError as e:
        # Se evento não encontrado, retorna HTTP 404
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/eventos/{evento_id}")
def excluir_evento_endpoint(evento_id: int, db: Session = Depends(get_db)):
    """
    Exclui um evento do sistema.

    Procedimento:
    1. Recebe ID do evento na URL
    2. Obtém sessão de banco
    3. Instancia repositório e serviço
    4. Chama excluir_evento() passando ID
    5. Repositório delete evento (cascata remove lembretes/notificações)
    6. Se sucesso: retorna mensagem de confirmação
    7. Se evento não existe: retorna HTTP 404

    Parâmetro URL:
    - evento_id: ID do evento a excluir

    Retorno: {"status": "ok", "mensagem": "Evento excluído."}
    """

    # Instancia repositório para acesso ao banco
    repo = SQLAlchemyEventoRepository(db)
    # Instancia serviço de negócio
    service = AgendaService(repo)

    try:
        # Chama método de exclusão
        service.excluir_evento(evento_id)
        # Retorna mensagem de sucesso
        return {"status": "ok", "mensagem": "Evento excluído."}

    except ValueError as e:
        # Se evento não encontrado, retorna HTTP 404
        raise HTTPException(status_code=404, detail=str(e))
