import json
import customtkinter as ctk
import csv
from datetime import datetime
from tkinter import filedialog

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    TableStyle,
) 
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from xml.sax.saxutils import escape

from tkinter import messagebox

from core.history import (
    listar_historial,
    obtener_analisis,
    eliminar_analisis,
)


class HistoryFrame(ctk.CTkFrame):

    # ============================================================
    # COLORES NETPRO
    # ============================================================

    FONDO = "#2b2b2b"
    PANEL = "#181818"
    PANEL_2 = "#202020"
    BORDE = "#444444"

    AZUL = "#3498db"
    AZUL_OSCURO = "#2878b5"

    TEXTO = "#ffffff"
    TEXTO_2 = "#b7b7b7"

    VERDE = "#2ecc71"
    ROJO = "#e74c3c"
    AMARILLO = "#f1c40f"

    
    # ============================================================
    # INICIALIZACION
    # ============================================================

    def __init__(self, master, **kwargs):

        super().__init__(
            master,
            fg_color=self.FONDO,
            **kwargs
        )

        self.registro_seleccionado = None
        self.botones_registros = []
        self.registros_filtrados = []

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        # ========================================================
        # SCROLL PRINCIPAL
        # ========================================================
        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=self.FONDO,
            corner_radius=0,
            scrollbar_fg_color=self.FONDO,
            scrollbar_button_color="#168BEB",
            scrollbar_button_hover_color="#36A5FF"
        )

        self.scroll.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.scroll.grid_columnconfigure(
            0,
            weight=1
        )

        # ========================================================
        # CONSTRUIR INTERFAZ
        # ========================================================

        self.crear_encabezado()
        self.crear_estadisticas()
        self.crear_filtros()
        self.crear_contenido()


        # ========================================================
        # CARGAR DATOS
        # ========================================================

        self.after(
            100,
            self.actualizar_historial
        )

    # ============================================================
    # ENCABEZADO
    # ============================================================

    def crear_encabezado(self):

        header = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=30,
            pady=(25, 12)
        )

        # ========================================================
        # TITULO
        # ========================================================

        titulo_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        titulo_frame.pack(
            side="left",
            fill="x",
            expand=True
        )

        ctk.CTkLabel(
            titulo_frame,
            text="📋 Historial",
            font=(
                "Arial",
                28,
                "bold"
            ),
            text_color=self.AZUL
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            titulo_frame,
            text=(
                "Consulta y analiza la actividad "
                "registrada por NetPro."
            ),
            font=(
                "Arial",
                13
            ),
            text_color=self.TEXTO_2
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        # ========================================================
        # BOTON ACTUALIZAR
        # ========================================================

        self.btn_actualizar = ctk.CTkButton(
            header,
            text="⟳ ACTUALIZAR",
            width=140,
            height=38,
            corner_radius=6,
            fg_color=self.AZUL_OSCURO,
            hover_color=self.AZUL,
            command=self.actualizar_historial
        )

        self.btn_actualizar.pack(
            side="right"
        )


        
        # BOTON EXPORTAR PDF
        self.btn_pdf = ctk.CTkButton(
            header,
            text="EXPORTAR PDF",
            width=125,
            height=38,
            fg_color=self.AZUL_OSCURO,
            hover_color=self.AZUL,
            command=self.exportar_pdf
        )

        self.btn_pdf.pack(
            side="right",
            padx=(0, 8)
        )

        # BOTON EXPORTAR CSV
        self.btn_csv = ctk.CTkButton(
            header,
            text="EXPORTAR CSV",
            width=125,
            height=38,
            fg_color=self.AZUL_OSCURO,
            hover_color=self.AZUL,
            command=self.exportar_csv
        )

        self.btn_csv.pack(
            side="right",
            padx=(0, 8)
        )


    # ============================================================
    # ESTADISTICAS
    # ============================================================

    def crear_estadisticas(self):

        contenedor = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent"
        )

        contenedor.pack(
            fill="x",
            padx=30,
            pady=(5, 15)
        )

        for columna in range(4):

            contenedor.grid_columnconfigure(
                columna,
                weight=1
            )

        self.stat_total = self.crear_tarjeta_estadistica(
            contenedor,
            0,
            "Total analisis"
        )

        self.stat_exitosos = self.crear_tarjeta_estadistica(
            contenedor,
            1,
            "Exitosos"
        )

        self.stat_errores = self.crear_tarjeta_estadistica(
            contenedor,
            2,
            "Errores"
        )

        self.stat_modulos = self.crear_tarjeta_estadistica(
            contenedor,
            3,
            "Modulos"
        )

    # ============================================================
    # TARJETA ESTADISTICA
    # ============================================================

    def crear_tarjeta_estadistica(
        self,
        master,
        columna,
        titulo
    ):

        tarjeta = ctk.CTkFrame(
            master,
            fg_color=self.PANEL,
            border_width=1,
            border_color=self.BORDE,
            corner_radius=8
        )

        tarjeta.grid(
            row=0,
            column=columna,
            sticky="ew",
            padx=6
        )

        ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=(
                "Arial",
                11
            ),
            text_color=self.TEXTO_2
        ).pack(
            pady=(13, 3)
        )

        valor = ctk.CTkLabel(
            tarjeta,
            text="0",
            font=(
                "Arial",
                24,
                "bold"
            ),
            text_color=self.TEXTO
        )

        valor.pack(
            pady=(0, 13)
        )

        return valor

    # ============================================================
    # FILTROS
    # ============================================================

    def crear_filtros(self):

        filtros = ctk.CTkFrame(
            self.scroll,
            fg_color=self.PANEL,
            border_width=1,
            border_color=self.BORDE,
            corner_radius=8
        )

        filtros.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        interior = ctk.CTkFrame(
            filtros,
            fg_color="transparent"
        )

        interior.pack(
            fill="x",
            padx=15,
            pady=14
        )

        # ========================================================
        # FILTRO MODULO
        # ========================================================

        ctk.CTkLabel(
            interior,
            text="Modulo",
            text_color=self.TEXTO_2
        ).pack(
            side="left",
            padx=(0, 8)
        )

        self.filtro_modulo = ctk.CTkComboBox(
            interior,
            values=[
                "Todos",
                "IPv4",
                "IPv6",
                "DNS",
                "Ping",
                "Traceroute",
                "Network Status",
                "Puertos",
                "HTTP",
                "Sistema",
            ],
            width=150,
            fg_color=self.PANEL_2,
            border_color=self.BORDE,
            button_color=self.AZUL_OSCURO,
            button_hover_color=self.AZUL,
            command=lambda _: self.actualizar_historial()
        )

        self.filtro_modulo.set(
            "Todos"
        )

        self.filtro_modulo.pack(
            side="left",
            padx=(0, 20)
        )

        # ========================================================
        # BUSQUEDA
        # ========================================================

        ctk.CTkLabel(
            interior,
            text="Buscar",
            text_color=self.TEXTO_2
        ).pack(
            side="left",
            padx=(0, 8)
        )

        self.entry_buscar = ctk.CTkEntry(
            interior,
            placeholder_text=(
                "IP, dominio, URL, host..."
            ),
            height=34,
            fg_color=self.PANEL_2,
            border_color=self.BORDE
        )

        self.entry_buscar.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.entry_buscar.bind(
            "<Return>",
            lambda event: self.actualizar_historial()
        )

        self.btn_buscar = ctk.CTkButton(
            interior,
            text="BUSCAR",
            width=100,
            height=34,
            fg_color=self.AZUL_OSCURO,
            hover_color=self.AZUL,
            command=self.actualizar_historial
        )

        self.btn_buscar.pack(
            side="left",
            padx=(10, 0)
        )

    # ============================================================
    # CONTENIDO PRINCIPAL
    # ============================================================

    def crear_contenido(self):

        contenido = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent"
        )

        contenido.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        contenido.grid_columnconfigure(
            0,
            weight=1
        )

        contenido.grid_columnconfigure(
            1,
            weight=1
        )

        contenido.grid_rowconfigure(
            0,
            weight=1
        )

        # ========================================================
        # PANEL IZQUIERDO
        # ========================================================

        panel_historial = ctk.CTkFrame(
            contenido,
            fg_color=self.PANEL,
            border_width=1,
            border_color=self.BORDE,
            corner_radius=8
        )

        panel_historial.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 7)
        )

        ctk.CTkLabel(
            panel_historial,
            text="Historial de analisis",
            font=(
                "Arial",
                16,
                "bold"
            ),
            text_color=self.TEXTO
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 10)
        )

        self.lista_historial = ctk.CTkScrollableFrame(
            panel_historial,
            fg_color="transparent",
            height=450
        )

        self.lista_historial.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        # ========================================================
        # PANEL DERECHO
        # ========================================================

        panel_detalle = ctk.CTkFrame(
            contenido,
            fg_color=self.PANEL,
            border_width=1,
            border_color=self.BORDE,
            corner_radius=8
        )

        panel_detalle.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(7, 0)
        )

        detalle_header = ctk.CTkFrame(
            panel_detalle,
            fg_color="transparent"
        )

        detalle_header.pack(
            fill="x",
            padx=18,
            pady=(16, 10)
        )

        ctk.CTkLabel(
            detalle_header,
            text="Detalle",
            font=(
                "Arial",
                16,
                "bold"
            ),
            text_color=self.TEXTO
        ).pack(
            side="left"
        )

        self.btn_eliminar = ctk.CTkButton(
            detalle_header,
            text="Eliminar",
            width=90,
            height=30,
            fg_color=self.PANEL_2,
            hover_color=self.ROJO,
            border_width=1,
            border_color=self.BORDE,
            state="disabled",
            command=self.eliminar_seleccionado
        )

        self.btn_eliminar.pack(
            side="right"
        )

        self.detalle_texto = ctk.CTkTextbox(
            panel_detalle,
            fg_color=self.PANEL,
            border_width=0,
            font=(
                "Consolas",
                12
            ),
            text_color=self.TEXTO,
            wrap="word",
            height=450
        )

        self.detalle_texto.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 18)
        )

        self.mostrar_mensaje_inicial()

    # ============================================================
    # MENSAJE INICIAL
    # ============================================================

    def mostrar_mensaje_inicial(self):

        texto = (
            "Selecciona un analisis para consultar "
            "su informacion detallada.\n\n"

            "NetPro almacena los resultados de los "
            "modulos compatibles en una base de datos "
            "SQLite local.\n\n"

            "El historial permite revisar actividad "
            "anterior sin mostrar el JSON interno "
            "directamente al usuario."
        )

        self.escribir_detalle(
            texto
        )

    # ============================================================
    # ACTUALIZAR HISTORIAL
    # ============================================================

    def actualizar_historial(self):

        try:

            registros = listar_historial(
                limite=500
            )

            modulo = self.filtro_modulo.get()

            buscar = (
                self.entry_buscar
                .get()
                .strip()
                .lower()
            )

            # ====================================================
            # FILTROS
            # ====================================================

            filtrados = []

            for registro in registros:

                if (
                    modulo != "Todos"
                    and registro.get("modulo") != modulo
                ):
                    continue

                if buscar:

                    contenido = (
                        f"{registro.get('objetivo', '')} "
                        f"{registro.get('resumen', '')} "
                        f"{registro.get('modulo', '')}"
                    ).lower()

                    if buscar not in contenido:
                        continue

                filtrados.append(
                    registro
                )

            # ====================================================
            # ACTUALIZAR INTERFAZ
            # ====================================================

            
            self.registros_filtrados = filtrados.copy()

            self.cargar_lista(
                filtrados
            )

            self.actualizar_estadisticas(
                registros
            )

        except Exception as error:

            self.escribir_detalle(
                "No fue posible cargar el historial.\n\n"
                f"{error}"
            )

    # ============================================================
    # ACTUALIZAR ESTADISTICAS
    # ============================================================

    def actualizar_estadisticas(
        self,
        registros
    ):

        total = len(
            registros
        )

        exitosos = sum(
            1
            for registro in registros
            if registro.get("exitoso")
        )

        errores = (
            total - exitosos
        )

        modulos = {
            registro.get("modulo")
            for registro in registros
            if registro.get("modulo")
        }

        self.stat_total.configure(
            text=str(total)
        )

        self.stat_exitosos.configure(
            text=str(exitosos)
        )

        self.stat_errores.configure(
            text=str(errores)
        )

        self.stat_modulos.configure(
            text=str(
                len(modulos)
            )
        )

    # ============================================================
    # CARGAR LISTA
    # ============================================================

    def cargar_lista(
        self,
        registros
    ):

        for widget in (
            self.lista_historial
            .winfo_children()
        ):

            widget.destroy()

        self.botones_registros.clear()

        if not registros:

            ctk.CTkLabel(
                self.lista_historial,
                text=(
                    "No hay analisis para mostrar."
                ),
                text_color=self.TEXTO_2
            ).pack(
                pady=30
            )

            return

        for registro in registros:

            self.crear_registro(
                registro
            )

    # ============================================================
    # CREAR REGISTRO
    # ============================================================

    def crear_registro(
        self,
        registro
    ):

        contenedor = ctk.CTkFrame(
            self.lista_historial,
            fg_color=self.PANEL_2,
            border_width=1,
            border_color=self.BORDE,
            corner_radius=7
        )

        contenedor.pack(
            fill="x",
            pady=5
        )

        # ========================================================
        # PARTE SUPERIOR
        # ========================================================

        superior = ctk.CTkFrame(
            contenedor,
            fg_color="transparent"
        )

        superior.pack(
            fill="x",
            padx=12,
            pady=(10, 3)
        )

        modulo = registro.get(
            "modulo",
            "Desconocido"
        )

        exitoso = registro.get(
            "exitoso",
            0
        )

        estado = (
            "● OK"
            if exitoso
            else "● ERROR"
        )

        color_estado = (
            self.VERDE
            if exitoso
            else self.ROJO
        )

        ctk.CTkLabel(
            superior,
            text=modulo,
            font=(
                "Arial",
                13,
                "bold"
            ),
            text_color=self.AZUL
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            superior,
            text=estado,
            font=(
                "Arial",
                10,
                "bold"
            ),
            text_color=color_estado
        ).pack(
            side="right"
        )

        # ========================================================
        # OBJETIVO
        # ========================================================

        objetivo = registro.get(
            "objetivo"
        ) or "Sin objetivo"

        ctk.CTkLabel(
            contenedor,
            text=objetivo,
            font=(
                "Arial",
                12
            ),
            text_color=self.TEXTO,
            anchor="w"
        ).pack(
            fill="x",
            padx=12
        )

        # ========================================================
        # FECHA Y RESUMEN
        # ========================================================

        fecha = registro.get(
            "fecha",
            ""
        )

        resumen = registro.get(
            "resumen"
        ) or ""

        inferior = ctk.CTkLabel(
            contenedor,
            text=(
                f"{fecha}\n"
                f"{resumen}"
            ),
            font=(
                "Arial",
                10
            ),
            text_color=self.TEXTO_2,
            justify="left",
            anchor="w"
        )

        inferior.pack(
            fill="x",
            padx=12,
            pady=(3, 6)
        )

        # ========================================================
        # BOTON DETALLE
        # ========================================================

        boton = ctk.CTkButton(
            contenedor,
            text="VER DETALLE",
            height=30,
            fg_color=self.AZUL_OSCURO,
            hover_color=self.AZUL,
            command=lambda r=registro: (
                self.seleccionar_registro(r)
            )
        )

        boton.pack(
            fill="x",
            padx=12,
            pady=(0, 10)
        )

        self.botones_registros.append(
            boton
        )

    # ============================================================
    # SELECCIONAR REGISTRO
    # ============================================================

    def seleccionar_registro(
        self,
        registro
    ):

        historial_id = registro.get(
            "id"
        )

        if historial_id is None:
            return

        try:

            detalle = obtener_analisis(
                historial_id
            )

            if not detalle:

                self.escribir_detalle(
                    "No se encontro informacion "
                    "para este analisis."
                )

                return

            self.registro_seleccionado = (
                historial_id
            )

            self.btn_eliminar.configure(
                state="normal"
            )

            texto = self.formatear_detalle(
                detalle
            )

            self.escribir_detalle(
                texto
            )

        except Exception as error:

            self.escribir_detalle(
                "No fue posible cargar "
                "el detalle del analisis.\n\n"
                f"{error}"
            )

    # ============================================================
    # FORMATEAR DETALLE
    # ============================================================

    def formatear_detalle(
        self,
        datos
    ):

        general = datos.get(
            "general",
            {}
        )

        detalle = datos.get(
            "detalle",
            {}
        )

        modulo = general.get(
            "modulo",
            "Desconocido"
        )

        lineas = []

        # ========================================================
        # INFORMACION GENERAL
        # ========================================================

        lineas.append(
            "INFORMACION GENERAL"
        )

        lineas.append(
            "─" * 52
        )

        lineas.append(
            f"Modulo:      {modulo}"
        )

        lineas.append(
            f"Fecha:       {general.get('fecha', '')}"
        )

        lineas.append(
            f"Objetivo:    {general.get('objetivo', '')}"
        )

        lineas.append(
            f"Resumen:     {general.get('resumen', '')}"
        )

        estado = (
            "Exitoso"
            if general.get("exitoso")
            else "Error"
        )

        lineas.append(
            f"Estado:      {estado}"
        )

        if general.get("error"):

            lineas.append(
                f"Error:       {general.get('error')}"
            )

        # ========================================================
        # DETALLE TECNICO
        # ========================================================

        lineas.append("")
        lineas.append(
            "DETALLE TECNICO"
        )

        lineas.append(
            "─" * 52
        )

        if not detalle:

            lineas.append(
                "No hay informacion tecnica adicional."
            )

            return "\n".join(
                lineas
            )

        # ========================================================
        # CAMPOS INTERNOS
        # ========================================================

        ignorar = {
            "id",
            "historial_id",
            "datos_json",
            "resultado_json",
            "raw_json",
            "headers_json",
            "seguridad_json",
        }

        for clave, valor in detalle.items():

            if clave in ignorar:
                continue

            nombre = self.nombre_amigable(
                clave
            )

            valor_formateado = (
                self.formatear_valor(
                    clave,
                    valor
                )
            )

            lineas.append(
                f"{nombre}:"
            )

            lineas.append(
                f"  {valor_formateado}"
            )

            lineas.append("")

        return "\n".join(
            lineas
        )

    # ============================================================
    # NOMBRES AMIGABLES
    # ============================================================

    def nombre_amigable(
        self,
        clave
    ):

        nombres = {

            # IPv4
            "ip": "Direccion IP",
            "cidr": "CIDR",
            "network": "Red",
            "netmask": "Mascara de red",
            "wildcard": "Wildcard",
            "broadcast": "Broadcast",
            "first_host": "Primer host",
            "last_host": "Ultimo host",
            "total_addresses": "Direcciones totales",
            "usable_hosts": "Hosts utilizables",
            "private": "IP privada",
            "version": "Version IP",

            # IPv6
            "first_address": "Primera direccion",
            "last_address": "Ultima direccion",
            "expanded": "Direccion expandida",
            "compressed": "Direccion comprimida",
            "hexadecimal": "Hextetos",
            "binary": "Representacion binaria",
            "global_ip": "Global",
            "private_ip": "Privada",
            "link_local": "Link-Local",
            "multicast": "Multicast",
            "loopback": "Loopback",
            "unspecified": "Unspecified",
            "reserved": "Reservada",
            "ipv4_mapped": "IPv4 mapeada",
            "scope_id": "Scope ID",

            # DNS
            "hostname": "Hostname",
            "direccion": "Direccion",
            "familia": "Familia",
            "tipo": "Tipo",
            "ttl": "TTL",
            "registros_dns": "Registros DNS",

            # Ping
            "latencia_ms": "Latencia",
            "tiempo_ms": "Tiempo",
            "perdida_paquetes": "Perdida de paquetes",
            "paquetes_enviados": "Paquetes enviados",
            "paquetes_recibidos": "Paquetes recibidos",

            # Traceroute
            "saltos": "Saltos",

            # Puertos
            "puertos": "Puertos",
            "puerto": "Puerto",
            "protocolo": "Protocolo",
            "estado": "Estado",
            "servicio": "Servicio",

            # HTTP
            "url": "URL",
            "status_code": "Estado HTTP",
            "metodo": "Metodo",
            "servidor": "Servidor",
            "tls": "TLS",
            "headers": "Headers",
            "seguridad": "Seguridad",
            "redirecciones": "Redirecciones",

            # Sistema
            "ram_modulos": "Modulos RAM",
            "gpus": "Tarjetas graficas",
            "monitores": "Monitores",
            "discos": "Discos",
            "volumenes": "Volumenes",
            "adaptadores_red": "Adaptadores de red",
            "firewall": "Firewall",
        }

        if clave in nombres:
            return nombres[clave]

        return (
            clave
            .replace("_", " ")
            .strip()
            .capitalize()
        )

    # ============================================================
    # FORMATEAR VALOR
    # ============================================================

    def formatear_valor(
        self,
        clave,
        valor
    ):

        if valor is None:
            return "No disponible"

        # ========================================================
        # CAMPOS BOOLEANOS GUARDADOS COMO 0 / 1
        # ========================================================

        campos_booleanos = {
            "private",
            "global_ip",
            "private_ip",
            "link_local",
            "multicast",
            "loopback",
            "unspecified",
            "reserved",
            "tls",
        }

        if clave in campos_booleanos:

            return (
                "Si"
                if bool(valor)
                else "No"
            )

        # ========================================================
        # BOOLEAN PYTHON
        # ========================================================

        if isinstance(
            valor,
            bool
        ):

            return (
                "Si"
                if valor
                else "No"
            )

        # ========================================================
        # LISTA
        # ========================================================

        if isinstance(
            valor,
            (list, tuple)
        ):

            if not valor:
                return "Sin registros"

            lineas = []

            for elemento in valor:

                if isinstance(
                    elemento,
                    dict
                ):

                    partes = []

                    for subclave, subvalor in elemento.items():

                        if subclave in {
                            "id",
                            "historial_id",
                            "dns_id",
                            "http_id",
                            "snapshot_id",
                        }:
                            continue

                        nombre = self.nombre_amigable(
                            subclave
                        )

                        partes.append(
                            f"{nombre}: {subvalor}"
                        )

                    lineas.append(
                        " | ".join(
                            partes
                        )
                    )

                else:

                    lineas.append(
                        str(elemento)
                    )

            return "\n  ".join(
                lineas
            )

        # ========================================================
        # DICCIONARIO
        # ========================================================

        if isinstance(
            valor,
            dict
        ):

            lineas = []

            for subclave, contenido in valor.items():

                nombre = self.nombre_amigable(
                    subclave
                )

                lineas.append(
                    f"{nombre}: {contenido}"
                )

            return "\n  ".join(
                lineas
            )

        # ========================================================
        # JSON GUARDADO COMO TEXTO
        # ========================================================

        if isinstance(
            valor,
            str
        ):

            texto = valor.strip()

            if (
                texto.startswith("[")
                or texto.startswith("{")
            ):

                try:

                    convertido = json.loads(
                        texto
                    )

                    return self.formatear_valor(
                        clave,
                        convertido
                    )

                except (
                    json.JSONDecodeError,
                    TypeError
                ):
                    pass

        # ========================================================
        # VALOR NORMAL
        # ========================================================

        return str(
            valor
        )

    # ============================================================
    # ESCRIBIR DETALLE
    # ============================================================

    def escribir_detalle(
        self,
        texto
    ):

        self.detalle_texto.configure(
            state="normal"
        )

        self.detalle_texto.delete(
            "1.0",
            "end"
        )

        self.detalle_texto.insert(
            "1.0",
            texto
        )

        self.detalle_texto.configure(
            state="disabled"
        )

    # ============================================================
    # ELIMINAR REGISTRO
    # ============================================================

    def eliminar_seleccionado(self):

        if self.registro_seleccionado is None:
            return

        confirmar = messagebox.askyesno(
            "Eliminar analisis",
            (
                "¿Deseas eliminar este registro "
                "del historial?\n\n"
                "Esta accion no se puede deshacer."
            )
        )

        if not confirmar:
            return

        try:

            eliminado = eliminar_analisis(
                self.registro_seleccionado
            )

            if not eliminado:

                messagebox.showwarning(
                    "NetPro",
                    "El registro ya no existe."
                )

                self.actualizar_historial()

                return

            self.registro_seleccionado = None

            self.btn_eliminar.configure(
                state="disabled"
            )

            self.mostrar_mensaje_inicial()

            self.actualizar_historial()

        except Exception as error:

            messagebox.showerror(
                "NetPro",
                (
                    "No fue posible eliminar "
                    "el analisis.\n\n"
                    f"{error}"
                )
            )

    
    # ============================================================
    # EXPORTAR HISTORIAL A CSV
    # ============================================================

    def exportar_csv(self):

        registros = self.registros_filtrados

        if not registros:
            messagebox.showwarning(
                "NetPro",
                "No hay registros para exportar."
            )
            return

        ruta = filedialog.asksaveasfilename(
            title="Guardar historial NetPro",
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv")],
            initialfile="NetPro_Historial.csv"
        )

        if not ruta:
            return

        try:
            with open(
                ruta,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as archivo:

                escritor = csv.writer(
                    archivo,
                    delimiter=";"
                )

                escritor.writerow([
                    "ID",
                    "Fecha",
                    "Modulo",
                    "Objetivo",
                    "Estado",
                    "Resumen",
                    "Error"
                ])

                for registro in registros:

                    estado = (
                        "Exitoso"
                        if registro.get("exitoso")
                        else "Error"
                    )

                    escritor.writerow([
                        registro.get("id", ""),
                        registro.get("fecha", ""),
                        registro.get("modulo", ""),
                        registro.get("objetivo", ""),
                        estado,
                        registro.get("resumen", ""),
                        registro.get("error", "")
                    ])

            messagebox.showinfo(
                "NetPro",
                "Historial exportado correctamente a CSV."
            )

        except Exception as error:
            messagebox.showerror(
                "NetPro",
                f"No fue posible exportar el CSV:\n{error}"
            )

    
   
    # ============================================================
    # EXPORTAR HISTORIAL A PDF - NETPRO
    # ============================================================

    def exportar_pdf(self):

        registros = self.registros_filtrados

        if not registros:
            messagebox.showwarning(
                "NetPro",
                "No hay registros para exportar."
            )
            return

        ruta = filedialog.asksaveasfilename(
            title="Exportar historial NetPro",
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            initialfile="NetPro_Historial.pdf"
        )

        if not ruta:
            return

        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            from reportlab.lib.enums import TA_LEFT
            from reportlab.platypus import (
                LongTable,
                HRFlowable,
                CondPageBreak,
            )
            from pathlib import Path
            import os

            # Fuentes Unicode para caracteres especiales
            fuentes = [
                (
                    "C:/Windows/Fonts/arial.ttf",
                    "C:/Windows/Fonts/arialbd.ttf"
                ),
                (
                    "C:/Windows/Fonts/calibri.ttf",
                    "C:/Windows/Fonts/calibrib.ttf"
                ),
            ]

            fuente = "Helvetica"
            fuente_negrita = "Helvetica-Bold"

            for normal, negrita in fuentes:
                if os.path.isfile(normal) and os.path.isfile(negrita):
                    pdfmetrics.registerFont(
                        TTFont("NetProRegular", normal)
                    )
                    pdfmetrics.registerFont(
                        TTFont("NetProBold", negrita)
                    )
                    pdfmetrics.registerFontFamily(
                        "NetProRegular",
                        normal="NetProRegular",
                        bold="NetProBold"
                    )
                    fuente = "NetProRegular"
                    fuente_negrita = "NetProBold"
                    break

            azul = colors.HexColor("#2878B5")
            azul_claro = colors.HexColor("#EAF3FA")
            gris = colors.HexColor("#555555")
            borde = colors.HexColor("#DDE4EA")

            documento = SimpleDocTemplate(
                ruta,
                pagesize=A4,
                leftMargin=1.7 * cm,
                rightMargin=1.7 * cm,
                topMargin=1.9 * cm,
                bottomMargin=1.8 * cm
            )

            estilos = getSampleStyleSheet()

            estilo_titulo = ParagraphStyle(
                "NPTitulo",
                fontName=fuente_negrita,
                fontSize=18,
                leading=23,
                textColor=azul,
                alignment=TA_CENTER,
                spaceAfter=8
            )

            estilo_subtitulo = ParagraphStyle(
                "NPSubtitulo",
                fontName=fuente,
                fontSize=9,
                leading=13,
                textColor=gris,
                alignment=TA_CENTER,
                spaceAfter=14
            )

            estilo_modulo = ParagraphStyle(
                "NPModulo",
                fontName=fuente_negrita,
                fontSize=11,
                leading=15,
                textColor=azul,
                spaceBefore=10,
                spaceAfter=6,
                keepWithNext=True
            )

            estilo_celda = ParagraphStyle(
                "NPCelda",
                fontName=fuente,
                fontSize=8,
                leading=11,
                splitLongWords=True,
                wordWrap="CJK"
            )

            estilo_etiqueta = ParagraphStyle(
                "NPEtiqueta",
                parent=estilo_celda,
                fontName=fuente_negrita,
                textColor=azul
            )

            estilo_seccion = ParagraphStyle(
                "NPSeccion",
                fontName=fuente_negrita,
                fontSize=9,
                leading=13,
                textColor=azul,
                spaceBefore=9,
                spaceAfter=5,
                keepWithNext=True
            )

            def limpiar(valor):
                if valor is None:
                    return "No disponible"

                if isinstance(valor, bool):
                    return "Si" if valor else "No"

                return str(valor)

            def parrafo(valor, estilo=estilo_celda):
                texto = escape(limpiar(valor))
                texto = texto.replace("\n", "<br/>")
                return Paragraph(texto, estilo)

            def crear_tabla(campos):
                filas = []

                for nombre, valor in campos:
                    filas.append([
                        parrafo(nombre, estilo_etiqueta),
                        parrafo(valor)
                    ])

                tabla = LongTable(
                    filas,
                    colWidths=[4.1 * cm, 13 * cm],
                    hAlign="LEFT",
                    repeatRows=0
                )

                tabla.setStyle(TableStyle([
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BACKGROUND", (0, 0), (0, -1), azul_claro),
                    ("LINEBELOW", (0, 0), (-1, -1), 0.3, borde),
                    ("LEFTPADDING", (0, 0), (-1, -1), 7),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]))

                return tabla

            contenido = []

            contenido.append(
                Paragraph(
                    "NETPRO",
                    estilo_titulo
                )
            )

            contenido.append(
                Paragraph(
                    "INFORME DE HISTORIAL DE ANALISIS",
                    estilo_subtitulo
                )
            )

            fecha_exportacion = datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            )

            exitosos = sum(
                1 for r in registros if r.get("exitoso")
            )

            contenido.append(
                crear_tabla([
                    ("Fecha de exportacion", fecha_exportacion),
                    ("Total de analisis", len(registros)),
                    ("Exitosos", exitosos),
                    ("Errores", len(registros) - exitosos),
                    (
                        "Modulos",
                        len({
                            r.get("modulo")
                            for r in registros
                            if r.get("modulo")
                        })
                    )
                ])
            )

            contenido.append(Spacer(1, 12))

            # Campos internos que no deben mostrarse
            ignorar = {
                "id",
                "historial_id",
                "datos_json",
                "resultado_json",
                "raw_json",
                "headers_json",
                "seguridad_json",
            }

            for numero, registro in enumerate(registros, 1):

                modulo = registro.get(
                    "modulo", "Desconocido"
                )

                contenido.append(
                CondPageBreak(8 * cm)
                )

                contenido.append(
                    Paragraph(
                        f"{numero}. {escape(str(modulo))}",
                        estilo_modulo
                    )
                )

                estado = (
                    "Exitoso"
                    if registro.get("exitoso")
                    else "Error"
                )

                campos_generales = [
                    ("Fecha", registro.get("fecha", "")),
                    ("Objetivo", registro.get("objetivo", "")),
                    ("Estado", estado),
                    ("Resumen", registro.get("resumen", "")),
                ]

                if registro.get("error"):
                    campos_generales.append(
                        ("Error", registro.get("error"))
                    )

                contenido.append(
                    crear_tabla(campos_generales)
                )

                historial_id = registro.get("id")

                if historial_id is None:
                    continue

                datos = obtener_analisis(historial_id)

                if not datos:
                    continue

                detalle = datos.get("detalle", {})

                if not isinstance(detalle, dict):
                    continue

                campos_tecnicos = []

                for clave, valor in detalle.items():

                    if clave in ignorar:
                        continue

                    nombre = self.nombre_amigable(clave)

                    # Reutiliza el formato existente
                    # del modulo Historial.
                    valor = self.formatear_valor(
                        clave,
                        valor
                    )

                    campos_tecnicos.append(
                        (nombre, valor)
                    )

                if campos_tecnicos:

                    contenido.append(
                        Paragraph(
                            "DETALLE TECNICO",
                            estilo_seccion
                        )
                    )

                    contenido.append(
                        crear_tabla(campos_tecnicos)
                    )

                contenido.append(Spacer(1, 10))

            def pie_pagina(canvas, doc):

                canvas.saveState()

                ancho, alto = A4

                canvas.setStrokeColor(borde)
                canvas.line(
                    1.7 * cm,
                    1.35 * cm,
                    ancho - 1.7 * cm,
                    1.35 * cm
                )

                canvas.setFont(fuente, 8)
                canvas.setFillColor(gris)

                canvas.drawString(
                    1.7 * cm,
                    1.05 * cm,
                    "NetPro - Network & Security Toolkit"
                )

                canvas.drawRightString(
                    ancho - 1.7 * cm,
                    1.05 * cm,
                    f"Pagina {doc.page}"
                )

                canvas.restoreState()

            documento.build(
                contenido,
                onFirstPage=pie_pagina,
                onLaterPages=pie_pagina
            )

            messagebox.showinfo(
                "NetPro",
                "Informe PDF generado correctamente."
            )

        except Exception as error:

            messagebox.showerror(
                "NetPro",
                f"No fue posible generar el PDF:\n{error}"
            )
