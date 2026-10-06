import subprocess
import json
import platform
import re


# ============================================================
# RESULTADO VACÍO / ERROR
# ============================================================

def _resultado_vacio(estado, error=None):
    """
    Genera una estructura de resultado consistente.
    """

    return {
        "detectado": False,
        "conectado": False,
        "nombre": None,
        "descripcion": None,
        "velocidad": None,
        "estado": estado,
        "error": error
    }


# ============================================================
# DETECTAR SI UN ADAPTADOR ES VIRTUAL
# ============================================================

def _es_adaptador_virtual(adaptador):
    """
    Intenta identificar adaptadores virtuales, VPN,
    hipervisores y túneles para evitar confundirlos
    con adaptadores físicos.
    """

    nombre = str(
        adaptador.get("Name", "")
    ).lower()

    descripcion = str(
        adaptador.get(
            "InterfaceDescription",
            ""
        )
    ).lower()

    texto = (
        nombre
        + " "
        + descripcion
    )

    palabras_virtuales = [
        "radmin",
        "vpn",
        "virtual",
        "vmware",
        "virtualbox",
        "hyper-v",
        "vethernet",
        "tap",
        "tun",
        "tunnel",
        "wsl",
        "loopback",
        "npcap",
        "hamachi",
        "zerotier",
        "tailscale",
        "wireguard",
        "openvpn",
        "fortinet",
        "forticlient",
        "nordvpn",
        "protonvpn"
    ]

    return any(
        palabra in texto
        for palabra in palabras_virtuales
    )


# ============================================================
# DETECTAR SI ES WI-FI
# ============================================================

def _es_wifi(adaptador):
    """
    Identifica adaptadores Wi-Fi físicos.
    """

    # --------------------------------------------------------
    # Debe ser hardware físico
    # --------------------------------------------------------

    hardware = adaptador.get(
        "HardwareInterface",
        False
    )

    if not hardware:
        return False

    # --------------------------------------------------------
    # Excluir adaptadores virtuales
    # --------------------------------------------------------

    if _es_adaptador_virtual(adaptador):
        return False

    nombre = str(
        adaptador.get("Name", "")
    ).lower()

    descripcion = str(
        adaptador.get(
            "InterfaceDescription",
            ""
        )
    ).lower()

    medio = str(
        adaptador.get(
            "PhysicalMediaType",
            ""
        )
    ).lower()

    texto = (
        nombre
        + " "
        + descripcion
        + " "
        + medio
    )

    palabras_wifi = [
        "wi-fi",
        "wifi",
        "wireless",
        "802.11",
        "wlan"
    ]

    return any(
        palabra in texto
        for palabra in palabras_wifi
    )


# ============================================================
# DETECTAR SI ES ETHERNET
# ============================================================

def _es_ethernet(adaptador):
    """
    Determina si el adaptador parece corresponder
    a una interfaz Ethernet física.
    """

    # --------------------------------------------------------
    # Primero debe ser una interfaz de hardware real.
    # --------------------------------------------------------

    hardware = adaptador.get(
        "HardwareInterface",
        False
    )

    if not hardware:
        return False

    # --------------------------------------------------------
    # Excluir Wi-Fi
    # --------------------------------------------------------

    if _es_wifi(adaptador):
        return False

    # --------------------------------------------------------
    # Excluir adaptadores virtuales
    # --------------------------------------------------------

    if _es_adaptador_virtual(adaptador):
        return False

    nombre = str(
        adaptador.get("Name", "")
    ).lower()

    descripcion = str(
        adaptador.get(
            "InterfaceDescription",
            ""
        )
    ).lower()

    medio = str(
        adaptador.get(
            "PhysicalMediaType",
            ""
        )
    ).lower()

    texto = (
        nombre
        + " "
        + descripcion
        + " "
        + medio
    )

    indicadores_ethernet = [
        "ethernet",
        "802.3",
        "gbe",
        "gigabit",
        "2.5gbe",
        "5gbe",
        "10gbe",
        "realtek pcie",
        "realtek usb",
        "intel(r) ethernet",
        "intel ethernet",
        "broadcom",
        "killer e",
        "usb ethernet"
    ]

    return any(
        palabra in texto
        for palabra in indicadores_ethernet
    )


# ============================================================
# CONSULTAR ADAPTADORES DE WINDOWS
# ============================================================

