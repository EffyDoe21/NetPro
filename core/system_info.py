"""
NetPro - Network & Security Toolkit
Core: Informacion avanzada del sistema
Version 2

Recopila informacion real del equipo local.
No realiza diagnosticos de seguridad por inferencia.
No utiliza IA para obtener datos tecnicos.
"""

from __future__ import annotations

import getpass
import json
import os
import platform
import shutil
import socket
import subprocess
import sys
import time
import unicodedata

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any


# ============================================================
# CONFIGURACION
# ============================================================

POWERSHELL_TIMEOUT = 10


# ============================================================
# MODELOS
# ============================================================

@dataclass
class CPUInfo:
    nombre: str = "No disponible"
    fabricante: str = "No disponible"
    socket: str = "No disponible"
    nucleos_fisicos: int | None = None
    procesadores_logicos: int | None = None
    frecuencia_actual_mhz: int | None = None
    frecuencia_max_mhz: int | None = None
    carga_porcentaje: float | None = None
    virtualizacion_firmware: bool | None = None
    arquitectura: str = "No disponible"


@dataclass
class RAMModuleInfo:
    banco: str = "No disponible"
    dispositivo: str = "No disponible"
    capacidad_bytes: int | None = None
    fabricante: str = "No disponible"
    numero_parte: str = "No disponible"
    numero_serie: str = "No disponible"
    velocidad_mhz: int | None = None
    velocidad_configurada_mhz: int | None = None
    tipo_memoria: str = "No disponible"


@dataclass
class MemoriaInfo:
    total_bytes: int | None = None
    disponible_bytes: int | None = None
    usada_bytes: int | None = None
    uso_porcentaje: float | None = None
    modulos: list[RAMModuleInfo] = field(default_factory=list)


@dataclass
class MotherboardInfo:
    fabricante: str = "No disponible"
    producto: str = "No disponible"
    version: str = "No disponible"
    serial: str = "No disponible"


@dataclass
class BIOSInfo:
    fabricante: str = "No disponible"
    version: str = "No disponible"
    fecha: str = "No disponible"
    serial: str = "No disponible"
    modo_firmware: str = "No determinado"


@dataclass
class GPUInfo:
    nombre: str = "No disponible"
    memoria_bytes: int | None = None
    driver: str = "No disponible"
    resolucion: str = "No disponible"
    frecuencia_refresco_hz: int | None = None
    estado: str = "No disponible"
    tipo: str = "No determinado"


@dataclass
class MonitorInfo:
    nombre: str = "No disponible"
    fabricante: str = "No disponible"
    activo: bool | None = None


@dataclass
class PhysicalDiskInfo:
    numero: int | None = None
    nombre: str = "No disponible"
    modelo: str = "No disponible"
    serial: str = "No disponible"
    tipo_medio: str = "No disponible"
    bus: str = "No disponible"
    tamano_bytes: int | None = None
    estado_salud: str = "No disponible"
    estado_operacional: str = "No disponible"


@dataclass
class VolumeInfo:
    unidad: str = ""
    etiqueta: str = ""
    sistema_archivos: str = "No disponible"
    total_bytes: int | None = None
    usado_bytes: int | None = None
    libre_bytes: int | None = None
    uso_porcentaje: float | None = None


@dataclass
class NetworkAdapterInfo:
    nombre: str = "No disponible"
    descripcion: str = "No disponible"
    tipo: str = "No determinado"
    estado: str = "No disponible"
    mac: str = "No disponible"
    velocidad_mbps: float | None = None
    mtu: int | None = None
    metrica: int | None = None
    ipv4: list[str] = field(default_factory=list)
    ipv6: list[str] = field(default_factory=list)
    gateway: list[str] = field(default_factory=list)
    dns: list[str] = field(default_factory=list)
    dhcp: bool | None = None
    fisico: bool | None = None


@dataclass
class FirewallProfileInfo:
    nombre: str = "No disponible"
    habilitado: bool | None = None
    entrada_predeterminada: str = "No disponible"
    salida_predeterminada: str = "No disponible"


@dataclass
class SecurityInfo:
    secure_boot: bool | None = None
    tpm_presente: bool | None = None
    tpm_listo: bool | None = None
    tpm_habilitado: bool | None = None
    tpm_version: str = "No disponible"
    defender_disponible: bool | None = None
    defender_antivirus: bool | None = None
    defender_tiempo_real: bool | None = None
    firewall: list[FirewallProfileInfo] = field(default_factory=list)


@dataclass
class EnvironmentInfo:
    python_version: str = "No disponible"
    python_executable: str = "No disponible"
    entorno_virtual: bool = False
    virtual_env: str = "No disponible"
    powershell_disponible: bool = False
    ollama_disponible: bool = False
    ollama_version: str = "No disponible"
    modelos_ollama: list[str] = field(default_factory=list)


@dataclass
class SistemaInfo:
    fecha_consulta: str = ""
    nombre_equipo: str = "No disponible"
    hostname: str = "No disponible"
    usuario: str = "No disponible"

    sistema_operativo: str = "No disponible"
    version_sistema: str = "No disponible"
    build: str = "No disponible"
    arquitectura: str = "No disponible"

    fabricante_equipo: str = "No disponible"
    modelo_equipo: str = "No disponible"

    fecha_instalacion_windows: str = "No disponible"
    zona_horaria: str = "No disponible"

    ultimo_arranque: str = "No disponible"
    uptime_segundos: float | None = None

    cpu: CPUInfo = field(default_factory=CPUInfo)
    memoria: MemoriaInfo = field(default_factory=MemoriaInfo)

    placa_base: MotherboardInfo = field(default_factory=MotherboardInfo)
    bios: BIOSInfo = field(default_factory=BIOSInfo)

    gpus: list[GPUInfo] = field(default_factory=list)
    monitores: list[MonitorInfo] = field(default_factory=list)

    discos_fisicos: list[PhysicalDiskInfo] = field(default_factory=list)
    volumenes: list[VolumeInfo] = field(default_factory=list)

    adaptadores_red: list[NetworkAdapterInfo] = field(default_factory=list)
    ip_local_principal: str = "No disponible"

    seguridad: SecurityInfo = field(default_factory=SecurityInfo)
    entorno: EnvironmentInfo = field(default_factory=EnvironmentInfo)

    procesos_totales: int | None = None

    errores: list[str] = field(default_factory=list)


# ============================================================
# UTILIDADES
# ============================================================

def bytes_legibles(valor: int | float | None) -> str:
    if valor is None:
        return "No disponible"

    try:
        valor = float(valor)
    except (TypeError, ValueError):
        return "No disponible"

    unidades = ["B", "KB", "MB", "GB", "TB", "PB"]
    indice = 0

    while valor >= 1024 and indice < len(unidades) - 1:
        valor /= 1024
        indice += 1

    if indice == 0:
        return f"{valor:.0f} {unidades[indice]}"

    return f"{valor:.2f} {unidades[indice]}"


def convertir_entero(valor: Any) -> int | None:
    try:
        return int(valor) if valor is not None else None
    except (TypeError, ValueError):
        return None


def convertir_float(valor: Any) -> float | None:
    try:
        return float(valor) if valor is not None else None
    except (TypeError, ValueError):
        return None


def calcular_porcentaje(usado, total):
    if usado is None or total in (None, 0):
        return None

    try:
        return round((float(usado) / float(total)) * 100, 2)
    except Exception:
        return None


def lista_segura(valor) -> list[str]:
    if valor is None:
        return []

    if isinstance(valor, list):
        return [str(x) for x in valor if x]

    return [str(valor)]


def normalizar_json(valor):
    if valor is None:
        return []

    if isinstance(valor, list):
        return valor

    return [valor]


def bool_windows(valor) -> bool | None:
    if valor is None:
        return None

    texto = str(valor).strip().lower()

    if texto in ("true", "enabled", "1", "yes"):
        return True

    if texto in ("false", "disabled", "0", "no"):
        return False

    return None


def traducir_tipo_memoria(codigo) -> str:
    tipos = {
        0: "Desconocido",
        1: "Otro",
        2: "DRAM",
        3: "Synchronous DRAM",
        18: "DDR",
        19: "DDR2",
        20: "DDR2 FB-DIMM",
        24: "DDR3",
        26: "DDR4",
        27: "LPDDR",
        28: "LPDDR2",
        29: "LPDDR3",
        30: "LPDDR4",
        34: "DDR5",
        35: "LPDDR5"
    }

    try:
        codigo = int(codigo)
    except (TypeError, ValueError):
        return "No disponible"

    return tipos.get(codigo, f"SMBIOS {codigo}")


# ============================================================
# POWERSHELL
# ============================================================

