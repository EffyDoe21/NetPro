"""
NetPro - Network & Security Toolkit
Core: Historial y persistencia SQLite

Centraliza el almacenamiento de los resultados generados por:

- Analizador IPv4
- Analizador IPv6
- DNS Lookup
- Ping
- Traceroute
- Estado de red
- Escáner de puertos
- Analizador HTTP / HTTPS
- Información del sistema

La base de datos utilizada es:

    data/netpro.db
"""

from __future__ import annotations

import json
import sqlite3

from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


# ============================================================
# CONFIGURACIÓN
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DB_PATH = DATA_DIR / "netpro.db"


# ============================================================
# UTILIDADES
# ============================================================

def _fecha_actual() -> str:
    """
    Devuelve la fecha y hora actual en formato ISO.
    """

    return datetime.now().astimezone().isoformat(
        timespec="seconds"
    )


def _normalizar_valor(valor: Any):
    """
    Convierte valores complejos en formatos compatibles
    con SQLite.
    """

    if valor is None:
        return None

    if isinstance(
        valor,
        (str, int, float, bytes)
    ):
        return valor

    if isinstance(valor, bool):
        return int(valor)

    if is_dataclass(valor):
        valor = asdict(valor)

    if isinstance(
        valor,
        (dict, list, tuple, set)
    ):
        return json.dumps(
            valor,
            ensure_ascii=False,
            default=str
        )

    return str(valor)


def _a_dict(resultado: Any) -> dict:
    """
    Convierte un resultado de NetPro a diccionario.
    """

    if resultado is None:
        return {}

    if is_dataclass(resultado):
        return asdict(resultado)

    if isinstance(resultado, dict):
        return resultado

    if hasattr(resultado, "__dict__"):
        return dict(resultado.__dict__)

    raise TypeError(
        "El resultado no puede convertirse a diccionario."
    )


# ============================================================
# CONEXIÓN
# ============================================================

def obtener_conexion() -> sqlite3.Connection:
    """
    Abre la conexión principal con netpro.db.
    """

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    conexion = sqlite3.connect(
        DB_PATH
    )

    conexion.row_factory = sqlite3.Row

    conexion.execute(
        "PRAGMA foreign_keys = ON"
    )

    conexion.execute(
        "PRAGMA journal_mode = WAL"
    )

    return conexion


# ============================================================
# CREAR BASE DE DATOS
# ============================================================