def _consultar_adaptadores():
    """
    Consulta todos los adaptadores de red mediante PowerShell.

    Esta función permite reutilizar la misma lógica para
    Ethernet y Wi-Fi.
    """

    if platform.system().lower() != "windows":

        return None, (
            "Esta detección está configurada "
            "actualmente para Windows."
        )

    script = (
        "Get-NetAdapter | "
        "Select-Object "
        "Name,"
        "InterfaceDescription,"
        "Status,"
        "LinkSpeed,"
        "PhysicalMediaType,"
        "HardwareInterface | "
        "ConvertTo-Json -Compress"
    )

    comando = [
        "powershell.exe",
        "-NoLogo",
        "-NoProfile",
        "-NonInteractive",
        "-Command",
        script
    ]

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

        return None, (
            "Windows tardó demasiado en consultar "
            "los adaptadores de red."
        )

    except FileNotFoundError:

        return None, (
            "PowerShell no está disponible."
        )

    except Exception as error:

        return None, str(error)

    salida = proceso.stdout.strip()

    if not salida:

        error_powershell = (
            proceso.stderr.strip()
        )

        return None, (
            error_powershell
            if error_powershell
            else (
                "Windows no devolvió información "
                "de adaptadores."
            )
        )

    try:

        datos = json.loads(
            salida
        )

    except json.JSONDecodeError:

        return None, (
            "No fue posible interpretar la "
            "información de los adaptadores."
        )

    if isinstance(datos, dict):

        datos = [datos]

    return datos, None


# ============================================================
# ELEGIR ADAPTADOR
# ============================================================

def _elegir_adaptador(adaptadores):
    """
    Prioriza un adaptador conectado.

    Si ninguno está conectado, devuelve el primero
    para que NetPro pueda mostrar que existe pero
    está desconectado.
    """

    if not adaptadores:
        return None

    for adaptador in adaptadores:

        estado = str(
            adaptador.get(
                "Status",
                ""
            )
        ).lower()

        if estado == "up":

            return adaptador

    return adaptadores[0]


# ============================================================
# CREAR RESULTADO DE ADAPTADOR
# ============================================================

def _crear_resultado_adaptador(adaptador):
    """
    Convierte un adaptador de Windows al formato
    utilizado por NetPro.
    """

    if adaptador is None:

        return _resultado_vacio(
            "No detectado"
        )

    estado_windows = str(
        adaptador.get(
            "Status",
            ""
        )
    )

    conectado = (
        estado_windows.lower()
        == "up"
    )

    return {
        "detectado": True,

        "conectado": conectado,

        "nombre": adaptador.get(
            "Name"
        ),

        "descripcion": adaptador.get(
            "InterfaceDescription"
        ),

        "velocidad": adaptador.get(
            "LinkSpeed"
        ),

        "estado": (
            "Conectado"
            if conectado
            else "Desconectado"
        ),

        "error": None
    }


# ============================================================
# DETALLES DE LA CONEXIÓN WI-FI
# ============================================================

def _obtener_detalles_wifi():
    """
    Consulta detalles de la conexión inalámbrica
    mediante NETSH.

    Intenta obtener:
        SSID
        señal
        velocidad de recepción
        velocidad de transmisión
    """

    resultado = {
        "ssid": None,
        "senal": None,
        "recepcion": None,
        "transmision": None
    }

    if platform.system().lower() != "windows":

        return resultado

    comando = [
        "netsh",
        "wlan",
        "show",
        "interfaces"
    ]

    try:

        proceso = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            shell=False,
            timeout=8,
            errors="replace"
        )

    except Exception:

        return resultado

    salida = proceso.stdout

    if not salida:

        return resultado

    # ========================================================
    # SSID
    # ========================================================

    coincidencia = re.search(
        r"^\s*SSID\s*:\s*(.+)$",
        salida,
        flags=(
            re.MULTILINE
            | re.IGNORECASE
        )
    )

    if coincidencia:

        ssid = (
            coincidencia
            .group(1)
            .strip()
        )

        # Evitar confundir BSSID con SSID.
        if ssid:

            resultado["ssid"] = ssid

    # ========================================================
    # SEÑAL
    # ========================================================

    coincidencia = re.search(
        r"^\s*(?:Signal|Señal)\s*:\s*(.+)$",
        salida,
        flags=(
            re.MULTILINE
            | re.IGNORECASE
        )
    )

    if coincidencia:

        resultado["senal"] = (
            coincidencia
            .group(1)
            .strip()
        )

    # ========================================================
    # VELOCIDAD DE RECEPCIÓN
    # ========================================================

    patrones_recepcion = [
        (
            r"^\s*Receive rate.*?:\s*(.+)$"
        ),
        (
            r"^\s*Velocidad de recepción.*?:\s*(.+)$"
        )
    ]

    for patron in patrones_recepcion:

        coincidencia = re.search(
            patron,
            salida,
            flags=(
                re.MULTILINE
                | re.IGNORECASE
            )
        )

        if coincidencia:

            resultado["recepcion"] = (
                coincidencia
                .group(1)
                .strip()
            )

            break

    # ========================================================
    # VELOCIDAD DE TRANSMISIÓN
    # ========================================================

    patrones_transmision = [
        (
            r"^\s*Transmit rate.*?:\s*(.+)$"
        ),
        (
            r"^\s*Velocidad de transmisión.*?:\s*(.+)$"
        )
    ]

    for patron in patrones_transmision:

        coincidencia = re.search(
            patron,
            salida,
            flags=(
                re.MULTILINE
                | re.IGNORECASE
            )
        )

        if coincidencia:

            resultado["transmision"] = (
                coincidencia
                .group(1)
                .strip()
            )

            break

    return resultado


