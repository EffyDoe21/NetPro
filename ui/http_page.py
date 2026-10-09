import customtkinter as ctk
import threading
from tkinter import messagebox

from core.http_analyzer import (
    analizar_http,
    resumir_headers_seguridad,
    descripcion_codigo_http
)

from AI.ollama_client import generar_respuesta


class HTTPFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        # ==========================================================
        # ESTADO
        # ==========================================================

        self.resultado = None
        self.analizando = False
        self.ia_analizando = False

        # ==========================================================
        # COLORES NETPRO
        # ==========================================================

        self.COLOR_FONDO = "#2B2B2B"
        self.COLOR_PANEL = "#1A1A1A"
        self.COLOR_PANEL_SECUNDARIO = "#242424"

        self.COLOR_AZUL = "#3B8ED0"
        self.COLOR_AZUL_HOVER = "#36719F"

        self.COLOR_VERDE = "#2ECC71"
        self.COLOR_ROJO = "#E74C3C"
        self.COLOR_AMARILLO = "#F1C40F"

        self.COLOR_TEXTO = "#FFFFFF"
        self.COLOR_SECUNDARIO = "#A0A0A0"

        # ==========================================================
        # GRID PRINCIPAL
        # ==========================================================

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # ==========================================================
        # ENCABEZADO
        # ==========================================================

        encabezado = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        encabezado.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(20, 5)
        )

        encabezado.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            encabezado,
            text="🌍 HTTP / HTTPS",
            font=("Arial", 28, "bold"),
            text_color=self.COLOR_AZUL
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 4)
        )

        ctk.CTkLabel(
            encabezado,
            text=(
                "Analiza respuestas HTTP, conexiones HTTPS, "
                "TLS y encabezados de seguridad."
            ),
            font=("Arial", 13),
            text_color=self.COLOR_TEXTO
        ).grid(
            row=1,
            column=0,
            sticky="w"
        )

        # ==========================================================
        # URL
        # ==========================================================

        panel_url = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        panel_url.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=(10, 5)
        )

        panel_url.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel_url,
            text="URL",
            font=("Arial", 12),
            text_color=self.COLOR_AZUL
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=(0, 5)
        )

        self.entry_url = ctk.CTkEntry(
            panel_url,
            placeholder_text="Ejemplo: https://example.com",
            height=36
        )

        self.entry_url.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=0
        )

        self.entry_url.bind(
            "<Return>",
            lambda event: self.iniciar_analisis()
        )

        self.btn_analizar = ctk.CTkButton(
            panel_url,
            text="🌐 ANALIZAR",
            width=325,
            height=36,
            font=("Arial", 12),
            fg_color=self.COLOR_AZUL,
            hover_color=self.COLOR_AZUL_HOVER,
            command=self.iniciar_analisis
        )

        self.btn_analizar.grid(
            row=2,
            column=0,
            sticky="w",
            pady=(12, 5)
        )

        # ==========================================================
        # RESUMEN
        # ==========================================================

        panel_resumen = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        panel_resumen.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=25,
            pady=(8, 5)
        )

        for columna in range(4):
            panel_resumen.grid_columnconfigure(
                columna,
                weight=1
            )

        self.card_protocolo = self.crear_card(
            panel_resumen,
            0,
            "Protocolo",
            "—"
        )

        self.card_estado = self.crear_card(
            panel_resumen,
            1,
            "Estado HTTP",
            "—"
        )

        self.card_tiempo = self.crear_card(
            panel_resumen,
            2,
            "Tiempo",
            "—"
        )

        self.card_tls = self.crear_card(
            panel_resumen,
            3,
            "TLS",
            "—"
        )

        # ==========================================================
        # SEPARADOR
        # ==========================================================

        separador = ctk.CTkFrame(
            self,
            height=1,
            fg_color="#444444"
        )

        separador.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=25,
            pady=(5, 8)
        )

        # ==========================================================
        # ÁREA CENTRAL
        # ==========================================================

        self.area_central = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.area_central.grid(
            row=4,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(0, 20)
        )

        self.area_central.grid_rowconfigure(0, weight=1)

        self.area_central.grid_columnconfigure(
            0,
            weight=1,
            minsize=250
        )

        self.area_central.grid_columnconfigure(
            1,
            weight=0,
            minsize=12
        )

        self.area_central.grid_columnconfigure(
            2,
            weight=1,
            minsize=250
        )

        # ==========================================================
        # PANEL RESULTADOS
        # ==========================================================

        panel_resultados = ctk.CTkFrame(
            self.area_central,
            fg_color=self.COLOR_PANEL,
            corner_radius=8
        )

        panel_resultados.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        panel_resultados.grid_columnconfigure(0, weight=1)
        panel_resultados.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            panel_resultados,
            text="Resultados",
            font=("Arial", 17, "bold"),
            text_color=self.COLOR_TEXTO
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(15, 8)
        )

        self.scroll_resultados = ctk.CTkScrollableFrame(
            panel_resultados,
            fg_color=self.COLOR_PANEL
        )

        self.scroll_resultados.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=8,
            pady=(0, 8)
        )

        self.scroll_resultados.grid_columnconfigure(
            0,
            weight=1
        )

        # ==========================================================
        # PANEL NETPRO AI
        # ==========================================================

        panel_ia = ctk.CTkFrame(
            self.area_central,
            fg_color=self.COLOR_PANEL,
            corner_radius=8
        )

        panel_ia.grid(
            row=0,
            column=2,
            sticky="nsew"
        )

        panel_ia.grid_columnconfigure(0, weight=1)
        panel_ia.grid_rowconfigure(2, weight=1)

        # ==========================================================
        # CABECERA IA
        # ==========================================================

        cabecera_ia = ctk.CTkFrame(
            panel_ia,
            fg_color="transparent"
        )

        cabecera_ia.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(15, 8)
        )

        cabecera_ia.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            cabecera_ia,
            text="✦  NetPro AI",
            font=("Arial", 17, "bold"),
            text_color=self.COLOR_TEXTO
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.label_ia_estado = ctk.CTkLabel(
            cabecera_ia,
            text="● LOCAL",
            font=("Arial", 10, "bold"),
            text_color=self.COLOR_VERDE
        )

        self.label_ia_estado.grid(
            row=0,
            column=1,
            sticky="e"
        )

        # ==========================================================
        # BOTÓN IA
        # ==========================================================

        self.btn_ia = ctk.CTkButton(
            panel_ia,
            text="✦  ANALIZAR CON NETPRO AI",
            height=36,
            font=("Arial", 11, "bold"),
            fg_color=self.COLOR_AZUL,
            hover_color=self.COLOR_AZUL_HOVER,
            command=self.iniciar_analisis_ia,
            state="disabled"
        )

        self.btn_ia.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 10)
        )

        # ==========================================================
        # TEXTO IA
        # ==========================================================

        self.texto_ia = ctk.CTkTextbox(
            panel_ia,
            wrap="word",
            font=("Consolas", 11),
            fg_color=self.COLOR_PANEL,
            corner_radius=6,
            border_width=0
        )

        self.texto_ia.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(0, 18)
        )

        self.mostrar_texto_ia(
            "Introduce una URL y realiza un análisis para "
            "obtener una interpretación educativa mediante "
            "NetPro AI."
        )

        self.mostrar_estado_inicial()

    # ==========================================================
    # CREAR CARD
    # ==========================================================

    def crear_card(
        self,
        parent,
        columna,
        titulo,
        valor
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        frame.grid(
            row=0,
            column=columna,
            sticky="ew",
            padx=5
        )

        ctk.CTkLabel(
            frame,
            text=titulo,
            font=("Arial", 10),
            text_color=self.COLOR_SECUNDARIO
        ).pack()

        label = ctk.CTkLabel(
            frame,
            text=valor,
            font=("Arial", 20, "bold"),
            text_color=self.COLOR_TEXTO
        )

        label.pack(pady=(2, 3))

        return label

    # ==========================================================
    # ESTADO INICIAL
    # ==========================================================

    def mostrar_estado_inicial(self):

        self.limpiar_resultados()

        texto = (
            "Introduce una URL para comenzar.\n\n"
            "NetPro analizará:\n\n"
            "• Código de estado HTTP\n"
            "• Tiempo de respuesta\n"
            "• Protocolo HTTP / HTTPS\n"
            "• Redirecciones\n"
            "• Información TLS\n"
            "• Certificado digital\n"
            "• Headers HTTP\n"
            "• Headers de seguridad\n\n"
            "Posteriormente NetPro AI puede interpretar "
            "los resultados obtenidos."
        )

        ctk.CTkLabel(
            self.scroll_resultados,
            text=texto,
            justify="left",
            anchor="nw",
            font=("Consolas", 11),
            text_color=self.COLOR_SECUNDARIO
        ).grid(
            row=0,
            column=0,
            sticky="nw",
            padx=15,
            pady=15
        )

    # ==========================================================
    # LIMPIAR RESULTADOS
    # ==========================================================

    def limpiar_resultados(self):

        for widget in self.scroll_resultados.winfo_children():
            widget.destroy()

    # ==========================================================
    # INICIAR ANÁLISIS
    # ==========================================================

    def iniciar_analisis(self):

        if self.analizando:
            return

        url = self.entry_url.get().strip()

        if not url:

            messagebox.showwarning(
                "NetPro",
                "Introduce una URL para analizar."
            )

            return

        self.analizando = True
        self.resultado = None

        self.btn_analizar.configure(
            text="⏳ ANALIZANDO...",
            state="disabled"
        )

        self.btn_ia.configure(
            state="disabled"
        )

        self.card_protocolo.configure(
            text="..."
        )

        self.card_estado.configure(
            text="..."
        )

        self.card_tiempo.configure(
            text="..."
        )

        self.card_tls.configure(
            text="..."
        )

        self.mostrar_texto_ia(
            "Esperando los resultados técnicos de NetPro..."
        )

        threading.Thread(
            target=self.ejecutar_analisis,
            args=(url,),
            daemon=True
        ).start()

    # ==========================================================
    # EJECUTAR ANÁLISIS
    # ==========================================================

    def ejecutar_analisis(
        self,
        url
    ):

        try:

            resultado = analizar_http(
                url
            )

            self.after(
                0,
                lambda:
                    self.finalizar_analisis(
                        resultado
                    )
            )

        except Exception as error:

            mensaje = str(error)

            self.after(
                0,
                lambda:
                    self.mostrar_error(
                        mensaje
                    )
            )

    # ==========================================================
    # FINALIZAR ANÁLISIS
    # ==========================================================

    def finalizar_analisis(
        self,
        resultado
    ):

        self.analizando = False
        self.resultado = resultado

        self.btn_analizar.configure(
            text="🌐 ANALIZAR",
            state="normal"
        )

        self.btn_ia.configure(
            state="normal"
        )

        # PROTOCOLO

        self.card_protocolo.configure(
            text=resultado.protocolo,
            text_color=self.COLOR_TEXTO
        )

        # ESTADO HTTP

        self.card_estado.configure(
            text=str(
                resultado.codigo_estado
            ),
            text_color=self.COLOR_TEXTO
        )

        # TIEMPO

        if resultado.tiempo_ms is not None:

            tiempo = (
                f"{resultado.tiempo_ms:.0f} ms"
            )

        else:

            tiempo = "—"

        self.card_tiempo.configure(
            text=tiempo,
            text_color=self.COLOR_TEXTO
        )

        # TLS

        if resultado.usa_https:

            if resultado.certificado_valido is True:

                self.card_tls.configure(
                    text="Válido",
                    text_color=self.COLOR_VERDE
                )

            elif resultado.certificado_valido is False:

                self.card_tls.configure(
                    text="No validado",
                    text_color=self.COLOR_AMARILLO
                )

            else:

                self.card_tls.configure(
                    text="HTTPS",
                    text_color=self.COLOR_TEXTO
                )

        else:

            self.card_tls.configure(
                text="No aplica",
                text_color=self.COLOR_SECUNDARIO
            )

        self.mostrar_resultados(
            resultado
        )

        self.mostrar_texto_ia(
            "El análisis técnico ha finalizado.\n\n"
            "Pulsa «ANALIZAR CON NETPRO AI» para obtener "
            "una interpretación educativa mediante Ollama."
        )

    # ==========================================================
    # MOSTRAR RESULTADOS
    # ==========================================================

    def mostrar_resultados(
        self,
        resultado
    ):

        self.limpiar_resultados()

        fila = 0

        # ======================================================
        # INFORMACIÓN GENERAL
        # ======================================================

        self.crear_titulo_seccion(
            "INFORMACIÓN GENERAL",
            fila
        )

        fila += 1

        datos = [
            (
                "URL solicitada",
                resultado.url_solicitada
            ),
            (
                "URL final",
                resultado.url_final
            ),
            (
                "Host",
                resultado.host
            ),
            (
                "Dirección IP",
                resultado.ip
            ),
            (
                "Protocolo",
                resultado.protocolo
            ),
            (
                "Estado HTTP",
                (
                    f"{resultado.codigo_estado} "
                    f"{resultado.razon_estado}"
                )
            ),
            (
                "Tiempo",
                (
                    f"{resultado.tiempo_ms:.2f} ms"
                    if resultado.tiempo_ms is not None
                    else "No disponible"
                )
            ),
            (
                "Servidor informado",
                resultado.servidor
            ),
            (
                "Content-Type",
                resultado.content_type
            )
        ]

        for nombre, valor in datos:

            if valor is None:
                valor = "No disponible"

            self.crear_dato(
                nombre,
                valor,
                fila
            )

            fila += 1

        # ======================================================
        # SIGNIFICADO HTTP
        # ======================================================

        self.crear_titulo_seccion(
            "SIGNIFICADO DEL ESTADO",
            fila
        )

        fila += 1

        self.crear_texto(
            descripcion_codigo_http(
                resultado.codigo_estado
            ),
            fila
        )

        fila += 1

        # ======================================================
        # REDIRECCIONES
        # ======================================================

        if resultado.redirecciones:

            self.crear_titulo_seccion(
                "REDIRECCIONES",
                fila
            )

            fila += 1

            for redireccion in resultado.redirecciones:

                texto = (
                    f'{redireccion["codigo"]}\n'
                    f'{redireccion["desde"]}\n'
                    f'→ {redireccion["hacia"]}'
                )

                self.crear_texto(
                    texto,
                    fila
                )

                fila += 1

        # ======================================================
        # TLS
        # ======================================================

        self.crear_titulo_seccion(
            "TLS / CERTIFICADO",
            fila
        )

        fila += 1

        if resultado.usa_https:

            if resultado.certificado_valido is True:

                estado_tls = (
                    "Certificado validado correctamente"
                )

                color_tls = self.COLOR_VERDE

            elif resultado.certificado_valido is False:

                estado_tls = (
                    "El certificado no pudo validarse"
                )

                color_tls = self.COLOR_AMARILLO

            else:

                estado_tls = (
                    "No fue posible determinar la "
                    "validación del certificado"
                )

                color_tls = self.COLOR_SECUNDARIO

            self.crear_dato(
                "Estado",
                estado_tls,
                fila,
                color_tls
            )

            fila += 1

            self.crear_dato(
                "Sujeto",
                resultado.certificado_sujeto,
                fila
            )

            fila += 1

            self.crear_dato(
                "Emisor",
                resultado.certificado_emisor,
                fila
            )

            fila += 1

            self.crear_dato(
                "Válido desde",
                resultado.certificado_desde,
                fila
            )

            fila += 1

            self.crear_dato(
                "Válido hasta",
                resultado.certificado_hasta,
                fila
            )

            fila += 1

            if (
                resultado.dias_restantes_certificado
                is not None
            ):

                self.crear_dato(
                    "Días restantes",
                    resultado.dias_restantes_certificado,
                    fila
                )

                fila += 1

        else:

            self.crear_texto(
                (
                    "La URL final utiliza HTTP. "
                    "Esta comprobación no obtuvo "
                    "un certificado TLS."
                ),
                fila
            )

            fila += 1

        # ======================================================
        # HEADERS DE SEGURIDAD
        # ======================================================

        self.crear_titulo_seccion(
            "HEADERS DE SEGURIDAD",
            fila
        )

        fila += 1

        resumen = resumir_headers_seguridad(
            resultado
        )

        self.crear_texto(
            (
                f'Observados: '
                f'{resumen["presentes"]} de '
                f'{resumen["total"]}\n'
                f'No observados: '
                f'{resumen["no_observados"]}\n\n'
                "La no observación de un encabezado "
                "no demuestra por sí sola una vulnerabilidad."
            ),
            fila
        )

        fila += 1

        for nombre, datos_header in (
            resultado.headers_seguridad.items()
        ):

            if datos_header.get(
                "presente",
                False
            ):

                estado = "✓ PRESENTE"
                color = self.COLOR_VERDE

            else:

                estado = "○ NO OBSERVADO"
                color = self.COLOR_SECUNDARIO

            self.crear_header_seguridad(
                nombre,
                estado,
                datos_header,
                fila,
                color
            )

            fila += 1

        # ======================================================
        # TODOS LOS HEADERS
        # ======================================================

        self.crear_titulo_seccion(
            "HEADERS HTTP",
            fila
        )

        fila += 1

        boton = ctk.CTkButton(
            self.scroll_resultados,
            text="VER TODOS LOS HEADERS",
            height=32,
            fg_color=self.COLOR_AZUL,
            hover_color=self.COLOR_AZUL_HOVER,
            command=self.mostrar_todos_headers
        )

        boton.grid(
            row=fila,
            column=0,
            sticky="ew",
            padx=10,
            pady=(5, 15)
        )

    # ==========================================================
    # TÍTULO DE SECCIÓN
    # ==========================================================

    def crear_titulo_seccion(
        self,
        titulo,
        fila
    ):

        ctk.CTkLabel(
            self.scroll_resultados,
            text=titulo,
            font=("Arial", 12, "bold"),
            text_color=self.COLOR_AZUL,
            anchor="w"
        ).grid(
            row=fila,
            column=0,
            sticky="ew",
            padx=12,
            pady=(15, 5)
        )

    # ==========================================================
    # DATO
    # ==========================================================

    def crear_dato(
        self,
        nombre,
        valor,
        fila,
        color_valor=None
    ):

        if color_valor is None:
            color_valor = self.COLOR_TEXTO

        if valor is None:
            valor = "No disponible"

        frame = ctk.CTkFrame(
            self.scroll_resultados,
            fg_color=self.COLOR_PANEL_SECUNDARIO,
            corner_radius=5
        )

        frame.grid(
            row=fila,
            column=0,
            sticky="ew",
            padx=10,
            pady=2
        )

        frame.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            frame,
            text=nombre,
            width=130,
            font=("Arial", 10, "bold"),
            text_color=self.COLOR_SECUNDARIO,
            anchor="w"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(10, 5),
            pady=7
        )

        ctk.CTkLabel(
            frame,
            text=str(valor),
            font=("Consolas", 10),
            text_color=color_valor,
            anchor="w",
            justify="left",
            wraplength=350
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(5, 10),
            pady=7
        )

    # ==========================================================
    # TEXTO
    # ==========================================================

    def crear_texto(
        self,
        texto,
        fila
    ):

        frame = ctk.CTkFrame(
            self.scroll_resultados,
            fg_color=self.COLOR_PANEL_SECUNDARIO,
            corner_radius=5
        )

        frame.grid(
            row=fila,
            column=0,
            sticky="ew",
            padx=10,
            pady=2
        )

        ctk.CTkLabel(
            frame,
            text=texto,
            font=("Arial", 10),
            text_color=self.COLOR_TEXTO,
            justify="left",
            anchor="w",
            wraplength=500
        ).pack(
            fill="x",
            padx=10,
            pady=8
        )

    # ==========================================================
    # HEADER DE SEGURIDAD
    # ==========================================================

    def crear_header_seguridad(
        self,
        nombre,
        estado,
        datos,
        fila,
        color
    ):

        frame = ctk.CTkFrame(
            self.scroll_resultados,
            fg_color=self.COLOR_PANEL_SECUNDARIO,
            corner_radius=5
        )

        frame.grid(
            row=fila,
            column=0,
            sticky="ew",
            padx=10,
            pady=2
        )

        frame.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            frame,
            text=nombre,
            font=("Arial", 10, "bold"),
            text_color=self.COLOR_TEXTO,
            anchor="w"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=(7, 2)
        )

        ctk.CTkLabel(
            frame,
            text=estado,
            font=("Arial", 9, "bold"),
            text_color=color
        ).grid(
            row=0,
            column=1,
            sticky="e",
            padx=10,
            pady=(7, 2)
        )

        descripcion = datos.get(
            "descripcion",
            ""
        )

        ctk.CTkLabel(
            frame,
            text=descripcion,
            font=("Arial", 9),
            text_color=self.COLOR_SECUNDARIO,
            anchor="w",
            justify="left",
            wraplength=470
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=(0, 7)
        )

    # ==========================================================
    # MOSTRAR TODOS LOS HEADERS
    # ==========================================================

    def mostrar_todos_headers(self):

        if self.resultado is None:
            return

        ventana = ctk.CTkToplevel(
            self
        )

        ventana.title(
            "NetPro - Headers HTTP"
        )

        ventana.geometry(
            "800x600"
        )

        ventana.minsize(
            600,
            400
        )

        ventana.grid_columnconfigure(
            0,
            weight=1
        )

        ventana.grid_rowconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            ventana,
            text="Headers HTTP",
            font=("Arial", 22, "bold"),
            text_color=self.COLOR_AZUL
        ).grid(
            row=0,
            column=0,
            pady=(20, 10)
        )

        texto = ctk.CTkTextbox(
            ventana,
            font=("Consolas", 11),
            wrap="word"
        )

        texto.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(0, 20)
        )

        if not self.resultado.headers:

            texto.insert(
                "end",
                "No se obtuvieron headers."
            )

        else:

            for clave, valor in (
                self.resultado.headers.items()
            ):

                texto.insert(
                    "end",
                    f"{clave}: {valor}\n\n"
                )

        texto.configure(
            state="disabled"
        )

    # ==========================================================
    # INICIAR NETPRO AI
    # ==========================================================

    def iniciar_analisis_ia(self):

        if self.resultado is None:
            return

        if self.ia_analizando:
            return

        self.ia_analizando = True

        self.btn_ia.configure(
            text="✦  NETPRO AI ANALIZANDO...",
            state="disabled"
        )

        self.mostrar_texto_ia(
            "NetPro AI está interpretando los resultados...\n\n"
            "El procesamiento se realiza localmente con Ollama."
        )

        threading.Thread(
            target=self.ejecutar_analisis_ia,
            daemon=True
        ).start()

    # ==========================================================
    # EJECUTAR NETPRO AI
    # ==========================================================

    def ejecutar_analisis_ia(self):

        try:

            resultado = self.resultado

            if resultado is None:

                raise RuntimeError(
                    "No existen resultados HTTP/HTTPS "
                    "para interpretar."
                )

            resumen = resumir_headers_seguridad(
                resultado
            )

            # ==================================================
            # TLS
            # ==================================================

            if resultado.certificado_valido is True:

                estado_tls = "VALIDADO"

            elif resultado.certificado_valido is False:

                estado_tls = "NO VALIDADO"

            else:

                estado_tls = "NO DETERMINADO"

            # ==================================================
            # HEADERS
            # ==================================================

            headers_seguridad = []

            for nombre, datos in (
                resultado.headers_seguridad.items()
            ):

                if datos.get(
                    "presente",
                    False
                ):

                    estado = "PRESENTE"

                else:

                    estado = "NO OBSERVADO"

                headers_seguridad.append(
                    f"- {nombre}: {estado}"
                )

            if headers_seguridad:

                headers_texto = "\n".join(
                    headers_seguridad
                )

            else:

                headers_texto = (
                    "No existen resultados disponibles."
                )

            # ==================================================
            # DATOS OPCIONALES
            # ==================================================

            if resultado.tiempo_ms is not None:

                tiempo = (
                    f"{resultado.tiempo_ms:.2f} ms"
                )

            else:

                tiempo = "No disponible"

            servidor = (
                resultado.servidor
                if resultado.servidor
                else "No informado"
            )

            content_type = (
                resultado.content_type
                if resultado.content_type
                else "No informado"
            )

            sujeto = (
                resultado.certificado_sujeto
                if resultado.certificado_sujeto
                else "No disponible"
            )

            emisor = (
                resultado.certificado_emisor
                if resultado.certificado_emisor
                else "No disponible"
            )

            valido_desde = (
                resultado.certificado_desde
                if resultado.certificado_desde
                else "No disponible"
            )

            valido_hasta = (
                resultado.certificado_hasta
                if resultado.certificado_hasta
                else "No disponible"
            )

            dias_restantes = (
                resultado.dias_restantes_certificado
                if (
                    resultado.dias_restantes_certificado
                    is not None
                )
                else "No disponible"
            )

            # ==================================================
            # PROMPT NETPRO AI
            # ==================================================

            prompt = f"""
MÓDULO: HTTP / HTTPS

NetPro realizó una comprobación técnica HTTP/HTTPS.

Los datos siguientes fueron obtenidos mediante código
y constituyen la fuente de verdad.

Tu función es únicamente INTERPRETARLOS.

RESULTADOS

URL solicitada:
{resultado.url_solicitada}

URL final:
{resultado.url_final}

Host:
{resultado.host}

Dirección IP observada:
{resultado.ip}

Protocolo:
{resultado.protocolo}

Estado HTTP:
{resultado.codigo_estado} {resultado.razon_estado}

Significado del estado HTTP:
{descripcion_codigo_http(resultado.codigo_estado)}

Tiempo de respuesta:
{tiempo}

Servidor informado:
{servidor}

Content-Type:
{content_type}

HTTPS:
{"SÍ" if resultado.usa_https else "NO"}

TLS / CERTIFICADO

Estado de validación:
{estado_tls}

Sujeto:
{sujeto}

Emisor:
{emisor}

Válido desde:
{valido_desde}

Válido hasta:
{valido_hasta}

Días restantes:
{dias_restantes}

HEADERS DE SEGURIDAD

Observados:
{resumen["presentes"]} de {resumen["total"]}

No observados:
{resumen["no_observados"]}

Detalle:

{headers_texto}

INSTRUCCIONES

Interpreta los resultados anteriores para un estudiante
de redes y ciberseguridad.

Utiliza este formato:

INTERPRETACIÓN

Explica brevemente qué ocurrió durante la comprobación.

ESTADO HTTP

Explica qué significa el código HTTP observado.

HTTPS Y TLS

Explica exclusivamente lo que permiten concluir los
resultados HTTPS y TLS.

HEADERS DE SEGURIDAD

Explica los encabezados observados y los no observados.

SEGURIDAD

Explica qué puede concluirse y qué NO puede concluirse
con esta comprobación.

SIGUIENTE PASO

Sugiere como máximo una comprobación defensiva o educativa
si aporta información adicional.

REGLAS OBLIGATORIAS

Responde siempre en español.

No cambies ningún dato proporcionado por NetPro.

No cambies:
- URL
- dirección IP
- protocolo
- código HTTP
- estado TLS
- headers

No inventes vulnerabilidades.

No inventes CVE.

No inventes versiones de software.

No inventes servicios.

No inventes configuraciones.

No afirmes que HTTPS significa que un sitio es
completamente seguro.

No afirmes que un certificado válido demuestra que
la aplicación no tiene vulnerabilidades.

No afirmes que un header NO OBSERVADO representa
automáticamente una vulnerabilidad.

NO OBSERVADO significa únicamente que NetPro no observó
ese encabezado en la respuesta analizada.

No conviertas una posibilidad general en un hallazgo
específico.

Si los datos no permiten determinar algo, indica:

"No puede determinarse con este análisis."

No proporciones instrucciones para comprometer,
explotar o acceder sin autorización a sistemas.

No muestres razonamiento interno.

No muestres cadena de pensamiento.

Entrega únicamente la respuesta final.

Mantén la respuesta por debajo de 220 palabras.
"""

            # ==================================================
            # OLLAMA
            # ==================================================

            respuesta = generar_respuesta(
                prompt
            )

            if respuesta is None:

                raise RuntimeError(
                    "NetPro AI no devolvió ninguna respuesta."
                )

            respuesta = str(
                respuesta
            ).strip()

            if not respuesta:

                raise RuntimeError(
                    "NetPro AI devolvió una respuesta vacía."
                )

            self.after(
                0,
                lambda texto=respuesta:
                    self.finalizar_analisis_ia(
                        texto
                    )
            )

        except Exception as error:

            mensaje = str(error)

            self.after(
                0,
                lambda texto=mensaje:
                    self.error_analisis_ia(
                        texto
                    )
            )

    # ==========================================================
    # FINALIZAR NETPRO AI
    # ==========================================================

    def finalizar_analisis_ia(
        self,
        texto
    ):

        self.ia_analizando = False

        self.btn_ia.configure(
            text="✦  ANALIZAR CON NETPRO AI",
            state="normal"
        )

        self.mostrar_texto_ia(
            texto
        )

    # ==========================================================
    # ERROR NETPRO AI
    # ==========================================================

    def error_analisis_ia(
        self,
        mensaje
    ):

        self.ia_analizando = False

        self.btn_ia.configure(
            text="✦  ANALIZAR CON NETPRO AI",
            state="normal"
        )

        self.mostrar_texto_ia(
            "No fue posible completar la interpretación "
            "con NetPro AI.\n\n"
            f"Detalle: {mensaje}\n\n"
            "Los resultados técnicos obtenidos por NetPro "
            "continúan siendo válidos."
        )

    # ==========================================================
    # MOSTRAR TEXTO IA
    # ==========================================================

    def mostrar_texto_ia(
        self,
        texto
    ):

        self.texto_ia.configure(
            state="normal"
        )

        self.texto_ia.delete(
            "1.0",
            "end"
        )

        self.texto_ia.insert(
            "1.0",
            texto
        )

        self.texto_ia.configure(
            state="disabled"
        )

    # ==========================================================
    # ERROR GENERAL
    # ==========================================================

    def mostrar_error(
        self,
        mensaje
    ):

        self.analizando = False
        self.resultado = None

        self.btn_analizar.configure(
            text="🌐 ANALIZAR",
            state="normal"
        )

        self.btn_ia.configure(
            state="disabled"
        )

        self.card_protocolo.configure(
            text="—",
            text_color=self.COLOR_TEXTO
        )

        self.card_estado.configure(
            text="Error",
            text_color=self.COLOR_ROJO
        )

        self.card_tiempo.configure(
            text="—",
            text_color=self.COLOR_TEXTO
        )

        self.card_tls.configure(
            text="—",
            text_color=self.COLOR_TEXTO
        )

        self.mostrar_texto_ia(
            "El análisis HTTP/HTTPS no pudo completarse."
        )

        messagebox.showerror(
            "NetPro - HTTP / HTTPS",
            mensaje
        )