class NodoTransaccion:
    def __init__(self, transaccion):
        self.transaccion = transaccion
        self.siguiente = self.anterior = None

class HistorialTransacciones:
    def __init__(self, L=5):
        self.inicio = self.final = None
        self.L = L
        self.tamano = 0

    def agregar(self, transaccion):
        aux = NodoTransaccion(transaccion)
        if not self.inicio:
            self.inicio = self.final = aux
        else:
            self.final.siguiente = aux
            aux.anterior = self.final
            self.final = aux
        self.tamano += 1
        # Mantener el límite de historial
        while self.tamano > self.L:
            temp = self.inicio
            self.inicio = self.inicio.siguiente
            if self.inicio:
                self.inicio.anterior = None
            temp.siguiente = None
            self.tamano -= 1

    def __iter__(self):
        x = self.inicio
        while x:
            yield x.transaccion
            x = x.siguiente

    def iterar_recientes(self):
        x = self.final
        while x:
            yield x.transaccion
            x = x.anterior

# Uso: cuentas/views.py ✅ Historial de transacciones en detalle de cuenta