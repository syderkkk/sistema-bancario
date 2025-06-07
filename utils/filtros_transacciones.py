from utils.arbol_binario import ArbolTransacciones
from datetime import datetime

def filtrar_y_ordenar_transacciones(transacciones_qs, filtros):
    """
    Aplica ordenamiento con árbol binario y luego filtra en memoria según los filtros dados.
    """
    orden = filtros.get('orden', 'fecha_desc')
    tipo = filtros.get('tipo', '')
    fecha_inicio = filtros.get('fecha_inicio', '')
    fecha_fin = filtros.get('fecha_fin', '')
    monto_min = filtros.get('monto_min', '')
    monto_max = filtros.get('monto_max', '')
    descripcion = filtros.get('descripcion', '')

    # Árbol para ordenamiento
    arbol = ArbolTransacciones()
    if orden in ['monto_asc', 'monto_desc']:
        clave_func = lambda t: t.monto
    else:
        clave_func = lambda t: t.fecha

    for t in transacciones_qs:
        arbol.insertar(t, clave_func)

    if orden in ['fecha_asc', 'monto_asc']:
        transacciones = arbol.inorden()
    else:
        transacciones = arbol.inorden_reverso()

    # Filtros en memoria
    if tipo:
        transacciones = [t for t in transacciones if t.tipo == tipo]
    if fecha_inicio:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            transacciones = [t for t in transacciones if t.fecha.date() >= fecha_inicio_dt]
        except ValueError:
            pass
    if fecha_fin:
        try:
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            transacciones = [t for t in transacciones if t.fecha.date() <= fecha_fin_dt]
        except ValueError:
            pass
    if monto_min:
        try:
            monto_min_f = float(monto_min)
            transacciones = [t for t in transacciones if float(t.monto) >= monto_min_f]
        except ValueError:
            pass
    if monto_max:
        try:
            monto_max_f = float(monto_max)
            transacciones = [t for t in transacciones if float(t.monto) <= monto_max_f]
        except ValueError:
            pass
    if descripcion:
        transacciones = [t for t in transacciones if t.descripcion and descripcion.lower() in t.descripcion.lower()]

    return transacciones