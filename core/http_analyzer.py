import http.client
import ssl
import socket
import time

from dataclasses import dataclass, field
from urllib.parse import urlparse, urljoin
from datetime import datetime, timezone


# ============================================================
# CONFIGURACIÓN
# ============================================================

TIMEOUT = 6
MAX_REDIRECCIONES = 5

USER_AGENT = "NetPro/1.0 - Network & Security Toolkit"


# ============================================================
# HEADERS DE SEGURIDAD QUE NETPRO REVISARÁ
# ============================================================

HEADERS_SEGURIDAD = {
    "strict-transport-security": {
        "nombre": "HSTS",
        "descripcion": (
            "Indica al navegador que debe utilizar HTTPS "
            "para comunicarse con el sitio."
        )
    },

    "content-security-policy": {
        "nombre": "CSP",
        "descripcion": (
            "Define restricciones sobre los recursos que "
            "puede cargar el navegador."
        )
    },

    "x-content-type-options": {
        "nombre": "X-Content-Type-Options",
        "descripcion": (
            "Ayuda a evitar interpretaciones incorrectas "
            "del tipo de contenido."
        )
    },

    "x-frame-options": {
        "nombre": "X-Frame-Options",
        "descripcion": (
            "Controla si el contenido puede mostrarse "
            "dentro de determinados frames."
        )
    },

    "referrer-policy": {
        "nombre": "Referrer-Policy",
        "descripcion": (
            "Controla qué información de referencia "
            "envía el navegador."
        )
    },

    "permissions-policy": {
        "nombre": "Permissions-Policy",
        "descripcion": (
            "Controla el acceso del sitio a determinadas "
            "funciones del navegador."
        )
    }
}


# ============================================================
# CLASE RESULTADO
# ============================================================

@dataclass
class ResultadoHTTP:

    url_solicitada: str
    url_final: str

    host: str
    ip: str

    protocolo: str

    codigo_estado: int | None
    razon_estado: str

    tiempo_ms: float | None

    servidor: str = "No informado"
    content_type: str = "No informado"

    redirecciones: list = field(
        default_factory=list
    )

    headers: dict = field(
        default_factory=dict
    )

    headers_seguridad: dict = field(
        default_factory=dict
    )

    usa_https: bool = False

    certificado_disponible: bool = False
    certificado_valido: bool | None = None

    certificado_sujeto: str = "No disponible"
    certificado_emisor: str = "No disponible"

    certificado_desde: str = "No disponible"
    certificado_hasta: str = "No disponible"

    dias_restantes_certificado: int | None = None

    error: str | None = None


# ============================================================
# NORMALIZAR URL
# ============================================================

def normalizar_url(url):
    """
    Valida y normaliza la URL.

    Si el usuario escribe:
        example.com

    NetPro utilizará:
        https://example.com
    """

    if not isinstance(url, str):
        raise ValueError(
            "La URL debe ser texto."
        )

    url = url.strip()

    if not url:
        raise ValueError(
            "Debes introducir una URL."
        )

    if not url.lower().startswith(
        ("http://", "https://")
    ):
        url = "https://" + url

    parsed = urlparse(url)

    if parsed.scheme not in (
        "http",
        "https"
    ):
        raise ValueError(
            "Solo se permiten direcciones HTTP o HTTPS."
        )

    if not parsed.hostname:
        raise ValueError(
            "No se encontró un host válido."
        )

    return url


# ============================================================
# RESOLVER IP
# ============================================================

def resolver_ip(host):
    """
    Obtiene una dirección IP asociada al host.
    """

    try:

        return socket.gethostbyname(
            host
        )

    except socket.gaierror:

        return "No disponible"


# ============================================================
# CONVERTIR DATOS DEL CERTIFICADO
# ============================================================

def formatear_nombre_certificado(datos):
    """
    Convierte subject/issuer del certificado
    a una cadena legible.
    """

    elementos = []

    for grupo in datos:

        for clave, valor in grupo:

            elementos.append(
                f"{clave}={valor}"
            )

    if not elementos:
        return "No disponible"

    return ", ".join(elementos)


# ============================================================
# FECHA DEL CERTIFICADO
# ============================================================

def convertir_fecha_certificado(fecha):
    """
    Convierte la fecha TLS proporcionada por Python
    a datetime.
    """

    if not fecha:
        return None

    try:

        timestamp = (
            ssl.cert_time_to_seconds(
                fecha
            )
        )

        return datetime.fromtimestamp(
            timestamp,
            tz=timezone.utc
        )

    except Exception:

        return None


# ============================================================
# CERTIFICADO TLS
# ============================================================

