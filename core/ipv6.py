import ipaddress


# ============================================================
# VALIDACION IPv6
# ============================================================

def validar_ipv6(direccion):
    """
    Comprueba si una direccion IPv6 es valida.
    Acepta direcciones con o sin prefijo.
    """

    try:
        texto = direccion.strip()

        if "/" in texto:
            ipaddress.IPv6Interface(texto)
        else:
            ipaddress.IPv6Address(texto)

        return True

    except (ValueError, AttributeError):
        return False


# ============================================================
# ANALISIS PRINCIPAL
# ============================================================

def analizar_ipv6(direccion):
    """
    Analiza una direccion IPv6 y devuelve informacion
    detallada sobre la direccion y su prefijo.
    """

    texto = direccion.strip()

    if not texto:
        raise ValueError(
            "Debes introducir una direccion IPv6."
        )

    # Si no se proporciona prefijo, utilizamos /128
    if "/" not in texto:
        texto = f"{texto}/128"

    try:
        interfaz = ipaddress.IPv6Interface(texto)

    except ValueError as error:
        raise ValueError(
            "La direccion IPv6 introducida no es valida."
        ) from error

    ip = interfaz.ip
    red = interfaz.network
    prefijo = red.prefixlen

    bits_restantes = 128 - prefijo
    cantidad_direcciones = 2 ** bits_restantes

    return {
        # ----------------------------------------------------
        # DIRECCION
        # ----------------------------------------------------
        "direccion": str(ip),

        "direccion_comprimida": ip.compressed,

        "direccion_expandida": ip.exploded,

        # ----------------------------------------------------
        # PREFIJO
        # ----------------------------------------------------
        "prefijo": prefijo,

        "bits_prefijo": prefijo,

        "bits_restantes": bits_restantes,

        # ----------------------------------------------------
        # RED
        # ----------------------------------------------------
        "red": str(red.network_address),

        "red_cidr": str(red),

        "primera_direccion": str(
            red.network_address
        ),

        "ultima_direccion": str(
            red[-1]
        ),

        "cantidad_direcciones": cantidad_direcciones,

        # ----------------------------------------------------
        # CLASIFICACION
        # ----------------------------------------------------
        "tipo": clasificar_ipv6(ip),

        # ----------------------------------------------------
        # INFORMACION GENERAL
        # ----------------------------------------------------
        "version": ip.version,

        "bits": ip.max_prefixlen,

        # ----------------------------------------------------
        # REPRESENTACION
        # ----------------------------------------------------
        "hexadecimal": obtener_hextetos(ip),

        "binario": obtener_binario(ip),

        # ----------------------------------------------------
        # PROPIEDADES
        # ----------------------------------------------------
        "es_global": ip.is_global,

        "es_privada": ip.is_private,

        "es_link_local": ip.is_link_local,

        "es_multicast": ip.is_multicast,

        "es_loopback": ip.is_loopback,

        "es_unspecified": ip.is_unspecified,

        "es_reserved": ip.is_reserved,

        # ----------------------------------------------------
        # IPv4 MAPPED
        # ----------------------------------------------------
        "ipv4_mapped": (
            str(ip.ipv4_mapped)
            if ip.ipv4_mapped is not None
            else None
        ),

        # ----------------------------------------------------
        # SCOPE
        # ----------------------------------------------------
        "scope_id": getattr(
            ip,
            "scope_id",
            None
        ),
    }


# ============================================================
# CLASIFICACION IPv6
# ============================================================

