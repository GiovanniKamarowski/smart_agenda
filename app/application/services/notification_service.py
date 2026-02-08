from datetime import datetime
from app.domain.entities import Notificacao
from app.infrastructure.notifications.email_adapter import EmailAdapter
from app.infrastructure.config import logger


class NotificationService:
    """
    Serviço responsável por orquestrar o envio de notificações.

    Ele não acessa o banco diretamente.
    Ele apenas chama o adapter correto (email, whatsapp futuramente).
    """

    def __init__(self):
        """
        Inicializa o serviço com o adapter de email.

        Instancia o EmailAdapter que será usado para enviar notificações
        via SMTP com configurações do .env.
        """
        # Cria instância do adapter para orquestrar envios de emails
        self.email_adapter = EmailAdapter()

    def enviar_notificacao_email(
        self, destinatario: str, titulo_evento: str, data_evento: datetime
    ):
        """
        Envia uma notificação via e-mail para um evento específico.

        Procedimento:
        1. Monta assunto com nome do evento
        2. Monta corpo amigável com detalhes do compromisso
        3. Faz log da preparação
        4. Delega envio para EmailAdapter
        5. Se falhar, lança exceção para registro na tabela de notificações
        """

        # Cria assunto com nome descritivo do evento
        assunto = f"Lembrete: {titulo_evento}"

        # Cria corpo do email com informações do compromisso
        mensagem = (
            f"Você tem um compromisso agendado!\n\n"
            f"Título: {titulo_evento}\n"
            f"Data/Hora: {data_evento}\n\n"
            f"SmartAgenda - Notificação automática"
        )

        # Registra tentativa de envio para rastreamento
        logger.info(
            f"[SERVICE] Preparando envio de email para {destinatario} (evento: {titulo_evento})"
        )

        # Delega envio ao adapter (qualquer erro sobe para o chamador tratar)
        self.email_adapter.enviar_email(destinatario, assunto, mensagem)
