import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.infrastructure.config import settings, logger, validar_config_smtp


class EmailAdapter:
    """
    Adapter responsável por enviar e-mails usando SMTP.

    Esse adapter fica isolado da regra de negócio, permitindo trocar SMTP
    por qualquer outro serviço no futuro (SendGrid, AWS SES, etc).
    """

    def enviar_email(self, destinatario: str, assunto: str, mensagem: str):
        """
        Envia um e-mail via SMTP.

        Procedimento:
        1. Valida se configurações SMTP estão completas
        2. Monta estrutura MIME (From, To, Subject, corpo)
        3. Faz dica rápida se detectado SMTP do Gmail
        4. Conecta ao servidor SMTP com timeout de 20s
        5. Autentica com TLS (criptografia)
        6. Envia mensagem
        7. Se sucesso: log de sucesso
        8. Se falha: log completo com stacktrace e relança exceção

        Parâmetros:
        - destinatario: email que vai receber a mensagem
        - assunto: título do email
        - mensagem: conteúdo principal do email (texto simples)
        """

        # Valida se todas as variáveis necessárias estão carregadas do .env
        try:
            validar_config_smtp()
        except Exception as e:
            logger.error(f"[EMAIL] Configuração SMTP inválida: {e}")
            raise

        # Cria estrutura MIME correta com headers necessários
        msg = MIMEMultipart()
        msg["From"] = settings.SMTP_FROM  # Remetente
        msg["To"] = destinatario  # Destinatário
        msg["Subject"] = assunto  # Assunto

        # Adiciona corpo do email (texto simples, não HTML)
        msg.attach(MIMEText(mensagem, "plain"))

        # Detecta Gmail e faz recomendação de configuração
        if "gmail" in settings.SMTP_HOST.lower():
            logger.info(
                "[EMAIL] Detectado SMTP do Gmail. Use senha de app e porta 587 (TLS)."
            )

        # Conecta ao servidor SMTP e envia o email
        try:
            # Abre conexão com servidor SMTP (timeout evita travamentos)
            with smtplib.SMTP(
                settings.SMTP_HOST, settings.SMTP_PORT, timeout=20
            ) as server:
                # Protocolo SMTP: cumprimento inicial
                server.ehlo()
                # Inicia criptografia TLS (segurança)
                server.starttls()
                # Cumprimento novo após TLS ativado
                server.ehlo()
                # Autentica com usuário e senha do .env
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                # Envia a mensagem para todos os destinatários
                server.send_message(msg)

                # Log de sucesso para rastreamento
                logger.info(
                    f"[EMAIL] Email enviado para {destinatario} (assunto: {assunto})"
                )

        except Exception as exc:
            # Log de erro com mensagem clara
            logger.error(f"[EMAIL] Falha ao enviar email para {destinatario}: {exc}")
            # Log do stacktrace completo para debugging detalhado
            logger.error(traceback.format_exc())
            # Relança exceção para caller tratar (scheduler registra falha no banco)
            raise
