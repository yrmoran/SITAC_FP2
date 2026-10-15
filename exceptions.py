class TicketError(Exception): pass
class ValidacionError(TicketError): pass
class TicketNoEncontradoError(TicketError): pass
class AsignacionError(TicketError): pass