def inicializar_base_datos():
    """
    Crea todas las tablas necesarias para el historial.
    """

    with obtener_conexion() as conexion:

        cursor = conexion.cursor()

        # ====================================================
        # HISTORIAL PRINCIPAL
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                modulo TEXT NOT NULL,
                objetivo TEXT,
                resumen TEXT,
                exitoso INTEGER NOT NULL DEFAULT 1,
                error TEXT
            )
            """
        )

        # ====================================================
        # IPv4
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS historial_ipv4 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                historial_id INTEGER NOT NULL,

                ip TEXT,
                cidr TEXT,
                network TEXT,
                netmask TEXT,
                wildcard TEXT,
                broadcast TEXT,

                first_host TEXT,
                last_host TEXT,

                total_addresses INTEGER,
                usable_hosts INTEGER,

                private INTEGER,
                version INTEGER,

                FOREIGN KEY(historial_id)
                    REFERENCES historial(id)
                    ON DELETE CASCADE
            )
            """
        )

        # ====================================================
        # IPv6
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS historial_ipv6 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                historial_id INTEGER NOT NULL,

                ip TEXT,
                cidr TEXT,
                network TEXT,
                first_address TEXT,
                last_address TEXT,
                total_addresses TEXT,
                expanded TEXT,
                compressed TEXT,
                hexadecimal TEXT,
                binary TEXT,
                global_ip INTEGER,
                private_ip INTEGER,
                link_local INTEGER,
                multicast INTEGER,
                loopback INTEGER,
                unspecified INTEGER,
                reserved INTEGER,
                ipv4_mapped TEXT,
                scope_id TEXT,
                datos_json TEXT,

                FOREIGN KEY(historial_id)
                    REFERENCES historial(id)
                    ON DELETE CASCADE
            )
            """
        )

        # ====================================================
        # DNS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS historial_dns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                historial_id INTEGER NOT NULL,

                dominio TEXT,

                FOREIGN KEY(historial_id)
                    REFERENCES historial(id)
                    ON DELETE CASCADE
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS historial_dns_registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dns_id INTEGER NOT NULL,

                tipo TEXT NOT NULL,
                valor TEXT,

                FOREIGN KEY(dns_id)
                    REFERENCES historial_dns(id)
                    ON DELETE CASCADE
            )
            """
        )

        # ====================================================
        # PING
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS historial_ping (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                historial_id INTEGER NOT NULL,

                destino TEXT,
                ip TEXT,

                enviados INTEGER,
                recibidos INTEGER,
                perdidos INTEGER,

                perdida REAL,

                minimo REAL,
                maximo REAL,
                promedio REAL,

                respuesta INTEGER,

                FOREIGN KEY(historial_id)
                    REFERENCES historial(id)
                    ON DELETE CASCADE
            )
            """
        )

        # ====================================================
        # TRACEROUTE
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS historial_traceroute (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                historial_id INTEGER NOT NULL,

                destino TEXT,
                max_saltos INTEGER,

                comando TEXT,
                salida TEXT,

                exitoso INTEGER,
                error TEXT,

                FOREIGN KEY(historial_id)
                    REFERENCES historial(id)
                    ON DELETE CASCADE
            )
            """
        )

        # ====================================================
        # ESTADO DE RED
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS historial_network_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                historial_id INTEGER NOT NULL,

                detectado INTEGER,
                conectado INTEGER,

                nombre TEXT,
                descripcion TEXT,
                velocidad TEXT,

                estado TEXT,
                error TEXT,

                tipo TEXT,

                datos_json TEXT,

                FOREIGN KEY(historial_id)
                    REFERENCES historial(id)
                    ON DELETE CASCADE
            )
            """
        )

        # ====================================================
        # ESCANEO DE PUERTOS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS historial_puertos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                historial_id INTEGER NOT NULL,

                host TEXT,
                ip TEXT,

                puerto INTEGER,
                protocolo TEXT,

                estado TEXT,
                servicio TEXT,
                descripcion TEXT,

                tiempo_ms REAL,
                codigo INTEGER,
                error TEXT,

                FOREIGN KEY(historial_id)
                    REFERENCES historial(id)
                    ON DELETE CASCADE
            )
            """
        )

        # ====================================================
        # HTTP / HTTPS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS historial_http (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                historial_id INTEGER NOT NULL,

                url_solicitada TEXT,
                url_final TEXT,

                host TEXT,
                ip TEXT,
                protocolo TEXT,

                codigo_estado INTEGER,
                razon_estado TEXT,

                tiempo_ms REAL,

                servidor TEXT,
                content_type TEXT,

                usa_https INTEGER,

                certificado_disponible INTEGER,
                certificado_valido INTEGER,

                certificado_sujeto TEXT,
                certificado_emisor TEXT,

                certificado_desde TEXT,
                certificado_hasta TEXT,

                dias_restantes_certificado INTEGER,

                error TEXT,

                FOREIGN KEY(historial_id)
                    REFERENCES historial(id)
                    ON DELETE CASCADE
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS historial_http_headers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                http_id INTEGER NOT NULL,

                nombre TEXT,
                valor TEXT,

                FOREIGN KEY(http_id)
                    REFERENCES historial_http(id)
                    ON DELETE CASCADE
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS historial_http_seguridad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                http_id INTEGER NOT NULL,

                nombre TEXT,
                presente INTEGER,
                valor TEXT,
                descripcion TEXT,

                FOREIGN KEY(http_id)
                    REFERENCES historial_http(id)
                    ON DELETE CASCADE
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS historial_http_redirecciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                http_id INTEGER NOT NULL,

                codigo INTEGER,
                desde_url TEXT,
                hacia_url TEXT,

                FOREIGN KEY(http_id)
                    REFERENCES historial_http(id)
                    ON DELETE CASCADE
            )
            """
        )

        # ====================================================
        # SNAPSHOTS DEL SISTEMA
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS snapshots_sistema (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                fecha TEXT NOT NULL,

                nombre_equipo TEXT,
                hostname TEXT,
                usuario TEXT,

                sistema_operativo TEXT,
                version_sistema TEXT,
                build TEXT,
                arquitectura TEXT,

                fabricante_equipo TEXT,
                modelo_equipo TEXT,

                fecha_instalacion_windows TEXT,
                zona_horaria TEXT,

                ultimo_arranque TEXT,
                uptime_segundos REAL,

                ip_local_principal TEXT,

                procesos_totales INTEGER,

                cpu_json TEXT,
                placa_base_json TEXT,
                bios_json TEXT,
                seguridad_json TEXT,
                entorno_json TEXT,

                datos_completos_json TEXT
            )
            """
        )

        # ====================================================
        # MÓDULOS RAM
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sistema_ram_modulos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id INTEGER NOT NULL,

                banco TEXT,
                dispositivo TEXT,

                capacidad_bytes INTEGER,

                fabricante TEXT,
                numero_parte TEXT,
                numero_serie TEXT,

                velocidad_mhz INTEGER,
                velocidad_configurada_mhz INTEGER,

                tipo_memoria TEXT,

                FOREIGN KEY(snapshot_id)
                    REFERENCES snapshots_sistema(id)
                    ON DELETE CASCADE
            )
            """
        )

        # ====================================================
        # GPU
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sistema_gpus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id INTEGER NOT NULL,

                nombre TEXT,
                memoria_bytes INTEGER,
                driver TEXT,
                resolucion TEXT,
                frecuencia_refresco_hz INTEGER,
                estado TEXT,
                tipo TEXT,

                FOREIGN KEY(snapshot_id)
                    REFERENCES snapshots_sistema(id)
                    ON DELETE CASCADE
            )
            """
        )

        # ====================================================
        # MONITORES
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sistema_monitores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id INTEGER NOT NULL,

                nombre TEXT,
                fabricante TEXT,
                activo INTEGER,

                FOREIGN KEY(snapshot_id)
                    REFERENCES snapshots_sistema(id)
                    ON DELETE CASCADE
            )
            """
        )

        # ====================================================
        # DISCOS FÍSICOS
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sistema_discos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id INTEGER NOT NULL,

                numero INTEGER,
                nombre TEXT,
                modelo TEXT,
                serial TEXT,

                tipo_medio TEXT,
                bus TEXT,

                tamano_bytes INTEGER,

                estado_salud TEXT,
                estado_operacional TEXT,

                FOREIGN KEY(snapshot_id)
                    REFERENCES snapshots_sistema(id)
                    ON DELETE CASCADE
            )
            """
        )

        # ====================================================
        # VOLÚMENES
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sistema_volumenes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id INTEGER NOT NULL,

                unidad TEXT,
                etiqueta TEXT,
                sistema_archivos TEXT,

                total_bytes INTEGER,
                usado_bytes INTEGER,
                libre_bytes INTEGER,

                uso_porcentaje REAL,

                FOREIGN KEY(snapshot_id)
                    REFERENCES snapshots_sistema(id)
                    ON DELETE CASCADE
            )
            """
        )

        # ====================================================
        # ADAPTADORES DE RED
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sistema_adaptadores_red (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id INTEGER NOT NULL,

                nombre TEXT,
                descripcion TEXT,
                tipo TEXT,
                estado TEXT,

                mac TEXT,

                velocidad_mbps REAL,
                mtu INTEGER,
                metrica INTEGER,

                ipv4_json TEXT,
                ipv6_json TEXT,
                gateway_json TEXT,
                dns_json TEXT,

                dhcp INTEGER,
                fisico INTEGER,

                FOREIGN KEY(snapshot_id)
                    REFERENCES snapshots_sistema(id)
                    ON DELETE CASCADE
            )
            """
        )

        # ====================================================
        # FIREWALL
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sistema_firewall (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id INTEGER NOT NULL,

                nombre TEXT,
                habilitado INTEGER,

                entrada_predeterminada TEXT,
                salida_predeterminada TEXT,

                FOREIGN KEY(snapshot_id)
                    REFERENCES snapshots_sistema(id)
                    ON DELETE CASCADE
            )
            """
        )

        # ====================================================
        # CONFIGURACIÓN
        # ====================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS configuracion (
                clave TEXT PRIMARY KEY,
                valor TEXT
            )
            """
        )

        # ====================================================
        # ÍNDICES
        # ====================================================

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_historial_fecha
            ON historial(fecha)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_historial_modulo
            ON historial(modulo)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_historial_objetivo
            ON historial(objetivo)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_puertos_puerto
            ON historial_puertos(puerto)
            """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_dns_tipo
            ON historial_dns_registros(tipo)
            """
        )

        conexion.commit()