# ============================================================
# ESTADO COMPLETO DE RED
# ============================================================

def obtener_estado_red():
    """
    Obtiene Ethernet y Wi-Fi en una sola consulta.

    Devuelve:

        {
            "ethernet": {...},
            "wifi": {...}
        }
    """

    datos, error = (
        _consultar_adaptadores()
    )

    # ========================================================
    # ERROR GENERAL
    # ========================================================

    if error:

        ethernet = _resultado_vacio(
            "Error",
            error
        )

        wifi = _resultado_vacio(
            "Error",
            error
        )

        wifi.update({
            "ssid": None,
            "senal": None,
            "recepcion": None,
            "transmision": None
        })

        return {
            "ethernet": ethernet,
            "wifi": wifi
        }

    # ========================================================
    # BUSCAR ETHERNET
    # ========================================================

    adaptadores_ethernet = []

    for adaptador in datos:

        if _es_ethernet(
            adaptador
        ):

            adaptadores_ethernet.append(
                adaptador
            )

    ethernet = (
        _crear_resultado_adaptador(
            _elegir_adaptador(
                adaptadores_ethernet
            )
        )
    )

    # ========================================================
    # BUSCAR WI-FI
    # ========================================================

    adaptadores_wifi = []

    for adaptador in datos:

        if _es_wifi(
            adaptador
        ):

            adaptadores_wifi.append(
                adaptador
            )

    wifi = (
        _crear_resultado_adaptador(
            _elegir_adaptador(
                adaptadores_wifi
            )
        )
    )

    # Campos adicionales específicos de Wi-Fi.

    wifi.update({
        "ssid": None,
        "senal": None,
        "recepcion": None,
        "transmision": None
    })

    # Si está conectado, consultar detalles.

    if wifi["conectado"]:

        detalles_wifi = (
            _obtener_detalles_wifi()
        )

        wifi.update(
            detalles_wifi
        )

    # ========================================================
    # RESULTADO
    # ========================================================

    return {
        "ethernet": ethernet,
        "wifi": wifi
    }


# ============================================================
# ESTADO ETHERNET
# ============================================================

def obtener_estado_ethernet():
    """
    Mantiene la función que NetPro ya utilizaba.

    Ahora utiliza el monitor combinado internamente.
    """

    resultado = obtener_estado_red()

    return resultado["ethernet"]


# ============================================================
# ESTADO WI-FI
# ============================================================

def obtener_estado_wifi():
    """
    Devuelve únicamente el estado Wi-Fi.
    """

    resultado = obtener_estado_red()

    return resultado["wifi"]


# ============================================================
# PRUEBA
# ============================================================

if __name__ == "__main__":

    print()

    print(
        "NETPRO - ESTADO DE RED"
    )

    print(
        "────────────────────────────"
    )

    resultado = (
        obtener_estado_red()
    )

    # ========================================================
    # ETHERNET
    # ========================================================

    print()

    print(
        "ETHERNET"
    )

    print(
        "────────────────────────────"
    )

    for clave, valor in (
        resultado["ethernet"].items()
    ):

        print(
            f"{clave}: {valor}"
        )

    # ========================================================
    # WI-FI
    # ========================================================

    print()

    print(
        "WI-FI"
    )

    print(
        "────────────────────────────"
    )

    for clave, valor in (
        resultado["wifi"].items()
    ):

        print(
            f"{clave}: {valor}"
        )