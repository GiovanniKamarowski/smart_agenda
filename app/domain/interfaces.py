from abc import ABC, abstractmethod
from typing import List
from app.domain.entities import Evento

class EventoRepositoryInterface(ABC):
    @abstractmethod
    def salvar(self, evento: Evento) -> Evento:
        pass

    @abstractmethod
    def listar(self) -> List[Evento]:
        pass

class NotificadorInterface(ABC):
    @abstractmethod
    def enviar_notificacao(self, destinatario: str, mensagem: str):
        pass