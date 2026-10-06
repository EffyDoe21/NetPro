import subprocess
import re
import ipaddress
import socket


# ============================================================
# VALIDAR DESTINO
# ============================================================

def validar_destino(destino: str) -> str:
    """
    Valida que el destino sea una dirección IPv4,
    IPv6 o un nombre de host válido.
    """

    destino = destino.strip()

    if not destino:
        raise ValueError(
            "Debes introducir una IP o dominio."
        )

    # ========================================================
    # COMPROBAR SI ES UNA DIRECCIÓN IP
    # ========================================================

    try:
        ipaddress.ip_address(destino)
        return destino

    except ValueError:
        pass

    # ========================================================
    # VALIDAR NOMBRE DE HOST
    # ========================================================

    patron = (
        r"^(?=.{1,253}$)"
        r"(?:"
        r"[A-Za-z0-9]"
        r"(?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
        r"\."
        r")*"
        r"[A-Za-z0-9]"
        r"(?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
        r"$"
    )

    if not re.fullmatch(patron, destino):
        raise ValueError(
            "El dominio o dirección IP no es válido."
        )

    return destino


# ============================================================
# EJECUTAR PING
# ============================================================

def ejecutar_ping(destino: str, paquetes: int = 4) -> dict:
    """
    Ejecuta Ping en Windows.

    Devuelve información estructurada sobre:

        destino
        IP
        paquetes enviados
        paquetes recibidos
        paquetes perdidos
        porcentaje de pérdida
        latencia mínima
        latencia máxima
        latencia promedio
        respuesta
    """

    # ========================================================
    # VALIDAR DESTINO
    # ========================================================

    destino = validar_destino(destino)

    # ========================================================
    # VALIDAR CANTIDAD DE PAQUETES
    # ========================================================

    if paquetes < 1 or paquetes > 100:
        raise ValueError(
            "La cantidad de paquetes debe estar entre 1 y 100."
        )

    # ========================================================
    # RESOLVER IP
    # ========================================================

    try:

        ip = socket.gethostbyname(destino)

    except socket.gaierror:

        raise ValueError(
            "No fue posible resolver el destino."
        )

    # ========================================================
    # COMANDO PING
    # ========================================================

    comando = [
        "ping",
        "-n",
        str(paquetes),
        destino
    ]

    # ========================================================
    # EJECUTAR
    # ========================================================

    try:

        proceso = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            shell=False,
            timeout=15,
            errors="replace"
        )

    except subprocess.TimeoutExpired:

        raise ValueError(
            "La prueba de Ping excedió "
            "el tiempo permitido."
        )

    except FileNotFoundError:

        raise ValueError(
            "No se encontró el comando PING "
            "en Windows."
        )

    # ========================================================
    # OBTENER SALIDA
    # ========================================================

    salida = proceso.stdout

    if not salida:
        salida = proceso.stderr

    # ========================================================
    # EXTRAER TIEMPOS
    # ========================================================

    # Windows puede mostrar:
    #
    # time=20ms
    # time<1ms
    # tiempo=20ms
    # tiempo<1ms

    tiempos = re.findall(
        r"(?:time|tiempo)[=<]\s*(\d+)\s*ms",
        salida,
        flags=re.IGNORECASE
    )

    tiempos = [
        int(t)
        for t in tiempos
    ]

    # ========================================================
    # PAQUETES
    # ========================================================

    enviados = paquetes

    recibidos = len(tiempos)

    perdidos = (
        enviados - recibidos
    )

    perdida_porcentaje = round(
        (perdidos / enviados) * 100,
        2
    )

    # ========================================================
    # LATENCIA
    # ========================================================

    if tiempos:

        minimo = min(tiempos)

        maximo = max(tiempos)

        promedio = round(
            sum(tiempos) / len(tiempos),
            2
        )

    else:

        minimo = None
        maximo = None
        promedio = None

    # ========================================================
    # RESULTADO
    # ========================================================

    return {
        "destino": destino,
        "ip": ip,

        "enviados": enviados,
        "recibidos": recibidos,
        "perdidos": perdidos,
        "perdida": perdida_porcentaje,

        "minimo": minimo,
        "maximo": maximo,
        "promedio": promedio,

        "respuesta": recibidos > 0
    }


# ============================================================
# PRUEBA
# ============================================================

if __name__ == "__main__":

    resultado = ejecutar_ping(
        "example.com"
    )

    for clave, valor in resultado.items():

        print(
            f"{clave}: {valor}"
        )