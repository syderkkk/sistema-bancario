class NodoArbol:
    def __init__(self, transaccion, clave):
        self.clave = clave
        self.transacciones = [transaccion]
        self.izquierda = None
        self.derecha = None

class ArbolTransacciones:
    def __init__(self):
        self.raiz = None

    def insertar(self, transaccion, clave_func):
        clave_nueva = clave_func(transaccion)
        def _insertar(nodo):
            if not nodo:
                return NodoArbol(transaccion, clave_nueva)
            if clave_nueva < nodo.clave:
                nodo.izquierda = _insertar(nodo.izquierda)
            elif clave_nueva > nodo.clave:
                nodo.derecha = _insertar(nodo.derecha)
            else:
                nodo.transacciones.append(transaccion)
            return nodo
        self.raiz = _insertar(self.raiz)

    def inorden(self):
        def _inorden(nodo):
            if nodo:
                yield from _inorden(nodo.izquierda)
                for t in nodo.transacciones:
                    yield t
                yield from _inorden(nodo.derecha)
        return list(_inorden(self.raiz))

    def inorden_reverso(self):
        def _inorden_rev(nodo):
            if nodo:
                yield from _inorden_rev(nodo.derecha)
                for t in nodo.transacciones:
                    yield t
                yield from _inorden_rev(nodo.izquierda)
        return list(_inorden_rev(self.raiz))