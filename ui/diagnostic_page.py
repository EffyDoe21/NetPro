import customtkinter as ctk
from tkinter import messagebox

import threading
import re
import ipaddress

from core.ping import ejecutar_ping
from core.traceroute import ejecutar_traceroute


class DiagnosticFrame(ctk.CTkFrame):

    AZUL = "#3B8ED0"
    AZUL_HOVER = "#367EB8"
    PANEL_COLOR = "#1A1A1A"
    PANEL_BORDER = "#343638"

    def __init__(self, parent):
        super().__init__(parent)

        self.ultimo_ping = None
        self.ultimo_traceroute = None

        # ========================================================
        # TÍTULO
        # ========================================================

        title = ctk.CTkLabel(
            self,
            text="📡 Diagnóstico",
            font=("Arial", 30, "bold"),
            text_color=self.AZUL
        )
        title.pack(pady=(35, 5))

        subtitle = ctk.CTkLabel(
            self,
            text=(
                "Comprueba conectividad, latencia, "
                "pérdida de paquetes y ruta de red."
            ),
            font=("Arial", 14)
        )
        subtitle.pack(pady=(0, 25))

        # ========================================================
        # DESTINO
        # ========================================================

        entrada_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        entrada_frame.pack(
            padx=30,
            pady=(5, 10)
        )

        ctk.CTkLabel(
            entrada_frame,
            text="Destino",
            font=("Arial", 13, "bold"),
            text_color=self.AZUL
        ).pack(pady=(0, 6))

        self.destino_entry = ctk.CTkEntry(
            entrada_frame,
            width=460,
            height=42,
            placeholder_text="Ejemplo: google.com o 8.8.8.8"
        )
        self.destino_entry.pack()

        # ========================================================
        # BOTONES
        # ========================================================

        botones = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        botones.pack(pady=15)

        self.btn_ping = ctk.CTkButton(
            botones,
            text="PING",
            width=180,
            height=42,
            font=("Arial", 13, "bold"),
            fg_color=self.AZUL,
            hover_color=self.AZUL_HOVER,
            command=self.iniciar_ping
        )
        self.btn_ping.grid(
            row=0,
            column=0,
            padx=8
        )

        self.btn_traceroute = ctk.CTkButton(
            botones,
            text="TRACEROUTE",
            width=180,
            height=42,
            font=("Arial", 13, "bold"),
            fg_color=self.AZUL,
            hover_color=self.AZUL_HOVER,
            command=self.iniciar_traceroute
        )
        self.btn_traceroute.grid(
            row=0,
            column=1,
            padx=8
        )


        # ========================================================
        # ESTADO
        # ========================================================

        self.estado_label = ctk.CTkLabel(
            self,
            text="Introduce un destino para comenzar.",
            font=("Arial", 13)
        )
        self.estado_label.pack(
            pady=(0, 10)
        )

        # ========================================================
        # ÁREA PRINCIPAL
        # ========================================================

 
        self.contenido = ctk.CTkScrollableFrame(
            self,
            width=800,
            height=430,
            corner_radius=12,
            fg_color="#1A1A1A",
            border_width=1,
            border_color="#343638"
        )

        self.contenido.pack(
            padx=30,
            pady=(5, 12),
            fill="both",
            expand=True
        )

    # ========================================================
    # BOTÓN EDUCATIVO INFERIOR
    # ========================================================

        botones_educativos = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        botones_educativos.pack(
            pady=(0, 25)
        )

        self.btn_aprender = ctk.CTkButton(
            botones_educativos,
            text="¿QUÉ SIGNIFICA?",
            width=220,
            height=40,
            font=("Arial", 13),
            fg_color=self.AZUL,
            hover_color=self.AZUL_HOVER,
            command=self.mostrar_aprendizaje
        )

        self.btn_aprender.pack()

        self.mostrar_inicio()   

    # ============================================================
    # UTILIDADES DE INTERFAZ
    # ============================================================

    def limpiar_contenido(self):

        for widget in self.contenido.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):

        self.limpiar_contenido()

        texto_inicio = (
            "Introduce un destino para comenzar.\n\n"
            "Herramientas:\n"
            "PING:        Comprueba conectividad, latencia y pérdida de paquetes.\n"
            "TRACEROUTE:  Muestra la ruta que siguen los paquetes hasta el destino."
        )

        ctk.CTkLabel(
            self.contenido,
            text=texto_inicio,
            font=("Consolas", 13),
            text_color="#FFFFFF",
            justify="left",
            anchor="nw"
        ).pack(
            anchor="nw",
            padx=12,
            pady=10
        )

    def crear_tarjeta(
        self,
        parent,
        titulo,
        valor,
        descripcion=""
    ):

        tarjeta = ctk.CTkFrame(
            parent,
            corner_radius=10,
            border_width=1
        )

        tarjeta.pack(
            padx=12,
            pady=7,
            fill="x"
        )

        ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=("Arial", 11, "bold"),
            text_color=self.AZUL
        ).pack(
            anchor="w",
            padx=16,
            pady=(12, 3)
        )

        ctk.CTkLabel(
            tarjeta,
            text=str(valor),
            font=("Consolas", 18, "bold")
        ).pack(
            anchor="w",
            padx=16
        )

        if descripcion:

            ctk.CTkLabel(
                tarjeta,
                text=descripcion,
                font=("Arial", 12),
                justify="left",
                anchor="w",
                wraplength=700
            ).pack(
                anchor="w",
                padx=16,
                pady=(5, 12)
            )

        else:

            ctk.CTkFrame(
                tarjeta,
                height=8,
                fg_color="transparent"
            ).pack()

        return tarjeta

    def bloquear_botones(self, bloquear=True):

        estado = (
            "disabled"
            if bloquear
            else "normal"
        )

        self.btn_ping.configure(
            state=estado
        )

        self.btn_traceroute.configure(
            state=estado
        )

    # ============================================================
    # PING
    # ============================================================

    def iniciar_ping(self):

        destino = (
            self.destino_entry
            .get()
            .strip()
        )

        if not destino:

            messagebox.showwarning(
                "NetPro",
                "Introduce una dirección IP o dominio."
            )

            return

        self.bloquear_botones(True)

        self.estado_label.configure(
            text=f"Ejecutando Ping a {destino}..."
        )

        hilo = threading.Thread(
            target=self._ejecutar_ping_thread,
            args=(destino,),
            daemon=True
        )

        hilo.start()

    def _ejecutar_ping_thread(
        self,
        destino
    ):

        try:

            resultado = ejecutar_ping(
                destino
            )

            self.after(
                0,
                self.mostrar_resultado_ping,
                resultado
            )

        except Exception as error:

            self.after(
                0,
                self.mostrar_error,
                str(error)
            )

    def mostrar_resultado_ping(
        self,
        resultado
    ):

        self.bloquear_botones(False)

        self.ultimo_ping = resultado

        self.estado_label.configure(
            text="Prueba Ping finalizada."
        )

        self.limpiar_contenido()

        # ========================================================
        # CABECERA
        # ========================================================

        ctk.CTkLabel(
            self.contenido,
            text="RESULTADO PING",
            font=("Arial", 20, "bold"),
            text_color=self.AZUL
        ).pack(
            pady=(20, 4)
        )

        ctk.CTkLabel(
            self.contenido,
            text=resultado["destino"],
            font=("Consolas", 15, "bold")
        ).pack(
            pady=(0, 15)
        )

        # ========================================================
        # ESTADO
        # ========================================================

        if resultado["respuesta"]:

            estado = "RESPONDE"

            descripcion_estado = (
                "NetPro recibió al menos una respuesta "
                "durante esta prueba."
            )

        else:

            estado = "SIN RESPUESTA"

            descripcion_estado = (
                "NetPro no recibió respuestas durante "
                "esta prueba. Esto no demuestra por sí "
                "solo que el destino esté fuera de servicio."
            )

        self.crear_tarjeta(
            self.contenido,
            "ESTADO",
            estado,
            descripcion_estado
        )

        self.crear_tarjeta(
            self.contenido,
            "DESTINO RESUELTO",
            resultado["ip"],
            (
                "Dirección IP obtenida para "
                "el destino analizado."
            )
        )

        # ========================================================
        # PAQUETES
        # ========================================================

        paquetes_frame = ctk.CTkFrame(
            self.contenido,
            fg_color="transparent"
        )

        paquetes_frame.pack(
            padx=7,
            pady=5,
            fill="x"
        )

        for columna in range(4):

            paquetes_frame.grid_columnconfigure(
                columna,
                weight=1,
                uniform="paquetes"
            )

        datos_paquetes = [
            (
                "ENVIADOS",
                resultado["enviados"]
            ),
            (
                "RECIBIDOS",
                resultado["recibidos"]
            ),
            (
                "PERDIDOS",
                resultado["perdidos"]
            ),
            (
                "PÉRDIDA",
                f"{resultado['perdida']} %"
            )
        ]

        for columna, (
            titulo,
            valor
        ) in enumerate(
            datos_paquetes
        ):

            card = ctk.CTkFrame(
                paquetes_frame,
                height=100,
                corner_radius=10,
                border_width=1
            )

            card.grid(
                row=0,
                column=columna,
                padx=5,
                sticky="nsew"
            )

            card.grid_propagate(
                False
            )

            ctk.CTkLabel(
                card,
                text=titulo,
                font=("Arial", 10, "bold"),
                text_color=self.AZUL
            ).pack(
                pady=(16, 5)
            )

            ctk.CTkLabel(
                card,
                text=str(valor),
                font=("Consolas", 20, "bold")
            ).pack()

        # ========================================================
        # LATENCIA
        # ========================================================

        ctk.CTkLabel(
            self.contenido,
            text="LATENCIA",
            font=("Arial", 16, "bold"),
            text_color=self.AZUL
        ).pack(
            pady=(20, 8)
        )

        latencia_frame = ctk.CTkFrame(
            self.contenido,
            fg_color="transparent"
        )

        latencia_frame.pack(
            padx=7,
            pady=(0, 15),
            fill="x"
        )

        for columna in range(3):

            latencia_frame.grid_columnconfigure(
                columna,
                weight=1,
                uniform="latencia"
            )

        datos_latencia = [
            (
                "MÍNIMA",
                resultado["minimo"]
            ),
            (
                "PROMEDIO",
                resultado["promedio"]
            ),
            (
                "MÁXIMA",
                resultado["maximo"]
            )
        ]

        for columna, (
            titulo,
            valor
        ) in enumerate(
            datos_latencia
        ):

            if valor is None:
                valor_texto = "—"
            else:
                valor_texto = f"{valor} ms"

            card = ctk.CTkFrame(
                latencia_frame,
                height=100,
                corner_radius=10,
                border_width=1
            )

            card.grid(
                row=0,
                column=columna,
                padx=5,
                sticky="nsew"
            )

            card.grid_propagate(
                False
            )

            ctk.CTkLabel(
                card,
                text=titulo,
                font=("Arial", 10, "bold"),
                text_color=self.AZUL
            ).pack(
                pady=(16, 5)
            )

            ctk.CTkLabel(
                card,
                text=valor_texto,
                font=("Consolas", 20, "bold")
            ).pack()

        self.crear_tarjeta(
            self.contenido,
            "INTERPRETACIÓN",
            "Prueba completada",
            (
                "La latencia representa el tiempo de ida "
                "y vuelta observado durante esta prueba. "
                "La pérdida indica qué porcentaje de los "
                "paquetes enviados no produjo una respuesta."
            )
        )

    # ============================================================
    # TRACEROUTE
    # ============================================================

    def iniciar_traceroute(self):

        destino = (
            self.destino_entry
            .get()
            .strip()
        )

        if not destino:

            messagebox.showwarning(
                "NetPro",
                "Introduce una dirección IP o dominio."
            )

            return

        self.bloquear_botones(True)

        self.estado_label.configure(
            text=(
                f"Ejecutando Traceroute "
                f"hacia {destino}..."
            )
        )

        self.limpiar_contenido()

        ctk.CTkLabel(
            self.contenido,
            text="TRACEROUTE EN PROGRESO",
            font=("Arial", 18, "bold"),
            text_color=self.AZUL
        ).pack(
            pady=(35, 10)
        )

        ctk.CTkLabel(
            self.contenido,
            text=(
                "La prueba puede tardar varios segundos.\n"
                "NetPro continúa funcionando mientras "
                "se obtiene la ruta."
            ),
            font=("Arial", 13),
            justify="center"
        ).pack()

        hilo = threading.Thread(
            target=self._ejecutar_traceroute_thread,
            args=(destino,),
            daemon=True
        )

        hilo.start()

    def _ejecutar_traceroute_thread(
        self,
        destino
    ):

        try:

            resultado = ejecutar_traceroute(
                destino
            )

            self.after(
                0,
                self.mostrar_resultado_traceroute,
                resultado
            )

        except Exception as error:

            self.after(
                0,
                self.mostrar_error,
                str(error)
            )

    # ============================================================
    # RESULTADO TRACEROUTE
    # ============================================================

    def mostrar_resultado_traceroute(
        self,
        resultado
    ):

        self.bloquear_botones(False)

        self.ultimo_traceroute = resultado

        self.estado_label.configure(
            text="Traceroute finalizado."
        )

        self.limpiar_contenido()

        # ========================================================
        # ERROR
        # ========================================================

        if resultado.get("error"):

            self.crear_tarjeta(
                self.contenido,
                "ERROR",
                "No fue posible completar la prueba",
                resultado["error"]
            )

            return

        salida = resultado.get(
            "salida",
            ""
        )

        saltos = self._analizar_saltos_traceroute(
            salida
        )

        cantidad_saltos = len(saltos)

        if saltos:
            ip_destino = saltos[-1]["ip"]
        else:
            ip_destino = "No identificado"

        salida_minuscula = salida.lower()

        completado = (
            "traza completa" in salida_minuscula
            or "trace complete" in salida_minuscula
        )

        estado = (
            "COMPLETADO"
            if completado
            else "FINALIZADO"
        )

        # ========================================================
        # CABECERA
        # ========================================================

        ctk.CTkLabel(
            self.contenido,
            text="RESULTADO TRACEROUTE",
            font=("Arial", 20, "bold"),
            text_color=self.AZUL
        ).pack(
            pady=(20, 4)
        )

        ctk.CTkLabel(
            self.contenido,
            text=resultado["destino"],
            font=("Consolas", 15, "bold")
        ).pack(
            pady=(0, 15)
        )

        # ========================================================
        # RESUMEN
        # ========================================================

        resumen_frame = ctk.CTkFrame(
            self.contenido,
            fg_color="transparent"
        )

        resumen_frame.pack(
            padx=7,
            pady=(0, 15),
            fill="x"
        )

        for columna in range(3):

            resumen_frame.grid_columnconfigure(
                columna,
                weight=1,
                uniform="resumen_traceroute"
            )

        resumen = [
            (
                "DESTINO",
                ip_destino
            ),
            (
                "SALTOS OBSERVADOS",
                cantidad_saltos
            ),
            (
                "ESTADO",
                estado
            )
        ]

        for columna, (
            titulo,
            valor
        ) in enumerate(resumen):

            card = ctk.CTkFrame(
                resumen_frame,
                height=105,
                corner_radius=10,
                border_width=1
            )

            card.grid(
                row=0,
                column=columna,
                padx=5,
                sticky="nsew"
            )

            card.grid_propagate(False)

            ctk.CTkLabel(
                card,
                text=titulo,
                font=("Arial", 10, "bold"),
                text_color=self.AZUL
            ).pack(
                pady=(17, 6)
            )

            ctk.CTkLabel(
                card,
                text=str(valor),
                font=("Consolas", 16, "bold")
            ).pack()

        # ========================================================
        # RUTA OBSERVADA
        # ========================================================

        ctk.CTkLabel(
            self.contenido,
            text="RUTA OBSERVADA",
            font=("Arial", 17, "bold"),
            text_color=self.AZUL
        ).pack(
            pady=(15, 8)
        )

        if not saltos:

            self.crear_tarjeta(
                self.contenido,
                "SIN SALTOS INTERPRETADOS",
                "No se pudieron estructurar los saltos",
                (
                    "NetPro conserva la salida original "
                    "para que puedas revisarla."
                )
            )

        else:

            for indice, salto in enumerate(saltos):

                es_ultimo = (
                    indice == len(saltos) - 1
                )

                self._crear_tarjeta_salto(
                    self.contenido,
                    salto,
                    es_ultimo
                )

        # ========================================================
        # DETALLE TÉCNICO
        # ========================================================

        limite = resultado.get(
            "max_saltos",
            30
        )

        self.crear_tarjeta(
            self.contenido,
            "DETALLE TÉCNICO",
            f"Límite configurado: {limite} saltos",
            (
                f"NetPro observó {cantidad_saltos} saltos "
                "durante esta prueba. El límite configurado "
                "es el máximo que Traceroute puede intentar."
            )
        )

        # ========================================================
        # SALIDA ORIGINAL
        # ========================================================

        boton_original = ctk.CTkButton(
            self.contenido,
            text="VER SALIDA ORIGINAL",
            width=230,
            height=40,
            font=("Arial", 12, "bold"),
            fg_color=self.AZUL,
            hover_color=self.AZUL_HOVER,
            command=lambda: self._mostrar_salida_original(
                resultado
            )
        )

        boton_original.pack(
            pady=(15, 25)
        )

    # ============================================================
    # ANALIZAR SALTOS
    # ============================================================

    def _analizar_saltos_traceroute(
        self,
        salida
    ):

        saltos = []

        for linea in salida.splitlines():

            linea = linea.strip()

            if not linea:
                continue

            coincidencia = re.match(
                r"^(\d+)\s+(.+)$",
                linea
            )

            if not coincidencia:
                continue

            numero = int(
                coincidencia.group(1)
            )

            resto = coincidencia.group(2)

            # ====================================================
            # IP
            # ====================================================

            ips = re.findall(
                r"(?:\d{1,3}\.){3}\d{1,3}",
                resto
            )

            ip = (
                ips[-1]
                if ips
                else "Sin respuesta"
            )

            # ====================================================
            # TIEMPOS
            # ====================================================

            tiempos = re.findall(
                r"(?:<\s*1|\d+)\s*ms|\*",
                resto,
                flags=re.IGNORECASE
            )

            tiempos_limpios = []

            for tiempo in tiempos[:3]:

                tiempo = re.sub(
                    r"\s+",
                    "",
                    tiempo
                )

                tiempos_limpios.append(
                    tiempo
                )

            while len(tiempos_limpios) < 3:

                tiempos_limpios.append("—")

            tipo = self._clasificar_ip_salto(
                ip
            )

            saltos.append({
                "numero": numero,
                "ip": ip,
                "tiempos": tiempos_limpios,
                "tipo": tipo
            })

        return saltos

    # ============================================================
    # CLASIFICAR IP
    # ============================================================

    def _clasificar_ip_salto(
        self,
        ip
    ):

        if ip == "Sin respuesta":
            return "Sin respuesta"

        try:

            direccion = ipaddress.ip_address(
                ip
            )

            if direccion.is_loopback:
                return "Loopback"

            if direccion.is_link_local:
                return "Link-local"

            if direccion.is_private:
                return "Dirección privada"

            if direccion.is_multicast:
                return "Multicast"

            return "Dirección pública"

        except ValueError:

            return "No identificada"

    # ============================================================
    # TARJETA DE SALTO
    # ============================================================

    def _crear_tarjeta_salto(
        self,
        parent,
        salto,
        es_ultimo=False
    ):

        tarjeta = ctk.CTkFrame(
            parent,
            corner_radius=10,
            border_width=1
        )

        tarjeta.pack(
            padx=12,
            pady=6,
            fill="x"
        )

        encabezado = ctk.CTkFrame(
            tarjeta,
            fg_color="transparent"
        )

        encabezado.pack(
            padx=16,
            pady=(13, 5),
            fill="x"
        )

        ctk.CTkLabel(
            encabezado,
            text=f"SALTO {salto['numero']}",
            font=("Arial", 13, "bold"),
            text_color=self.AZUL
        ).pack(
            side="left"
        )

        etiqueta_derecha = (
            "DESTINO"
            if es_ultimo
            else salto["tipo"]
        )

        ctk.CTkLabel(
            encabezado,
            text=etiqueta_derecha,
            font=("Arial", 11, "bold"),
            text_color=self.AZUL
        ).pack(
            side="right"
        )

        # ========================================================
        # IP
        # ========================================================

        ctk.CTkLabel(
            tarjeta,
            text=salto["ip"],
            font=("Consolas", 16, "bold"),
            anchor="w"
        ).pack(
            padx=16,
            pady=(3, 8),
            anchor="w"
        )

        # ========================================================
        # TIEMPOS
        # ========================================================

        tiempos_frame = ctk.CTkFrame(
            tarjeta,
            fg_color="transparent"
        )

        tiempos_frame.pack(
            padx=12,
            pady=(0, 12),
            fill="x"
        )

        for columna in range(3):

            tiempos_frame.grid_columnconfigure(
                columna,
                weight=1,
                uniform="tiempos"
            )

        for columna, tiempo in enumerate(
            salto["tiempos"]
        ):

            bloque = ctk.CTkFrame(
                tiempos_frame,
                corner_radius=7
            )

            bloque.grid(
                row=0,
                column=columna,
                padx=4,
                sticky="ew"
            )

            ctk.CTkLabel(
                bloque,
                text=f"Intento {columna + 1}",
                font=("Arial", 9),
                text_color=self.AZUL
            ).pack(
                pady=(7, 1)
            )

            ctk.CTkLabel(
                bloque,
                text=tiempo,
                font=("Consolas", 13, "bold")
            ).pack(
                pady=(0, 7)
            )

    # ============================================================
    # SALIDA ORIGINAL TRACEROUTE
    # ============================================================

    def _mostrar_salida_original(
        self,
        resultado
    ):

        ventana = ctk.CTkToplevel(self)

        ventana.title(
            "NetPro - Salida original de Traceroute"
        )

        ventana.geometry(
            "850x600"
        )

        ventana.minsize(
            700,
            500
        )

        ventana.transient(
            self.winfo_toplevel()
        )

        ctk.CTkLabel(
            ventana,
            text="Salida original de Traceroute",
            font=("Arial", 24, "bold"),
            text_color=self.AZUL
        ).pack(
            pady=(25, 5)
        )

        ctk.CTkLabel(
            ventana,
            text=resultado["destino"],
            font=("Consolas", 14)
        ).pack(
            pady=(0, 15)
        )

        texto = ctk.CTkTextbox(
            ventana,
            font=("Consolas", 13),
            wrap="none"
        )

        texto.pack(
            padx=25,
            pady=(0, 25),
            fill="both",
            expand=True
        )

        texto.insert(
            "1.0",
            resultado.get(
                "salida",
                "Sin salida."
            )
        )

        texto.configure(
            state="disabled"
        )

    # ============================================================
    # ERRORES
    # ============================================================

    def mostrar_error(
        self,
        mensaje
    ):

        self.bloquear_botones(False)

        self.estado_label.configure(
            text="No fue posible completar la prueba."
        )

        self.limpiar_contenido()

        self.crear_tarjeta(
            self.contenido,
            "ERROR",
            "Prueba no completada",
            mensaje
        )

    # ============================================================
    # MODO APRENDIZAJE
    # ============================================================

    def mostrar_aprendizaje(self):

        ventana = ctk.CTkToplevel(self)

        ventana.title(
            "NetPro - Diagnóstico de red"
        )

        ventana.geometry(
            "850x700"
        )

        ventana.minsize(
            750,
            600
        )

        ventana.transient(
            self.winfo_toplevel()
        )

        ctk.CTkLabel(
            ventana,
            text="¿Qué significa cada concepto?",
            font=("Arial", 26, "bold"),
            text_color=self.AZUL
        ).pack(
            pady=(25, 5)
        )

        ctk.CTkLabel(
            ventana,
            text="Modo aprendizaje · Diagnóstico",
            font=("Arial", 14),
            text_color=self.AZUL
        ).pack(
            pady=(0, 15)
        )

        scroll = ctk.CTkScrollableFrame(
            ventana,
            width=760,
            height=570,
            corner_radius=12
        )

        scroll.pack(
            padx=25,
            pady=(0, 25),
            fill="both",
            expand=True
        )

        conceptos = [
            (
                "PING",
                "Prueba de conectividad",
                (
                    "Ping envía solicitudes hacia un destino "
                    "y observa si recibe respuestas. También "
                    "permite medir el tiempo de ida y vuelta."
                )
            ),
            (
                "LATENCIA",
                "Tiempo de respuesta",
                (
                    "Se expresa normalmente en milisegundos "
                    "(ms). Representa el tiempo observado entre "
                    "el envío de una solicitud y la recepción "
                    "de su respuesta."
                )
            ),
            (
                "PÉRDIDA DE PAQUETES",
                "Paquetes sin respuesta",
                (
                    "Indica qué porcentaje de los paquetes "
                    "enviados durante la prueba no produjo "
                    "una respuesta."
                )
            ),
            (
                "TRACEROUTE",
                "Ruta hacia un destino",
                (
                    "Permite observar una secuencia de saltos "
                    "intermedios entre tu equipo y un destino."
                )
            ),
            (
                "SALTO",
                "Dispositivo intermedio",
                (
                    "Un salto representa un punto intermedio "
                    "observado durante el recorrido hacia "
                    "el destino."
                )
            ),
            (
                "TTL",
                "Time To Live",
                (
                    "Es un campo de IP que limita cuánto puede "
                    "avanzar un paquete. Los routers reducen "
                    "su valor a medida que el paquete atraviesa "
                    "la red."
                )
            ),
            (
                "* * *",
                "Sin respuesta en ese intento",
                (
                    "En Traceroute, los asteriscos indican que "
                    "no se obtuvo una respuesta dentro del "
                    "tiempo esperado. Esto no demuestra por "
                    "sí solo que ese dispositivo esté caído."
                )
            )
        ]

        for (
            titulo,
            valor,
            descripcion
        ) in conceptos:

            self.crear_tarjeta(
                scroll,
                titulo,
                valor,
                descripcion
            )