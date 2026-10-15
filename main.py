from exceptions import TicketError
from models import Cliente,AgenteATC,EstadoTicket,IncidenciaApuesta,IncidenciaMercado,IncidenciaPlataforma,Prioridad,Ticket
from services import GestorTickets

gestor=GestorTickets()
def pausa(): input('\nPresione ENTER para continuar...')
def seleccionar_prioridad():
    op=input('Criticidad [1-Alta, 2-Media, 3-Baja]: ').strip(); m={'1':Prioridad.ALTA,'2':Prioridad.MEDIA,'3':Prioridad.BAJA}
    if op not in m: raise ValueError('Criticidad inválida.')
    return m[op]
def seleccionar_incidencia():
    op=input('Tipo [1-Apuesta, 2-Mercado, 3-Plataforma]: ').strip(); d=input('Descripción: ').strip(); p=seleccionar_prioridad()
    m={'1':IncidenciaApuesta,'2':IncidenciaMercado,'3':IncidenciaPlataforma}
    if op not in m: raise ValueError('Tipo inválido.')
    return m[op](d,p)
def registrar():
    print('\n=== REGISTRAR TICKET ==='); tid=input('ID: ').strip(); c=Cliente(input('Cliente: '),input('ID cliente: '),input('Correo: ')); t=Ticket(tid,c,seleccionar_incidencia()); gestor.registrar_ticket(t); print('Registrado:',t.resumen())
def buscar(): print(gestor.buscar_ticket(input('ID: ')).resumen())
def listar():
    ts=gestor.listar_tickets(); print('\n'.join(t.resumen() for t in ts) if ts else 'No hay tickets.')
def priorizar():
    for i,t in enumerate(gestor.priorizar_tickets(),1): print(i,t.resumen())
def asignar():
    for a in gestor.agentes: print(a.identificador,a.nombre,a.especialidad)
    gestor.asignar_ticket(input('Ticket: '),input('Agente: ')); print('Asignado correctamente.')
def actualizar():
    op=input('Estado [1-Pendiente,2-Asignado,3-En proceso,4-Resuelto]: '); m={'1':EstadoTicket.PENDIENTE,'2':EstadoTicket.ASIGNADO,'3':EstadoTicket.EN_PROCESO,'4':EstadoTicket.RESUELTO}
    if op not in m: raise ValueError('Estado inválido.')
    gestor.actualizar_estado(input('Ticket: '),m[op]); print('Estado actualizado.')
def estadisticas():
    d=gestor.estadisticas(); print('Total:',d['total']); [print(k,':',v) for grupo in ('por_criticidad','por_estado','por_tipo') for k,v in d[grupo].items()]
def menu():
    while True:
        print('''\n=== SITAC - GESTIÓN DE INCIDENCIAS ===\n1 Registrar\n2 Buscar\n3 Listar\n4 Priorizar\n5 Asignar\n6 Actualizar estado\n7 Estadísticas\n8 Cargar demo\n0 Salir''')
        op=input('Opción: ').strip()
        try:
            acciones={'1':registrar,'2':buscar,'3':listar,'4':priorizar,'5':asignar,'6':actualizar,'7':estadisticas,'8':lambda: (gestor.cargar_datos_demo(),print('Datos demo cargados.'))}
            if op=='0': print('Programa finalizado.'); break
            if op not in acciones: print('Opción inválida.'); continue
            acciones[op]()
        except (TicketError,ValueError) as e: print('[ERROR]',e)
        pausa()
if __name__=='__main__': menu()
