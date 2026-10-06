import socket
import time
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed


# ============================================================
# CONFIGURACIÓN
# ============================================================

TIMEOUT_PREDETERMINADO = 1.0
MAX_TRABAJADORES = 50


# ============================================================
# SERVICIOS HABITUALES
# ============================================================

SERVICIOS_COMUNES = {
    20: ("FTP-DATA", "Transferencia de datos mediante FTP."),
    21: ("FTP", "Control de transferencia de archivos."),
    22: ("SSH", "Administración remota segura."),
    23: ("TELNET", "Administración remota sin cifrado."),
    25: ("SMTP", "Envío de correo electrónico."),
    53: ("DNS", "Resolución de nombres de dominio."),
    67: ("DHCP", "Asignación de configuración IP a clientes."),
    68: ("DHCP", "Recepción de configuración IP por clientes."),
    69: ("TFTP", "Transferencia simple de archivos."),
    80: ("HTTP", "Servicio web sin cifrado TLS."),
    110: ("POP3", "Recepción de correo electrónico."),
    123: ("NTP", "Sincronización de hora en red."),
    135: ("RPC", "Llamadas a procedimientos remotos."),
    137: ("NetBIOS-NS", "Resolución de nombres NetBIOS."),
    138: ("NetBIOS-DGM", "Datagramas NetBIOS."),
    139: ("NetBIOS-SSN", "Sesiones NetBIOS."),
    143: ("IMAP", "Acceso y administración de correo."),
    161: ("SNMP", "Administración y monitoreo de dispositivos."),
    162: ("SNMPTRAP", "Recepción de notificaciones SNMP."),
    389: ("LDAP", "Servicios de directorio."),
    443: ("HTTPS", "Servicio web habitualmente protegido con TLS."),
    445: ("SMB", "Compartición de archivos y recursos."),
    465: ("SMTPS", "SMTP habitualmente protegido mediante TLS."),
    514: ("SYSLOG", "Registro y envío de eventos del sistema."),
    587: ("SMTP Submission", "Envío autenticado de correo."),
    636: ("LDAPS", "LDAP habitualmente protegido mediante TLS."),
    993: ("IMAPS", "IMAP habitualmente protegido mediante TLS."),
    995: ("POP3S", "POP3 habitualmente protegido mediante TLS."),
    1433: ("MSSQL", "Servicio habitual de Microsoft SQL Server."),
    1521: ("Oracle", "Servicio habitual de Oracle Database."),
    2049: ("NFS", "Sistema de archivos de red."),
    3306: ("MySQL", "Servicio habitual de bases de datos MySQL."),
    3389: ("RDP", "Escritorio remoto de Microsoft."),
    5432: ("PostgreSQL", "Servicio habitual de PostgreSQL."),
    5900: ("VNC", "Control remoto mediante VNC."),
    6379: ("Redis", "Servicio habitual de Redis."),
    8000: ("HTTP alternativo", "Puerto usado habitualmente por servicios web."),
    8080: ("HTTP alternativo", "Puerto alternativo habitual para HTTP."),
    8443: ("HTTPS alternativo", "Puerto alternativo habitual para HTTPS."),
    9200: ("Elasticsearch", "Servicio habitual de Elasticsearch.")
}


# Puertos que mostraremos como conjunto de prueba rápida.
PUERTOS_COMUNES = [
    21,
    22,
    23,
    25,
    53,
    80,
    110,
    135,
    139,
    143,
    389,
    443,
    445,
    587,
    636,
    993,
    995,
    1433,
    3306,
    3389,
    5432,
    5900,
    6379,
    8080,
    8443
]


# ============================================================
# RESULTADO
# ============================================================

@dataclass
class ResultadoPuerto:
    """
    Representa el resultado técnico de una comprobación.

    Esta clase será la que reciba posteriormente
    AI/ollama_client.py.
    """

    host: str
    ip: str
    puerto: int
    protocolo: str
    estado: str
    servicio: str
    descripcion: str
    tiempo_ms: float | None = None
    codigo: int | None = None
    error: str | None = None


