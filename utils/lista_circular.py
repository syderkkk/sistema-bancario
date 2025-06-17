class NodoCircular:
    def __init__(self, imagen):
        self.imagen = imagen
        self.siguiente = self.anterior = None

class ListaCircular:
    def __init__(self):
        self.inicio = None

    def agregar(self, imagen):
        aux = NodoCircular(imagen)
        if not self.inicio:
            self.inicio = aux
            aux.siguiente = aux
            aux.anterior = aux
        else:
            fin = self.inicio.anterior
            fin.siguiente = aux
            aux.anterior = fin
            aux.siguiente = self.inicio
            self.inicio.anterior = aux

    def buscar(self, posicion):
        x = self.inicio
        for i in range(posicion):
            x = x.siguiente
        return x

    def __iter__(self):
        if not self.inicio:
            return
        x = self.inicio
        while True:
            yield x.imagen
            x = x.siguiente
            if x == self.inicio:
                break

    def longitud(self):
        if not self.inicio:
            return 0
        x = self.inicio
        count = 1
        while x.siguiente != self.inicio:
            count += 1
            x = x.siguiente
        return count
    
# Uso: usuarios/views.py ✅ Carrusel de imágenes en la landing page