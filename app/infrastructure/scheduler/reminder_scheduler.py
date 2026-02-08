import time
from datetime import datetime, timedelta
import traceback

from app.infrastructure.db.database import SessionLocal
from app.infrastructure.db.models import EventoModel, LembreteModel
from app.infrastructure.db.repositories import SQLAlchemyNotificacaoRepository
from app.domain.entities import Notificacao
from app.application.services.notification_service import NotificationService
from app.infrastructure.config import logger


class ReminderScheduler:
    """
    Scheduler responsável por verificar lembretes pendentes e disparar notificações.

    Esse scheduler roda em loop e executa uma checagem periódica no banco.
    Cada ação importante é logada com prefixo [SCHEDULER].
    """

    def __init__(self, intervalo_segundos: int = 30):
        """
        Inicializa o scheduler definindo o intervalo de checagem.

        Parâmetro:
        - intervalo_segundos: tempo em segundos entre cada verificação de lembretes
                             (padrão: 30 segundos)
        """
        # Tempo em segundos que o scheduler aguarda entre checagens
        self.intervalo_segundos = intervalo_segundos
        # Flag que controla se o scheduler está rodando (True) ou parado (False)
        self.rodando = False

    def iniciar(self):
        """
        Inicia o loop do scheduler.

        Procedimento:
        1. Liga flag rodando (True)
        2. Faz log de início
        3. Entra em loop infinito:
           - chama processar_lembretes() a cada intervalo
           - captura erros inesperados e faz log completo
           - aguarda intervalo_segundos
        4. Para quando rodando=False (chamada parar())
        """
        # Liga flag que mantém loop ativo
        self.rodando = True
        # Registra que o scheduler está iniciando
        logger.info("[SCHEDULER] Iniciando ReminderScheduler")

        # Loop principal: roda enquanto rodando=True
        while self.rodando:
            try:
                # Executa verificação de lembretes
                self.processar_lembretes()
            except Exception:
                # Captura erros inesperados e faz log com exceção traceback
                logger.exception("[SCHEDULER] Erro inesperado durante processamento")

            # Aguarda intervalo antes de próxima verificação
            time.sleep(self.intervalo_segundos)

    def parar(self):
        """
        Para o scheduler.
        """
        self.rodando = False
        logger.info("[SCHEDULER] Parando ReminderScheduler")

    def processar_lembretes(self):
        """
        Processa todos os eventos e lembretes e verifica se está na hora de enviar notificação.

        Lógica:
        1. Conexão com banco e instância de repositórios/serviços
        2. Obtém data/hora atual
        3. Busca todos os eventos no banco
        4. Para cada evento: busca lembretes associados
        5. Para cada lembrete: calcula horário de disparo (evento - minutos)
        6. Se agora >= horário_disparo:
           - Verifica se já foi enviado (evita duplicação)
           - Cria registro "PENDENTE" na tabela notificacoes
           - Tenta enviar email via NotificationService
           - Marca como ENVIADO se sucesso ou FALHOU se erro
        7. Fecha conexão com banco
        """

        # Abre nova conexão com banco (requisito SQLAlchemy)
        db = SessionLocal()
        # Instancia repositório para manipular notificações no banco
        notificacao_repo = SQLAlchemyNotificacaoRepository(db)

        try:
            # Busca TODOS os eventos cadastrados no banco
            eventos = db.query(EventoModel).all()

            # Obtém data/hora atual no servidor
            agora = datetime.now()

            # Instancia serviço para orquestrar envio de notificações
            notification_service = NotificationService()

            # Log de transparência mostrando quantos eventos foram encontrados
            logger.info(f"[SCHEDULER] Encontrados {len(eventos)} evento(s) na checagem")

            # Processa cada evento individualmente
            for evento in eventos:
                # Busca lembretes vinculados a este evento específico
                lembretes = (
                    db.query(LembreteModel)
                    .filter(LembreteModel.evento_id == evento.id)
                    .all()
                )

                # Processa cada lembrete do evento
                for lembrete in lembretes:
                    # Calcula horário em que a notificação deve ser disparada
                    # Exemplo: evento 14:30h com lembrete 30min = disparo 14:00h
                    horario_disparo = evento.data_horario - timedelta(
                        minutes=lembrete.minutos_antecedencia
                    )

                    # Se ainda não chegou na hora de enviar, pula para próximo lembrete
                    if agora < horario_disparo:
                        continue

                    # Log mostrando lembrete que está na hora de ser disparado
                    logger.info(
                        f"[SCHEDULER] Lembrete devido: evento_id={evento.id} "
                        f"email={evento.email_usuario} minutos={lembrete.minutos_antecedencia}"
                    )

                    # Verifica se ja_enviada() retorna True (evita reenvios duplicados)
                    if notificacao_repo.ja_enviada(
                        evento_id=evento.id,
                        lembrete_minutos=lembrete.minutos_antecedencia,
                        canal="email",
                    ):
                        # Log informando que notificação já foi enviada anteriormente
                        logger.info(
                            f"[SCHEDULER] Notificação já enviada anteriormente para evento_id={evento.id} minutos={lembrete.minutos_antecedencia}"
                        )
                        # Pula para próximo lembrete (não reenvia)
                        continue

                    # Cria registro de notificação no banco com status "PENDENTE"
                    notificacao = Notificacao(
                        evento_id=evento.id,
                        lembrete_minutos=lembrete.minutos_antecedencia,
                        canal="email",
                        status="PENDENTE",
                    )

                    # Insere notificação no banco e obtém ID
                    notificacao = notificacao_repo.criar(notificacao)

                    # Tenta enviar email (pode falhar por SMTP, internet, etc)
                    try:
                        # Log informando tentativa de envio
                        logger.info(
                            f"[SCHEDULER] Tentando enviar email para {evento.email_usuario}"
                        )
                        # Chama serviço para montar e enviar email
                        notification_service.enviar_notificacao_email(
                            destinatario=evento.email_usuario,
                            titulo_evento=evento.titulo,
                            data_evento=evento.data_horario,
                        )
                        # Se sucesso, marca notificação como ENVIADO no banco
                        notificacao_repo.marcar_enviado(notificacao.id)

                        # Log de sucesso para auditoria
                        logger.info(
                            f"[SCHEDULER] Email enviado com sucesso para {evento.email_usuario}"
                        )

                    except Exception as erro_envio:
                        # Captura qualquer erro no envio (SMTP, timeout, etc)
                        # Log com mensagem erro
                        logger.error(
                            f"[SCHEDULER] Falha ao enviar email para {evento.email_usuario}: {erro_envio}"
                        )
                        # Log com stacktrace completo para debugging
                        logger.error(traceback.format_exc())
                        # Marca notificação como FALHOU no banco e armazena erro
                        notificacao_repo.marcar_falha(notificacao.id, str(erro_envio))

        finally:
            # Fecha conexão com banco (libera recurso) sempre, mesmo em erro
            db.close()

    def enviar_email(
        self, email_destino: str, titulo_evento: str, data_evento: datetime
    ):
        """
        Método legacy mantido para compatibilidade com código antigo.

        Antes era usado para simular envio de email com print().
        Agora apenas realiza um log informativo.

        Não é mais utilizado pela lógica principal (use enviar_notificacao_email do serviço).
        """
        # Log informando que método legacy foi chamado
        logger.info("[SCHEDULER] enviar_email chamado (modo legacy)")
        # Log informativo com os dados que foram passados (sem enviar realmente)
        logger.info(
            f"[SCHEDULER] ENVIANDO EMAIL PARA: {email_destino} | EVENTO: {titulo_evento} | DATA: {data_evento}"
        )
