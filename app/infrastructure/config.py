import os
import logging
from dotenv import load_dotenv


# Carrega variáveis de ambiente do arquivo .env na raiz do projeto.
# Sem isto, as variáveis ficariam None e os serviços falhariam.
load_dotenv()


class Settings:
    """
    Classe que centraliza todas as configurações do projeto.

    Lê variáveis de ambiente (via .env) eliminando hardcoding de senhas
    e hosts de produção no código-fonte.

    Padrão:
    - Se variável estiver no .env, usa o valor
    - Se não estiver, usa default (ex: porta 587 para SMTP)
    - Se não tiver default, fica cadeia vazia
    """

    # Host SMTP para envio de email (ex: smtp.gmail.com ou mail.seudominio.com)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")

    # Porta SMTP (padrão: 587 para TLS, 465 para SSL, 25 para plain)
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))

    # Usuário SMTP (email ou usuário do serviço)
    SMTP_USER: str = os.getenv("SMTP_USER", "")

    # Senha SMTP (pode ser senha de app no Gmail, não a senha da conta)
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")

    # Email remetente (endereço que aparece no "De:" do email enviado)
    SMTP_FROM: str = os.getenv("SMTP_FROM", "")


# Instancia a classe Settings criando objeto singleton 'settings'
# Usado em todo o projeto para acessar configurações
settings = Settings()


# Configuração de logging para o projeto inteiro.
# Registra mensagens de todo o sistema com prefixos como [EMAIL], [SCHEDULER], etc
logger = logging.getLogger("smart_agenda")

# Garante que logger só é configurado uma vez (evita duplicação de handlers)
if not logger.handlers:
    # Cria handler para enviar logs ao console (stdout)
    handler = logging.StreamHandler()

    # Define formato de log com timestamp, nível e mensagem
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    # Adiciona handler ao logger
    logger.addHandler(handler)

    # Define nível mínimo de log (INFO = mostra INFO, WARNING, ERROR; oculta DEBUG)
    logger.setLevel(logging.INFO)


def validar_config_smtp() -> None:
    """
    Valida se as configurações SMTP mínimas estão presentes.

    Procedimento:
    1. Cria lista de variáveis faltando
    2. Verifica cada configuração necessária
    3. Se alguma falta, adiciona à lista
    4. No final, se lista não está vazia, lança ValueError com detalhes

    Chamado por EmailAdapter antes de tentar enviar email.

    Lança:
    - ValueError: se alguma variável essencial estiver vazia
    """

    # Lista para armazenar nomes das variáveis que faltam
    missing = []

    # Verifica se host SMTP está preenchido
    if not settings.SMTP_HOST:
        missing.append("SMTP_HOST")

    # Verifica se usuário SMTP está preenchido
    if not settings.SMTP_USER:
        missing.append("SMTP_USER")

    # Verifica se senha SMTP está preenchida
    if not settings.SMTP_PASSWORD:
        missing.append("SMTP_PASSWORD")

    # Verifica se email remetente está preenchido
    if not settings.SMTP_FROM:
        missing.append("SMTP_FROM")

    # Se faltou alguma, lança erro listando as faltando
    if missing:
        raise ValueError(f"Variáveis SMTP faltando: {', '.join(missing)}")
