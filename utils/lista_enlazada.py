class NodoTransaccion:
    def __init__(self, transaccion):
        self.transaccion = transaccion
        self.siguiente = None
        self.anterior = None

class HistorialTransacciones:
    def __init__(self, limite=10):
        self.inicio = None
        self.final = None
        self.limite = limite
        self.tamano = 0

    def agregar(self, transaccion):
        nuevo = NodoTransaccion(transaccion)
        if not self.inicio:
            self.inicio = self.final = nuevo
        else:
            self.final.siguiente = nuevo
            nuevo.anterior = self.final
            self.final = nuevo
        self.tamano += 1
        # Mantener el límite de historial
        while self.tamano > self.limite:
            temp = self.inicio
            self.inicio = self.inicio.siguiente
            if self.inicio:
                self.inicio.anterior = None
            temp.siguiente = None
            self.tamano -= 1

    def __iter__(self):
        actual = self.inicio
        while actual:
            yield actual.transaccion
            actual = actual.siguiente

    def iterar_recientes(self):
        actual = self.final
        while actual:
            yield actual.transaccion
            actual = actual.anterior