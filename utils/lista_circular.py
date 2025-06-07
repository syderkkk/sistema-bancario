class NodoCircular:
    def __init__(self, imagen):
        self.imagen = imagen
        self.siguiente = None
        self.anterior = None

class ListaCircular:
    def __init__(self):
        self.inicio = None

    def agregar(self, imagen):
        nuevo = NodoCircular(imagen)
        if not self.inicio:
            self.inicio = nuevo
            nuevo.siguiente = nuevo
            nuevo.anterior = nuevo
        else:
            fin = self.inicio.anterior
            fin.siguiente = nuevo
            nuevo.anterior = fin
            nuevo.siguiente = self.inicio
            self.inicio.anterior = nuevo

    def buscar(self, posicion):
        actual = self.inicio
        for i in range(posicion):
            actual = actual.siguiente
        return actual

    def __iter__(self):
        if not self.inicio:
            return
        actual = self.inicio
        while True:
            yield actual.imagen
            actual = actual.siguiente
            if actual == self.inicio:
                break

    def longitud(self):
        if not self.inicio:
            return 0
        actual = self.inicio
        count = 1
        while actual.siguiente != self.inicio:
            count += 1
            actual = actual.siguiente
        return count