# ============================================================
# REGISTRO GENERAL
# ============================================================

def crear_historial(
    modulo: str,
    objetivo: str | None = None,
    resumen: str | None = None,
    exitoso: bool = True,
    error: str | None = None,
    conexion=None
) -> int:
    """
    Crea el registro principal de un análisis.
    """

    propia = conexion is None

    if propia:
        conexion = obtener_conexion()

    try:

        cursor = conexion.execute(
            """
            INSERT INTO historial (
                fecha,
                modulo,
                objetivo,
                resumen,
                exitoso,
                error
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                _fecha_actual(),
                modulo,
                objetivo,
                resumen,
                int(bool(exitoso)),
                error
            )
        )

        historial_id = cursor.lastrowid

        if propia:
            conexion.commit()

        return historial_id

    finally:

        if propia:
            conexion.close()


# ============================================================
# GUARDAR IPv4
# ============================================================

def guardar_ipv4(resultado: dict) -> int:

    datos = _a_dict(resultado)

    with obtener_conexion() as conexion:

        historial_id = crear_historial(
            modulo="IPv4",
            objetivo=datos.get("ip"),
            resumen=(
                f'{datos.get("ip", "")}'
                f'{datos.get("cidr", "")}'
            ),
            conexion=conexion
        )

        conexion.execute(
            """
            INSERT INTO historial_ipv4 (
                historial_id,
                ip,
                cidr,
                network,
                netmask,
                wildcard,
                broadcast,
                first_host,
                last_host,
                total_addresses,
                usable_hosts,
                private,
                version
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                historial_id,
                datos.get("ip"),
                datos.get("cidr"),
                datos.get("network"),
                datos.get("netmask"),
                datos.get("wildcard"),
                datos.get("broadcast"),
                datos.get("first_host"),
                datos.get("last_host"),
                datos.get("total_addresses"),
                datos.get("usable_hosts"),
                int(bool(datos.get("private"))),
                datos.get("version")
            )
        )

        conexion.commit()

        return historial_id


# ============================================================
# GUARDAR IPv6
# ============================================================

def guardar_ipv6(resultado: dict) -> int:
    """Guarda un analisis IPv6 completo en SQLite."""

    datos = _a_dict(resultado)

    ip = datos.get("direccion") or datos.get("ip")
    prefijo = datos.get("prefijo")
    cidr = datos.get("cidr")

    if cidr is None and prefijo is not None:
        cidr = f"/{prefijo}"

    network = datos.get("red") or datos.get("network")
    first_address = datos.get("primera_direccion") or datos.get("first_address")
    last_address = datos.get("ultima_direccion") or datos.get("last_address")

    total_addresses = datos.get("cantidad_direcciones")
    if total_addresses is None:
        total_addresses = datos.get("total_addresses")

    expanded = datos.get("direccion_expandida") or datos.get("expanded")
    compressed = datos.get("direccion_comprimida") or datos.get("compressed")
    hexadecimal = datos.get("hexadecimal") or datos.get("hextetos")
    binary = datos.get("binario") or datos.get("binary")

    def _bool_ipv6(clave_real: str, clave_alterna: str):
        if clave_real in datos:
            valor = datos.get(clave_real)
        else:
            valor = datos.get(clave_alterna)
        return None if valor is None else int(bool(valor))

    valores = (
        ip,
        cidr,
        network,
        first_address,
        last_address,
        str(total_addresses) if total_addresses is not None else None,
        expanded,
        compressed,
        hexadecimal,
        binary,
        _bool_ipv6("es_global", "global"),
        _bool_ipv6("es_privada", "private"),
        _bool_ipv6("es_link_local", "link_local"),
        _bool_ipv6("es_multicast", "multicast"),
        _bool_ipv6("es_loopback", "loopback"),
        _bool_ipv6("es_unspecified", "unspecified"),
        _bool_ipv6("es_reserved", "reserved"),
        datos.get("ipv4_mapped"),
        datos.get("scope_id"),
        datos,
    )

    # SQLite no acepta list/dict/tuple/set directamente.
    valores_sql = tuple(_normalizar_valor(valor) for valor in valores)

    with obtener_conexion() as conexion:
        resumen = str(ip or "")
        if cidr and "/" not in resumen:
            resumen += str(cidr)

        historial_id = crear_historial(
            modulo="IPv6",
            objetivo=_normalizar_valor(ip),
            resumen=resumen,
            conexion=conexion,
        )

        conexion.execute(
            """
            INSERT INTO historial_ipv6 (
                historial_id,
                ip,
                cidr,
                network,
                first_address,
                last_address,
                total_addresses,
                expanded,
                compressed,
                hexadecimal,
                binary,
                global_ip,
                private_ip,
                link_local,
                multicast,
                loopback,
                unspecified,
                reserved,
                ipv4_mapped,
                scope_id,
                datos_json
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (historial_id, *valores_sql),
        )

        conexion.commit()
        return historial_id


# ============================================================
# GUARDAR DNS
# ============================================================
def guardar_dns(resultado: dict) -> int:
    """
    Guarda una consulta DNS completa en SQLite.
    """

    datos = _a_dict(resultado)

    # ========================================================
    # DOMINIO CONSULTADO
    # ========================================================

    dominio = (
        datos.get("domain")
        or datos.get("dominio")
        or datos.get("host")
        or datos.get("objetivo")
    )

    dominio = _normalizar_valor(dominio)

    # ========================================================
    # TIPOS DE REGISTROS DNS
    # ========================================================

    tipos = (
        "A",
        "AAAA",
        "CNAME",
        "MX",
        "NS",
        "TXT"
    )

    # ========================================================
    # CONTAR REGISTROS ENCONTRADOS
    # ========================================================

    total_registros = 0

    for tipo in tipos:

        registros = (
            datos.get(tipo)
            or datos.get(tipo.lower())
            or []
        )

        if isinstance(
            registros,
            (list, tuple, set)
        ):
            total_registros += len(registros)

        elif registros:
            total_registros += 1

    # ========================================================
    # GUARDAR EN BASE DE DATOS
    # ========================================================

    with obtener_conexion() as conexion:

        # ----------------------------------------------------
        # HISTORIAL GENERAL
        # ----------------------------------------------------

        historial_id = crear_historial(
            modulo="DNS",
            objetivo=dominio,
            resumen=(
                f"Consulta DNS: {dominio} - "
                f"{total_registros} registros"
            ),
            conexion=conexion
        )

        # ----------------------------------------------------
        # CONSULTA DNS
        # ----------------------------------------------------

        cursor = conexion.execute(
            """
            INSERT INTO historial_dns (
                historial_id,
                dominio
            )
            VALUES (?, ?)
            """,
            (
                historial_id,
                dominio
            )
        )

        dns_id = cursor.lastrowid

        # ----------------------------------------------------
        # REGISTROS DNS
        # ----------------------------------------------------

        for tipo in tipos:

            registros = (
                datos.get(tipo)
                or datos.get(tipo.lower())
                or []
            )

            if not isinstance(
                registros,
                (list, tuple, set)
            ):
                registros = [registros]

            for valor in registros:

                if valor is None:
                    continue

                conexion.execute(
                    """
                    INSERT INTO historial_dns_registros (
                        dns_id,
                        tipo,
                        valor
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        dns_id,
                        tipo,
                        _normalizar_valor(valor)
                    )
                )

        conexion.commit()

        return historial_id


