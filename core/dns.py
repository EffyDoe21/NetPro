from urllib.parse import urlparse

import dns.exception
import dns.resolver


# ============================================================
# NORMALIZAR DOMINIO
# ============================================================

def normalizar_dominio(entrada: str) -> str:
    """
    Convierte lo que introduce el usuario en un hostname.

    Ejemplos:

    google.com
        -> google.com

    https://www.google.com/search?q=test
        -> www.google.com
    """

    entrada = entrada.strip()

    if not entrada:
        raise ValueError("Debes introducir un dominio.")

    # Si no incluye esquema, añadimos uno temporalmente
    # para que urlparse pueda separar correctamente el hostname.
    if "://" not in entrada:
        entrada_parsear = "https://" + entrada
    else:
        entrada_parsear = entrada

    try:
        parsed = urlparse(entrada_parsear)
        dominio = parsed.hostname

    except Exception:
        dominio = None

    if not dominio:
        raise ValueError(
            "No se pudo identificar un dominio válido."
        )

    # DNS no necesita el punto final para nuestras consultas
    dominio = dominio.rstrip(".").lower()

    return dominio


# ============================================================
# CONSULTA DNS GENÉRICA
# ============================================================

def consultar_registro(resolver, dominio, tipo):
    """
    Consulta un tipo de registro DNS.

    Si el registro no existe, devuelve una lista vacía.
    """

    try:

        respuesta = resolver.resolve(
            dominio,
            tipo,
            raise_on_no_answer=False
        )

        if respuesta.rrset is None:
            return []

        return list(respuesta)

    except (
        dns.resolver.NoAnswer,
        dns.resolver.NXDOMAIN,
        dns.resolver.NoNameservers,
        dns.exception.Timeout,
        dns.resolver.LifetimeTimeout,
    ):
        return []


# ============================================================
# LIMPIAR NOMBRES DNS
# ============================================================

def limpiar_nombre(nombre):
    """
    Convierte objetos DNS en texto y elimina el punto final.

    Ejemplo:

    mail.example.com.
        -> mail.example.com
    """

    return str(nombre).rstrip(".")


# ============================================================
# RESOLVER DOMINIO
# ============================================================

def resolver_dominio(entrada: str) -> dict:
    """
    Consulta los registros DNS utilizados actualmente
    por la interfaz DNS de NetPro.

    Devuelve:

    {
        "domain": "...",
        "A": [],
        "AAAA": [],
        "CNAME": [],
        "MX": [],
        "NS": [],
        "TXT": []
    }
    """

    dominio = normalizar_dominio(entrada)

    resolver = dns.resolver.Resolver()

    # Tiempo máximo razonable para la aplicación
    resolver.timeout = 3
    resolver.lifetime = 5

    # ========================================================
    # A
    # ========================================================

    registros_a = []

    for registro in consultar_registro(
        resolver,
        dominio,
        "A"
    ):
        registros_a.append(
            registro.address
        )

    # ========================================================
    # AAAA
    # ========================================================

    registros_aaaa = []

    for registro in consultar_registro(
        resolver,
        dominio,
        "AAAA"
    ):
        registros_aaaa.append(
            registro.address
        )

    # ========================================================
    # CNAME
    # ========================================================

    registros_cname = []

    for registro in consultar_registro(
        resolver,
        dominio,
        "CNAME"
    ):
        registros_cname.append(
            limpiar_nombre(registro.target)
        )

    # ========================================================
    # MX
    # ========================================================

    registros_mx = []

    for registro in consultar_registro(
        resolver,
        dominio,
        "MX"
    ):

        registros_mx.append(
            {
                "priority": registro.preference,
                "server": limpiar_nombre(
                    registro.exchange
                )
            }
        )

    # Ordenar por prioridad MX
    registros_mx.sort(
        key=lambda x: x["priority"]
    )

    # ========================================================
    # NS
    # ========================================================

    registros_ns = []

    for registro in consultar_registro(
        resolver,
        dominio,
        "NS"
    ):

        registros_ns.append(
            limpiar_nombre(
                registro.target
            )
        )

    # ========================================================
    # TXT
    # ========================================================

    registros_txt = []

    for registro in consultar_registro(
        resolver,
        dominio,
        "TXT"
    ):

        try:

            partes = [
                parte.decode(
                    "utf-8",
                    errors="replace"
                )
                for parte in registro.strings
            ]

            registros_txt.append(
                "".join(partes)
            )

        except Exception:

            registros_txt.append(
                str(registro)
            )

    # ========================================================
    # RESULTADO
    # ========================================================

    return {
        "domain": dominio,
        "A": registros_a,
        "AAAA": registros_aaaa,
        "CNAME": registros_cname,
        "MX": registros_mx,
        "NS": registros_ns,
        "TXT": registros_txt
    }