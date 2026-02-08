from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Lembrete:
    """
    Representa uma configuração de lembrete.
    Define quantos minutos antes do evento o sistema deve avisar.
    """
    minutos_antecedencia: int


@dataclass
class Notificacao:
    """
    Representa o registro de envio de uma notificação.

    Serve para armazenar no banco:
    - se foi enviada ou falhou
    - quando foi enviada
    - qual canal foi usado (email / whatsapp futuramente)
    - erro caso falhe
    """
    evento_id: int
    lembrete_minutos: int
    canal: str
    status: str = "PENDENTE"  # PENDENTE, ENVIADO, FALHOU
    data_envio: Optional[datetime] = None
    erro: Optional[str] = None
    id: Optional[int] = None

    def marcar_enviado(self):
        """
        Marca a notificação como enviada e registra a data/hora do envio.
        """
        self.status = "ENVIADO"
        self.data_envio = datetime.utcnow()
        self.erro = None

    def marcar_falha(self, mensagem_erro: str):
        """
        Marca a notificação como falha e registra o erro ocorrido.
        """
        self.status = "FALHOU"
        self.data_envio = datetime.utcnow()
        self.erro = mensagem_erro


@dataclass
class Evento:
    """
    Representa um compromisso cadastrado.

    Contém:
    - título
    - data/hora
    - email do usuário (para envio de notificação)
    - lembretes configurados
    """
    titulo: str
    data_horario: datetime
    email_usuario: str
    descricao: Optional[str] = None
    lembretes: List[Lembrete] = field(default_factory=list)
    id: Optional[int] = None

    def adicionar_lembrete(self, minutos: int):
        """
        Adiciona um lembrete ao evento.

        Regra de negócio:
        - não permitir lembrete com tempo negativo.
        """
        if minutos < 0:
            raise ValueError("O tempo de antecedência não pode ser negativo.")

        self.lembretes.append(Lembrete(minutos_antecedencia=minutos))