# ============================================================
# GUARDAR PING
# ============================================================

def guardar_ping(resultado: dict) -> int:

    datos = _a_dict(resultado)

    with obtener_conexion() as conexion:

        historial_id = crear_historial(
            modulo="Ping",
            objetivo=datos.get("destino"),
            resumen=(
                f'Ping a {datos.get("destino", "")} - '
                f'{datos.get("perdida", 0)}% pérdida'
            ),
            exitoso=bool(
                datos.get("respuesta")
            ),
            conexion=conexion
        )

        conexion.execute(
            """
            INSERT INTO historial_ping (
                historial_id,
                destino,
                ip,
                enviados,
                recibidos,
                perdidos,
                perdida,
                minimo,
                maximo,
                promedio,
                respuesta
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                historial_id,
                datos.get("destino"),
                datos.get("ip"),
                datos.get("enviados"),
                datos.get("recibidos"),
                datos.get("perdidos"),
                datos.get("perdida"),
                datos.get("minimo"),
                datos.get("maximo"),
                datos.get("promedio"),
                int(bool(datos.get("respuesta")))
            )
        )

        conexion.commit()

        return historial_id


# ============================================================
# GUARDAR TRACEROUTE
# ============================================================

def guardar_traceroute(resultado: dict) -> int:

    datos = _a_dict(resultado)

    with obtener_conexion() as conexion:

        historial_id = crear_historial(
            modulo="Traceroute",
            objetivo=datos.get("destino"),
            resumen=(
                f'Traceroute a '
                f'{datos.get("destino", "")}'
            ),
            exitoso=bool(
                datos.get("exitoso")
            ),
            error=datos.get("error"),
            conexion=conexion
        )

        conexion.execute(
            """
            INSERT INTO historial_traceroute (
                historial_id,
                destino,
                max_saltos,
                comando,
                salida,
                exitoso,
                error
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                historial_id,
                datos.get("destino"),
                datos.get("max_saltos"),
                datos.get("comando"),
                datos.get("salida"),
                int(bool(datos.get("exitoso"))),
                datos.get("error")
            )
        )

        conexion.commit()

        return historial_id


# ============================================================
# GUARDAR ESTADO DE RED
# ============================================================

def guardar_estado_red(
    resultado: dict,
    tipo: str | None = None
) -> int:

    datos = _a_dict(resultado)

    objetivo = (
        datos.get("nombre")
        or tipo
        or "Red local"
    )

    with obtener_conexion() as conexion:

        historial_id = crear_historial(
            modulo="Estado de red",
            objetivo=objetivo,
            resumen=datos.get("estado"),
            exitoso=(
                datos.get("error") is None
            ),
            error=datos.get("error"),
            conexion=conexion
        )

        conexion.execute(
            """
            INSERT INTO historial_network_status (
                historial_id,
                detectado,
                conectado,
                nombre,
                descripcion,
                velocidad,
                estado,
                error,
                tipo,
                datos_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                historial_id,
                int(bool(datos.get("detectado"))),
                int(bool(datos.get("conectado"))),
                datos.get("nombre"),
                datos.get("descripcion"),
                datos.get("velocidad"),
                datos.get("estado"),
                datos.get("error"),
                tipo,
                _normalizar_valor(datos)
            )
        )

        conexion.commit()

        return historial_id


# ============================================================
# GUARDAR ESCANEO DE PUERTOS
# ============================================================

def guardar_puertos(
    resultados,
    objetivo: str | None = None
) -> int:

    if not isinstance(
        resultados,
        (list, tuple)
    ):
        resultados = [resultados]

    datos_resultados = [
        _a_dict(resultado)
        for resultado in resultados
    ]

    if not objetivo and datos_resultados:

        objetivo = (
            datos_resultados[0].get("host")
            or datos_resultados[0].get("ip")
        )

    abiertos = sum(
        1
        for datos in datos_resultados
        if str(
            datos.get("estado", "")
        ).lower() == "abierto"
    )

    with obtener_conexion() as conexion:

        historial_id = crear_historial(
            modulo="Puertos",
            objetivo=objetivo,
            resumen=(
                f"{len(datos_resultados)} puertos analizados - "
                f"{abiertos} abiertos"
            ),
            conexion=conexion
        )

        for datos in datos_resultados:

            conexion.execute(
                """
                INSERT INTO historial_puertos (
                    historial_id,
                    host,
                    ip,
                    puerto,
                    protocolo,
                    estado,
                    servicio,
                    descripcion,
                    tiempo_ms,
                    codigo,
                    error
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    historial_id,
                    datos.get("host"),
                    datos.get("ip"),
                    datos.get("puerto"),
                    datos.get("protocolo"),
                    datos.get("estado"),
                    datos.get("servicio"),
                    datos.get("descripcion"),
                    datos.get("tiempo_ms"),
                    datos.get("codigo"),
                    datos.get("error")
                )
            )

        conexion.commit()

        return historial_id


