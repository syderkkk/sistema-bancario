class NodoArbol:
    def __init__(self, transaccion):
        self.transaccion = transaccion
        self.izquierda = self.derecha = None

class ArbolTransacciones:
    def __init__(self, clave):
        self.raiz = None
        self.clave = clave

    def insertar(self, transaccion):
        if self.raiz == None: self.raiz = NodoArbol(transaccion)
        else: self._insertarR(self.raiz, transaccion)

    def _insertarR(self, raiz_actual, transaccion):
        if self.clave(transaccion) < self.clave(raiz_actual.transaccion):
            if raiz_actual.izquierda == None: raiz_actual.izquierda = NodoArbol(transaccion)
            else: self._insertarR(raiz_actual.izquierda, transaccion)
        else:
            if raiz_actual.derecha == None: raiz_actual.derecha = NodoArbol(transaccion)
            else: self._insertarR(raiz_actual.derecha, transaccion)

    def inOrden(self):
        return self._inOrdenR(self.raiz)

    def _inOrdenR(self, raiz_actual):
        if raiz_actual == None:
            return []
        return self._inOrdenR(raiz_actual.izquierda) + [raiz_actual.transaccion] + self._inOrdenR(raiz_actual.derecha)
    
    def inorden_reverso(self):
        return self._inorden_reversoR(self.raiz)
    
    def _inorden_reversoR(self, raiz_actual):
        if raiz_actual == None:
            return []
        return self._inorden_reversoR(raiz_actual.derecha) + [raiz_actual.transaccion] + self._inorden_reversoR(raiz_actual.izquierda)

# Uso: filtros_transacciones.py ✅