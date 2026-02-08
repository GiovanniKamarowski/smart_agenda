from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.infrastructure.db.database import Base


class EventoModel(Base):
    """
    Representa a tabela de eventos no banco de dados.

    Essa tabela guarda os compromissos criados pelo usuário.
    """
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(Text, nullable=True)
    data_horario = Column(DateTime, nullable=False)
    email_usuario = Column(String, nullable=False)

    # Relacionamento: um evento pode ter vários lembretes
    lembretes = relationship("LembreteModel", back_populates="evento", cascade="all, delete-orphan")

    # Relacionamento: um evento pode ter várias notificações registradas
    notificacoes = relationship("NotificacaoModel", back_populates="evento", cascade="all, delete-orphan")


class LembreteModel(Base):
    """
    Representa a tabela de lembretes no banco de dados.

    Um lembrete é uma configuração do evento que diz quantos minutos antes avisar.
    """
    __tablename__ = "lembretes"

    id = Column(Integer, primary_key=True, index=True)
    minutos_antecedencia = Column(Integer, nullable=False)

    # FK para evento
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)

    # Relacionamento com EventoModel
    evento = relationship("EventoModel", back_populates="lembretes")


class NotificacaoModel(Base):
    """
    Representa a tabela de notificações no banco de dados.

    Cada registro representa uma tentativa real de envio de notificação.
    Serve para:
    - evitar reenvio duplicado
    - registrar falhas
    - permitir auditoria do sistema

    Essa tabela é essencial no MVP.
    """
    __tablename__ = "notificacoes"

    id = Column(Integer, primary_key=True, index=True)

    # FK do evento relacionado
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)

    # Minutos de antecedência do lembrete que originou a notificação
    lembrete_minutos = Column(Integer, nullable=False)

    # Canal de envio (email, whatsapp futuramente)
    canal = Column(String, nullable=False)

    # Status do envio: PENDENTE, ENVIADO, FALHOU
    status = Column(String, nullable=False, default="PENDENTE")

    # Data/hora em que foi enviado (ou falhou)
    data_envio = Column(DateTime, nullable=True)

    # Caso tenha falhado, salva o erro
    erro = Column(Text, nullable=True)

    # Data/hora em que o registro foi criado no banco
    criado_em = Column(DateTime, default=datetime.utcnow)

    # Relacionamento com EventoModel
    evento = relationship("EventoModel", back_populates="notificacoes")
