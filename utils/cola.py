class NodoCola:
    def __init__(self, solicitud):
        self.solicitud = solicitud
        self.siguiente = None

class ColaSolicitudes:
    def __init__(self):
        self.frente = None
        self.final = None

    def encolar(self, solicitud):
        nuevo = NodoCola(solicitud)
        if not self.frente:
            self.frente = self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo

    def desencolar(self):
        if not self.frente:
            return None
        solicitud = self.frente.solicitud
        self.frente = self.frente.siguiente
        if not self.frente:
            self.final = None
        return solicitud

    def esta_vacia(self):
        return self.frente is None

    def ver_frente(self):
        if self.frente:
            return self.frente.solicitud
        return None