def obtener_certificado_tls(
    host,
    puerto=443,
    timeout=TIMEOUT
):
    """
    Obtiene información básica del certificado TLS.

    El certificado se valida utilizando el almacén
    de certificados de confianza disponible para Python.
    """

    resultado = {

        "disponible": False,

        "valido": None,

        "sujeto": "No disponible",

        "emisor": "No disponible",

        "desde": "No disponible",

        "hasta": "No disponible",

        "dias_restantes": None
    }

    contexto = (
        ssl.create_default_context()
    )

    try:

        with socket.create_connection(
            (host, puerto),
            timeout=timeout
        ) as conexion_tcp:

            with contexto.wrap_socket(
                conexion_tcp,
                server_hostname=host
            ) as conexion_tls:

                certificado = (
                    conexion_tls.getpeercert()
                )

                resultado[
                    "disponible"
                ] = True

                resultado[
                    "valido"
                ] = True

                # --------------------------------------------
                # SUJETO
                # --------------------------------------------

                resultado[
                    "sujeto"
                ] = formatear_nombre_certificado(
                    certificado.get(
                        "subject",
                        ()
                    )
                )

                # --------------------------------------------
                # EMISOR
                # --------------------------------------------

                resultado[
                    "emisor"
                ] = formatear_nombre_certificado(
                    certificado.get(
                        "issuer",
                        ()
                    )
                )

                # --------------------------------------------
                # FECHAS
                # --------------------------------------------

                fecha_inicio = certificado.get(
                    "notBefore"
                )

                fecha_fin = certificado.get(
                    "notAfter"
                )

                if fecha_inicio:

                    resultado[
                        "desde"
                    ] = fecha_inicio

                if fecha_fin:

                    resultado[
                        "hasta"
                    ] = fecha_fin

                    expiracion = (
                        convertir_fecha_certificado(
                            fecha_fin
                        )
                    )

                    if expiracion:

                        ahora = datetime.now(
                            timezone.utc
                        )

                        diferencia = (
                            expiracion - ahora
                        )

                        resultado[
                            "dias_restantes"
                        ] = diferencia.days

    except ssl.SSLCertVerificationError:

        resultado[
            "disponible"
        ] = True

        resultado[
            "valido"
        ] = False

    except (
        socket.timeout,
        socket.gaierror,
        ConnectionError,
        OSError
    ):

        pass

    return resultado


# ============================================================
# ANALIZAR HEADERS DE SEGURIDAD
# ============================================================

def analizar_headers_seguridad(headers):
    """
    Comprueba si determinados encabezados fueron
    observados en la respuesta HTTP.

    IMPORTANTE:

    La ausencia de un header NO significa
    automáticamente que exista una vulnerabilidad.
    """

    headers_lower = {

        clave.lower(): valor

        for clave, valor
        in headers.items()
    }

    resultado = {}

    for header, informacion in (
        HEADERS_SEGURIDAD.items()
    ):

        presente = (
            header in headers_lower
        )

        resultado[
            informacion["nombre"]
        ] = {

            "presente": presente,

            "valor": headers_lower.get(
                header
            ),

            "descripcion": informacion[
                "descripcion"
            ]
        }

    return resultado


# ============================================================
# PETICIÓN HTTP
# ============================================================

def realizar_peticion(
    url,
    timeout=TIMEOUT
):
    """
    Realiza una petición HTTP GET.

    No utiliza IA.

    Esta función obtiene los datos técnicos reales
    proporcionados por el servidor.
    """

    parsed = urlparse(url)

    host = parsed.hostname

    if not host:

        raise ValueError(
            "No fue posible determinar el host."
        )

    protocolo = (
        parsed.scheme.lower()
    )

    # ========================================================
    # HTTPS
    # ========================================================

    if protocolo == "https":

        puerto = (
            parsed.port or 443
        )

        contexto = (
            ssl.create_default_context()
        )

        conexion = (
            http.client.HTTPSConnection(
                host,
                port=puerto,
                timeout=timeout,
                context=contexto
            )
        )

    # ========================================================
    # HTTP
    # ========================================================

    else:

        puerto = (
            parsed.port or 80
        )

        conexion = (
            http.client.HTTPConnection(
                host,
                port=puerto,
                timeout=timeout
            )
        )

    # ========================================================
    # RUTA
    # ========================================================

    ruta = (
        parsed.path or "/"
    )

    if parsed.query:

        ruta += (
            "?" + parsed.query
        )

    headers_peticion = {

        "User-Agent": USER_AGENT,

        "Accept": "*/*",

        "Connection": "close"
    }

    # ========================================================
    # MEDIR TIEMPO
    # ========================================================

    inicio = (
        time.perf_counter()
    )

    try:

        conexion.request(
            "GET",
            ruta,
            headers=headers_peticion
        )

        respuesta = (
            conexion.getresponse()
        )

        tiempo_ms = (
            time.perf_counter()
            - inicio
        ) * 1000

        headers = dict(
            respuesta.getheaders()
        )

        # Solo leemos una pequeña parte.
        # NetPro no necesita descargar el sitio completo.

        respuesta.read(
            1024
        )

        return {

            "codigo":
                respuesta.status,

            "razon":
                respuesta.reason or "",

            "headers":
                headers,

            "tiempo_ms":
                round(
                    tiempo_ms,
                    2
                )
        }

    finally:

        conexion.close()


