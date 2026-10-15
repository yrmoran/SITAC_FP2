import unittest
from models import Cliente,AgenteATC,EstadoTicket,IncidenciaApuesta,IncidenciaMercado,Prioridad,Ticket
from services import GestorTickets
class TestGestor(unittest.TestCase):
    def setUp(self):
        self.g=GestorTickets(); self.g.tickets.clear(); self.g.agentes.clear(); self.c=Cliente('Prueba','C1','p@test.com'); self.a=AgenteATC('Agente','A1','Apuestas'); self.g.registrar_agente(self.a)
    def test_registro_busqueda(self):
        self.g.registrar_ticket(Ticket('T1',self.c,IncidenciaApuesta('x',Prioridad.ALTA))); self.assertEqual(self.g.buscar_ticket('T1').id_ticket,'T1')
    def test_prioridad(self):
        self.g.registrar_ticket(Ticket('T1',self.c,IncidenciaMercado('x',Prioridad.BAJA))); self.g.registrar_ticket(Ticket('T2',self.c,IncidenciaApuesta('x',Prioridad.ALTA))); self.assertEqual(self.g.priorizar_tickets()[0].id_ticket,'T2')
    def test_asignacion_estado(self):
        t=Ticket('T1',self.c,IncidenciaApuesta('x',Prioridad.MEDIA)); self.g.registrar_ticket(t); self.g.asignar_ticket('T1','A1'); self.assertEqual(t.estado,EstadoTicket.ASIGNADO)
    def test_estadisticas(self):
        self.g.registrar_ticket(Ticket('T1',self.c,IncidenciaApuesta('x',Prioridad.ALTA))); self.assertEqual(self.g.estadisticas()['total'],1)
if __name__=='__main__': unittest.main()