def clasificar_ipv6(ip):
    """
    Clasifica una direccion IPv6 con mayor precision.

    Puede identificar:

    - Unspecified
    - Loopback
    - IPv4-Mapped
    - Documentation
    - Link-Local
    - Unique Local
    - Multicast
    - Global Unicast
    - Especial / Reservada
    """

    if not isinstance(ip, ipaddress.IPv6Address):
        ip = ipaddress.IPv6Address(ip)

    # --------------------------------------------------------
    # UNSPECIFIED
    # ::
    # --------------------------------------------------------

    if ip.is_unspecified:
        return "Unspecified"

    # --------------------------------------------------------
    # LOOPBACK
    # ::1
    # --------------------------------------------------------

    if ip.is_loopback:
        return "Loopback"

    # --------------------------------------------------------
    # IPv4-MAPPED
    # ::ffff:0:0/96
    #
    # Ejemplo:
    # ::ffff:192.168.1.10
    # --------------------------------------------------------

    if ip.ipv4_mapped is not None:
        return "IPv4-Mapped IPv6"

    # --------------------------------------------------------
    # DOCUMENTATION
    # 2001:db8::/32
    #
    # Utilizado para ejemplos y documentacion.
    # --------------------------------------------------------

    documentation = ipaddress.IPv6Network(
        "2001:db8::/32"
    )

    if ip in documentation:
        return "Documentation"

    # --------------------------------------------------------
    # LINK-LOCAL
    # fe80::/10
    # --------------------------------------------------------

    link_local = ipaddress.IPv6Network(
        "fe80::/10"
    )

    if ip in link_local:
        return "Link-Local"

    # --------------------------------------------------------
    # UNIQUE LOCAL ADDRESS
    # fc00::/7
    # --------------------------------------------------------

    unique_local = ipaddress.IPv6Network(
        "fc00::/7"
    )

    if ip in unique_local:
        return "Unique Local"

    # --------------------------------------------------------
    # MULTICAST
    # ff00::/8
    # --------------------------------------------------------

    multicast = ipaddress.IPv6Network(
        "ff00::/8"
    )

    if ip in multicast:
        return clasificar_multicast(ip)

    # --------------------------------------------------------
    # GLOBAL UNICAST
    # 2000::/3
    # --------------------------------------------------------

    global_unicast = ipaddress.IPv6Network(
        "2000::/3"
    )

    if ip in global_unicast:
        return "Global Unicast"

    # --------------------------------------------------------
    # RESERVADAS / ESPECIALES
    # --------------------------------------------------------

    if ip.is_reserved:
        return "Especial / Reservada"

    return "IPv6 no clasificada"


# ============================================================
# CLASIFICACION MULTICAST
# ============================================================

def clasificar_multicast(ip):
    """
    Determina el alcance (scope) de una direccion
    multicast IPv6.

    Las direcciones multicast pertenecen a:

    ff00::/8
    """

    if not isinstance(ip, ipaddress.IPv6Address):
        ip = ipaddress.IPv6Address(ip)

    # Segundo byte de la direccion IPv6
    segundo_byte = ip.packed[1]

    # Los cuatro bits inferiores representan el scope
    scope = segundo_byte & 0x0F

    scopes = {
        0x0: "Reserved",
        0x1: "Interface-Local",
        0x2: "Link-Local",
        0x3: "Realm-Local",
        0x4: "Admin-Local",
        0x5: "Site-Local",
        0x8: "Organization-Local",
        0xE: "Global",
        0xF: "Reserved",
    }

    nombre_scope = scopes.get(
        scope,
        f"Scope 0x{scope:X}"
    )

    return f"Multicast ({nombre_scope})"


# ============================================================
# HEXTETOS
# ============================================================

def obtener_hextetos(ip):
    """
    Devuelve los ocho hextetos de una direccion IPv6
    completamente expandida.
    """

    if not isinstance(ip, ipaddress.IPv6Address):
        ip = ipaddress.IPv6Address(ip)

    return ip.exploded.split(":")


# ============================================================
# REPRESENTACION BINARIA
# ============================================================

def obtener_binario(ip):
    """
    Devuelve los 128 bits de una direccion IPv6
    separados en ocho grupos de 16 bits.
    """

    if not isinstance(ip, ipaddress.IPv6Address):
        ip = ipaddress.IPv6Address(ip)

    binario = f"{int(ip):0128b}"

    return [
        binario[i:i + 16]
        for i in range(
            0,
            128,
            16
        )
    ]


# ============================================================
# COMPRIMIR IPv6
# ============================================================

def comprimir_ipv6(direccion):
    """
    Devuelve una direccion IPv6 en formato comprimido.
    """

    try:
        ip = ipaddress.IPv6Address(
            direccion.strip()
        )

        return ip.compressed

    except ValueError as error:
        raise ValueError(
            "La direccion IPv6 no es valida."
        ) from error


