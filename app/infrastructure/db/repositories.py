from sqlalchemy.orm import Session
from datetime import datetime

from app.infrastructure.db.models import EventoModel, LembreteModel, NotificacaoModel
from app.domain.entities import Evento, Lembrete, Notificacao


class SQLAlchemyEventoRepository:
    """
    Repositório responsável por manipular eventos no banco usando SQLAlchemy.
    """

    def __init__(self, db: Session):
        """
        Recebe uma sessão ativa do banco.
        """
        self.db = db

    def salvar(self, evento: Evento) -> Evento:
        """
        Salva um novo evento no banco e retorna o evento com ID preenchido.

        Procedimento:
        1. Converte a entidade Evento para o modelo SQLAlchemy EventoModel
        2. Insere na tabela 'eventos' e confirma transação (commit)
        3. Obtém o ID gerado automaticamente pelo banco
        4. Itera sobre lembretes da entidade e insere cada um (LembreteModel)
        5. Confirma novamente e retorna a entidade com ID preenchido
        """

        # Monta o modelo SQL convertendo dados da entidade de domínio
        evento_model = EventoModel(
            titulo=evento.titulo,
            descricao=evento.descricao,
            data_horario=evento.data_horario,
            email_usuario=evento.email_usuario,
        )

        # Adiciona o evento à sessão e confirma inserção no banco
        self.db.add(evento_model)
        self.db.commit()
        # Refresh sincroniza o modelo local com dados do banco (obtém ID)
        self.db.refresh(evento_model)

        # Itera sobre cada lembrete da entidade e cria corresponde modelo SQL
        for lembrete in evento.lembretes:
            lembrete_model = LembreteModel(
                minutos_antecedencia=lembrete.minutos_antecedencia,
                evento_id=evento_model.id,  # Usa ID do evento que foi inserido
            )
            self.db.add(lembrete_model)

        # Confirma inserção de todos os lembretes
        self.db.commit()

        # Preenche ID da entidade de domínio com o ID gerado no banco
        evento.id = evento_model.id
        return evento

    def listar(self):
        """
        Lista todos os eventos cadastrados.
        """
        return self.db.query(EventoModel).all()

    def buscar_por_id(self, evento_id: int) -> EventoModel | None:
        """
        Busca um evento pelo ID no banco.
        Retorna o model do SQLAlchemy (não a entidade).
        """
        return self.db.query(EventoModel).filter(EventoModel.id == evento_id).first()

    def atualizar(self, evento_id: int, evento: Evento) -> Evento:
        """
        Atualiza um evento existente e seus lembretes.

        Procedimento:
        1. Busca o evento no banco pelo ID
        2. Atualiza campos escalares (titulo, descricao, etc)
        3. Remove lembretes antigos da relação
        4. Insere novos lembretes conforme a entidade recebida
        5. Confirma transação e retorna entidade com ID

        Lança ValueError se o evento não existir.
        """

        # Consulta o banco buscando evento com o ID informado
        evento_model = (
            self.db.query(EventoModel).filter(EventoModel.id == evento_id).first()
        )

        # Se não encontrar, lança erro de validação
        if not evento_model:
            raise ValueError("Evento não encontrado")

        # Atualiza os campos escalares com novos valores
        evento_model.titulo = evento.titulo
        evento_model.descricao = evento.descricao
        evento_model.data_horario = evento.data_horario
        evento_model.email_usuario = evento.email_usuario

        # Remove lembretes antigos (cascade automático garante integridade)
        evento_model.lembretes.clear()
        self.db.commit()

        # Itera sobre novos lembretes da entidade e insere todos
        for lembrete in evento.lembretes:
            lembrete_model = LembreteModel(
                minutos_antecedencia=lembrete.minutos_antecedencia,
                evento_id=evento_model.id,
            )
            self.db.add(lembrete_model)

        # Confirma todas as mudanças no banco
        self.db.commit()
        # Sincroniza modelo local com estado do banco
        self.db.refresh(evento_model)

        # Preenche ID e retorna a entidade
        evento.id = evento_model.id
        return evento

    def excluir(self, evento_id: int) -> None:
        """
        Remove um evento do banco de dados (e seus lembretes/notificações via cascade).

        Procedimento:
        1. Busca o evento no banco pelo ID
        2. Deleta o evento (SQL cascade remove filhos: lembretes e notificações)
        3. Confirma transação

        Lança ValueError se o evento não existir.
        """

        # Consulta o banco buscando evento pelo ID
        evento_model = (
            self.db.query(EventoModel).filter(EventoModel.id == evento_id).first()
        )

        # Se não encontrar, lança erro
        if not evento_model:
            raise ValueError("Evento não encontrado")

        # Marca evento para deleção e confirma
        self.db.delete(evento_model)
        self.db.commit()


