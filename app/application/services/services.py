from app.domain.entities import Evento


class AgendaService:
    """
    Serviço de orquestração para Cadastro e Gerenciamento de Eventos.

    Responsabilidades:
    - Recebe requisições da API
    - Instancia entidades do domínio
    - Valida regras de negócio (ex: lembretes negativos)
    - Delega persistência ao repositório
    - Retorna domínio ao chamador

    Esta classe é a ponte entre a camada de interfaces (API) e
    a camada de infraestrutura (banco de dados).
    """

    def __init__(self, repo):
        """
        Inicializa o serviço com um repositório.

        Parâmetro:
        - repo: instância de repositório (SQLAlchemyEventoRepository)
        """
        # Armazena referência ao repositório para operações de banco
        self.repo = repo

    def criar_novo_evento(
        self, titulo, data, email_usuario, descricao=None, lembretes=None
    ):
        """
        Cria um evento novo e adiciona lembretes se forem informados.

        Procedimento:
        1. Instancia nova entidade Evento com dados fornecidos
        2. Itera sobre lista de lembretes e adiciona cada um
           (validação de negativos feita pela entidade)
        3. Delega persistência ao repositório
        4. Retorna evento com ID gerado pelo banco

        Parâmetros:
        - titulo: nome do compromisso
        - data: data e hora do evento
        - email_usuario: email para notificações
        - descricao: detalhes opcionais
        - lembretes: lista de inteiros (minutos antes do evento)

        Lança ValueError se minutos de lembrete for negativo.
        """

        # Cria nova instância de evento (entidade de domínio)
        novo_evento = Evento(
            titulo=titulo,
            data_horario=data,
            email_usuario=email_usuario,
            descricao=descricao,
        )

        # Itera sobre minutos de antecedência e adiciona lembrete
        if lembretes:
            for minutos in lembretes:
                # Método adicionar_lembrete valida negativos
                novo_evento.adicionar_lembrete(minutos)

        # Delega persistência ao repositório (salva no banco)
        return self.repo.salvar(novo_evento)

    def atualizar_evento(
        self, evento_id, titulo, data, email_usuario, descricao=None, lembretes=None
    ):
        """
        Atualiza um evento existente. Substitui os lembretes pelos novos fornecidos.

        Procedimento:
        1. Instancia entidade Evento com dados atualizados
        2. Itera sobre novos lembretes e adiciona à entidade
        3. Delega atualização ao repositório
        4. Retorna evento atualizado

        Parâmetros:
        - evento_id: ID do evento a atualizar (banco de dados)
        - titulo: novo título
        - data: nova data/hora
        - email_usuario: novo email
        - descricao: nova descrição (opcional)
        - lembretes: nova lista de minutos

        Lança ValueError se evento_id não existir.
        """

        # Cria nova entidade com dados atualizados
        evento = Evento(
            titulo=titulo,
            data_horario=data,
            email_usuario=email_usuario,
            descricao=descricao,
        )

        # Itera sobre novos lembretes
        if lembretes:
            for minutos in lembretes:
                evento.adicionar_lembrete(minutos)

        # Delega atualização ao repositório (remove antigos, insere novos)
        return self.repo.atualizar(evento_id, evento)

    def excluir_evento(self, evento_id):
        """
        Exclui um evento pelo seu ID.

        Procedimento:
        1. Delega exclusão ao repositório
        2. Repositório remove evento e seus filhos (lembretes, notificações)
           via cascade do banco

        Parâmetro:
        - evento_id: ID do evento a excluir

        Lança ValueError se evento_id não existir.
        """
        # Delega exclusão ao repositório (SQL delete com cascade)
        return self.repo.excluir(evento_id)