# ============================================================
# EXPANDIR IPv6
# ============================================================

def expandir_ipv6(direccion):
    """
    Devuelve una direccion IPv6 completamente expandida.
    """

    try:
        ip = ipaddress.IPv6Address(
            direccion.strip()
        )

        return ip.exploded

    except ValueError as error:
        raise ValueError(
            "La direccion IPv6 no es valida."
        ) from error


# ============================================================
# INFORMACION DEL PREFIJO
# ============================================================

def informacion_prefijo(prefijo):
    """
    Devuelve informacion sobre un prefijo IPv6.
    """

    try:
        prefijo = int(prefijo)

    except (TypeError, ValueError) as error:
        raise ValueError(
            "El prefijo debe ser un numero entre 0 y 128."
        ) from error

    if not 0 <= prefijo <= 128:
        raise ValueError(
            "El prefijo IPv6 debe estar entre 0 y 128."
        )

    bits_restantes = 128 - prefijo

    cantidad = 2 ** bits_restantes

    return {
        "prefijo": prefijo,

        "bits_red": prefijo,

        "bits_restantes": bits_restantes,

        "cantidad_direcciones": cantidad,
    }


# ============================================================
# FORMATEAR CANTIDAD DE DIRECCIONES
# ============================================================

def formatear_cantidad_direcciones(cantidad):
    """
    Convierte cantidades extremadamente grandes
    en una representacion mas legible.
    """

    if cantidad < 1_000:
        return f"{cantidad:,}"

    if cantidad < 1_000_000:
        return f"{cantidad:,}"

    return f"{cantidad:,}".replace(
        ",",
        "."
    )


# ============================================================
# PRUEBAS
# ============================================================

if __name__ == "__main__":

    pruebas = [
        "2001:db8:1234:5678::25/64",
        "2606:4700:4700::1111/128",
        "fe80::1/64",
        "fd12:3456:789a::1/64",
        "::1/128",
        "::/128",
        "ff02::1/128",
        "ff0e::1/128",
        "::ffff:192.168.1.10/128",
    ]

    print()
    print("=" * 75)
    print("NETPRO - ANALIZADOR IPv6")
    print("=" * 75)

    for direccion in pruebas:

        resultado = analizar_ipv6(
            direccion
        )

        print()
        print(
            f"{direccion:<38}"
            f" -> {resultado['tipo']}"
        )

    print()
    print("=" * 75)

    # --------------------------------------------------------
    # PRUEBA DETALLADA
    # --------------------------------------------------------

    ejemplo = "2001:db8:1234:5678::25/64"

    resultado = analizar_ipv6(
        ejemplo
    )

    print()
    print("ANALISIS DETALLADO")
    print("-" * 75)

    print(
        f"Direccion:           "
        f"{resultado['direccion']}"
    )

    print(
        f"Comprimida:          "
        f"{resultado['direccion_comprimida']}"
    )

    print(
        f"Expandida:           "
        f"{resultado['direccion_expandida']}"
    )

    print(
        f"Tipo:                "
        f"{resultado['tipo']}"
    )

    print(
        f"Prefijo:             "
        f"/{resultado['prefijo']}"
    )

    print(
        f"Bits de prefijo:     "
        f"{resultado['bits_prefijo']}"
    )

    print(
        f"Bits restantes:      "
        f"{resultado['bits_restantes']}"
    )

    print(
        f"Red:                 "
        f"{resultado['red']}"
    )

    print(
        f"Red CIDR:            "
        f"{resultado['red_cidr']}"
    )

    print(
        f"Primera direccion:   "
        f"{resultado['primera_direccion']}"
    )

    print(
        f"Ultima direccion:    "
        f"{resultado['ultima_direccion']}"
    )

    print()
    print("HEXTETOS")
    print("-" * 75)

    for numero, hexteto in enumerate(
        resultado["hexadecimal"],
        start=1
    ):

        print(
            f"Hexteto {numero}: "
            f"{hexteto}"
        )

    print()
    print("BINARIO")
    print("-" * 75)

    for numero, grupo in enumerate(
        resultado["binario"],
        start=1
    ):

        print(
            f"{numero}: {grupo}"
        )

    print()
    print("=" * 75)