# ============================================================
# GUARDAR HTTP / HTTPS
# ============================================================

def guardar_http(resultado) -> int:

    datos = _a_dict(resultado)

    with obtener_conexion() as conexion:

        historial_id = crear_historial(
            modulo="HTTP",
            objetivo=datos.get(
                "url_solicitada"
            ),
            resumen=(
                f'{datos.get("codigo_estado", "")} '
                f'{datos.get("razon_estado", "")}'
            ).strip(),
            exitoso=(
                datos.get("error") is None
            ),
            error=datos.get("error"),
            conexion=conexion
        )

        cursor = conexion.execute(
            """
            INSERT INTO historial_http (
                historial_id,
                url_solicitada,
                url_final,
                host,
                ip,
                protocolo,
                codigo_estado,
                razon_estado,
                tiempo_ms,
                servidor,
                content_type,
                usa_https,
                certificado_disponible,
                certificado_valido,
                certificado_sujeto,
                certificado_emisor,
                certificado_desde,
                certificado_hasta,
                dias_restantes_certificado,
                error
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                historial_id,
                datos.get("url_solicitada"),
                datos.get("url_final"),
                datos.get("host"),
                datos.get("ip"),
                datos.get("protocolo"),
                datos.get("codigo_estado"),
                datos.get("razon_estado"),
                datos.get("tiempo_ms"),
                datos.get("servidor"),
                datos.get("content_type"),
                int(bool(datos.get("usa_https"))),
                int(bool(
                    datos.get(
                        "certificado_disponible"
                    )
                )),
                (
                    None
                    if datos.get(
                        "certificado_valido"
                    ) is None
                    else int(
                        bool(
                            datos.get(
                                "certificado_valido"
                            )
                        )
                    )
                ),
                datos.get("certificado_sujeto"),
                datos.get("certificado_emisor"),
                datos.get("certificado_desde"),
                datos.get("certificado_hasta"),
                datos.get(
                    "dias_restantes_certificado"
                ),
                datos.get("error")
            )
        )

        http_id = cursor.lastrowid

        # ====================================================
        # HEADERS
        # ====================================================

        for nombre, valor in (
            datos.get("headers", {})
        ).items():

            conexion.execute(
                """
                INSERT INTO historial_http_headers (
                    http_id,
                    nombre,
                    valor
                )
                VALUES (?, ?, ?)
                """,
                (
                    http_id,
                    nombre,
                    _normalizar_valor(valor)
                )
            )

        # ====================================================
        # HEADERS DE SEGURIDAD
        # ====================================================

        for nombre, info in (
            datos.get(
                "headers_seguridad",
                {}
            )
        ).items():

            if not isinstance(info, dict):
                info = {
                    "valor": info
                }

            conexion.execute(
                """
                INSERT INTO historial_http_seguridad (
                    http_id,
                    nombre,
                    presente,
                    valor,
                    descripcion
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    http_id,
                    nombre,
                    int(
                        bool(
                            info.get(
                                "presente"
                            )
                        )
                    ),
                    _normalizar_valor(
                        info.get("valor")
                    ),
                    info.get("descripcion")
                )
            )

        # ====================================================
        # REDIRECCIONES
        # ====================================================

        for redireccion in (
            datos.get(
                "redirecciones",
                []
            )
        ):

            conexion.execute(
                """
                INSERT INTO historial_http_redirecciones (
                    http_id,
                    codigo,
                    desde_url,
                    hacia_url
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    http_id,
                    redireccion.get("codigo"),
                    redireccion.get("desde"),
                    redireccion.get("hacia")
                )
            )

        conexion.commit()

        return historial_id


# ============================================================
# GUARDAR SNAPSHOT DEL SISTEMA
# ============================================================

def guardar_snapshot_sistema(sistema) -> int:
    """
    Guarda una fotografía completa del estado del equipo.
    """

    datos = _a_dict(sistema)

    memoria = (
        datos.get("memoria")
        or {}
    )

    seguridad = (
        datos.get("seguridad")
        or {}
    )

    entorno = (
        datos.get("entorno")
        or {}
    )

    with obtener_conexion() as conexion:

        cursor = conexion.execute(
            """
            INSERT INTO snapshots_sistema (
                fecha,
                nombre_equipo,
                hostname,
                usuario,
                sistema_operativo,
                version_sistema,
                build,
                arquitectura,
                fabricante_equipo,
                modelo_equipo,
                fecha_instalacion_windows,
                zona_horaria,
                ultimo_arranque,
                uptime_segundos,
                ip_local_principal,
                procesos_totales,
                cpu_json,
                placa_base_json,
                bios_json,
                seguridad_json,
                entorno_json,
                datos_completos_json
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                _fecha_actual(),
                datos.get("nombre_equipo"),
                datos.get("hostname"),
                datos.get("usuario"),
                datos.get("sistema_operativo"),
                datos.get("version_sistema"),
                datos.get("build"),
                datos.get("arquitectura"),
                datos.get("fabricante_equipo"),
                datos.get("modelo_equipo"),
                datos.get(
                    "fecha_instalacion_windows"
                ),
                datos.get("zona_horaria"),
                datos.get("ultimo_arranque"),
                datos.get("uptime_segundos"),
                datos.get("ip_local_principal"),
                datos.get("procesos_totales"),
                _normalizar_valor(
                    datos.get("cpu")
                ),
                _normalizar_valor(
                    datos.get("placa_base")
                ),
                _normalizar_valor(
                    datos.get("bios")
                ),
                _normalizar_valor(seguridad),
                _normalizar_valor(entorno),
                _normalizar_valor(datos)
            )
        )

        snapshot_id = cursor.lastrowid

        # ====================================================
        # RAM
        # ====================================================

        for modulo in memoria.get(
            "modulos",
            []
        ):

            conexion.execute(
                """
                INSERT INTO sistema_ram_modulos (
                    snapshot_id,
                    banco,
                    dispositivo,
                    capacidad_bytes,
                    fabricante,
                    numero_parte,
                    numero_serie,
                    velocidad_mhz,
                    velocidad_configurada_mhz,
                    tipo_memoria
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    snapshot_id,
                    modulo.get("banco"),
                    modulo.get("dispositivo"),
                    modulo.get("capacidad_bytes"),
                    modulo.get("fabricante"),
                    modulo.get("numero_parte"),
                    modulo.get("numero_serie"),
                    modulo.get("velocidad_mhz"),
                    modulo.get(
                        "velocidad_configurada_mhz"
                    ),
                    modulo.get("tipo_memoria")
                )
            )

        # ====================================================
        # GPU
        # ====================================================

        for gpu in datos.get(
            "gpus",
            []
        ):

            conexion.execute(
                """
                INSERT INTO sistema_gpus (
                    snapshot_id,
                    nombre,
                    memoria_bytes,
                    driver,
                    resolucion,
                    frecuencia_refresco_hz,
                    estado,
                    tipo
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    snapshot_id,
                    gpu.get("nombre"),
                    gpu.get("memoria_bytes"),
                    gpu.get("driver"),
                    gpu.get("resolucion"),
                    gpu.get(
                        "frecuencia_refresco_hz"
                    ),
                    gpu.get("estado"),
                    gpu.get("tipo")
                )
            )

        # ====================================================
        # MONITORES
        # ====================================================

        for monitor in datos.get(
            "monitores",
            []
        ):

            conexion.execute(
                """
                INSERT INTO sistema_monitores (
                    snapshot_id,
                    nombre,
                    fabricante,
                    activo
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    snapshot_id,
                    monitor.get("nombre"),
                    monitor.get("fabricante"),
                    (
                        None
                        if monitor.get("activo") is None
                        else int(
                            bool(
                                monitor.get("activo")
                            )
                        )
                    )
                )
            )

        # ====================================================
        # DISCOS
        # ====================================================

        for disco in datos.get(
            "discos_fisicos",
            []
        ):

            conexion.execute(
                """
                INSERT INTO sistema_discos (
                    snapshot_id,
                    numero,
                    nombre,
                    modelo,
                    serial,
                    tipo_medio,
                    bus,
                    tamano_bytes,
                    estado_salud,
                    estado_operacional
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    snapshot_id,
                    disco.get("numero"),
                    disco.get("nombre"),
                    disco.get("modelo"),
                    disco.get("serial"),
                    disco.get("tipo_medio"),
                    disco.get("bus"),
                    disco.get("tamano_bytes"),
                    disco.get("estado_salud"),
                    disco.get(
                        "estado_operacional"
                    )
                )
            )

        # ====================================================
        # VOLÚMENES
        # ====================================================

        for volumen in datos.get(
            "volumenes",
            []
        ):

            conexion.execute(
                """
                INSERT INTO sistema_volumenes (
                    snapshot_id,
                    unidad,
                    etiqueta,
                    sistema_archivos,
                    total_bytes,
                    usado_bytes,
                    libre_bytes,
                    uso_porcentaje
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    snapshot_id,
                    volumen.get("unidad"),
                    volumen.get("etiqueta"),
                    volumen.get(
                        "sistema_archivos"
                    ),
                    volumen.get("total_bytes"),
                    volumen.get("usado_bytes"),
                    volumen.get("libre_bytes"),
                    volumen.get(
                        "uso_porcentaje"
                    )
                )
            )

        # ====================================================
        # ADAPTADORES DE RED
        # ====================================================

        for adaptador in datos.get(
            "adaptadores_red",
            []
        ):

            conexion.execute(
                """
                INSERT INTO sistema_adaptadores_red (
                    snapshot_id,
                    nombre,
                    descripcion,
                    tipo,
                    estado,
                    mac,
                    velocidad_mbps,
                    mtu,
                    metrica,
                    ipv4_json,
                    ipv6_json,
                    gateway_json,
                    dns_json,
                    dhcp,
                    fisico
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?
                )
                """,
                (
                    snapshot_id,
                    adaptador.get("nombre"),
                    adaptador.get("descripcion"),
                    adaptador.get("tipo"),
                    adaptador.get("estado"),
                    adaptador.get("mac"),
                    adaptador.get(
                        "velocidad_mbps"
                    ),
                    adaptador.get("mtu"),
                    adaptador.get("metrica"),
                    _normalizar_valor(
                        adaptador.get("ipv4", [])
                    ),
                    _normalizar_valor(
                        adaptador.get("ipv6", [])
                    ),
                    _normalizar_valor(
                        adaptador.get("gateway", [])
                    ),
                    _normalizar_valor(
                        adaptador.get("dns", [])
                    ),
                    (
                        None
                        if adaptador.get("dhcp") is None
                        else int(
                            bool(
                                adaptador.get("dhcp")
                            )
                        )
                    ),
                    (
                        None
                        if adaptador.get("fisico") is None
                        else int(
                            bool(
                                adaptador.get("fisico")
                            )
                        )
                    )
                )
            )

        # ====================================================
        # FIREWALL
        # ====================================================

        for perfil in seguridad.get(
            "firewall",
            []
        ):

            conexion.execute(
                """
                INSERT INTO sistema_firewall (
                    snapshot_id,
                    nombre,
                    habilitado,
                    entrada_predeterminada,
                    salida_predeterminada
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    snapshot_id,
                    perfil.get("nombre"),
                    (
                        None
                        if perfil.get(
                            "habilitado"
                        ) is None
                        else int(
                            bool(
                                perfil.get(
                                    "habilitado"
                                )
                            )
                        )
                    ),
                    perfil.get(
                        "entrada_predeterminada"
                    ),
                    perfil.get(
                        "salida_predeterminada"
                    )
                )
            )

        conexion.commit()

        return snapshot_id