class SQLAlchemyNotificacaoRepository:
    """
    Repositório responsável por registrar e consultar notificações enviadas.
    """

    def __init__(self, db: Session):
        """
        Recebe uma sessão ativa do banco.
        """
        self.db = db

    def criar(self, notificacao: Notificacao) -> Notificacao:
        """
        Cria um registro de notificação no banco.

        Procedimento:
        1. Converte entidade Notificacao para modelo SQLAlchemy NotificacaoModel
        2. Insere na tabela 'notificacoes' (status inicial: PENDENTE)
        3. Obtém ID gerado automaticamente e preenche a entidade
        4. Retorna entidade com ID

        Contexto: chamado quando o scheduler identifica que um lembrete deve ser disparado.
        """

        # Monta modelo SQL convertendo dados da entidade de domínio
        notificacao_model = NotificacaoModel(
            evento_id=notificacao.evento_id,
            lembrete_minutos=notificacao.lembrete_minutos,
            canal=notificacao.canal,
            status=notificacao.status,
            data_envio=notificacao.data_envio,
            erro=notificacao.erro,
        )

        # Adiciona à sessão, confirma e sincroniza com banco
        self.db.add(notificacao_model)
        self.db.commit()
        self.db.refresh(notificacao_model)

        # Preenche ID da entidade e retorna
        notificacao.id = notificacao_model.id
        return notificacao

    def marcar_enviado(self, notificacao_id: int):
        """
        Atualiza a notificação no banco marcando como ENVIADO.

        Procedimento:
        1. Busca a notificação pelo ID
        2. Atualiza status para "ENVIADO" e registra data/hora
        3. Limpa campo de erro (já que foi sucesso)
        4. Confirma no banco
        """

        # Busca a notificação no banco
        notificacao = (
            self.db.query(NotificacaoModel)
            .filter(NotificacaoModel.id == notificacao_id)
            .first()
        )

        # Se encontrar, atualiza seus campos
        if notificacao:
            notificacao.status = "ENVIADO"
            notificacao.data_envio = datetime.now()
            notificacao.erro = None

            self.db.commit()

    def marcar_falha(self, notificacao_id: int, erro: str):
        """
        Atualiza a notificação no banco marcando como FALHOU e registrando o erro.

        Procedimento:
        1. Busca a notificação pelo ID
        2. Atualiza status para "FALHOU" e registra data/hora
        3. Armazena mensagem de erro completa
        4. Confirma no banco
        """

        # Busca a notificação no banco
        notificacao = (
            self.db.query(NotificacaoModel)
            .filter(NotificacaoModel.id == notificacao_id)
            .first()
        )

        # Se encontrar, marca como falha e armazena erro
        if notificacao:
            notificacao.status = "FALHOU"
            notificacao.data_envio = datetime.now()
            notificacao.erro = erro

            self.db.commit()

    def ja_enviada(self, evento_id: int, lembrete_minutos: int, canal: str) -> bool:
        """
        Verifica se uma notificação já foi enviada para aquele evento.

        Regra: evita reenvio duplicado verificando se existe registro
        com status ENVIADO para a mesma combinação de evento/lembrete/canal.

        Retorna:
        - True se já foi enviada (evita duplicação)
        - False se ainda não foi enviada
        """

        # Consulta banco buscando notificação com os critérios
        notificacao = (
            self.db.query(NotificacaoModel)
            .filter(NotificacaoModel.evento_id == evento_id)
            .filter(NotificacaoModel.lembrete_minutos == lembrete_minutos)
            .filter(NotificacaoModel.canal == canal)
            .filter(
                NotificacaoModel.status == "ENVIADO"
            )  # Só checa enviadas com sucesso
            .first()
        )

        # Retorna True se encontrou, False caso contrário
        return notificacao is not None

    def listar_pendentes(self):
        """
        Lista notificações pendentes no banco.

        Utilidade: permite implementar fila/reprocessamento de notificações
        que falharam anteriormente.

        Retorna lista de NotificacaoModel com status PENDENTE.
        """

        # Consulta e retorna todas as notificações pendentes
        return (
            self.db.query(NotificacaoModel)
            .filter(NotificacaoModel.status == "PENDENTE")
            .all()
        )
