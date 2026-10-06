import customtkinter as ctk
import threading
from tkinter import messagebox

from core.ports import (
    comprobar_puerto,
    comprobar_puertos_comunes,
    comprobar_rango,
    resumir_resultados
)

from AI.ollama_client import (
    analizar_puerto_con_ia,
    analizar_resultados_con_ia,
    ollama_disponible,
    modelo_disponible
)


class PortsFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        # ====================================================
        # ESTADO
        # ====================================================

        self.resultados = []
        self.resultado_seleccionado = None
        self.analizando = False

        # ====================================================
        # COLORES NETPRO
        # ====================================================

        self.COLOR_FONDO = "#2B2B2B"
        self.COLOR_PANEL = "#1A1A1A"
        self.COLOR_PANEL_SECUNDARIO = "#242424"

        self.COLOR_AZUL = "#3B8ED0"
        self.COLOR_AZUL_HOVER = "#36719F"

        self.COLOR_VERDE = "#2ECC71"
        self.COLOR_ROJO = "#E74C3C"
        self.COLOR_AMARILLO = "#F1C40F"

        self.COLOR_TEXTO = "#FFFFFF"
        self.COLOR_SECUNDARIO = "#FFFFFF"

        # ====================================================
        # GRID PRINCIPAL
        # ====================================================

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # ====================================================
        # ENCABEZADO
        # ====================================================

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
            text="🔌 Puertos",
            font=("Arial", 28, "bold"),
            text_color=self.COLOR_AZUL
        ).grid(
            row=0,
            column=0,
            pady=(0, 4)
        )

        ctk.CTkLabel(
            encabezado,
            text=(
                "Comprueba puertos TCP, servicios asociados "
                "y exposición de red."
            ),
            font=("Arial", 13),
            text_color=self.COLOR_TEXTO
        ).grid(
            row=1,
            column=0
        )

        self.label_estado_ia = ctk.CTkLabel(
            encabezado,
            text="● Comprobando NetPro AI...",
            font=("Arial", 10, "bold"),
            text_color=self.COLOR_AMARILLO
        )

        self.label_estado_ia.grid(
            row=2,
            column=0,
            pady=(5, 0)
        )

        # ====================================================
        # PANEL DE CONFIGURACIÓN
        # ====================================================

        panel_config = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        panel_config.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=(10, 5)
        )

        panel_config.grid_columnconfigure(0, weight=1)

        # ====================================================
        # DESTINO
        # ====================================================

        ctk.CTkLabel(
            panel_config,
            text="Destino",
            font=("Arial", 12),
            text_color=self.COLOR_AZUL
        ).grid(
            row=0,
            column=0,
            pady=(0, 5)
        )

        self.entry_host = ctk.CTkEntry(
            panel_config,
            placeholder_text="Ejemplo: localhost o 192.168.1.1",
            height=36
        )

        self.entry_host.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=120
        )

        # ====================================================
        # CONTROLES
        # ====================================================

        controles = ctk.CTkFrame(
            panel_config,
            fg_color="transparent"
        )

        controles.grid(
            row=2,
            column=0,
            pady=(15, 5)
        )

        # ====================================================
        # MODO
        # ====================================================

        self.modo = ctk.StringVar(
            value="Puerto individual"
        )

        self.combo_modo = ctk.CTkOptionMenu(
            controles,
            values=[
                "Puerto individual",
                "Puertos comunes",
                "Rango"
            ],
            variable=self.modo,
            command=self.cambiar_modo,
            width=170,
            fg_color=self.COLOR_AZUL,
            button_color=self.COLOR_AZUL,
            button_hover_color=self.COLOR_AZUL_HOVER
        )

        self.combo_modo.grid(
            row=0,
            column=0,
            padx=5
        )

        # ====================================================
        # PUERTO INDIVIDUAL
        # ====================================================

        self.label_puerto = ctk.CTkLabel(
            controles,
            text="Puerto:",
            font=("Arial", 12)
        )

        self.entry_puerto = ctk.CTkEntry(
            controles,
            width=90,
            placeholder_text="443"
        )

        # ====================================================
        # RANGO
        # ====================================================

        self.label_rango = ctk.CTkLabel(
            controles,
            text="Rango:",
            font=("Arial", 12)
        )

        self.entry_inicio = ctk.CTkEntry(
            controles,
            width=80,
            placeholder_text="1"
        )

        self.label_hasta = ctk.CTkLabel(
            controles,
            text="a"
        )

        self.entry_fin = ctk.CTkEntry(
            controles,
            width=80,
            placeholder_text="1024"
        )

        # ====================================================
        # BOTÓN ANALIZAR
        # ====================================================

        self.btn_analizar = ctk.CTkButton(
            panel_config,
            text="🔎 ANALIZAR",
            width=325,
            height=36,
            font=("Arial", 12),
            fg_color=self.COLOR_AZUL,
            hover_color=self.COLOR_AZUL_HOVER,
            command=self.iniciar_analisis
        )

        self.btn_analizar.grid(
            row=3,
            column=0,
            pady=(10, 5)
        )

        # ====================================================
        # RESUMEN
        # ====================================================

        self.panel_resumen = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.panel_resumen.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=25,
            pady=(8, 5)
        )

        for columna in range(4):
            self.panel_resumen.grid_columnconfigure(
                columna,
                weight=1
            )

        self.card_total = self.crear_card(
            self.panel_resumen,
            0,
            "Analizados",
            "0"
        )

        self.card_abiertos = self.crear_card(
            self.panel_resumen,
            1,
            "Abiertos",
            "0"
        )

        self.card_cerrados = self.crear_card(
            self.panel_resumen,
            2,
            "Cerrados",
            "0"
        )

        self.card_sin_respuesta = self.crear_card(
            self.panel_resumen,
            3,
            "Sin respuesta",
            "0"
        )

        # ====================================================
        # SEPARADOR
        # ====================================================

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

        # ====================================================
        # ÁREA CENTRAL RESPONSIVE
        # ====================================================

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

        self.area_central.grid_rowconfigure(
            0,
            weight=1
        )

        # Resultados
        self.area_central.grid_columnconfigure(
            0,
            weight=1,
            minsize=350
        )

        # Separación real entre los paneles
        self.area_central.grid_columnconfigure(
            1,
            weight=0,
            minsize=12
        )

        # NetPro AI
        self.area_central.grid_columnconfigure(
            2,
            weight=1,
            minsize=350
        )

        # ====================================================
        # PANEL RESULTADOS
        # ====================================================

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

        panel_resultados.grid_columnconfigure(
            0,
            weight=1
        )

        panel_resultados.grid_rowconfigure(
            1,
            weight=1
        )

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

        # ====================================================
        # PANEL NETPRO AI
        # ====================================================

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

        panel_ia.grid_columnconfigure(
            0,
            weight=1
        )

        panel_ia.grid_rowconfigure(
            2,
            weight=1
        )

        # ====================================================
        # CABECERA NETPRO AI
        # ====================================================

        cabecera_ia = ctk.CTkFrame(
            panel_ia,
            fg_color="transparent",
            height=45
        )

        cabecera_ia.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(15, 8)
        )

        cabecera_ia.grid_columnconfigure(
            0,
            weight=1
        )

        cabecera_ia.grid_columnconfigure(
            1,
            weight=0
        )

        # ====================================================
        # TÍTULO NETPRO AI
        # ====================================================

        self.titulo_ia = ctk.CTkLabel(
            cabecera_ia,
            text="✦  NetPro AI",
            font=("Arial", 17, "bold"),
            text_color=self.COLOR_TEXTO,
            anchor="w"
        )

        self.titulo_ia.grid(
            row=0,
            column=0,
            sticky="w",
            padx=(5, 10)
        )

        # ====================================================
        # ESTADO LOCAL
        # ====================================================

        self.label_local = ctk.CTkLabel(
            cabecera_ia,
            text="● LOCAL",
            font=("Arial", 10, "bold"),
            text_color=self.COLOR_VERDE,
            anchor="e"
        )

        self.label_local.grid(
            row=0,
            column=1,
            sticky="e",
            padx=(10, 5)
        )

        # ====================================================
        # BOTÓN NETPRO AI
        # ====================================================

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

        # ====================================================
        # TEXTO NETPRO AI
        # ====================================================

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
            "Selecciona o analiza un puerto para obtener "
            "una explicación educativa mediante NetPro AI."
        )

        # ====================================================
        # ESTADO INICIAL
        # ====================================================

        self.cambiar_modo(
            self.modo.get()
        )

        threading.Thread(
            target=self.comprobar_estado_ia,
            daemon=True
        ).start()

    # ========================================================
    # CREAR TARJETAS DEL RESUMEN
    # ========================================================

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

        label_valor = ctk.CTkLabel(
            frame,
            text=valor,
            font=("Arial", 20, "bold"),
            text_color=self.COLOR_TEXTO
        )

        label_valor.pack(
            pady=(2, 3)
        )

        return label_valor

    # ========================================================
    # CAMBIAR MODO
    # ========================================================

    def cambiar_modo(self, modo):

        self.label_puerto.grid_remove()
        self.entry_puerto.grid_remove()

        self.label_rango.grid_remove()
        self.entry_inicio.grid_remove()
        self.label_hasta.grid_remove()
        self.entry_fin.grid_remove()

        if modo == "Puerto individual":

            self.label_puerto.grid(
                row=0,
                column=1,
                padx=(20, 5)
            )

            self.entry_puerto.grid(
                row=0,
                column=2,
                padx=5
            )

        elif modo == "Rango":

            self.label_rango.grid(
                row=0,
                column=1,
                padx=(20, 5)
            )

            self.entry_inicio.grid(
                row=0,
                column=2,
                padx=5
            )

            self.label_hasta.grid(
                row=0,
                column=3,
                padx=3
            )

            self.entry_fin.grid(
                row=0,
                column=4,
                padx=5
            )

    # ========================================================
    # COMPROBAR ESTADO DE NETPRO AI
    # ========================================================

    def comprobar_estado_ia(self):

        try:

            disponible = (
                ollama_disponible()
                and modelo_disponible()
            )

        except Exception:

            disponible = False

        self.after(
            0,
            lambda: self.actualizar_estado_ia(
                disponible
            )
        )

    # ========================================================
    # ACTUALIZAR ESTADO DE NETPRO AI
    # ========================================================

    def actualizar_estado_ia(
        self,
        disponible
    ):

        if disponible:

            self.label_estado_ia.configure(
                text="● NetPro AI disponible",
                text_color=self.COLOR_VERDE
            )

            self.label_local.configure(
                text="● LOCAL",
                text_color=self.COLOR_VERDE
            )

        else:

            self.label_estado_ia.configure(
                text="● NetPro AI no disponible",
                text_color=self.COLOR_ROJO
            )

            self.label_local.configure(
                text="● OFFLINE",
                text_color=self.COLOR_ROJO
            )

    # ========================================================
    # INICIAR ANÁLISIS DE PUERTOS
    # ========================================================

    def iniciar_analisis(self):

        if self.analizando:
            return

        host = self.entry_host.get().strip()

        if not host:

            messagebox.showwarning(
                "NetPro",
                "Introduce un host o una dirección IP."
            )

            return

        modo = self.modo.get()

        # ----------------------------------------------------
        # PUERTO INDIVIDUAL
        # ----------------------------------------------------

        if modo == "Puerto individual":

            puerto = self.entry_puerto.get().strip()

            if not puerto:

                messagebox.showwarning(
                    "NetPro",
                    "Introduce un número de puerto."
                )

                return

            try:
                puerto_num = int(puerto)

            except ValueError:

                messagebox.showwarning(
                    "NetPro",
                    "El puerto debe ser un número."
                )

                return

            if puerto_num < 1 or puerto_num > 65535:

                messagebox.showwarning(
                    "NetPro",
                    "El puerto debe estar entre 1 y 65535."
                )

                return

            parametros = (
                modo,
                host,
                puerto_num,
                None
            )

        # ----------------------------------------------------
        # RANGO
        # ----------------------------------------------------

        elif modo == "Rango":

            inicio = self.entry_inicio.get().strip()
            fin = self.entry_fin.get().strip()

            if not inicio or not fin:

                messagebox.showwarning(
                    "NetPro",
                    "Introduce el puerto inicial y final."
                )

                return

            try:

                inicio_num = int(inicio)
                fin_num = int(fin)

            except ValueError:

                messagebox.showwarning(
                    "NetPro",
                    "Los puertos deben ser números."
                )

                return

            if (
                inicio_num < 1
                or inicio_num > 65535
                or fin_num < 1
                or fin_num > 65535
            ):

                messagebox.showwarning(
                    "NetPro",
                    "Los puertos deben estar entre 1 y 65535."
                )

                return

            if inicio_num > fin_num:

                messagebox.showwarning(
                    "NetPro",
                    "El puerto inicial no puede ser mayor "
                    "que el puerto final."
                )

                return

            # Evita escaneos enormes accidentalmente
            if fin_num - inicio_num > 1000:

                messagebox.showwarning(
                    "NetPro",
                    "Por seguridad y rendimiento, analiza "
                    "un máximo de 1000 puertos por rango."
                )

                return

            parametros = (
                modo,
                host,
                inicio_num,
                fin_num
            )

        # ----------------------------------------------------
        # PUERTOS COMUNES
        # ----------------------------------------------------

        else:

            parametros = (
                modo,
                host,
                None,
                None
            )

        self.analizando = True

        self.btn_analizar.configure(
            text="⏳ ANALIZANDO...",
            state="disabled"
        )

        self.btn_ia.configure(
            state="disabled"
        )

        self.limpiar_resultados()

        self.mostrar_texto_ia(
            "Esperando resultados del análisis..."
        )

        threading.Thread(
            target=self.ejecutar_analisis,
            args=parametros,
            daemon=True
        ).start()

    # ========================================================
    # EJECUTAR ANÁLISIS
    # ========================================================

    def ejecutar_analisis(
        self,
        modo,
        host,
        valor1,
        valor2
    ):

        try:

            if modo == "Puerto individual":

                resultado = comprobar_puerto(
                    host,
                    valor1
                )

                resultados = [resultado]

            elif modo == "Puertos comunes":

                resultados = comprobar_puertos_comunes(
                    host
                )

            elif modo == "Rango":

                resultados = comprobar_rango(
                    host,
                    valor1,
                    valor2
                )

            else:

                raise ValueError(
                    "Modo de análisis desconocido."
                )

            self.after(
                0,
                lambda: self.finalizar_analisis(
                    resultados
                )
            )

        except Exception as error:

            mensaje = str(error)

            self.after(
                0,
                lambda: self.mostrar_error(
                    mensaje
                )
            )

    # ========================================================
    # FINALIZAR ANÁLISIS
    # ========================================================

    def finalizar_analisis(
        self,
        resultados
    ):

        self.analizando = False
        self.resultados = resultados

        self.btn_analizar.configure(
            text="🔎 ANALIZAR",
            state="normal"
        )

        self.mostrar_resultados(
            resultados
        )

        self.actualizar_resumen(
            resultados
        )

        if resultados:

            self.btn_ia.configure(
                state="normal"
            )

            if len(resultados) == 1:

                self.resultado_seleccionado = (
                    resultados[0]
                )

                self.mostrar_detalle_resultado(
                    resultados[0]
                )

            else:

                self.resultado_seleccionado = None

                self.mostrar_texto_ia(
                    f"Se analizaron {len(resultados)} "
                    "puertos.\n\n"
                    "Selecciona «Ver» en un puerto para "
                    "consultar su detalle.\n\n"
                    "También puedes utilizar "
                    "«ANALIZAR CON NETPRO AI» para obtener "
                    "una interpretación educativa general."
                )

    # ========================================================
    # MOSTRAR ERROR
    # ========================================================

    def mostrar_error(
        self,
        mensaje
    ):

        self.analizando = False

        self.btn_analizar.configure(
            text="🔎 ANALIZAR",
            state="normal"
        )

        messagebox.showerror(
            "Error de NetPro",
            mensaje
        )

    # ========================================================
    # LIMPIAR RESULTADOS
    # ========================================================

    def limpiar_resultados(self):

        for widget in (
            self.scroll_resultados.winfo_children()
        ):
            widget.destroy()

        self.resultados = []
        self.resultado_seleccionado = None

        self.actualizar_resumen([])

    # ========================================================
    # MOSTRAR RESULTADOS
    # ========================================================

    def mostrar_resultados(
        self,
        resultados
    ):

        for widget in (
            self.scroll_resultados.winfo_children()
        ):
            widget.destroy()

        if not resultados:

            ctk.CTkLabel(
                self.scroll_resultados,
                text="No hay resultados.",
                text_color=self.COLOR_SECUNDARIO
            ).grid(
                row=0,
                column=0,
                pady=20
            )

            return

        for indice, resultado in enumerate(
            resultados
        ):

            self.crear_fila_resultado(
                indice,
                resultado
            )

    # ========================================================
    # CREAR FILA DE RESULTADO
    # ========================================================

    def crear_fila_resultado(
        self,
        indice,
        resultado
    ):

        frame = ctk.CTkFrame(
            self.scroll_resultados,
            fg_color=self.COLOR_PANEL_SECUNDARIO,
            corner_radius=6
        )

        frame.grid(
            row=indice,
            column=0,
            sticky="ew",
            padx=3,
            pady=3
        )

        frame.grid_columnconfigure(
            1,
            weight=1
        )

        # ====================================================
        # ESTADO
        # ====================================================

        if resultado.estado == "ABIERTO":

            color_estado = self.COLOR_VERDE
            simbolo = "●"

        elif resultado.estado == "CERRADO":

            color_estado = self.COLOR_ROJO
            simbolo = "●"

        elif resultado.estado == "SIN RESPUESTA":

            color_estado = self.COLOR_AMARILLO
            simbolo = "●"

        else:

            color_estado = self.COLOR_SECUNDARIO
            simbolo = "●"

        # ====================================================
        # PUERTO
        # ====================================================

        ctk.CTkLabel(
            frame,
            text=f"{resultado.puerto}/TCP",
            width=75,
            font=("Consolas", 12, "bold"),
            text_color=self.COLOR_TEXTO
        ).grid(
            row=0,
            column=0,
            padx=(10, 5),
            pady=10
        )

        # ====================================================
        # SERVICIO
        # ====================================================

        ctk.CTkLabel(
            frame,
            text=resultado.servicio,
            font=("Arial", 11),
            text_color=self.COLOR_SECUNDARIO
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=5
        )

        # ====================================================
        # ESTADO
        # ====================================================

        ctk.CTkLabel(
            frame,
            text=f"{simbolo} {resultado.estado}",
            width=105,
            font=("Arial", 10, "bold"),
            text_color=color_estado
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        # ====================================================
        # TIEMPO
        # ====================================================

        if resultado.tiempo_ms is not None:

            tiempo = (
                f"{resultado.tiempo_ms:.1f} ms"
            )

        else:

            tiempo = "—"

        ctk.CTkLabel(
            frame,
            text=tiempo,
            width=70,
            font=("Consolas", 10),
            text_color=self.COLOR_SECUNDARIO
        ).grid(
            row=0,
            column=3,
            padx=5
        )

        # ====================================================
        # BOTÓN VER
        # ====================================================

        ctk.CTkButton(
            frame,
            text="Ver",
            width=50,
            height=26,
            font=("Arial", 10),
            fg_color=self.COLOR_AZUL,
            hover_color=self.COLOR_AZUL_HOVER,
            command=lambda r=resultado: (
                self.seleccionar_resultado(r)
            )
        ).grid(
            row=0,
            column=4,
            padx=(5, 10)
        )

    # ========================================================
    # SELECCIONAR RESULTADO
    # ========================================================

    def seleccionar_resultado(
        self,
        resultado
    ):

        self.resultado_seleccionado = resultado

        self.mostrar_detalle_resultado(
            resultado
        )

    # ========================================================
    # MOSTRAR DETALLE DEL RESULTADO
    # ========================================================

    def mostrar_detalle_resultado(
        self,
        resultado
    ):

        if resultado.tiempo_ms is not None:

            tiempo = (
                f"{resultado.tiempo_ms:.1f} ms"
            )

        else:

            tiempo = "No disponible"

        texto = (
            "RESULTADO DEL ANÁLISIS\n"
            "────────────────────────────────\n\n"
            f"Objetivo: {resultado.host}\n"
            f"Dirección IP: {resultado.ip}\n"
            f"Puerto: {resultado.puerto}/"
            f"{resultado.protocolo}\n"
            f"Estado: {resultado.estado}\n"
            f"Servicio habitual: "
            f"{resultado.servicio}\n"
            f"Tiempo: {tiempo}\n\n"
            "DESCRIPCIÓN\n"
            "────────────────────────────────\n"
            f"{resultado.descripcion}\n\n"
            "Pulsa «ANALIZAR CON NETPRO AI» "
            "para obtener una explicación educativa."
        )

        self.mostrar_texto_ia(
            texto
        )

    # ========================================================
    # ACTUALIZAR RESUMEN
    # ========================================================

    def actualizar_resumen(
        self,
        resultados
    ):

        resumen = resumir_resultados(
            resultados
        )

        self.card_total.configure(
            text=str(
                resumen["total"]
            )
        )

        self.card_abiertos.configure(
            text=str(
                resumen["abiertos"]
            )
        )

        self.card_cerrados.configure(
            text=str(
                resumen["cerrados"]
            )
        )

        self.card_sin_respuesta.configure(
            text=str(
                resumen["sin_respuesta"]
            )
        )

    # ========================================================
    # INICIAR ANÁLISIS CON NETPRO AI
    # ========================================================

    def iniciar_analisis_ia(self):

        if not self.resultados:
            return

        self.btn_ia.configure(
            text="✦  NETPRO AI ANALIZANDO...",
            state="disabled"
        )

        self.mostrar_texto_ia(
            "NetPro AI está interpretando los "
            "resultados...\n\n"
            "El procesamiento se realiza localmente "
            "mediante Ollama."
        )

        threading.Thread(
            target=self.ejecutar_analisis_ia,
            daemon=True
        ).start()

    # ========================================================
    # EJECUTAR NETPRO AI
    # ========================================================

    def ejecutar_analisis_ia(self):

        try:

            if (
                self.resultado_seleccionado
                is not None
            ):

                respuesta = (
                    analizar_puerto_con_ia(
                        self.resultado_seleccionado
                    )
                )

            else:

                respuesta = (
                    analizar_resultados_con_ia(
                        self.resultados
                    )
                )

            self.after(
                0,
                lambda: self.finalizar_analisis_ia(
                    respuesta
                )
            )

        except Exception as error:

            mensaje = str(error)

            self.after(
                0,
                lambda: self.error_analisis_ia(
                    mensaje
                )
            )

    # ========================================================
    # FINALIZAR NETPRO AI
    # ========================================================

    def finalizar_analisis_ia(
        self,
        respuesta
    ):

        self.btn_ia.configure(
            text="✦  ANALIZAR CON NETPRO AI",
            state="normal"
        )

        self.mostrar_texto_ia(
            respuesta
        )

    # ========================================================
    # ERROR NETPRO AI
    # ========================================================

    def error_analisis_ia(
        self,
        mensaje
    ):

        self.btn_ia.configure(
            text="✦  ANALIZAR CON NETPRO AI",
            state="normal"
        )

        self.mostrar_texto_ia(
            "No fue posible obtener la explicación "
            "de NetPro AI.\n\n"
            f"Detalle: {mensaje}\n\n"
            "Los resultados técnicos obtenidos por "
            "NetPro continúan siendo válidos."
        )

    # ========================================================
    # MOSTRAR TEXTO DE NETPRO AI
    # ========================================================

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