# ============================================================
# VALIDACIONES
# ============================================================

def validar_puerto(puerto):
    """
    Valida y convierte un puerto a entero.
    """

    try:
        puerto = int(puerto)

    except (TypeError, ValueError):
        raise ValueError(
            "El puerto debe ser un número entero."
        )

    if not 1 <= puerto <= 65535:
        raise ValueError(
            "El puerto debe estar entre 1 y 65535."
        )

    return puerto


def validar_rango(inicio, fin):
    """
    Valida un rango de puertos.
    """

    inicio = validar_puerto(inicio)
    fin = validar_puerto(fin)

    if inicio > fin:
        raise ValueError(
            "El puerto inicial no puede ser mayor "
            "que el puerto final."
        )

    return inicio, fin


# ============================================================
# INFORMACIÓN DEL SERVICIO
# ============================================================

def obtener_info_servicio(puerto):
    """
    Obtiene la asociación habitual conocida para un puerto.

    IMPORTANTE:
    Esto NO identifica realmente el servicio remoto.
    Solo devuelve una asociación educativa.
    """

    puerto = validar_puerto(puerto)

    if puerto in SERVICIOS_COMUNES:
        return SERVICIOS_COMUNES[puerto]

    # Intentamos consultar la base de servicios del SO.
    try:

        nombre = socket.getservbyport(
            puerto,
            "tcp"
        )

        return (
            nombre.upper(),
            (
                "Servicio habitualmente asociado según "
                "la base local de servicios del sistema."
            )
        )

    except OSError:

        return (
            "Desconocido",
            (
                "NetPro no dispone de una asociación "
                "habitual conocida para este puerto."
            )
        )


# ============================================================
# RESOLUCIÓN DEL OBJETIVO
# ============================================================

def resolver_host(host):
    """
    Resuelve un nombre de host o una IPv4.

    Devuelve la dirección IPv4 que será utilizada para
    realizar la comprobación TCP.
    """

    if not isinstance(host, str):
        raise ValueError(
            "El objetivo debe ser texto."
        )

    host = host.strip()

    if not host:
        raise ValueError(
            "Debes introducir un host o una dirección IP."
        )

    try:

        ip = socket.gethostbyname(host)

    except socket.gaierror as error:

        raise ValueError(
            f"No fue posible resolver el objetivo '{host}'."
        ) from error

    return ip


# ============================================================
# COMPROBACIÓN DE UN PUERTO TCP
# ============================================================

def comprobar_puerto(
    host,
    puerto,
    timeout=TIMEOUT_PREDETERMINADO,
    ip_resuelta=None
):
    """
    Comprueba si un puerto TCP acepta una conexión.

    NetPro utiliza connect_ex(), por lo que esta función
    realiza una comprobación TCP real.

    No identifica vulnerabilidades.
    No identifica versiones.
    No realiza explotación.
    """

    puerto = validar_puerto(
        puerto
    )

    if ip_resuelta is None:
        ip = resolver_host(host)
    else:
        ip = ip_resuelta

    servicio, descripcion = obtener_info_servicio(
        puerto
    )

    inicio = time.perf_counter()

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(
        timeout
    )

    codigo = None
    error_texto = None

    try:

        codigo = sock.connect_ex(
            (
                ip,
                puerto
            )
        )

        tiempo_ms = (
            time.perf_counter() - inicio
        ) * 1000

        # ----------------------------------------------------
        # connect_ex() == 0
        # ----------------------------------------------------

        if codigo == 0:

            estado = "ABIERTO"

        # ----------------------------------------------------
        # Connection refused
        #
        # Windows: 10061
        # Linux/macOS normalmente: 111 / 61
        # ----------------------------------------------------

        elif codigo in {
            61,
            111,
            10061
        }:

            estado = "CERRADO"

        # ----------------------------------------------------
        # Timeouts / sin respuesta
        # ----------------------------------------------------

        elif codigo in {
            60,
            110,
            10060
        }:

            estado = "SIN RESPUESTA"

        else:

            estado = "SIN RESPUESTA"

            error_texto = (
                f"connect_ex devolvió el código "
                f"{codigo}."
            )

    except socket.timeout:

        tiempo_ms = (
            time.perf_counter() - inicio
        ) * 1000

        estado = "SIN RESPUESTA"

        error_texto = (
            "Se agotó el tiempo de espera."
        )

    except OSError as error:

        tiempo_ms = (
            time.perf_counter() - inicio
        ) * 1000

        estado = "ERROR"

        error_texto = str(
            error
        )

    finally:

        sock.close()

    return ResultadoPuerto(
        host=host,
        ip=ip,
        puerto=puerto,
        protocolo="TCP",
        estado=estado,
        servicio=servicio,
        descripcion=descripcion,
        tiempo_ms=round(
            tiempo_ms,
            2
        ),
        codigo=codigo,
        error=error_texto
    )


