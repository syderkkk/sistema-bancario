class NodoPila:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class Pila:
    def __init__(self):
        self.cima = None

    def apilar(self, dato):
        nuevo = NodoPila(dato)
        nuevo.siguiente = self.cima
        self.cima = nuevo

    def desapilar(self):
        if self.cima is None:
            return None
        dato = self.cima.dato
        self.cima = self.cima.siguiente
        return dato

    def esta_vacia(self):
        return self.cima is None

    def recorrer(self):
        actual = self.cima
        elementos = []
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos