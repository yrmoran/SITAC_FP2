from collections import Counter
from datetime import datetime
from exceptions import AsignacionError, TicketNoEncontradoError, ValidacionError
from models import AgenteATC, EstadoTicket, Prioridad, Ticket

class GestorTickets:
    _instancia=None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia=super().__new__(cls); cls._instancia._inicializado=False
        return cls._instancia
    def __init__(self):
        if self._inicializado: return
        self.tickets=[]; self.agentes=[]; self._inicializado=True
    def registrar_agente(self, agente):
        if any(a.identificador==agente.identificador for a in self.agentes): raise ValidacionError('Ya existe ese agente.')
        self.agentes.append(agente)
    def registrar_ticket(self,ticket):
        if any(t.id_ticket==ticket.id_ticket for t in self.tickets): raise ValidacionError('Ya existe ese ticket.')
        self.tickets.append(ticket)
    def buscar_ticket(self,id_ticket):
        for t in self.tickets:
            if t.id_ticket.lower()==id_ticket.lower(): return t
        raise TicketNoEncontradoError(f'No se encontró el ticket {id_ticket}.')
    def listar_tickets(self): return list(self.tickets)
    def priorizar_tickets(self):
        return sorted(self.tickets,key=lambda t:(t.prioridad.value,t.fecha_reporte.timestamp()),reverse=True)
    def asignar_ticket(self,id_ticket,id_agente):
        ticket=self.buscar_ticket(id_ticket)
        agente=next((a for a in self.agentes if a.identificador.lower()==id_agente.lower()),None)
        if agente is None: raise AsignacionError('No existe el agente indicado.')
        ticket.asignar(agente)
    def actualizar_estado(self,id_ticket,estado): self.buscar_ticket(id_ticket).actualizar_estado(estado)
    def estadisticas(self):
        return {'total':len(self.tickets),'por_criticidad':dict(Counter(t.prioridad.name for t in self.tickets)),'por_estado':dict(Counter(t.estado.value for t in self.tickets)),'por_tipo':dict(Counter(t.incidencia.tipo() for t in self.tickets))}
    def cargar_datos_demo(self):
        from models import Cliente,IncidenciaApuesta,IncidenciaMercado,IncidenciaPlataforma
        if self.tickets: return
        for a in [AgenteATC('Ana Torres','A001','Apuestas'),AgenteATC('Luis Ramos','A002','Plataforma')]: self.registrar_agente(a)
        datos=[('Juan Pérez','C001','juan@example.com',IncidenciaApuesta('No puede visualizar el cupón.',Prioridad.ALTA)),('María López','C002','maria@example.com',IncidenciaMercado('No aparecen las cuotas.',Prioridad.MEDIA)),('Carlos Díaz','C003','carlos@example.com',IncidenciaPlataforma('No carga resultados.',Prioridad.BAJA))]
        for i,(n,c,e,inc) in enumerate(datos,1): self.registrar_ticket(Ticket(f'T{i:03}',Cliente(n,c,e),inc,datetime.now()))