def ejecutar_powershell(script: str, timeout=POWERSHELL_TIMEOUT):
    resultado = subprocess.run(
        [
            "powershell.exe",
            "-NoLogo",
            "-NoProfile",
            "-NonInteractive",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            script
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        creationflags=(
            subprocess.CREATE_NO_WINDOW
            if os.name == "nt"
            else 0
        )
    )

    if resultado.returncode != 0:
        raise RuntimeError(
            resultado.stderr.strip()
            or "PowerShell devolvio un error."
        )

    return resultado.stdout.strip()


def ejecutar_powershell_json(script: str, timeout=POWERSHELL_TIMEOUT):
    salida = ejecutar_powershell(
        f"""
        $ErrorActionPreference = 'Stop'

        $resultado = & {{
            {script}
        }}

        $resultado | ConvertTo-Json -Depth 10 -Compress
        """,
        timeout
    )

    if not salida:
        return None

    return json.loads(salida)


# ============================================================
# WINDOWS GENERAL
# ============================================================

def obtener_windows(sistema: SistemaInfo):
    script = """
    $os = Get-CimInstance Win32_OperatingSystem
    $cs = Get-CimInstance Win32_ComputerSystem

    [PSCustomObject]@{
        Caption = $os.Caption
        Version = $os.Version
        Build = $os.BuildNumber
        InstallDate = $os.InstallDate.ToString("o")
        LastBoot = $os.LastBootUpTime.ToString("o")
        Manufacturer = $cs.Manufacturer
        Model = $cs.Model
        TimeZone = (Get-TimeZone).DisplayName
    }
    """

    datos = ejecutar_powershell_json(script)

    sistema.sistema_operativo = (
        datos.get("Caption")
        or sistema.sistema_operativo
    )

    sistema.version_sistema = (
        datos.get("Version")
        or "No disponible"
    )

    sistema.build = str(
        datos.get("Build")
        or "No disponible"
    )

    sistema.fabricante_equipo = (
        datos.get("Manufacturer")
        or "No disponible"
    )

    sistema.modelo_equipo = (
        datos.get("Model")
        or "No disponible"
    )

    sistema.fecha_instalacion_windows = (
        datos.get("InstallDate")
        or "No disponible"
    )

    sistema.ultimo_arranque = (
        datos.get("LastBoot")
        or "No disponible"
    )

    sistema.zona_horaria = (
        datos.get("TimeZone")
        or "No disponible"
    )

    try:
        inicio = datetime.fromisoformat(
            sistema.ultimo_arranque
        )

        ahora = datetime.now(
            inicio.tzinfo
        )

        sistema.uptime_segundos = (
            ahora - inicio
        ).total_seconds()

    except Exception:
        pass


# ============================================================
# PLACA BASE
# ============================================================

def obtener_placa_base() -> MotherboardInfo:
    datos = ejecutar_powershell_json(
        """
        Get-CimInstance Win32_BaseBoard |
        Select-Object Manufacturer, Product, Version, SerialNumber
        """
    )

    if isinstance(datos, list):
        datos = datos[0]

    return MotherboardInfo(
        fabricante=(
            datos.get("Manufacturer")
            or "No disponible"
        ),

        producto=(
            datos.get("Product")
            or "No disponible"
        ),

        version=(
            datos.get("Version")
            or "No disponible"
        ),

        serial=(
            datos.get("SerialNumber")
            or "No disponible"
        )
    )


# ============================================================
# BIOS
# ============================================================

def obtener_bios() -> BIOSInfo:
    datos = ejecutar_powershell_json(
        """
        $bios = Get-CimInstance Win32_BIOS

        $fecha = $null

        if ($null -ne $bios.ReleaseDate) {
            $fecha = $bios.ReleaseDate.ToString("o")
        }

        [PSCustomObject]@{
            Manufacturer = $bios.Manufacturer
            Version = $bios.SMBIOSBIOSVersion
            Serial = $bios.SerialNumber
            ReleaseDate = $fecha
        }
        """
    )

    if isinstance(datos, list):
        datos = datos[0]

    bios = BIOSInfo(
        fabricante=(
            datos.get("Manufacturer")
            or "No disponible"
        ),

        version=(
            datos.get("Version")
            or "No disponible"
        ),

        serial=(
            datos.get("Serial")
            or "No disponible"
        ),

        fecha=(
            datos.get("ReleaseDate")
            or "No disponible"
        )
    )

    try:
        firmware = ejecutar_powershell(
            """
            $valor = (Get-ComputerInfo).BiosFirmwareType

            if ($null -ne $valor) {
                $valor.ToString()
            }
            """
        )

        if firmware:
            bios.modo_firmware = firmware.strip()

    except Exception:
        pass

    return bios


# ============================================================
# CPU
# ============================================================

def obtener_cpu() -> CPUInfo:
    datos = ejecutar_powershell_json(
        """
        $cpu = Get-CimInstance Win32_Processor |
            Select-Object -First 1

        [PSCustomObject]@{
            Name = $cpu.Name
            Manufacturer = $cpu.Manufacturer
            SocketDesignation = $cpu.SocketDesignation
            NumberOfCores = $cpu.NumberOfCores
            NumberOfLogicalProcessors = $cpu.NumberOfLogicalProcessors
            CurrentClockSpeed = $cpu.CurrentClockSpeed
            MaxClockSpeed = $cpu.MaxClockSpeed
            LoadPercentage = $cpu.LoadPercentage
            VirtualizationFirmwareEnabled = $cpu.VirtualizationFirmwareEnabled
            Architecture = $cpu.Architecture
        }
        """
    )

    if isinstance(datos, list):
        datos = datos[0]

    return CPUInfo(
        nombre=(
            datos.get("Name")
            or "No disponible"
        ),

        fabricante=(
            datos.get("Manufacturer")
            or "No disponible"
        ),

        socket=(
            datos.get("SocketDesignation")
            or "No disponible"
        ),

        nucleos_fisicos=convertir_entero(
            datos.get("NumberOfCores")
        ),

        procesadores_logicos=convertir_entero(
            datos.get("NumberOfLogicalProcessors")
        ),

        frecuencia_actual_mhz=convertir_entero(
            datos.get("CurrentClockSpeed")
        ),

        frecuencia_max_mhz=convertir_entero(
            datos.get("MaxClockSpeed")
        ),

        carga_porcentaje=convertir_float(
            datos.get("LoadPercentage")
        ),

        virtualizacion_firmware=bool_windows(
            datos.get("VirtualizationFirmwareEnabled")
        ),

        arquitectura=str(
            datos.get("Architecture")
            or "No disponible"
        )
    )


# ============================================================
# MEMORIA
# ============================================================

def obtener_memoria() -> MemoriaInfo:
    memoria = MemoriaInfo()

    os_info = ejecutar_powershell_json(
        """
        $os = Get-CimInstance Win32_OperatingSystem

        [PSCustomObject]@{
            TotalVisibleMemorySize = $os.TotalVisibleMemorySize
            FreePhysicalMemory = $os.FreePhysicalMemory
        }
        """
    )

    if isinstance(os_info, list):
        os_info = os_info[0]

    total_kb = convertir_entero(
        os_info.get("TotalVisibleMemorySize")
    )

    libre_kb = convertir_entero(
        os_info.get("FreePhysicalMemory")
    )

    if total_kb is not None:
        memoria.total_bytes = (
            total_kb * 1024
        )

    if libre_kb is not None:
        memoria.disponible_bytes = (
            libre_kb * 1024
        )

    if (
        memoria.total_bytes is not None
        and memoria.disponible_bytes is not None
    ):
        memoria.usada_bytes = (
            memoria.total_bytes
            - memoria.disponible_bytes
        )

        memoria.uso_porcentaje = calcular_porcentaje(
            memoria.usada_bytes,
            memoria.total_bytes
        )

    datos = ejecutar_powershell_json(
        """
        Get-CimInstance Win32_PhysicalMemory |
        ForEach-Object {
            [PSCustomObject]@{
                BankLabel = $_.BankLabel
                DeviceLocator = $_.DeviceLocator
                Capacity = $_.Capacity
                Manufacturer = $_.Manufacturer
                PartNumber = $_.PartNumber
                SerialNumber = $_.SerialNumber
                Speed = $_.Speed
                ConfiguredClockSpeed = $_.ConfiguredClockSpeed
                SMBIOSMemoryType = $_.SMBIOSMemoryType
            }
        }
        """
    )

    for item in normalizar_json(datos):
        memoria.modulos.append(
            RAMModuleInfo(
                banco=(
                    item.get("BankLabel")
                    or "No disponible"
                ),

                dispositivo=(
                    item.get("DeviceLocator")
                    or "No disponible"
                ),

                capacidad_bytes=convertir_entero(
                    item.get("Capacity")
                ),

                fabricante=str(
                    item.get("Manufacturer")
                    or "No disponible"
                ).strip(),

                numero_parte=str(
                    item.get("PartNumber")
                    or "No disponible"
                ).strip(),

                numero_serie=str(
                    item.get("SerialNumber")
                    or "No disponible"
                ).strip(),

                velocidad_mhz=convertir_entero(
                    item.get("Speed")
                ),

                velocidad_configurada_mhz=convertir_entero(
                    item.get("ConfiguredClockSpeed")
                ),

                tipo_memoria=traducir_tipo_memoria(
                    item.get("SMBIOSMemoryType")
                )
            )
        )

    return memoria


# ============================================================
# GPU
# ============================================================

def obtener_gpus() -> list[GPUInfo]:
    datos = ejecutar_powershell_json(
        """
        Get-CimInstance Win32_VideoController |
        ForEach-Object {
            [PSCustomObject]@{
                Name = $_.Name
                AdapterRAM = $_.AdapterRAM
                DriverVersion = $_.DriverVersion
                CurrentHorizontalResolution = $_.CurrentHorizontalResolution
                CurrentVerticalResolution = $_.CurrentVerticalResolution
                CurrentRefreshRate = $_.CurrentRefreshRate
                Status = $_.Status
            }
        }
        """
    )

    resultado = []

    for item in normalizar_json(datos):
        nombre = (
            item.get("Name")
            or "No disponible"
        )

        texto = nombre.lower()

        if any(
            x in texto
            for x in (
                "virtual",
                "parsec",
                "remote",
                "basic display"
            )
        ):
            tipo = "Virtual"

        else:
            tipo = "Fisica"

        horizontal = convertir_entero(
            item.get(
                "CurrentHorizontalResolution"
            )
        )

        vertical = convertir_entero(
            item.get(
                "CurrentVerticalResolution"
            )
        )

        if (
            horizontal is not None
            and vertical is not None
        ):
            resolucion = (
                f"{horizontal}x{vertical}"
            )

        else:
            resolucion = "No disponible"

        resultado.append(
            GPUInfo(
                nombre=nombre,

                memoria_bytes=convertir_entero(
                    item.get("AdapterRAM")
                ),

                driver=(
                    item.get("DriverVersion")
                    or "No disponible"
                ),

                resolucion=resolucion,

                frecuencia_refresco_hz=convertir_entero(
                    item.get("CurrentRefreshRate")
                ),

                estado=(
                    item.get("Status")
                    or "No disponible"
                ),

                tipo=tipo
            )
        )

    return resultado


# ============================================================
# MONITORES
# ============================================================

def obtener_monitores() -> list[MonitorInfo]:
    try:
        datos = ejecutar_powershell_json(
            r"""
            Get-CimInstance -Namespace root\wmi -ClassName WmiMonitorID -ErrorAction SilentlyContinue |
            ForEach-Object {

                $nombre = ""

                if ($_.UserFriendlyName) {
                    $nombre = (
                        [System.Text.Encoding]::ASCII.GetString(
                            [byte[]]$_.UserFriendlyName
                        )
                    ).Trim([char]0)
                }

                $fabricante = ""

                if ($_.ManufacturerName) {
                    $fabricante = (
                        [System.Text.Encoding]::ASCII.GetString(
                            [byte[]]$_.ManufacturerName
                        )
                    ).Trim([char]0)
                }

                [PSCustomObject]@{
                    Name = $nombre
                    Manufacturer = $fabricante
                    Active = $_.Active
                }
            }
            """
        )

    except Exception:
        return []

    resultado = []

    for item in normalizar_json(datos):
        resultado.append(
            MonitorInfo(
                nombre=(
                    item.get("Name")
                    or "No disponible"
                ),

                fabricante=(
                    item.get("Manufacturer")
                    or "No disponible"
                ),

                activo=bool_windows(
                    item.get("Active")
                )
            )
        )

    return resultado


# ============================================================
# DISCOS FISICOS
# ============================================================

def obtener_discos_fisicos() -> list[PhysicalDiskInfo]:
    try:
        datos = ejecutar_powershell_json(
            """
            Get-PhysicalDisk -ErrorAction SilentlyContinue |
            ForEach-Object {
                [PSCustomObject]@{
                    DeviceId = $_.DeviceId
                    FriendlyName = $_.FriendlyName
                    Model = $_.Model
                    SerialNumber = $_.SerialNumber
                    MediaType = $_.MediaType
                    BusType = $_.BusType
                    Size = $_.Size
                    HealthStatus = $_.HealthStatus
                    OperationalStatus = $_.OperationalStatus
                }
            }
            """
        )

    except Exception:
        return []

    resultado = []

    for item in normalizar_json(datos):
        operacional = item.get(
            "OperationalStatus"
        )

        if isinstance(
            operacional,
            list
        ):
            operacional = ", ".join(
                str(x)
                for x in operacional
            )

        resultado.append(
            PhysicalDiskInfo(
                numero=convertir_entero(
                    item.get("DeviceId")
                ),

                nombre=(
                    item.get("FriendlyName")
                    or "No disponible"
                ),

                modelo=(
                    item.get("Model")
                    or "No disponible"
                ),

                serial=str(
                    item.get("SerialNumber")
                    or "No disponible"
                ).strip(),

                tipo_medio=str(
                    item.get("MediaType")
                    or "No disponible"
                ),

                bus=str(
                    item.get("BusType")
                    or "No disponible"
                ),

                tamano_bytes=convertir_entero(
                    item.get("Size")
                ),

                estado_salud=str(
                    item.get("HealthStatus")
                    or "No disponible"
                ),

                estado_operacional=str(
                    operacional
                    or "No disponible"
                )
            )
        )

    return resultado

# ============================================================
# VOLUMENES
# ============================================================

def obtener_volumenes() -> list[VolumeInfo]:
    datos = ejecutar_powershell_json(
        """
        Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" |
        ForEach-Object {
            [PSCustomObject]@{
                DeviceID = $_.DeviceID
                VolumeName = $_.VolumeName
                FileSystem = $_.FileSystem
                Size = $_.Size
                FreeSpace = $_.FreeSpace
            }
        }
        """
    )

    resultado = []

    for item in normalizar_json(datos):
        total = convertir_entero(
            item.get("Size")
        )

        libre = convertir_entero(
            item.get("FreeSpace")
        )

        usado = (
            total - libre
            if total is not None
            and libre is not None
            else None
        )

        resultado.append(
            VolumeInfo(
                unidad=(
                    item.get("DeviceID")
                    or ""
                ),

                etiqueta=(
                    item.get("VolumeName")
                    or ""
                ),

                sistema_archivos=(
                    item.get("FileSystem")
                    or "No disponible"
                ),

                total_bytes=total,
                usado_bytes=usado,
                libre_bytes=libre,

                uso_porcentaje=calcular_porcentaje(
                    usado,
                    total
                )
            )
        )

    return resultado


# ============================================================
# VELOCIDAD DE RED
# ============================================================

def convertir_velocidad_mbps(valor) -> float | None:
    if valor is None:
        return None

    texto = str(
        valor
    ).strip().lower()

    try:
        numero = float(
            texto
            .split()[0]
            .replace(",", ".")
        )

        if "gbps" in texto:
            return numero * 1000

        if "mbps" in texto:
            return numero

        if "kbps" in texto:
            return numero / 1000

        if "bps" in texto:
            return numero / 1_000_000

    except Exception:
        return None

    return None


# ============================================================
# RED
# ============================================================

def obtener_adaptadores_red() -> list[NetworkAdapterInfo]:
    """
    Obtiene informacion de los adaptadores de red.

    La consulta evita depender de Get-NetIPConfiguration para todos
    los adaptadores, ya que algunas interfaces virtuales pueden tener
    indices inconsistentes o tardar demasiado en responder.
    """

    script = r"""
    $ErrorActionPreference = 'SilentlyContinue'

    $adaptadores = Get-NetAdapter -IncludeHidden -ErrorAction SilentlyContinue

    foreach ($adaptador in $adaptadores) {

        $indice = $adaptador.ifIndex

        $ipv4 = @(
            Get-NetIPAddress -InterfaceIndex $indice -AddressFamily IPv4 -ErrorAction SilentlyContinue |
            Where-Object {
                $_.IPAddress -and
                $_.IPAddress -ne "0.0.0.0"
            } |
            ForEach-Object {
                $_.IPAddress
            }
        )

        $ipv6 = @(
            Get-NetIPAddress -InterfaceIndex $indice -AddressFamily IPv6 -ErrorAction SilentlyContinue |
            Where-Object {
                $_.IPAddress -and
                $_.IPAddress -ne "::" -and
                $_.IPAddress -ne "::1"
            } |
            ForEach-Object {
                $_.IPAddress
            }
        )

        $gateway = @(
            Get-NetRoute -InterfaceIndex $indice -DestinationPrefix "0.0.0.0/0" -ErrorAction SilentlyContinue |
            Sort-Object RouteMetric |
            ForEach-Object {
                $_.NextHop
            }
        )

        $dns = @(
            Get-DnsClientServerAddress -InterfaceIndex $indice -AddressFamily IPv4 -ErrorAction SilentlyContinue |
            ForEach-Object {
                $_.ServerAddresses
            }
        )

        $ipif = Get-NetIPInterface -InterfaceIndex $indice -AddressFamily IPv4 -ErrorAction SilentlyContinue |
            Select-Object -First 1

        $dhcp = $null
        $mtu = $null
        $metrica = $null

        if ($null -ne $ipif) {
            $dhcp = $ipif.Dhcp.ToString()
            $mtu = $ipif.NlMtu
            $metrica = $ipif.InterfaceMetric
        }

        [PSCustomObject]@{
            Name = $adaptador.Name
            Description = $adaptador.InterfaceDescription
            Status = $adaptador.Status
            MAC = $adaptador.MacAddress
            LinkSpeed = $adaptador.LinkSpeed
            Physical = $adaptador.HardwareInterface

            IPv4 = @($ipv4)
            IPv6 = @($ipv6)
            Gateway = @($gateway)
            DNS = @($dns)

            DHCP = $dhcp
            MTU = $mtu
            Metric = $metrica
        }
    }
    """

    datos = ejecutar_powershell_json(
        script,
        timeout=15
    )

    resultado = []

    for item in normalizar_json(datos):
        nombre = (
            item.get("Name")
            or "No disponible"
        )

        descripcion = (
            item.get("Description")
            or "No disponible"
        )

        texto = (
            f"{nombre} {descripcion}"
        ).lower()

        if any(
            x in texto
            for x in (
                "wi-fi",
                "wifi",
                "wireless",
                "wlan",
                "802.11"
            )
        ):
            tipo = "Wi-Fi"

        elif "bluetooth" in texto:
            tipo = "Bluetooth"

        elif any(
            x in texto
            for x in (
                "virtual",
                "vpn",
                "hyper-v",
                "vmware",
                "virtualbox",
                "parsec",
                "tunnel",
                "teredo",
                "6to4",
                "isatap"
            )
        ):
            tipo = "Virtual"

        elif any(
            x in texto
            for x in (
                "ethernet",
                "gigabit",
                "realtek",
                "gbe"
            )
        ):
            tipo = "Ethernet"

        else:
            tipo = "Otro"

        resultado.append(
            NetworkAdapterInfo(
                nombre=nombre,
                descripcion=descripcion,
                tipo=tipo,

                estado=(
                    item.get("Status")
                    or "No disponible"
                ),

                mac=(
                    item.get("MAC")
                    or "No disponible"
                ),

                velocidad_mbps=convertir_velocidad_mbps(
                    item.get("LinkSpeed")
                ),

                mtu=convertir_entero(
                    item.get("MTU")
                ),

                metrica=convertir_entero(
                    item.get("Metric")
                ),

                ipv4=lista_segura(
                    item.get("IPv4")
                ),

                ipv6=lista_segura(
                    item.get("IPv6")
                ),

                gateway=lista_segura(
                    item.get("Gateway")
                ),

                dns=lista_segura(
                    item.get("DNS")
                ),

                dhcp=bool_windows(
                    item.get("DHCP")
                ),

                fisico=bool_windows(
                    item.get("Physical")
                )
            )
        )

    resultado.sort(
        key=lambda x: (
            0
            if str(x.estado).lower() == "up"
            else 1,

            0
            if x.ipv4
            else 1,

            0
            if x.fisico
            else 1,

            x.nombre.lower()
        )
    )

    return resultado


# ============================================================
# IP PRINCIPAL
# ============================================================

def obtener_ip_principal() -> str:
    sock = None

    try:
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        # UDP no necesita completar una conexion real.
        # Se utiliza para que Windows determine la interfaz
        # que emplearia para alcanzar una red externa.
        sock.connect(
            ("8.8.8.8", 80)
        )

        return sock.getsockname()[0]

    except Exception:
        try:
            return socket.gethostbyname(
                socket.gethostname()
            )

        except Exception:
            return "No disponible"

    finally:
        if sock is not None:
            sock.close()


# ============================================================
# SEGURIDAD
# ============================================================

def obtener_seguridad() -> SecurityInfo:
    seguridad = SecurityInfo()

    # --------------------------------------------------------
    # SECURE BOOT
    # --------------------------------------------------------

    try:
        salida = ejecutar_powershell(
            """
            try {
                $resultado = Confirm-SecureBootUEFI

                if ($resultado -eq $true) {
                    "TRUE"
                }
                elseif ($resultado -eq $false) {
                    "FALSE"
                }
                else {
                    "UNAVAILABLE"
                }
            }
            catch {
                "UNAVAILABLE"
            }
            """
        )

        texto = salida.strip().lower()

        if texto == "true":
            seguridad.secure_boot = True

        elif texto == "false":
            seguridad.secure_boot = False

        else:
            seguridad.secure_boot = None

    except Exception:
        seguridad.secure_boot = None

    # --------------------------------------------------------
    # TPM
    # --------------------------------------------------------

    try:
        datos = ejecutar_powershell_json(
            """
            $tpm = Get-Tpm -ErrorAction SilentlyContinue

            if ($null -ne $tpm) {

                [PSCustomObject]@{
                    Present = $tpm.TpmPresent
                    Ready = $tpm.TpmReady
                    Enabled = $tpm.TpmEnabled
                    Version = $tpm.ManufacturerVersion
                }
            }
            """
        )

        if datos:
            if isinstance(
                datos,
                list
            ):
                datos = datos[0]

            seguridad.tpm_presente = bool_windows(
                datos.get("Present")
            )

            seguridad.tpm_listo = bool_windows(
                datos.get("Ready")
            )

            seguridad.tpm_habilitado = bool_windows(
                datos.get("Enabled")
            )

            seguridad.tpm_version = str(
                datos.get("Version")
                or "No disponible"
            )

    except Exception:
        pass

    # --------------------------------------------------------
    # FIREWALL
    # --------------------------------------------------------

    try:
        datos = ejecutar_powershell_json(
            """
            Get-NetFirewallProfile -ErrorAction SilentlyContinue |
            ForEach-Object {

                [PSCustomObject]@{
                    Name = $_.Name
                    Enabled = $_.Enabled
                    DefaultInboundAction = $_.DefaultInboundAction
                    DefaultOutboundAction = $_.DefaultOutboundAction
                }
            }
            """
        )

        for item in normalizar_json(
            datos
        ):
            seguridad.firewall.append(
                FirewallProfileInfo(
                    nombre=str(
                        item.get("Name")
                        or "No disponible"
                    ),

                    habilitado=bool_windows(
                        item.get("Enabled")
                    ),

                    entrada_predeterminada=str(
                        item.get(
                            "DefaultInboundAction"
                        )
                        or "No disponible"
                    ),

                    salida_predeterminada=str(
                        item.get(
                            "DefaultOutboundAction"
                        )
                        or "No disponible"
                    )
                )
            )

    except Exception:
        pass

    # --------------------------------------------------------
    # MICROSOFT DEFENDER
    # --------------------------------------------------------

    try:
        datos = ejecutar_powershell_json(
            """
            $d = Get-MpComputerStatus -ErrorAction SilentlyContinue

            if ($null -ne $d) {

                [PSCustomObject]@{
                    AntivirusEnabled = $d.AntivirusEnabled
                    RealTime = $d.RealTimeProtectionEnabled
                }
            }
            """
        )

        if datos:
            if isinstance(
                datos,
                list
            ):
                datos = datos[0]

            seguridad.defender_disponible = True

            seguridad.defender_antivirus = bool_windows(
                datos.get("AntivirusEnabled")
            )

            seguridad.defender_tiempo_real = bool_windows(
                datos.get("RealTime")
            )

        else:
            seguridad.defender_disponible = None

    except Exception:
        seguridad.defender_disponible = None

    return seguridad


# ============================================================
# ENTORNO NETPRO
# ============================================================

def obtener_entorno() -> EnvironmentInfo:
    entorno = EnvironmentInfo()

    entorno.python_version = (
        platform.python_version()
    )

    entorno.python_executable = (
        sys.executable
    )

    virtual_env = os.environ.get(
        "VIRTUAL_ENV"
    )

    entorno.entorno_virtual = bool(
        virtual_env
        or sys.prefix
        != getattr(
            sys,
            "base_prefix",
            sys.prefix
        )
    )

    if virtual_env:
        entorno.virtual_env = (
            virtual_env
        )

    elif entorno.entorno_virtual:
        entorno.virtual_env = (
            sys.prefix
        )

    entorno.powershell_disponible = (
        shutil.which(
            "powershell.exe"
        )
        is not None
    )

    # --------------------------------------------------------
    # OLLAMA
    # --------------------------------------------------------

    try:
        resultado = subprocess.run(
            [
                "ollama",
                "--version"
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=4,
            creationflags=(
                subprocess.CREATE_NO_WINDOW
                if os.name == "nt"
                else 0
            )
        )

        if resultado.returncode == 0:
            entorno.ollama_disponible = True

            entorno.ollama_version = (
                resultado.stdout.strip()
                or resultado.stderr.strip()
                or "Disponible"
            )

    except Exception:
        pass

    # --------------------------------------------------------
    # MODELOS OLLAMA
    # --------------------------------------------------------

    if entorno.ollama_disponible:
        try:
            resultado = subprocess.run(
                [
                    "ollama",
                    "list"
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=5,
                creationflags=(
                    subprocess.CREATE_NO_WINDOW
                    if os.name == "nt"
                    else 0
                )
            )

            if resultado.returncode == 0:
                lineas = (
                    resultado.stdout
                    .splitlines()
                )

                for linea in lineas[1:]:
                    partes = linea.split()

                    if partes:
                        entorno.modelos_ollama.append(
                            partes[0]
                        )

        except Exception:
            pass

    return entorno


# ============================================================
# PROCESOS
# ============================================================

def obtener_procesos_totales() -> int | None:
    try:
        salida = ejecutar_powershell(
            """
            (Get-Process -ErrorAction SilentlyContinue).Count
            """
        )

        return int(
            salida.strip()
        )

    except Exception:
        return None


# ============================================================
# RECOLECTOR PRINCIPAL
# ============================================================

def obtener_informacion_sistema() -> SistemaInfo:
    sistema = SistemaInfo()

    sistema.fecha_consulta = (
        datetime.now()
        .astimezone()
        .isoformat(
            timespec="seconds"
        )
    )

    sistema.nombre_equipo = (
        platform.node()
        or "No disponible"
    )

    sistema.hostname = (
        socket.gethostname()
        or "No disponible"
    )

    sistema.usuario = (
        getpass.getuser()
        or "No disponible"
    )

    sistema.arquitectura = (
        platform.machine()
        or "No disponible"
    )

    sistema.sistema_operativo = (
        platform.system()
        or "No disponible"
    )

    recolectores = [
        (
            "Windows",
            lambda: obtener_windows(
                sistema
            )
        ),

        (
            "Placa base",
            lambda: setattr(
                sistema,
                "placa_base",
                obtener_placa_base()
            )
        ),

        (
            "BIOS",
            lambda: setattr(
                sistema,
                "bios",
                obtener_bios()
            )
        ),

        (
            "CPU",
            lambda: setattr(
                sistema,
                "cpu",
                obtener_cpu()
            )
        ),

        (
            "Memoria",
            lambda: setattr(
                sistema,
                "memoria",
                obtener_memoria()
            )
        ),

        (
            "GPU",
            lambda: setattr(
                sistema,
                "gpus",
                obtener_gpus()
            )
        ),

        (
            "Monitores",
            lambda: setattr(
                sistema,
                "monitores",
                obtener_monitores()
            )
        ),

        (
            "Discos fisicos",
            lambda: setattr(
                sistema,
                "discos_fisicos",
                obtener_discos_fisicos()
            )
        ),

        (
            "Volumenes",
            lambda: setattr(
                sistema,
                "volumenes",
                obtener_volumenes()
            )
        ),

        (
            "Adaptadores de red",
            lambda: setattr(
                sistema,
                "adaptadores_red",
                obtener_adaptadores_red()
            )
        ),

        (
            "Seguridad",
            lambda: setattr(
                sistema,
                "seguridad",
                obtener_seguridad()
            )
        ),

        (
            "Entorno",
            lambda: setattr(
                sistema,
                "entorno",
                obtener_entorno()
            )
        )
    ]

    for nombre, funcion in recolectores:
        try:
            funcion()

        except subprocess.TimeoutExpired:
            sistema.errores.append(
                f"{nombre}: tiempo de espera agotado."
            )

        except Exception as error:
            sistema.errores.append(
                f"{nombre}: {error}"
            )

    try:
        sistema.ip_local_principal = (
            obtener_ip_principal()
        )

    except Exception as error:
        sistema.errores.append(
            f"IP principal: {error}"
        )

    sistema.procesos_totales = (
        obtener_procesos_totales()
    )

    return sistema


# ============================================================
# CONVERSION A DICCIONARIO
# ============================================================

def sistema_a_dict(
    sistema: SistemaInfo
) -> dict:
    return asdict(
        sistema
    )


# ============================================================
# UPTIME
# ============================================================

def uptime_legible(
    segundos
) -> str:
    if segundos is None:
        return "No disponible"

    segundos = int(
        max(
            0,
            segundos
        )
    )

    dias, resto = divmod(
        segundos,
        86400
    )

    horas, resto = divmod(
        resto,
        3600
    )

    minutos, segundos_restantes = divmod(
        resto,
        60
    )

    partes = []

    if dias:
        partes.append(
            f"{dias} d"
        )

    if horas:
        partes.append(
            f"{horas} h"
        )

    if minutos:
        partes.append(
            f"{minutos} min"
        )

    if not partes:
        partes.append(
            f"{segundos_restantes} s"
        )

    return " ".join(
        partes
    )


# ============================================================
# FORMATO BOOLEANO
# ============================================================

def bool_legible(
    valor: bool | None
) -> str:
    if valor is True:
        return "Si"

    if valor is False:
        return "No"

    return "No disponible"


# ============================================================
# FORMATO NUMERICO
# ============================================================

def numero_legible(
    valor,
    sufijo=""
) -> str:
    if valor is None:
        return "No disponible"

    return (
        f"{valor}{sufijo}"
    )


# ============================================================
# ADAPTADOR PRINCIPAL
# ============================================================

def obtener_adaptador_principal(
    sistema: SistemaInfo
) -> NetworkAdapterInfo | None:
    """
    Intenta seleccionar la interfaz mas representativa de
    la conectividad principal del equipo.
    """

    if not sistema.adaptadores_red:
        return None

    # Primero: adaptador activo que contiene la IP principal.
    for adaptador in sistema.adaptadores_red:
        if (
            sistema.ip_local_principal
            in adaptador.ipv4
        ):
            return adaptador

    # Segundo: adaptador fisico activo con IPv4.
    for adaptador in sistema.adaptadores_red:
        if (
            str(
                adaptador.estado
            ).lower()
            == "up"
            and adaptador.fisico is True
            and adaptador.ipv4
        ):
            return adaptador

    # Tercero: cualquier adaptador activo con IPv4.
    for adaptador in sistema.adaptadores_red:
        if (
            str(
                adaptador.estado
            ).lower()
            == "up"
            and adaptador.ipv4
        ):
            return adaptador

    return sistema.adaptadores_red[0]


# ============================================================
# RESUMEN DEL SISTEMA
# ============================================================

def generar_resumen_sistema(
    sistema: SistemaInfo
) -> str:
    """
    Genera un resumen breve para que la interfaz de NetPro
    pueda mostrar los datos principales sin imprimir toda
    la informacion tecnica.
    """

    lineas = []

    lineas.append(
        f"Equipo: {sistema.nombre_equipo}"
    )

    lineas.append(
        f"Sistema: {sistema.sistema_operativo}"
    )

    lineas.append(
        f"CPU: {sistema.cpu.nombre}"
    )

    lineas.append(
        "RAM: "
        + bytes_legibles(
            sistema.memoria.total_bytes
        )
    )

    if sistema.gpus:
        gpu_fisica = next(
            (
                gpu
                for gpu in sistema.gpus
                if gpu.tipo == "Fisica"
            ),
            sistema.gpus[0]
        )

        lineas.append(
            f"GPU: {gpu_fisica.nombre}"
        )

    lineas.append(
        f"IP principal: {sistema.ip_local_principal}"
    )

    principal = obtener_adaptador_principal(
        sistema
    )

    if principal is not None:
        lineas.append(
            f"Red: {principal.nombre}"
        )

    lineas.append(
        "Ollama: "
        + (
            "Disponible"
            if sistema.entorno.ollama_disponible
            else "No disponible"
        )
    )

    return "\n".join(
        lineas
    )


# ============================================================
# DETECCION DE VOLUMENES CON POCO ESPACIO
# ============================================================

def obtener_volumenes_con_poco_espacio(
    sistema: SistemaInfo,
    limite_porcentaje: float = 90.0
) -> list[VolumeInfo]:
    resultado = []

    for volumen in sistema.volumenes:
        if (
            volumen.uso_porcentaje
            is not None
            and volumen.uso_porcentaje
            >= limite_porcentaje
        ):
            resultado.append(
                volumen
            )

    return resultado


# ============================================================
# DETECCION DE ADAPTADORES ACTIVOS
# ============================================================

def obtener_adaptadores_activos(
    sistema: SistemaInfo
) -> list[NetworkAdapterInfo]:
    return [
        adaptador
        for adaptador
        in sistema.adaptadores_red
        if str(
            adaptador.estado
        ).lower()
        == "up"
    ]


# ============================================================
# DETECCION DE GPU FISICA
# ============================================================

def obtener_gpu_principal(
    sistema: SistemaInfo
) -> GPUInfo | None:
    if not sistema.gpus:
        return None

    for gpu in sistema.gpus:
        if gpu.tipo == "Fisica":
            return gpu

    return sistema.gpus[0]


# ============================================================
# INFORMACION PARA LA INTERFAZ
# ============================================================

def generar_datos_interfaz(
    sistema: SistemaInfo
) -> dict:
    """
    Prepara informacion simplificada para ui/system_page.py.
    No reemplaza los datos completos del Core.
    """

    adaptador = obtener_adaptador_principal(
        sistema
    )

    gpu = obtener_gpu_principal(
        sistema
    )

    volumenes_alerta = (
        obtener_volumenes_con_poco_espacio(
            sistema
        )
    )

    return {
        "equipo": sistema.nombre_equipo,

        "usuario": sistema.usuario,

        "sistema_operativo": (
            sistema.sistema_operativo
        ),

        "version": (
            sistema.version_sistema
        ),

        "build": (
            sistema.build
        ),

        "arquitectura": (
            sistema.arquitectura
        ),

        "cpu": (
            sistema.cpu.nombre
        ),

        "nucleos": (
            sistema.cpu.nucleos_fisicos
        ),

        "logicos": (
            sistema.cpu.procesadores_logicos
        ),

        "ram_total": bytes_legibles(
            sistema.memoria.total_bytes
        ),

        "ram_usada": bytes_legibles(
            sistema.memoria.usada_bytes
        ),

        "ram_disponible": bytes_legibles(
            sistema.memoria.disponible_bytes
        ),

        "ram_porcentaje": (
            sistema.memoria.uso_porcentaje
        ),

        "gpu": (
            gpu.nombre
            if gpu
            else "No disponible"
        ),

        "gpu_vram": (
            bytes_legibles(
                gpu.memoria_bytes
            )
            if gpu
            else "No disponible"
        ),

        "ip_principal": (
            sistema.ip_local_principal
        ),

        "adaptador_principal": (
            adaptador.nombre
            if adaptador
            else "No disponible"
        ),

        "gateway": (
            adaptador.gateway[0]
            if adaptador
            and adaptador.gateway
            else "No disponible"
        ),

        "dns": (
            adaptador.dns
            if adaptador
            else []
        ),

        "velocidad_red_mbps": (
            adaptador.velocidad_mbps
            if adaptador
            else None
        ),

        "defender": (
            sistema.seguridad.defender_antivirus
        ),

        "defender_tiempo_real": (
            sistema.seguridad.defender_tiempo_real
        ),

        "secure_boot": (
            sistema.seguridad.secure_boot
        ),

        "ollama": (
            sistema.entorno.ollama_disponible
        ),

        "modelos_ollama": (
            sistema.entorno.modelos_ollama
        ),

        "volumenes_alerta": [
            {
                "unidad": volumen.unidad,
                "uso": volumen.uso_porcentaje,
                "libre": bytes_legibles(
                    volumen.libre_bytes
                )
            }
            for volumen
            in volumenes_alerta
        ],

        "errores": list(
            sistema.errores
        )
    }

# ============================================================
# IMPRESION DEL RESULTADO
# ============================================================

def imprimir_resultado(s: SistemaInfo):
    ancho = 78

    print()
    print("=" * ancho)
    print("NETPRO - INFORMACION AVANZADA DEL SISTEMA")
    print("=" * ancho)

    # ========================================================
    # SISTEMA
    # ========================================================

    print("\nSISTEMA")
    print("-" * ancho)

    print(
        f"Equipo:              "
        f"{s.nombre_equipo}"
    )

    print(
        f"Usuario:             "
        f"{s.usuario}"
    )

    print(
        f"Sistema operativo:   "
        f"{s.sistema_operativo}"
    )

    print(
        f"Version:             "
        f"{s.version_sistema}"
    )

    print(
        f"Build:               "
        f"{s.build}"
    )

    print(
        f"Arquitectura:        "
        f"{s.arquitectura}"
    )

    print(
        f"Fabricante:          "
        f"{s.fabricante_equipo}"
    )

    print(
        f"Modelo:              "
        f"{s.modelo_equipo}"
    )

    print(
        f"Zona horaria:        "
        f"{s.zona_horaria}"
    )

    print(
        f"Instalacion Windows: "
        f"{s.fecha_instalacion_windows}"
    )

    print(
        f"Ultimo arranque:     "
        f"{s.ultimo_arranque}"
    )

    print(
        f"Tiempo encendido:    "
        f"{uptime_legible(s.uptime_segundos)}"
    )

    print(
        f"Procesos:            "
        f"{numero_legible(s.procesos_totales)}"
    )

    # ========================================================
    # PLACA BASE
    # ========================================================

    print("\nPLACA BASE")
    print("-" * ancho)

    print(
        f"Fabricante:          "
        f"{s.placa_base.fabricante}"
    )

    print(
        f"Producto:            "
        f"{s.placa_base.producto}"
    )

    print(
        f"Version:             "
        f"{s.placa_base.version}"
    )

    print(
        f"Serial:              "
        f"{s.placa_base.serial}"
    )

    # ========================================================
    # BIOS
    # ========================================================

    print("\nBIOS / FIRMWARE")
    print("-" * ancho)

    print(
        f"Fabricante:          "
        f"{s.bios.fabricante}"
    )

    print(
        f"Version:             "
        f"{s.bios.version}"
    )

    print(
        f"Fecha:               "
        f"{s.bios.fecha}"
    )

    print(
        f"Serial:              "
        f"{s.bios.serial}"
    )

    print(
        f"Modo firmware:       "
        f"{s.bios.modo_firmware}"
    )

    # ========================================================
    # CPU
    # ========================================================

    print("\nCPU")
    print("-" * ancho)

    print(
        f"Modelo:              "
        f"{s.cpu.nombre}"
    )

    print(
        f"Fabricante:          "
        f"{s.cpu.fabricante}"
    )

    print(
        f"Socket:              "
        f"{s.cpu.socket}"
    )

    print(
        f"Nucleos fisicos:     "
        f"{numero_legible(s.cpu.nucleos_fisicos)}"
    )

    print(
        f"Logicos:             "
        f"{numero_legible(s.cpu.procesadores_logicos)}"
    )

    print(
        f"Frecuencia actual:   "
        f"{numero_legible(s.cpu.frecuencia_actual_mhz, ' MHz')}"
    )

    print(
        f"Frecuencia maxima:   "
        f"{numero_legible(s.cpu.frecuencia_max_mhz, ' MHz')}"
    )

    print(
        f"Carga actual:        "
        f"{numero_legible(s.cpu.carga_porcentaje, '%')}"
    )

    print(
        f"Virtualizacion FW:   "
        f"{bool_legible(s.cpu.virtualizacion_firmware)}"
    )

    print(
        f"Arquitectura CPU:    "
        f"{s.cpu.arquitectura}"
    )

    # ========================================================
    # MEMORIA RAM
    # ========================================================

    print("\nMEMORIA RAM")
    print("-" * ancho)

    print(
        f"Total:               "
        f"{bytes_legibles(s.memoria.total_bytes)}"
    )

    print(
        f"Usada:               "
        f"{bytes_legibles(s.memoria.usada_bytes)}"
    )

    print(
        f"Disponible:          "
        f"{bytes_legibles(s.memoria.disponible_bytes)}"
    )

    print(
        f"Uso:                 "
        f"{numero_legible(s.memoria.uso_porcentaje, '%')}"
    )

    print("\nMODULOS RAM")
    print("-" * ancho)

    if not s.memoria.modulos:
        print(
            "No se obtuvo informacion "
            "de los modulos fisicos."
        )

    for indice, modulo in enumerate(
        s.memoria.modulos,
        start=1
    ):
        print()

        print(
            f"[{indice}] "
            f"{modulo.dispositivo}"
        )

        print(
            f"    Banco:               "
            f"{modulo.banco}"
        )

        print(
            f"    Capacidad:           "
            f"{bytes_legibles(modulo.capacidad_bytes)}"
        )

        print(
            f"    Fabricante:          "
            f"{modulo.fabricante}"
        )

        print(
            f"    Part Number:         "
            f"{modulo.numero_parte}"
        )

        print(
            f"    Numero de serie:     "
            f"{modulo.numero_serie}"
        )

        print(
            f"    Velocidad:           "
            f"{numero_legible(modulo.velocidad_mhz, ' MHz')}"
        )

        print(
            f"    Configurada:         "
            f"{numero_legible(modulo.velocidad_configurada_mhz, ' MHz')}"
        )

        print(
            f"    Tipo:                "
            f"{modulo.tipo_memoria}"
        )

    # ========================================================
    # GPU
    # ========================================================

    print("\nGPU")
    print("-" * ancho)

    if not s.gpus:
        print(
            "No se obtuvo informacion "
            "de adaptadores graficos."
        )

    for indice, gpu in enumerate(
        s.gpus,
        start=1
    ):
        print()

        print(
            f"[{indice}] "
            f"{gpu.nombre}"
        )

        print(
            f"    Tipo:                "
            f"{gpu.tipo}"
        )

        print(
            f"    VRAM reportada:      "
            f"{bytes_legibles(gpu.memoria_bytes)}"
        )

        print(
            f"    Driver:              "
            f"{gpu.driver}"
        )

        print(
            f"    Resolucion:          "
            f"{gpu.resolucion}"
        )

        print(
            f"    Refresco:            "
            f"{numero_legible(gpu.frecuencia_refresco_hz, ' Hz')}"
        )

        print(
            f"    Estado:              "
            f"{gpu.estado}"
        )

    # ========================================================
    # MONITORES
    # ========================================================

    print("\nMONITORES")
    print("-" * ancho)

    if not s.monitores:
        print(
            "No se obtuvo informacion "
            "de monitores."
        )

    for indice, monitor in enumerate(
        s.monitores,
        start=1
    ):
        print(
            f"[{indice}] "
            f"{monitor.fabricante} "
            f"{monitor.nombre}"
        )

        print(
            f"    Activo: "
            f"{bool_legible(monitor.activo)}"
        )

    # ========================================================
    # DISCOS FISICOS
    # ========================================================

    print("\nDISCOS FISICOS")
    print("-" * ancho)

    if not s.discos_fisicos:
        print(
            "No se obtuvo informacion "
            "de discos fisicos."
        )

    for disco in s.discos_fisicos:
        print()

        numero_disco = (
            disco.numero
            if disco.numero is not None
            else "?"
        )

        print(
            f"Disco {numero_disco}"
        )

        print(
            f"    Nombre:              "
            f"{disco.nombre}"
        )

        print(
            f"    Modelo:              "
            f"{disco.modelo}"
        )

        print(
            f"    Serial:              "
            f"{disco.serial}"
        )

        print(
            f"    Tipo:                "
            f"{disco.tipo_medio}"
        )

        print(
            f"    Bus:                 "
            f"{disco.bus}"
        )

        print(
            f"    Tamano:              "
            f"{bytes_legibles(disco.tamano_bytes)}"
        )

        print(
            f"    Salud reportada:     "
            f"{disco.estado_salud}"
        )

        print(
            f"    Estado operacional: "
            f"{disco.estado_operacional}"
        )

    # ========================================================
    # VOLUMENES
    # ========================================================

    print("\nVOLUMENES")
    print("-" * ancho)

    if not s.volumenes:
        print(
            "No se obtuvo informacion "
            "de volumenes."
        )

    for volumen in s.volumenes:
        print()

        etiqueta = (
            volumen.etiqueta
            if volumen.etiqueta
            else "Sin etiqueta"
        )

        print(
            f"{volumen.unidad} "
            f"{etiqueta}"
        )

        print(
            f"    Sistema de archivos: "
            f"{volumen.sistema_archivos}"
        )

        print(
            f"    Total:               "
            f"{bytes_legibles(volumen.total_bytes)}"
        )

        print(
            f"    Usado:               "
            f"{bytes_legibles(volumen.usado_bytes)}"
        )

        print(
            f"    Libre:               "
            f"{bytes_legibles(volumen.libre_bytes)}"
        )

        print(
            f"    Uso:                 "
            f"{numero_legible(volumen.uso_porcentaje, '%')}"
        )

    # ========================================================
    # RED
    # ========================================================

    print("\nRED")
    print("-" * ancho)

    print(
        f"Hostname:            "
        f"{s.hostname}"
    )

    print(
        f"IP principal:        "
        f"{s.ip_local_principal}"
    )

    principal = obtener_adaptador_principal(
        s
    )

    if principal is not None:
        print(
            f"Adaptador principal: "
            f"{principal.nombre}"
        )

    if not s.adaptadores_red:
        print()
        print(
            "No se obtuvo informacion "
            "de adaptadores de red."
        )

    for indice, red in enumerate(
        s.adaptadores_red,
        start=1
    ):
        print()

        print(
            f"[{indice}] "
            f"{red.nombre}"
        )

        print(
            f"    Descripcion:         "
            f"{red.descripcion}"
        )

        print(
            f"    Tipo:                "
            f"{red.tipo}"
        )

        print(
            f"    Estado:              "
            f"{red.estado}"
        )

        print(
            f"    Fisico:              "
            f"{bool_legible(red.fisico)}"
        )

        print(
            f"    MAC:                 "
            f"{red.mac}"
        )

        print(
            f"    Velocidad:           "
            f"{numero_legible(red.velocidad_mbps, ' Mbps')}"
        )

        print(
            f"    MTU:                 "
            f"{numero_legible(red.mtu)}"
        )

        print(
            f"    Metrica:             "
            f"{numero_legible(red.metrica)}"
        )

        print(
            f"    IPv4:                "
            f"{', '.join(red.ipv4) if red.ipv4 else 'No disponible'}"
        )

        print(
            f"    IPv6:                "
            f"{', '.join(red.ipv6) if red.ipv6 else 'No disponible'}"
        )

        print(
            f"    Gateway:             "
            f"{', '.join(red.gateway) if red.gateway else 'No disponible'}"
        )

        print(
            f"    DNS:                 "
            f"{', '.join(red.dns) if red.dns else 'No disponible'}"
        )

        print(
            f"    DHCP:                "
            f"{bool_legible(red.dhcp)}"
        )

    # ========================================================
    # SEGURIDAD DE WINDOWS
    # ========================================================

    print("\nSEGURIDAD DE WINDOWS")
    print("-" * ancho)

    print(
        f"Secure Boot:             "
        f"{bool_legible(s.seguridad.secure_boot)}"
    )

    print(
        f"TPM presente:            "
        f"{bool_legible(s.seguridad.tpm_presente)}"
    )

    print(
        f"TPM listo:               "
        f"{bool_legible(s.seguridad.tpm_listo)}"
    )

    print(
        f"TPM habilitado:          "
        f"{bool_legible(s.seguridad.tpm_habilitado)}"
    )

    print(
        f"TPM version:             "
        f"{s.seguridad.tpm_version}"
    )

    print(
        f"Defender disponible:     "
        f"{bool_legible(s.seguridad.defender_disponible)}"
    )

    print(
        f"Antivirus:               "
        f"{bool_legible(s.seguridad.defender_antivirus)}"
    )

    print(
        f"Proteccion tiempo real:  "
        f"{bool_legible(s.seguridad.defender_tiempo_real)}"
    )

    # ========================================================
    # FIREWALL
    # ========================================================

    print("\nFIREWALL")
    print("-" * ancho)

    if not s.seguridad.firewall:
        print(
            "No se obtuvo informacion "
            "de los perfiles del firewall."
        )

    for perfil in s.seguridad.firewall:
        print()

        print(
            f"Perfil:              "
            f"{perfil.nombre}"
        )

        print(
            f"    Habilitado:          "
            f"{bool_legible(perfil.habilitado)}"
        )

        print(
            f"    Entrada:             "
            f"{perfil.entrada_predeterminada}"
        )

        print(
            f"    Salida:              "
            f"{perfil.salida_predeterminada}"
        )

    # ========================================================
    # ENTORNO NETPRO
    # ========================================================

    print("\nENTORNO NETPRO")
    print("-" * ancho)

    print(
        f"Python:              "
        f"{s.entorno.python_version}"
    )

    print(
        f"Ejecutable:          "
        f"{s.entorno.python_executable}"
    )

    print(
        f"Entorno virtual:     "
        f"{bool_legible(s.entorno.entorno_virtual)}"
    )

    print(
        f"VENV:                "
        f"{s.entorno.virtual_env}"
    )

    print(
        f"PowerShell:          "
        f"{bool_legible(s.entorno.powershell_disponible)}"
    )

    print(
        f"Ollama:              "
        f"{bool_legible(s.entorno.ollama_disponible)}"
    )

    print(
        f"Ollama version:      "
        f"{s.entorno.ollama_version}"
    )

    if s.entorno.modelos_ollama:
        print(
            "Modelos Ollama:"
        )

        for modelo in (
            s.entorno.modelos_ollama
        ):
            print(
                f"    - {modelo}"
            )

    else:
        print(
            "Modelos Ollama:      "
            "No disponibles"
        )

    # ========================================================
    # RESUMEN DE ALERTAS INFORMATIVAS
    # ========================================================

    print("\nRESUMEN")
    print("-" * ancho)

    volumenes_llenos = (
        obtener_volumenes_con_poco_espacio(
            s
        )
    )

    if volumenes_llenos:
        print(
            "Volumenes con uso igual "
            "o superior al 90%:"
        )

        for volumen in volumenes_llenos:
            print(
                f"    - {volumen.unidad}: "
                f"{volumen.uso_porcentaje}% usado, "
                f"{bytes_legibles(volumen.libre_bytes)} libres"
            )

    else:
        print(
            "No se observaron volumenes "
            "con uso igual o superior al 90%."
        )

    adaptadores_activos = (
        obtener_adaptadores_activos(
            s
        )
    )

    print(
        f"Adaptadores activos: "
        f"{len(adaptadores_activos)}"
    )

    print(
        f"Adaptadores detectados: "
        f"{len(s.adaptadores_red)}"
    )

    print(
        f"GPU detectadas: "
        f"{len(s.gpus)}"
    )

    print(
        f"Discos fisicos detectados: "
        f"{len(s.discos_fisicos)}"
    )

    print(
        f"Volumenes detectados: "
        f"{len(s.volumenes)}"
    )

    # ========================================================
    # ADVERTENCIAS
    # ========================================================

    if s.errores:
        print(
            "\nDATOS NO DISPONIBLES / ADVERTENCIAS"
        )

        print(
            "-" * ancho
        )

        for error in s.errores:
            print(
                f"- {error}"
            )

    # ========================================================
    # FINAL
    # ========================================================

    print()
    print("=" * ancho)
    print("FIN DEL ANALISIS")
    print("=" * ancho)


# ============================================================
# EXPORTACION JSON
# ============================================================

def exportar_json(
    sistema: SistemaInfo,
    ruta: str
) -> bool:
    """
    Guarda la informacion recopilada en formato JSON.
    """

    try:
        datos = sistema_a_dict(
            sistema
        )

        with open(
            ruta,
            "w",
            encoding="utf-8"
        ) as archivo:
            json.dump(
                datos,
                archivo,
                ensure_ascii=False,
                indent=4
            )

        return True

    except Exception:
        return False


# ============================================================
# TEXTO PARA NETPRO AI
# ============================================================

def generar_contexto_ia(
    sistema: SistemaInfo
) -> str:
    """
    Genera un contexto compacto y estructurado para que
    NetPro AI pueda interpretar la informacion del sistema.

    La IA debe interpretar estos datos como resultados
    obtenidos por el Core de NetPro.
    """

    lineas = []

    lineas.append(
        "RESULTADO DE NETPRO - MI SISTEMA"
    )

    lineas.append(
        ""
    )

    lineas.append(
        "SISTEMA"
    )

    lineas.append(
        f"Equipo: {sistema.nombre_equipo}"
    )

    lineas.append(
        f"Sistema operativo: {sistema.sistema_operativo}"
    )

    lineas.append(
        f"Version: {sistema.version_sistema}"
    )

    lineas.append(
        f"Build: {sistema.build}"
    )

    lineas.append(
        f"Arquitectura: {sistema.arquitectura}"
    )

    lineas.append(
        ""
    )

    lineas.append(
        "CPU"
    )

    lineas.append(
        f"Modelo: {sistema.cpu.nombre}"
    )

    lineas.append(
        f"Nucleos fisicos: {sistema.cpu.nucleos_fisicos}"
    )

    lineas.append(
        f"Procesadores logicos: {sistema.cpu.procesadores_logicos}"
    )

    lineas.append(
        f"Frecuencia maxima MHz: {sistema.cpu.frecuencia_max_mhz}"
    )

    lineas.append(
        f"Carga actual: {sistema.cpu.carga_porcentaje}"
    )

    lineas.append(
        ""
    )

    lineas.append(
        "MEMORIA"
    )

    lineas.append(
        f"Total: {bytes_legibles(sistema.memoria.total_bytes)}"
    )

    lineas.append(
        f"Usada: {bytes_legibles(sistema.memoria.usada_bytes)}"
    )

    lineas.append(
        f"Disponible: {bytes_legibles(sistema.memoria.disponible_bytes)}"
    )

    lineas.append(
        f"Uso porcentaje: {sistema.memoria.uso_porcentaje}"
    )

    if sistema.memoria.modulos:
        lineas.append(
            "Modulos:"
        )

        for modulo in (
            sistema.memoria.modulos
        ):
            lineas.append(
                "- "
                f"{modulo.capacidad_bytes} bytes, "
                f"{modulo.tipo_memoria}, "
                f"{modulo.velocidad_configurada_mhz} MHz"
            )

    lineas.append(
        ""
    )

    lineas.append(
        "GPU"
    )

    for gpu in sistema.gpus:
        lineas.append(
            "- "
            f"{gpu.nombre}; "
            f"tipo={gpu.tipo}; "
            f"VRAM={bytes_legibles(gpu.memoria_bytes)}; "
            f"resolucion={gpu.resolucion}; "
            f"estado={gpu.estado}"
        )

    lineas.append(
        ""
    )

    lineas.append(
        "ALMACENAMIENTO"
    )

    for disco in (
        sistema.discos_fisicos
    ):
        lineas.append(
            "- Disco fisico: "
            f"{disco.nombre}; "
            f"tamano={bytes_legibles(disco.tamano_bytes)}; "
            f"tipo={disco.tipo_medio}; "
            f"salud={disco.estado_salud}"
        )

    for volumen in (
        sistema.volumenes
    ):
        lineas.append(
            "- Volumen "
            f"{volumen.unidad}; "
            f"total={bytes_legibles(volumen.total_bytes)}; "
            f"libre={bytes_legibles(volumen.libre_bytes)}; "
            f"uso={volumen.uso_porcentaje}%"
        )

    lineas.append(
        ""
    )

    lineas.append(
        "RED"
    )

    lineas.append(
        f"IP principal: {sistema.ip_local_principal}"
    )

    adaptador = (
        obtener_adaptador_principal(
            sistema
        )
    )

    if adaptador:
        lineas.append(
            f"Adaptador principal: {adaptador.nombre}"
        )

        lineas.append(
            f"Tipo: {adaptador.tipo}"
        )

        lineas.append(
            f"Estado: {adaptador.estado}"
        )

        lineas.append(
            f"IPv4: {', '.join(adaptador.ipv4)}"
        )

        lineas.append(
            f"Gateway: {', '.join(adaptador.gateway)}"
        )

        lineas.append(
            f"DNS: {', '.join(adaptador.dns)}"
        )

        lineas.append(
            f"Velocidad Mbps: {adaptador.velocidad_mbps}"
        )

    lineas.append(
        ""
    )

    lineas.append(
        "SEGURIDAD"
    )

    lineas.append(
        f"Secure Boot: {sistema.seguridad.secure_boot}"
    )

    lineas.append(
        f"TPM presente: {sistema.seguridad.tpm_presente}"
    )

    lineas.append(
        f"Defender antivirus: {sistema.seguridad.defender_antivirus}"
    )

    lineas.append(
        "Defender tiempo real: "
        f"{sistema.seguridad.defender_tiempo_real}"
    )

    for perfil in (
        sistema.seguridad.firewall
    ):
        lineas.append(
            "- Firewall "
            f"{perfil.nombre}: "
            f"habilitado={perfil.habilitado}"
        )

    lineas.append(
        ""
    )

    lineas.append(
        "ENTORNO NETPRO"
    )

    lineas.append(
        f"Python: {sistema.entorno.python_version}"
    )

    lineas.append(
        f"Entorno virtual: {sistema.entorno.entorno_virtual}"
    )

    lineas.append(
        f"Ollama disponible: {sistema.entorno.ollama_disponible}"
    )

    lineas.append(
        "Modelos Ollama: "
        + (
            ", ".join(
                sistema.entorno.modelos_ollama
            )
            if sistema.entorno.modelos_ollama
            else "Ninguno detectado"
        )
    )

    if sistema.errores:
        lineas.append(
            ""
        )

        lineas.append(
            "DATOS NO DISPONIBLES"
        )

        for error in (
            sistema.errores
        ):
            lineas.append(
                f"- {error}"
            )

    return "\n".join(
        lineas
    )

    # ============================================================
# INFORME SIMPLE PARA LA GUI
# ============================================================

def generar_informe_gui(
    sistema: SistemaInfo
) -> str:
    """
    Genera un informe legible para mostrar dentro de
    la interfaz grafica de NetPro.
    """

    lineas = []

    lineas.append(
        "INFORMACION DEL SISTEMA"
    )

    lineas.append(
        "-" * 60
    )

    lineas.append(
        f"Equipo: {sistema.nombre_equipo}"
    )

    lineas.append(
        f"Usuario: {sistema.usuario}"
    )

    lineas.append(
        f"Sistema operativo: {sistema.sistema_operativo}"
    )

    lineas.append(
        f"Version: {sistema.version_sistema}"
    )

    lineas.append(
        f"Build: {sistema.build}"
    )

    lineas.append(
        f"Arquitectura: {sistema.arquitectura}"
    )

    lineas.append(
        ""
    )

    # ========================================================
    # HARDWARE
    # ========================================================

    lineas.append(
        "HARDWARE"
    )

    lineas.append(
        "-" * 60
    )

    lineas.append(
        f"CPU: {sistema.cpu.nombre}"
    )

    lineas.append(
        "Nucleos fisicos: "
        f"{numero_legible(sistema.cpu.nucleos_fisicos)}"
    )

    lineas.append(
        "Procesadores logicos: "
        f"{numero_legible(sistema.cpu.procesadores_logicos)}"
    )

    lineas.append(
        "RAM total: "
        f"{bytes_legibles(sistema.memoria.total_bytes)}"
    )

    lineas.append(
        "RAM usada: "
        f"{bytes_legibles(sistema.memoria.usada_bytes)}"
    )

    lineas.append(
        "RAM disponible: "
        f"{bytes_legibles(sistema.memoria.disponible_bytes)}"
    )

    lineas.append(
        "Uso RAM: "
        f"{numero_legible(sistema.memoria.uso_porcentaje, '%')}"
    )

    gpu = obtener_gpu_principal(
        sistema
    )

    if gpu:
        lineas.append(
            f"GPU: {gpu.nombre}"
        )

        lineas.append(
            "VRAM: "
            f"{bytes_legibles(gpu.memoria_bytes)}"
        )

    # ========================================================
    # ALMACENAMIENTO
    # ========================================================

    lineas.append(
        ""
    )

    lineas.append(
        "ALMACENAMIENTO"
    )

    lineas.append(
        "-" * 60
    )

    if sistema.volumenes:
        for volumen in sistema.volumenes:
            lineas.append(
                f"{volumen.unidad} "
                f"{bytes_legibles(volumen.total_bytes)} total | "
                f"{bytes_legibles(volumen.libre_bytes)} libre | "
                f"{numero_legible(volumen.uso_porcentaje, '%')} usado"
            )

    else:
        lineas.append(
            "No disponible"
        )

    # ========================================================
    # RED
    # ========================================================

    lineas.append(
        ""
    )

    lineas.append(
        "RED"
    )

    lineas.append(
        "-" * 60
    )

    lineas.append(
        f"IP principal: {sistema.ip_local_principal}"
    )

    adaptador = obtener_adaptador_principal(
        sistema
    )

    if adaptador:
        lineas.append(
            f"Adaptador: {adaptador.nombre}"
        )

        lineas.append(
            f"Estado: {adaptador.estado}"
        )

        lineas.append(
            "Velocidad: "
            f"{numero_legible(adaptador.velocidad_mbps, ' Mbps')}"
        )

        lineas.append(
            "IPv4: "
            + (
                ", ".join(adaptador.ipv4)
                if adaptador.ipv4
                else "No disponible"
            )
        )

        lineas.append(
            "Gateway: "
            + (
                ", ".join(adaptador.gateway)
                if adaptador.gateway
                else "No disponible"
            )
        )

        lineas.append(
            "DNS: "
            + (
                ", ".join(adaptador.dns)
                if adaptador.dns
                else "No disponible"
            )
        )

    # ========================================================
    # SEGURIDAD
    # ========================================================

    lineas.append(
        ""
    )

    lineas.append(
        "SEGURIDAD"
    )

    lineas.append(
        "-" * 60
    )

    lineas.append(
        "Secure Boot: "
        f"{bool_legible(sistema.seguridad.secure_boot)}"
    )

    lineas.append(
        "TPM: "
        f"{bool_legible(sistema.seguridad.tpm_presente)}"
    )

    lineas.append(
        "Defender: "
        f"{bool_legible(sistema.seguridad.defender_antivirus)}"
    )

    lineas.append(
        "Proteccion en tiempo real: "
        f"{bool_legible(sistema.seguridad.defender_tiempo_real)}"
    )

    # ========================================================
    # NETPRO
    # ========================================================

    lineas.append(
        ""
    )

    lineas.append(
        "NETPRO"
    )

    lineas.append(
        "-" * 60
    )

    lineas.append(
        f"Python: {sistema.entorno.python_version}"
    )

    lineas.append(
        "Entorno virtual: "
        f"{bool_legible(sistema.entorno.entorno_virtual)}"
    )

    lineas.append(
        "Ollama: "
        f"{bool_legible(sistema.entorno.ollama_disponible)}"
    )

    if sistema.entorno.modelos_ollama:
        lineas.append(
            "Modelos: "
            + ", ".join(
                sistema.entorno.modelos_ollama
            )
        )

    # ========================================================
    # ERRORES
    # ========================================================

    if sistema.errores:
        lineas.append(
            ""
        )

        lineas.append(
            "DATOS NO DISPONIBLES"
        )

        lineas.append(
            "-" * 60
        )

        for error in sistema.errores:
            lineas.append(
                f"- {error}"
            )

    return "\n".join(
        lineas
    )


# ============================================================
# INFORMACION DE ALMACENAMIENTO PARA GUI
# ============================================================

def obtener_datos_almacenamiento_gui(
    sistema: SistemaInfo
) -> list[dict]:
    resultado = []

    for volumen in sistema.volumenes:
        resultado.append(
            {
                "unidad": volumen.unidad,
                "etiqueta": volumen.etiqueta,
                "sistema_archivos": volumen.sistema_archivos,
                "total_bytes": volumen.total_bytes,
                "usado_bytes": volumen.usado_bytes,
                "libre_bytes": volumen.libre_bytes,
                "uso_porcentaje": volumen.uso_porcentaje,
                "total": bytes_legibles(
                    volumen.total_bytes
                ),
                "usado": bytes_legibles(
                    volumen.usado_bytes
                ),
                "libre": bytes_legibles(
                    volumen.libre_bytes
                )
            }
        )

    return resultado


# ============================================================
# INFORMACION DE RAM PARA GUI
# ============================================================

def obtener_datos_ram_gui(
    sistema: SistemaInfo
) -> dict:
    return {
        "total_bytes": (
            sistema.memoria.total_bytes
        ),

        "usada_bytes": (
            sistema.memoria.usada_bytes
        ),

        "disponible_bytes": (
            sistema.memoria.disponible_bytes
        ),

        "uso_porcentaje": (
            sistema.memoria.uso_porcentaje
        ),

        "total": bytes_legibles(
            sistema.memoria.total_bytes
        ),

        "usada": bytes_legibles(
            sistema.memoria.usada_bytes
        ),

        "disponible": bytes_legibles(
            sistema.memoria.disponible_bytes
        ),

        "modulos": [
            {
                "banco": modulo.banco,
                "dispositivo": modulo.dispositivo,

                "capacidad": bytes_legibles(
                    modulo.capacidad_bytes
                ),

                "fabricante": modulo.fabricante,

                "numero_parte": (
                    modulo.numero_parte
                ),

                "velocidad_mhz": (
                    modulo.velocidad_mhz
                ),

                "velocidad_configurada_mhz": (
                    modulo.velocidad_configurada_mhz
                ),

                "tipo": (
                    modulo.tipo_memoria
                )
            }

            for modulo
            in sistema.memoria.modulos
        ]
    }


# ============================================================
# INFORMACION DE RED PARA GUI
# ============================================================

def obtener_datos_red_gui(
    sistema: SistemaInfo
) -> dict:
    principal = obtener_adaptador_principal(
        sistema
    )

    activos = obtener_adaptadores_activos(
        sistema
    )

    datos = {
        "hostname": sistema.hostname,

        "ip_principal": (
            sistema.ip_local_principal
        ),

        "total_adaptadores": len(
            sistema.adaptadores_red
        ),

        "adaptadores_activos": len(
            activos
        ),

        "principal": None,

        "adaptadores": []
    }

    if principal:
        datos["principal"] = {
            "nombre": principal.nombre,
            "descripcion": principal.descripcion,
            "tipo": principal.tipo,
            "estado": principal.estado,
            "mac": principal.mac,

            "velocidad_mbps": (
                principal.velocidad_mbps
            ),

            "mtu": principal.mtu,
            "metrica": principal.metrica,
            "ipv4": principal.ipv4,
            "ipv6": principal.ipv6,
            "gateway": principal.gateway,
            "dns": principal.dns,
            "dhcp": principal.dhcp,
            "fisico": principal.fisico
        }

    for adaptador in (
        sistema.adaptadores_red
    ):
        datos[
            "adaptadores"
        ].append(
            {
                "nombre": adaptador.nombre,
                "descripcion": adaptador.descripcion,
                "tipo": adaptador.tipo,
                "estado": adaptador.estado,
                "mac": adaptador.mac,

                "velocidad_mbps": (
                    adaptador.velocidad_mbps
                ),

                "mtu": adaptador.mtu,
                "metrica": adaptador.metrica,
                "ipv4": adaptador.ipv4,
                "ipv6": adaptador.ipv6,
                "gateway": adaptador.gateway,
                "dns": adaptador.dns,
                "dhcp": adaptador.dhcp,
                "fisico": adaptador.fisico
            }
        )

    return datos


# ============================================================
# INFORMACION DE SEGURIDAD PARA GUI
# ============================================================

def obtener_datos_seguridad_gui(
    sistema: SistemaInfo
) -> dict:
    return {
        "secure_boot": (
            sistema.seguridad.secure_boot
        ),

        "tpm_presente": (
            sistema.seguridad.tpm_presente
        ),

        "tpm_listo": (
            sistema.seguridad.tpm_listo
        ),

        "tpm_habilitado": (
            sistema.seguridad.tpm_habilitado
        ),

        "tpm_version": (
            sistema.seguridad.tpm_version
        ),

        "defender_disponible": (
            sistema.seguridad.defender_disponible
        ),

        "defender_antivirus": (
            sistema.seguridad.defender_antivirus
        ),

        "defender_tiempo_real": (
            sistema.seguridad.defender_tiempo_real
        ),

        "firewall": [
            {
                "nombre": perfil.nombre,
                "habilitado": perfil.habilitado,

                "entrada": (
                    perfil.entrada_predeterminada
                ),

                "salida": (
                    perfil.salida_predeterminada
                )
            }

            for perfil
            in sistema.seguridad.firewall
        ]
    }


# ============================================================
# INFORMACION DE HARDWARE PARA GUI
# ============================================================

def obtener_datos_hardware_gui(
    sistema: SistemaInfo
) -> dict:
    gpu = obtener_gpu_principal(
        sistema
    )

    return {
        "cpu": {
            "nombre": sistema.cpu.nombre,

            "fabricante": (
                sistema.cpu.fabricante
            ),

            "socket": sistema.cpu.socket,

            "nucleos_fisicos": (
                sistema.cpu.nucleos_fisicos
            ),

            "procesadores_logicos": (
                sistema.cpu.procesadores_logicos
            ),

            "frecuencia_actual_mhz": (
                sistema.cpu.frecuencia_actual_mhz
            ),

            "frecuencia_max_mhz": (
                sistema.cpu.frecuencia_max_mhz
            ),

            "carga_porcentaje": (
                sistema.cpu.carga_porcentaje
            ),

            "virtualizacion": (
                sistema.cpu.virtualizacion_firmware
            )
        },

        "placa_base": {
            "fabricante": (
                sistema.placa_base.fabricante
            ),

            "producto": (
                sistema.placa_base.producto
            ),

            "version": (
                sistema.placa_base.version
            )
        },

        "bios": {
            "fabricante": (
                sistema.bios.fabricante
            ),

            "version": (
                sistema.bios.version
            ),

            "fecha": sistema.bios.fecha,

            "modo_firmware": (
                sistema.bios.modo_firmware
            )
        },

        "gpu": (
            {
                "nombre": gpu.nombre,
                "tipo": gpu.tipo,

                "memoria": bytes_legibles(
                    gpu.memoria_bytes
                ),

                "driver": gpu.driver,

                "resolucion": (
                    gpu.resolucion
                ),

                "frecuencia_refresco_hz": (
                    gpu.frecuencia_refresco_hz
                ),

                "estado": gpu.estado
            }

            if gpu
            else None
        )
    }


# ============================================================
# INFORMACION COMPLETA PARA GUI
# ============================================================

def obtener_paquete_gui(
    sistema: SistemaInfo
) -> dict:
    """
    Devuelve un unico diccionario preparado para que
    ui/system_page.py pueda consumir la informacion
    sin tener que conocer todos los dataclass internos.
    """

    return {
        "resumen": generar_datos_interfaz(
            sistema
        ),

        "hardware": obtener_datos_hardware_gui(
            sistema
        ),

        "ram": obtener_datos_ram_gui(
            sistema
        ),

        "almacenamiento": (
            obtener_datos_almacenamiento_gui(
                sistema
            )
        ),

        "red": obtener_datos_red_gui(
            sistema
        ),

        "seguridad": (
            obtener_datos_seguridad_gui(
                sistema
            )
        ),

        "entorno": {
            "python_version": (
                sistema.entorno.python_version
            ),

            "python_executable": (
                sistema.entorno.python_executable
            ),

            "entorno_virtual": (
                sistema.entorno.entorno_virtual
            ),

            "virtual_env": (
                sistema.entorno.virtual_env
            ),

            "powershell": (
                sistema.entorno.powershell_disponible
            ),

            "ollama": (
                sistema.entorno.ollama_disponible
            ),

            "ollama_version": (
                sistema.entorno.ollama_version
            ),

            "modelos_ollama": list(
                sistema.entorno.modelos_ollama
            )
        },

        "errores": list(
            sistema.errores
        )
    }


# ============================================================
# PRUEBA DIRECTA
# ============================================================

def main():
    print(
        "=" * 78
    )

    print(
        "NETPRO - RECOPILANDO INFORMACION DEL SISTEMA"
    )

    print(
        "=" * 78
    )

    print(
        "\nEspere mientras NetPro consulta "
        "la informacion del equipo...\n"
    )

    inicio = time.perf_counter()

    sistema = obtener_informacion_sistema()

    fin = time.perf_counter()

    imprimir_resultado(
        sistema
    )

    print(
        f"\nTiempo total de recopilacion: "
        f"{fin - inicio:.2f} segundos"
    )


if __name__ == "__main__":
    main()