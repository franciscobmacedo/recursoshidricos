from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Network(Base):
    __tablename__ = "networks"

    id = Column(String, primary_key=True, index=True)
    nome = Column(String, index=True)

    stations = relationship("Station", back_populates="network")


class StationParameter(Base):
    __tablename__ = "StationParameter"
    id = Column(Integer, primary_key=True, index=True)
    stationId = Column(String, ForeignKey("stations.id"))
    parameterId = Column(String, ForeignKey("parameters.id"))


class Station(Base):
    __tablename__ = "stations"

    id = Column(String, primary_key=True, index=True)
    codigo = Column(String, index=True)
    nome = Column(String, index=True)
    altitude = Column(String, index=True)
    latitude = Column(String, index=True)
    longitude = Column(String, index=True)
    coord_x = Column(String, index=True)
    coord_y = Column(String, index=True)
    bacia = Column(String, index=True)
    distrito = Column(String, index=True)
    concelho = Column(String, index=True)
    freguesia = Column(String, index=True)
    entidade_responsavel_automatica = Column(String, index=True)
    entidade_responsavel_convencional = Column(String, index=True)
    tipo_estacao_automatica = Column(String, index=True)
    tipo_estacao_convencional = Column(String, index=True)
    entrada_funcionamento_convencional = Column(String, index=True)
    entrada_funcionamento_automatica = Column(String, index=True)
    encerramento_convencional = Column(String, index=True)
    encerramento_automatica = Column(String, index=True)
    telemetria = Column(Boolean, index=True, unique=False, default=True)
    estado = Column(String, index=True)
    indice_qualidade = Column(String, index=True)

    network_id = Column(String, ForeignKey("networks.id"))
    network = relationship("Network", back_populates="stations")

    parameters = relationship(
        "Parameter", secondary="StationParameter", back_populates="stations"
    )


class Parameter(Base):
    __tablename__ = "parameters"

    id = Column(String, primary_key=True, index=True)
    nome = Column(String, index=True)

    stations = relationship(
        "Station", secondary="StationParameter", back_populates="parameters"
    )
