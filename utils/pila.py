class NodoPila:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class Pila:
    def __init__(self, L=10):
        self.elemento = None
        self.tope = 0
        self.L = L

    def es_vacia(self): return self.tope == 0

    def es_llena(self): return self.tope == self.L

    def apilar(self, dato):
        if self.es_llena(): return None
        aux = NodoPila(dato)
        aux.siguiente = self.elemento
        self.elemento = aux
        self.tope += 1
    
    def desapilar(self):
        if self.es_vacia(): return None
        dato = self.elemento.dato
        self.elemento = self.elemento.siguiente
        self.tope -= 1
        return dato

    def recorrer(self):
        x = self.elemento
        while x:
            yield x.dato
            x = x.siguiente

# Uso: auditoria/views.py ✅ Pila de auditoría para historial de sesiones