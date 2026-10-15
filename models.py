from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from exceptions import ValidacionError

class Prioridad(Enum):
    ALTA=3; MEDIA=2; BAJA=1

class EstadoTicket(Enum):
    PENDIENTE='Pendiente'; ASIGNADO='Asignado'; EN_PROCESO='En proceso'; RESUELTO='Resuelto'

@dataclass
class Persona(ABC):
    nombre: str
    identificador: str
    def __post_init__(self):
        if not self.nombre.strip(): raise ValidacionError('El nombre no puede estar vacío.')
        if not self.identificador.strip(): raise ValidacionError('El identificador no puede estar vacío.')
    @abstractmethod
    def descripcion_rol(self): pass

@dataclass
class Cliente(Persona):
    correo: str=''
    def descripcion_rol(self): return 'Cliente que reporta incidencias.'

@dataclass
class AgenteATC(Persona):
    especialidad: str='Atención al Cliente'
    def descripcion_rol(self): return f'Agente ATC - {self.especialidad}'

class Incidencia(ABC):
    def __init__(self, descripcion, criticidad):
        if not descripcion.strip(): raise ValidacionError('La descripción es obligatoria.')
        self.descripcion=descripcion; self.criticidad=criticidad
    @abstractmethod
    def tipo(self): pass
    @abstractmethod
    def detalle(self): pass

class IncidenciaApuesta(Incidencia):
    def tipo(self): return 'Apuesta'
    def detalle(self): return f'Problema relacionado con una apuesta. {self.descripcion}'

class IncidenciaMercado(Incidencia):
    def tipo(self): return 'Mercado'
    def detalle(self): return f'Problema relacionado con mercado/cuota. {self.descripcion}'

class IncidenciaPlataforma(Incidencia):
    def tipo(self): return 'Plataforma'
    def detalle(self): return f'Problema relacionado con la plataforma. {self.descripcion}'

@dataclass
class Ticket:
    id_ticket: str
    cliente: Cliente
    incidencia: Incidencia
    fecha_reporte: datetime=field(default_factory=datetime.now)
    estado: EstadoTicket=EstadoTicket.PENDIENTE
    agente: AgenteATC|None=None
    def __post_init__(self):
        if not self.id_ticket.strip(): raise ValidacionError('El ID del ticket es obligatorio.')
    @property
    def prioridad(self): return self.incidencia.criticidad
    def asignar(self, agente): self.agente=agente; self.estado=EstadoTicket.ASIGNADO
    def actualizar_estado(self, estado): self.estado=estado
    def resumen(self):
        agente=self.agente.nombre if self.agente else 'Sin asignar'
        return f'{self.id_ticket} | Cliente: {self.cliente.nombre} | Tipo: {self.incidencia.tipo()} | Criticidad: {self.prioridad.name} | Estado: {self.estado.value} | Fecha: {self.fecha_reporte:%d/%m/%Y %H:%M} | Agente: {agente}'
