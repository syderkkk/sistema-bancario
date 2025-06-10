from utils.arbol_binario import ArbolTransacciones
from datetime import datetime

def filtrar_y_ordenar_transacciones(transacciones_qs, filtros):

    def filtrar_fecha(transacciones, valor, op):
        try:
            fecha_dt = datetime.strptime(valor, "%Y-%m-%d").date()
            if op == "gte":
                return [t for t in transacciones if t.fecha.date() >= fecha_dt]
            elif op == "lte":
                return [t for t in transacciones if t.fecha.date() <= fecha_dt]
        except (ValueError, TypeError):
            return transacciones
        return transacciones

    def filtrar_monto(transacciones, valor, op):
        try:
            monto_f = float(valor)
            if op == "gte":
                return [t for t in transacciones if float(t.monto) >= monto_f]
            elif op == "lte":
                return [t for t in transacciones if float(t.monto) <= monto_f]
        except (ValueError, TypeError):
            return transacciones
        return transacciones

    orden = filtros.get('orden', 'fecha_desc')
    tipo = filtros.get('tipo', '')
    fecha_inicio = filtros.get('fecha_inicio', '')
    fecha_fin = filtros.get('fecha_fin', '')
    monto_min = filtros.get('monto_min', '')
    monto_max = filtros.get('monto_max', '')
    descripcion = filtros.get('descripcion', '')

    clave_func = (lambda t: float(t.monto)) if 'monto' in orden else (lambda t: t.fecha)
    
    ascendente = orden.endswith('_asc')

    arbol = ArbolTransacciones(clave_func)
    for t in transacciones_qs:
        arbol.insertar(t)

    transacciones = arbol.inOrden() if ascendente else arbol.inorden_reverso()

    # Filtros en memoria
    if tipo:
        transacciones = [t for t in transacciones if t.tipo == tipo]
    if fecha_inicio:
        transacciones = filtrar_fecha(transacciones, fecha_inicio, "gte")
    if fecha_fin:
        transacciones = filtrar_fecha(transacciones, fecha_fin, "lte")
    if monto_min:
        transacciones = filtrar_monto(transacciones, monto_min, "gte")
    if monto_max:
        transacciones = filtrar_monto(transacciones, monto_max, "lte")
    if descripcion:
        transacciones = [t for t in transacciones if t.descripcion and descripcion.lower() in t.descripcion.lower()]

    return transacciones