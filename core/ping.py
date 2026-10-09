
import subprocess
import re
import ipaddress
import socket
import os


# ============================================================
# VALIDAR DESTINO
# ============================================================

def validar_destino(destino: str) -> str:
    """
    Valida direcciones IPv4, IPv6 y nombres de host.
    """

    destino = destino.strip()

    if not destino:
        raise ValueError(
            "Debes introducir una IP o dominio."
        )

    try:
        ipaddress.ip_address(destino)
        return destino

    except ValueError:
        pass

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
# EJECUTAR PING SIN VENTANA DE CONSOLA
# ============================================================

def ejecutar_ping(destino: str, paquetes: int = 4) -> dict:
    """
    Ejecuta Ping sin abrir ventanas de CMD o PowerShell.

    Devuelve:
        destino
        ip
        enviados
        recibidos
        perdidos
        perdida
        minimo
        maximo
        promedio
        respuesta
    """

    # ========================================================
    # VALIDAR PARAMETROS
    # ========================================================

    destino = validar_destino(destino)

    if not isinstance(paquetes, int) or not 1 <= paquetes <= 100:
        raise ValueError(
            "La cantidad de paquetes debe estar entre 1 y 100."
        )

    # ========================================================
    # RESOLVER IP
    # ========================================================

    try:
        ip_obj = ipaddress.ip_address(destino)
        ip = str(ip_obj)

    except ValueError:
        try:
            direcciones = socket.getaddrinfo(
                destino,
                None,
                type=socket.SOCK_STREAM
            )
            ip = direcciones[0][4][0]

        except socket.gaierror as error:
            raise ValueError(
                "No fue posible resolver el destino."
            ) from error

    # ========================================================
    # PREPARAR COMANDO
    # ========================================================

    comando = [
        "ping",
        "-n",
        str(paquetes),
        ip
    ]

    # ========================================================
    # OCULTAR CONSOLA EN WINDOWS
    # ========================================================

    flags = 0

    if os.name == "nt":
        flags = subprocess.CREATE_NO_WINDOW

    # ========================================================
    # EJECUTAR PING
    # ========================================================

    try:
        proceso = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            shell=False,
            timeout=max(15, paquetes * 5 + 5),
            errors="replace",
            creationflags=flags
        )

    except subprocess.TimeoutExpired as error:
        raise ValueError(
            "La prueba de Ping excedió el tiempo permitido."
        ) from error

    except FileNotFoundError as error:
        raise ValueError(
            "No se encontró el comando PING en Windows."
        ) from error

    # ========================================================
    # OBTENER SALIDA
    # ========================================================

    salida = proceso.stdout or proceso.stderr or ""

    # ========================================================
    # EXTRAER TIEMPOS
    # ========================================================

    # Compatible con:
    # time=20ms
    # time<1ms
    # tiempo=20ms
    # tiempo<1ms

    coincidencias = re.findall(
        r"(?:time|tiempo)\s*[=<]\s*(\d+)\s*ms",
        salida,
        flags=re.IGNORECASE
    )

    tiempos = [
        int(valor)
        for valor in coincidencias
    ]

    # ========================================================
    # EXTRAER PAQUETES RECIBIDOS
    # ========================================================

    # El resumen de Windows es más fiable que contar
    # únicamente los tiempos de respuesta.

    coincidencia_recibidos = re.search(
        r"(?:Received|Recibidos)\s*=\s*(\d+)",
        salida,
        flags=re.IGNORECASE
    )

    if coincidencia_recibidos:
        recibidos = int(coincidencia_recibidos.group(1))
    else:
        recibidos = len(tiempos)

    enviados = paquetes
    recibidos = min(recibidos, enviados)

    perdidos = max(0, enviados - recibidos)

    perdida_porcentaje = round(
        (perdidos / enviados) * 100,
        2
    )

    # ========================================================
    # CALCULAR LATENCIAS
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

    resultado = ejecutar_ping("example.com")

    for clave, valor in resultado.items():
        print(f"{clave}: {valor}")