# ============================================================
# ANALIZAR HTTP / HTTPS
# ============================================================

def analizar_http(
    url,
    timeout=TIMEOUT,
    max_redirecciones=MAX_REDIRECCIONES
):
    """
    Función principal del módulo HTTP/HTTPS.

    NetPro realiza el análisis mediante Python.

    La inteligencia artificial NO determina estos
    resultados. Posteriormente podrá interpretarlos.
    """

    url_original = (
        normalizar_url(
            url
        )
    )

    url_actual = (
        url_original
    )

    redirecciones = []

    ultimo_resultado = None

    # ========================================================
    # SEGUIR REDIRECCIONES
    # ========================================================

    for _ in range(
        max_redirecciones + 1
    ):

        ultimo_resultado = (
            realizar_peticion(
                url_actual,
                timeout
            )
        )

        codigo = (
            ultimo_resultado[
                "codigo"
            ]
        )

        headers = (
            ultimo_resultado[
                "headers"
            ]
        )

        # Si no es una redirección terminamos.

        if codigo not in (
            301,
            302,
            303,
            307,
            308
        ):

            break

        # Buscar Location sin depender
        # de mayúsculas/minúsculas.

        location = None

        for clave, valor in (
            headers.items()
        ):

            if (
                clave.lower()
                == "location"
            ):

                location = valor
                break

        if not location:

            break

        nueva_url = urljoin(
            url_actual,
            location
        )

        redirecciones.append({

            "desde":
                url_actual,

            "hacia":
                nueva_url,

            "codigo":
                codigo
        })

        url_actual = nueva_url

    # ========================================================
    # VALIDACIÓN
    # ========================================================

    if ultimo_resultado is None:

        raise RuntimeError(
            "No se obtuvo una respuesta HTTP."
        )

    # ========================================================
    # URL FINAL
    # ========================================================

    parsed_final = (
        urlparse(
            url_actual
        )
    )

    host = (
        parsed_final.hostname
    )

    ip = resolver_ip(
        host
    )

    protocolo = (
        parsed_final.scheme.upper()
    )

    usa_https = (
        parsed_final.scheme.lower()
        == "https"
    )

    headers = (
        ultimo_resultado[
            "headers"
        ]
    )

    # ========================================================
    # SERVIDOR Y CONTENT TYPE
    # ========================================================

    servidor = (
        "No informado"
    )

    content_type = (
        "No informado"
    )

    for clave, valor in (
        headers.items()
    ):

        clave_lower = (
            clave.lower()
        )

        if clave_lower == "server":

            servidor = valor

        elif (
            clave_lower
            == "content-type"
        ):

            content_type = valor

    # ========================================================
    # HEADERS DE SEGURIDAD
    # ========================================================

    headers_seguridad = (
        analizar_headers_seguridad(
            headers
        )
    )

    # ========================================================
    # CERTIFICADO TLS
    # ========================================================

    certificado = {

        "disponible": False,

        "valido": None,

        "sujeto":
            "No disponible",

        "emisor":
            "No disponible",

        "desde":
            "No disponible",

        "hasta":
            "No disponible",

        "dias_restantes":
            None
    }

    if usa_https:

        puerto_tls = (
            parsed_final.port
            or 443
        )

        certificado = (
            obtener_certificado_tls(
                host,
                puerto_tls,
                timeout
            )
        )

    # ========================================================
    # CREAR RESULTADO
    # ========================================================

    return ResultadoHTTP(

        url_solicitada=
            url_original,

        url_final=
            url_actual,

        host=
            host,

        ip=
            ip,

        protocolo=
            protocolo,

        codigo_estado=
            ultimo_resultado[
                "codigo"
            ],

        razon_estado=
            ultimo_resultado[
                "razon"
            ],

        tiempo_ms=
            ultimo_resultado[
                "tiempo_ms"
            ],

        servidor=
            servidor,

        content_type=
            content_type,

        redirecciones=
            redirecciones,

        headers=
            headers,

        headers_seguridad=
            headers_seguridad,

        usa_https=
            usa_https,

        certificado_disponible=
            certificado[
                "disponible"
            ],

        certificado_valido=
            certificado[
                "valido"
            ],

        certificado_sujeto=
            certificado[
                "sujeto"
            ],

        certificado_emisor=
            certificado[
                "emisor"
            ],

        certificado_desde=
            certificado[
                "desde"
            ],

        certificado_hasta=
            certificado[
                "hasta"
            ],

        dias_restantes_certificado=
            certificado[
                "dias_restantes"
            ]
    )