# ============================================================
# CONSULTAR HISTORIAL
# ============================================================

def obtener_historial(
    modulo: str | None = None,
    limite: int = 100
) -> list[dict]:
    """
    Obtiene los registros más recientes.
    """

    limite = max(
        1,
        min(
            int(limite),
            1000
        )
    )

    with obtener_conexion() as conexion:

        if modulo:

            filas = conexion.execute(
                """
                SELECT *
                FROM historial
                WHERE modulo = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (
                    modulo,
                    limite
                )
            ).fetchall()

        else:

            filas = conexion.execute(
                """
                SELECT *
                FROM historial
                ORDER BY id DESC
                LIMIT ?
                """,
                (
                    limite,
                )
            ).fetchall()

    return [
        dict(fila)
        for fila in filas
    ]


# ============================================================
# OBTENER ÚLTIMOS SNAPSHOTS
# ============================================================

def obtener_snapshots(
    limite: int = 20
) -> list[dict]:

    limite = max(
        1,
        min(
            int(limite),
            100
        )
    )

    with obtener_conexion() as conexion:

        filas = conexion.execute(
            """
            SELECT *
            FROM snapshots_sistema
            ORDER BY id DESC
            LIMIT ?
            """,
            (
                limite,
            )
        ).fetchall()

    return [
        dict(fila)
        for fila in filas
    ]


# ============================================================
# ELIMINAR REGISTRO
# ============================================================

def eliminar_historial(
    historial_id: int
) -> bool:

    with obtener_conexion() as conexion:

        cursor = conexion.execute(
            """
            DELETE FROM historial
            WHERE id = ?
            """,
            (
                historial_id,
            )
        )

        conexion.commit()

        return cursor.rowcount > 0


# ============================================================
# LIMPIAR HISTORIAL
# ============================================================

def limpiar_historial():
    """
    Elimina los análisis guardados.

    No elimina los snapshots de Mi Sistema.
    """

    with obtener_conexion() as conexion:

        conexion.execute(
            """
            DELETE FROM historial
            """
        )

        conexion.commit()


# ============================================================
# CONFIGURACIÓN
# ============================================================

def guardar_configuracion(
    clave: str,
    valor: Any
):

    with obtener_conexion() as conexion:

        conexion.execute(
            """
            INSERT INTO configuracion (
                clave,
                valor
            )
            VALUES (?, ?)

            ON CONFLICT(clave)
            DO UPDATE SET
                valor = excluded.valor
            """,
            (
                clave,
                _normalizar_valor(valor)
            )
        )

        conexion.commit()


def obtener_configuracion(
    clave: str,
    predeterminado=None
):

    with obtener_conexion() as conexion:

        fila = conexion.execute(
            """
            SELECT valor
            FROM configuracion
            WHERE clave = ?
            """,
            (
                clave,
            )
        ).fetchone()

    if fila is None:
        return predeterminado

    return fila["valor"]


# ============================================================
# ESTADÍSTICAS
# ============================================================

def obtener_estadisticas() -> dict:
    """
    Genera estadísticas generales del historial.
    """

    with obtener_conexion() as conexion:

        total = conexion.execute(
            """
            SELECT COUNT(*)
            FROM historial
            """
        ).fetchone()[0]

        por_modulo = conexion.execute(
            """
            SELECT
                modulo,
                COUNT(*) AS cantidad
            FROM historial
            GROUP BY modulo
            ORDER BY cantidad DESC
            """
        ).fetchall()

        snapshots = conexion.execute(
            """
            SELECT COUNT(*)
            FROM snapshots_sistema
            """
        ).fetchone()[0]

        puertos_abiertos = conexion.execute(
            """
            SELECT COUNT(*)
            FROM historial_puertos
            WHERE LOWER(estado) = 'abierto'
            """
        ).fetchone()[0]

    return {
        "total_analisis": total,

        "por_modulo": [
            dict(fila)
            for fila in por_modulo
        ],

        "snapshots_sistema": snapshots,

        "puertos_abiertos_detectados":
            puertos_abiertos
    }


# ============================================================
# INICIALIZACIÓN AUTOMÁTICA
# ============================================================

inicializar_base_datos()


# ============================================================
# PRUEBA DIRECTA
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("NETPRO - BASE DE DATOS")
    print("=" * 70)

    print()
    print(f"Base de datos:")
    print(DB_PATH)

    print()
    print("Estadísticas:")
    print(
        json.dumps(
            obtener_estadisticas(),
            indent=4,
            ensure_ascii=False
        )
    )

    # ============================================================
# CONSULTAS PARA LA INTERFAZ DE HISTORIAL
# ============================================================


def listar_historial(limite=500, modulo=None, busqueda=None):
    """
    Devuelve los registros generales almacenados en historial.
    """

    try:
        limite = int(limite)
    except (TypeError, ValueError):
        limite = 500

    if limite <= 0:
        limite = 500

    consulta = """
        SELECT
            id,
            fecha,
            modulo,
            objetivo,
            resumen,
            exitoso,
            error
        FROM historial
        WHERE 1 = 1
    """

    parametros = []

    # ========================================================
    # FILTRO POR MODULO
    # ========================================================

    if modulo and modulo != "Todos":

        consulta += """
            AND modulo = ?
        """

        parametros.append(modulo)

    # ========================================================
    # BUSQUEDA
    # ========================================================

    if busqueda:

        texto = f"%{busqueda}%"

        consulta += """
            AND (
                objetivo LIKE ?
                OR resumen LIKE ?
                OR modulo LIKE ?
            )
        """

        parametros.extend(
            [
                texto,
                texto,
                texto,
            ]
        )

    # ========================================================
    # ORDEN Y LIMITE
    # ========================================================

    consulta += """
        ORDER BY id DESC
        LIMIT ?
    """

    parametros.append(limite)

    with obtener_conexion() as conexion:

        filas = conexion.execute(
            consulta,
            parametros
        ).fetchall()

        return [
            dict(fila)
            for fila in filas
        ]


# ============================================================
# OBTENER ANALISIS
# ============================================================


def obtener_analisis(historial_id):
    """
    Obtiene el registro general y el detalle tecnico
    correspondiente al modulo.
    """

    with obtener_conexion() as conexion:

        # ====================================================
        # INFORMACION GENERAL
        # ====================================================

        fila = conexion.execute(
            """
            SELECT
                id,
                fecha,
                modulo,
                objetivo,
                resumen,
                exitoso,
                error
            FROM historial
            WHERE id = ?
            """,
            (historial_id,)
        ).fetchone()

        if fila is None:
            return None

        general = dict(fila)

        modulo = general.get("modulo")

        detalle = {}

        # ====================================================
        # IPv4
        # ====================================================

        if modulo == "IPv4":

            fila_detalle = conexion.execute(
                """
                SELECT *
                FROM historial_ipv4
                WHERE historial_id = ?
                """,
                (historial_id,)
            ).fetchone()

            if fila_detalle:
                detalle = dict(fila_detalle)

        # ====================================================
        # IPv6
        # ====================================================

        elif modulo == "IPv6":

            fila_detalle = conexion.execute(
                """
                SELECT *
                FROM historial_ipv6
                WHERE historial_id = ?
                """,
                (historial_id,)
            ).fetchone()

            if fila_detalle:
                detalle = dict(fila_detalle)

        # ====================================================
        # DNS
        # ====================================================

        elif modulo == "DNS":

            fila_detalle = conexion.execute(
                """
                SELECT *
                FROM historial_dns
                WHERE historial_id = ?
                """,
                (historial_id,)
            ).fetchone()

            if fila_detalle:

                detalle = dict(fila_detalle)

                dns_id = detalle.get("id")

                registros = conexion.execute(
                    """
                    SELECT *
                    FROM historial_dns_registros
                    WHERE dns_id = ?
                    ORDER BY id ASC
                    """,
                    (dns_id,)
                ).fetchall()

                detalle["registros_dns"] = [
                    dict(registro)
                    for registro in registros
                ]

        # ====================================================
        # PING
        # ====================================================

        elif modulo == "Ping":

            fila_detalle = conexion.execute(
                """
                SELECT *
                FROM historial_ping
                WHERE historial_id = ?
                """,
                (historial_id,)
            ).fetchone()

            if fila_detalle:
                detalle = dict(fila_detalle)

        # ====================================================
        # TRACEROUTE
        # ====================================================

        elif modulo == "Traceroute":

            filas = conexion.execute(
                """
                SELECT *
                FROM historial_traceroute
                WHERE historial_id = ?
                ORDER BY id ASC
                """,
                (historial_id,)
            ).fetchall()

            detalle = {
                "saltos": [
                    dict(registro)
                    for registro in filas
                ]
            }

        # ====================================================
        # NETWORK STATUS
        # ====================================================

        elif modulo == "Network Status":

            fila_detalle = conexion.execute(
                """
                SELECT *
                FROM historial_network_status
                WHERE historial_id = ?
                """,
                (historial_id,)
            ).fetchone()

            if fila_detalle:
                detalle = dict(fila_detalle)

        # ====================================================
        # PUERTOS
        # ====================================================

        elif modulo == "Puertos":

            filas = conexion.execute(
                """
                SELECT *
                FROM historial_puertos
                WHERE historial_id = ?
                ORDER BY puerto ASC
                """,
                (historial_id,)
            ).fetchall()

            detalle = {
                "puertos": [
                    dict(registro)
                    for registro in filas
                ]
            }

        # ====================================================
        # HTTP / HTTPS
        # ====================================================

        elif modulo in (
            "HTTP",
            "HTTP / HTTPS",
            "HTTP/HTTPS"
        ):

            fila_http = conexion.execute(
                """
                SELECT *
                FROM historial_http
                WHERE historial_id = ?
                """,
                (historial_id,)
            ).fetchone()

            if fila_http:

                detalle = dict(fila_http)

                http_id = detalle.get("id")

                # ============================================
                # HEADERS
                # ============================================

                try:

                    headers = conexion.execute(
                        """
                        SELECT *
                        FROM historial_http_headers
                        WHERE http_id = ?
                        ORDER BY id ASC
                        """,
                        (http_id,)
                    ).fetchall()

                    detalle["headers"] = [
                        dict(registro)
                        for registro in headers
                    ]

                except Exception:
                    detalle["headers"] = []

                # ============================================
                # SEGURIDAD
                # ============================================

                try:

                    seguridad = conexion.execute(
                        """
                        SELECT *
                        FROM historial_http_seguridad
                        WHERE http_id = ?
                        ORDER BY id ASC
                        """,
                        (http_id,)
                    ).fetchall()

                    detalle["seguridad"] = [
                        dict(registro)
                        for registro in seguridad
                    ]

                except Exception:
                    detalle["seguridad"] = []

                # ============================================
                # REDIRECCIONES
                # ============================================

                try:

                    redirecciones = conexion.execute(
                        """
                        SELECT *
                        FROM historial_http_redirecciones
                        WHERE http_id = ?
                        ORDER BY id ASC
                        """,
                        (http_id,)
                    ).fetchall()

                    detalle["redirecciones"] = [
                        dict(registro)
                        for registro in redirecciones
                    ]

                except Exception:
                    detalle["redirecciones"] = []

        # ====================================================
        # SISTEMA
        # ====================================================

        elif modulo in (
            "Sistema",
            "Mi Sistema"
        ):

            fila_sistema = conexion.execute(
                """
                SELECT *
                FROM snapshots_sistema
                WHERE historial_id = ?
                """,
                (historial_id,)
            ).fetchone()

            if fila_sistema:

                detalle = dict(fila_sistema)

                snapshot_id = detalle.get("id")

                tablas = {
                    "ram_modulos": "sistema_ram_modulos",
                    "gpus": "sistema_gpus",
                    "monitores": "sistema_monitores",
                    "discos": "sistema_discos",
                    "volumenes": "sistema_volumenes",
                    "adaptadores_red": "sistema_adaptadores_red",
                    "firewall": "sistema_firewall",
                }

                for nombre, tabla in tablas.items():

                    try:

                        registros = conexion.execute(
                            f"""
                            SELECT *
                            FROM {tabla}
                            WHERE snapshot_id = ?
                            ORDER BY id ASC
                            """,
                            (snapshot_id,)
                        ).fetchall()

                        detalle[nombre] = [
                            dict(registro)
                            for registro in registros
                        ]

                    except Exception:

                        detalle[nombre] = []

        # ====================================================
        # RESULTADO
        # ====================================================

        return {
            "general": general,
            "detalle": detalle,
        }


# ============================================================
# ELIMINAR ANALISIS
# ============================================================


def eliminar_analisis(historial_id):
    """
    Elimina un analisis del historial.

    Las tablas relacionadas que tengan ON DELETE CASCADE
    se eliminan automaticamente.
    """

    with obtener_conexion() as conexion:

        existe = conexion.execute(
            """
            SELECT id
            FROM historial
            WHERE id = ?
            """,
            (historial_id,)
        ).fetchone()

        if existe is None:
            return False

        conexion.execute(
            """
            DELETE FROM historial
            WHERE id = ?
            """,
            (historial_id,)
        )

        conexion.commit()

        return True