# ============================================================
# COMPROBAR PUERTOS COMUNES
# ============================================================

def comprobar_puertos_comunes(
    host,
    timeout=TIMEOUT_PREDETERMINADO,
    max_trabajadores=MAX_TRABAJADORES
):
    """
    Comprueba el conjunto de puertos comunes de NetPro.
    """

    return comprobar_varios_puertos(
        host=host,
        puertos=PUERTOS_COMUNES,
        timeout=timeout,
        max_trabajadores=max_trabajadores
    )


# ============================================================
# COMPROBAR UN RANGO
# ============================================================

def comprobar_rango(
    host,
    inicio,
    fin,
    timeout=TIMEOUT_PREDETERMINADO,
    max_trabajadores=MAX_TRABAJADORES
):
    """
    Comprueba un rango de puertos TCP.
    """

    inicio, fin = validar_rango(
        inicio,
        fin
    )

    puertos = list(
        range(
            inicio,
            fin + 1
        )
    )

    return comprobar_varios_puertos(
        host=host,
        puertos=puertos,
        timeout=timeout,
        max_trabajadores=max_trabajadores
    )


# ============================================================
# COMPROBAR VARIOS PUERTOS
# ============================================================

def comprobar_varios_puertos(
    host,
    puertos,
    timeout=TIMEOUT_PREDETERMINADO,
    max_trabajadores=MAX_TRABAJADORES
):
    """
    Comprueba varios puertos utilizando hilos.

    Esto evita comprobar los puertos uno por uno y mejora
    considerablemente la velocidad.
    """

    if not puertos:
        return []

    # --------------------------------------------------------
    # Resolver host una sola vez
    # --------------------------------------------------------

    ip = resolver_host(
        host
    )

    # --------------------------------------------------------
    # Validar y eliminar duplicados
    # --------------------------------------------------------

    puertos_limpios = []

    vistos = set()

    for puerto in puertos:

        puerto = validar_puerto(
            puerto
        )

        if puerto not in vistos:

            vistos.add(
                puerto
            )

            puertos_limpios.append(
                puerto
            )

    # --------------------------------------------------------
    # Evitar crear más trabajadores de los necesarios
    # --------------------------------------------------------

    trabajadores = min(
        max_trabajadores,
        len(puertos_limpios)
    )

    trabajadores = max(
        1,
        trabajadores
    )

    resultados = []

    # --------------------------------------------------------
    # Ejecución concurrente
    # --------------------------------------------------------

    with ThreadPoolExecutor(
        max_workers=trabajadores
    ) as executor:

        futuros = {

            executor.submit(
                comprobar_puerto,
                host,
                puerto,
                timeout,
                ip
            ): puerto

            for puerto in puertos_limpios
        }

        for futuro in as_completed(
            futuros
        ):

            puerto = futuros[
                futuro
            ]

            try:

                resultado = futuro.result()

            except Exception as error:

                servicio, descripcion = (
                    obtener_info_servicio(
                        puerto
                    )
                )

                resultado = ResultadoPuerto(
                    host=host,
                    ip=ip,
                    puerto=puerto,
                    protocolo="TCP",
                    estado="ERROR",
                    servicio=servicio,
                    descripcion=descripcion,
                    tiempo_ms=None,
                    codigo=None,
                    error=str(error)
                )

            resultados.append(
                resultado
            )

    # --------------------------------------------------------
    # Ordenar por número de puerto
    # --------------------------------------------------------

    resultados.sort(
        key=lambda resultado: resultado.puerto
    )

    return resultados


