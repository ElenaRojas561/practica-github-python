# Excepciones personalizadas

class ErrorSoftwareFJ(Exception): pass
class DatoInvalidoError(ErrorSoftwareFJ): pass
class ParametroFaltanteError(ErrorSoftwareFJ): pass
class OperacionNoPermitidaError(ErrorSoftwareFJ): pass
class ServicioNoDisponibleError(ErrorSoftwareFJ): pass
class ReservaInvalidaError(ErrorSoftwareFJ): pass
class CalculoInconsistenteError(ErrorSoftwareFJ): pass
class ClienteDuplicadoError(ErrorSoftwareFJ): pass
class ClienteNoEncontradoError(ErrorSoftwareFJ): pass