# ============================================================
# RESUMEN DE HEADERS DE SEGURIDAD
# ============================================================

def resumir_headers_seguridad(
    resultado
):

    total = len(
        resultado.headers_seguridad
    )

    presentes = sum(

        1

        for datos in (
            resultado
            .headers_seguridad
            .values()
        )

        if datos[
            "presente"
        ]
    )

    return {

        "total":
            total,

        "presentes":
            presentes,

        "no_observados":
            total - presentes
    }


# ============================================================
# DESCRIPCIÓN DEL CÓDIGO HTTP
# ============================================================

def descripcion_codigo_http(
    codigo
):

    if codigo is None:

        return (
            "No se obtuvo código HTTP."
        )

    if 100 <= codigo <= 199:

        return (
            "Respuesta informativa."
        )

    if 200 <= codigo <= 299:

        return (
            "La respuesta pertenece a la familia "
            "de solicitudes procesadas correctamente."
        )

    if 300 <= codigo <= 399:

        return (
            "La respuesta pertenece a la familia "
            "de redirecciones."
        )

    if 400 <= codigo <= 499:

        return (
            "La respuesta pertenece a la familia "
            "de errores relacionados con la solicitud."
        )

    if 500 <= codigo <= 599:

        return (
            "La respuesta pertenece a la familia "
            "de errores del servidor."
        )

    return (
        "Código HTTP no clasificado."
    )


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 65)

    print(
        "NETPRO - ANALIZADOR HTTP / HTTPS"
    )

    print("=" * 65)

    objetivo = (
        "https://example.com"
    )

    print()

    print(
        f"Analizando: {objetivo}"
    )

    print()

    try:

        resultado = (
            analizar_http(
                objetivo
            )
        )

        print(
            f"URL solicitada: "
            f"{resultado.url_solicitada}"
        )

        print(
            f"URL final: "
            f"{resultado.url_final}"
        )

        print(
            f"Host: "
            f"{resultado.host}"
        )

        print(
            f"IP: "
            f"{resultado.ip}"
        )

        print(
            f"Protocolo: "
            f"{resultado.protocolo}"
        )

        print(
            f"Estado HTTP: "
            f"{resultado.codigo_estado} "
            f"{resultado.razon_estado}"
        )

        print(
            f"Tiempo: "
            f"{resultado.tiempo_ms} ms"
        )

        print(
            f"Servidor informado: "
            f"{resultado.servidor}"
        )

        print(
            f"Content-Type: "
            f"{resultado.content_type}"
        )

        print()

        print(
            "HEADERS DE SEGURIDAD"
        )

        print(
            "-" * 65
        )

        for nombre, datos in (
            resultado
            .headers_seguridad
            .items()
        ):

            if datos[
                "presente"
            ]:

                estado = (
                    "PRESENTE"
                )

            else:

                estado = (
                    "NO OBSERVADO"
                )

            print(
                f"{nombre:25} "
                f"{estado}"
            )

        # ====================================================
        # TLS
        # ====================================================

        if resultado.usa_https:

            print()

            print(
                "CERTIFICADO TLS"
            )

            print(
                "-" * 65
            )

            print(
                "Disponible: "
                f"{resultado.certificado_disponible}"
            )

            print(
                "Validación: "
                f"{resultado.certificado_valido}"
            )

            print(
                "Sujeto: "
                f"{resultado.certificado_sujeto}"
            )

            print(
                "Emisor: "
                f"{resultado.certificado_emisor}"
            )

            print(
                "Válido desde: "
                f"{resultado.certificado_desde}"
            )

            print(
                "Válido hasta: "
                f"{resultado.certificado_hasta}"
            )

            print(
                "Días restantes: "
                f"{resultado.dias_restantes_certificado}"
            )

        print()

        if resultado.redirecciones:

            print(
                "REDIRECCIONES"
            )

            print(
                "-" * 65
            )

            for redireccion in (
                resultado.redirecciones
            ):

                print(
                    f'{redireccion["codigo"]}: '
                    f'{redireccion["desde"]}'
                )

                print(
                    f'       → '
                    f'{redireccion["hacia"]}'
                )

    except Exception as error:

        print(
            f"❌ Error: {error}"
        )