# ============================================================
# RESUMEN
# ============================================================

def resumir_resultados(resultados):
    """
    Genera estadísticas simples del análisis.

    Estas estadísticas son calculadas por Python,
    no por la IA.
    """

    resumen = {
        "total": len(resultados),
        "abiertos": 0,
        "cerrados": 0,
        "sin_respuesta": 0,
        "errores": 0
    }

    for resultado in resultados:

        estado = resultado.estado.upper()

        if estado == "ABIERTO":

            resumen["abiertos"] += 1

        elif estado == "CERRADO":

            resumen["cerrados"] += 1

        elif estado == "SIN RESPUESTA":

            resumen["sin_respuesta"] += 1

        elif estado == "ERROR":

            resumen["errores"] += 1

    return resumen


# ============================================================
# FILTRAR PUERTOS ABIERTOS
# ============================================================

def obtener_abiertos(resultados):
    """
    Devuelve únicamente los resultados cuyo estado
    sea ABIERTO.
    """

    return [
        resultado
        for resultado in resultados
        if resultado.estado.upper() == "ABIERTO"
    ]


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("NETPRO - PRUEBA DEL MÓDULO DE PUERTOS")
    print("=" * 60)
    print()

    objetivo = "localhost"

    print(
        f"Objetivo: {objetivo}"
    )

    print()

    try:

        # ----------------------------------------------------
        # Prueba individual
        # ----------------------------------------------------

        resultado = comprobar_puerto(
            objetivo,
            443
        )

        print(
            "PRUEBA INDIVIDUAL"
        )

        print(
            "-" * 60
        )

        print(
            f"Host: {resultado.host}"
        )

        print(
            f"IP: {resultado.ip}"
        )

        print(
            f"Puerto: "
            f"{resultado.puerto}/"
            f"{resultado.protocolo}"
        )

        print(
            f"Estado: {resultado.estado}"
        )

        print(
            f"Servicio habitual: "
            f"{resultado.servicio}"
        )

        print(
            f"Tiempo: "
            f"{resultado.tiempo_ms} ms"
        )

        if resultado.error:

            print(
                f"Detalle: {resultado.error}"
            )

        print()

        # ----------------------------------------------------
        # Prueba de puertos comunes
        # ----------------------------------------------------

        print(
            "PUERTOS COMUNES"
        )

        print(
            "-" * 60
        )

        resultados = comprobar_puertos_comunes(
            objetivo
        )

        for resultado in resultados:

            print(
                f"{resultado.puerto:5}/TCP | "
                f"{resultado.estado:14} | "
                f"{resultado.servicio}"
            )

        print()

        # ----------------------------------------------------
        # Resumen
        # ----------------------------------------------------

        resumen = resumir_resultados(
            resultados
        )

        print(
            "RESUMEN"
        )

        print(
            "-" * 60
        )

        print(
            f"Total: "
            f"{resumen['total']}"
        )

        print(
            f"Abiertos: "
            f"{resumen['abiertos']}"
        )

        print(
            f"Cerrados: "
            f"{resumen['cerrados']}"
        )

        print(
            f"Sin respuesta: "
            f"{resumen['sin_respuesta']}"
        )

        print(
            f"Errores: "
            f"{resumen['errores']}"
        )

    except Exception as error:

        print(
            f"❌ Error: {error}"
        )