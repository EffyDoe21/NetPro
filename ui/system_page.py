import customtkinter as ctk
import threading

from core.system_info import (
    obtener_informacion_sistema,
    obtener_adaptador_principal,
    obtener_gpu_principal,
    bytes_legibles,
    bool_legible
)

try:
    from AI.ollama_client import generar_respuesta
except ImportError:
    generar_respuesta = None


class SystemFrame(ctk.CTkFrame):

    # ============================================================
    # COLORES NETPRO
    # ============================================================
    FONDO = "#2B2B2B"
    PANEL = "#1A1A1A"
    PANEL_2 = "#242424"
    BORDE = "#444444"

    AZUL = "#3B8ED0"
    AZUL_OSCURO = "#36719F"

    TEXTO = "#FFFFFF"
    TEXTO_2 = "#A0A0A0"

    VERDE = "#2ECC71"
    AMARILLO = "#F1C40F"
    ROJO = "#E74C3C"

    # ============================================================
    # INICIO
    # ============================================================

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color=self.FONDO
        )

        self.sistema = None
        self.detalles_visibles = False
        self.cargando = False

        # Permite que la pagina crezca con la ventana.
        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        # --------------------------------------------------------
        # SCROLL PRINCIPAL
        # --------------------------------------------------------

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=self.FONDO,
            corner_radius=0
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

        self.crear_encabezado()

        self.crear_estado_carga()

        self.crear_resumen()

        self.crear_sistema()

        self.crear_almacenamiento()

        self.crear_red()

        self.crear_seguridad()

        self.crear_netpro()

        self.crear_detalles()

        self.crear_panel_ia()

        # Carga inicial.
        self.after(
            300,
            self.actualizar_informacion
        )

    # ============================================================
    # ENCABEZADO
    # ============================================================
        # ============================================================
    # ENCABEZADO
    # ============================================================

    def crear_encabezado(self):

        frame = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent"
        )

        frame.pack(
            fill="x",
            padx=30,
            pady=(25, 10)
        )

        # ========================================================
        # TITULO Y DESCRIPCION - LADO IZQUIERDO
        # ========================================================

        titulo_frame = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        titulo_frame.pack(
            side="left",
            fill="x",
            expand=True
        )

        ctk.CTkLabel(
            titulo_frame,
            text="🖥 Mi Sistema",
            font=("Arial", 28, "bold"),
            text_color=self.AZUL
        ).pack(
            anchor="w",
            pady=(0, 4)
        )

        ctk.CTkLabel(
            titulo_frame,
            text=(
                "Informacion de hardware, "
                "red y seguridad del equipo"
            ),
            font=("Arial", 14),
            text_color=self.TEXTO_2
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # ========================================================
        # BOTONES - LADO DERECHO
        # ========================================================

        botones = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        botones.pack(
            side="right"
        )

        self.btn_actualizar = ctk.CTkButton(
            botones,
            text="Actualizar",
            width=120,
            height=38,
            corner_radius=7,
            fg_color=self.PANEL_2,
            hover_color=self.BORDE,
            border_width=1,
            border_color=self.BORDE,
            command=self.actualizar_informacion
        )

        self.btn_actualizar.pack(
            side="left",
            padx=5
        )

        self.btn_detalles = ctk.CTkButton(
            botones,
            text="Ver mas informacion",
            width=170,
            height=38,
            corner_radius=7,
            fg_color=self.PANEL_2,
            hover_color=self.BORDE,
            border_width=1,
            border_color=self.BORDE,
            command=self.alternar_detalles
        )

        self.btn_detalles.pack(
            side="left",
            padx=5
        )

        self.btn_ia = ctk.CTkButton(
            botones,
            text="Analizar con NetPro AI",
            width=180,
            height=38,
            corner_radius=7,
            fg_color=self.AZUL_OSCURO,
            hover_color=self.AZUL,
            command=self.analizar_ia
        )

        self.btn_ia.pack(
            side="left",
            padx=(5, 0)
        )

    # ============================================================
    # ESTADO DE CARGA
    # ============================================================

    def crear_estado_carga(self):

        self.estado_frame = ctk.CTkFrame(
            self.scroll,
            fg_color=self.PANEL,
            corner_radius=8,
            border_width=1,
            border_color=self.BORDE
        )

        self.estado_frame.pack(
            fill="x",
            padx=30,
            pady=(5, 15)
        )

        self.estado_label = ctk.CTkLabel(
            self.estado_frame,
            text=(
                "Preparando informacion "
                "del sistema..."
            ),
            font=("Arial", 13),
            text_color=self.TEXTO_2
        )

        self.estado_label.pack(
            padx=15,
            pady=10
        )

    # ============================================================
    # RESUMEN
    # ============================================================

    def crear_resumen(self):

        self.resumen_frame = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent"
        )

        self.resumen_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        for columna in range(3):
            self.resumen_frame.grid_columnconfigure(
                columna,
                weight=1
            )

        self.card_cpu = self.crear_tarjeta(
            self.resumen_frame,
            0,
            "CPU"
        )

        self.card_ram = self.crear_tarjeta(
            self.resumen_frame,
            1,
            "MEMORIA RAM"
        )

        self.card_gpu = self.crear_tarjeta(
            self.resumen_frame,
            2,
            "GPU"
        )

    def crear_tarjeta(
        self,
        parent,
        columna,
        titulo
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color=self.PANEL,
            corner_radius=10,
            border_width=1,
            border_color=self.BORDE
        )

        frame.grid(
            row=0,
            column=columna,
            sticky="nsew",
            padx=(
                0 if columna == 0 else 6,
                0 if columna == 2 else 6
            )
        )

        ctk.CTkLabel(
            frame,
            text=titulo,
            font=(
                "Arial",
                12,
                "bold"
            ),
            text_color=self.AZUL
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 4)
        )

        valor = ctk.CTkLabel(
            frame,
            text="Cargando...",
            font=(
                "Arial",
                18,
                "bold"
            ),
            text_color=self.TEXTO,
            wraplength=300,
            justify="left"
        )

        valor.pack(
            anchor="w",
            padx=18
        )

        detalle = ctk.CTkLabel(
            frame,
            text="",
            font=(
                "Arial",
                12
            ),
            text_color=self.TEXTO_2,
            justify="left"
        )

        detalle.pack(
            anchor="w",
            padx=18,
            pady=(5, 15)
        )

        return {
            "frame": frame,
            "valor": valor,
            "detalle": detalle
        }

    # ============================================================
    # CONTENEDOR DE SECCION
    # ============================================================

    def crear_seccion(
        self,
        titulo
    ):

        exterior = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent"
        )

        exterior.pack(
            fill="x",
            padx=30,
            pady=(0, 18)
        )

        ctk.CTkLabel(
            exterior,
            text=titulo,
            font=(
                "Arial",
                16,
                "bold"
            ),
            text_color=self.TEXTO
        ).pack(
            anchor="w",
            pady=(0, 7)
        )

        contenido = ctk.CTkFrame(
            exterior,
            fg_color=self.PANEL,
            corner_radius=10,
            border_width=1,
            border_color=self.BORDE
        )

        contenido.pack(
            fill="x"
        )

        return contenido

    # ============================================================
    # SISTEMA
    # ============================================================

    def crear_sistema(self):

        self.sistema_frame = self.crear_seccion(
            "SISTEMA"
        )

        self.sistema_label = ctk.CTkLabel(
            self.sistema_frame,
            text="Cargando...",
            justify="left",
            anchor="w",
            font=("Arial", 13),
            text_color=self.TEXTO
        )

        self.sistema_label.pack(
            fill="x",
            padx=18,
            pady=15
        )

    # ============================================================
    # ALMACENAMIENTO
    # ============================================================

    def crear_almacenamiento(self):

        self.almacenamiento_frame = (
            self.crear_seccion(
                "ALMACENAMIENTO"
            )
        )

        self.discos_contenedor = ctk.CTkFrame(
            self.almacenamiento_frame,
            fg_color="transparent"
        )

        self.discos_contenedor.pack(
            fill="x",
            padx=18,
            pady=15
        )

    # ============================================================
    # RED
    # ============================================================

    def crear_red(self):

        self.red_frame = self.crear_seccion(
            "RED"
        )

        self.red_label = ctk.CTkLabel(
            self.red_frame,
            text="Cargando...",
            justify="left",
            anchor="w",
            font=("Arial", 13),
            text_color=self.TEXTO
        )

        self.red_label.pack(
            fill="x",
            padx=18,
            pady=15
        )

    # ============================================================
    # SEGURIDAD
    # ============================================================

    def crear_seguridad(self):

        self.seguridad_frame = self.crear_seccion(
            "SEGURIDAD"
        )

        self.seguridad_label = ctk.CTkLabel(
            self.seguridad_frame,
            text="Cargando...",
            justify="left",
            anchor="w",
            font=("Arial", 13),
            text_color=self.TEXTO
        )

        self.seguridad_label.pack(
            fill="x",
            padx=18,
            pady=15
        )

    # ============================================================
    # NETPRO
    # ============================================================

    def crear_netpro(self):

        self.netpro_frame = self.crear_seccion(
            "ENTORNO NETPRO"
        )

        self.netpro_label = ctk.CTkLabel(
            self.netpro_frame,
            text="Cargando...",
            justify="left",
            anchor="w",
            font=("Arial", 13),
            text_color=self.TEXTO
        )

        self.netpro_label.pack(
            fill="x",
            padx=18,
            pady=15
        )

    # ============================================================
    # INFORMACION AVANZADA
    # ============================================================

    def crear_detalles(self):

        self.detalles_exterior = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent"
        )

        # No se muestra inicialmente.

        ctk.CTkLabel(
            self.detalles_exterior,
            text="INFORMACION AVANZADA",
            font=(
                "Arial",
                18,
                "bold"
            ),
            text_color=self.AZUL
        ).pack(
            anchor="w",
            pady=(5, 10)
        )

        self.detalles_texto = ctk.CTkTextbox(
            self.detalles_exterior,
            height=550,
            fg_color=self.PANEL,
            border_width=1,
            border_color=self.BORDE,
            corner_radius=10,
            text_color=self.TEXTO,
            font=(
                "Consolas",
                12
            ),
            wrap="word"
        )

        self.detalles_texto.pack(
            fill="x"
        )

        self.detalles_texto.configure(
            state="disabled"
        )

    # ============================================================
    # PANEL IA
    # ============================================================

    def crear_panel_ia(self):

        self.ia_exterior = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent"
        )

        # Oculto inicialmente.

        ctk.CTkLabel(
            self.ia_exterior,
            text="ANALISIS DE NETPRO AI",
            font=(
                "Arial",
                18,
                "bold"
            ),
            text_color=self.AZUL
        ).pack(
            anchor="w",
            pady=(5, 10)
        )

        self.ia_texto = ctk.CTkTextbox(
            self.ia_exterior,
            height=280,
            fg_color=self.PANEL,
            border_width=1,
            border_color=self.BORDE,
            corner_radius=10,
            text_color=self.TEXTO,
            font=(
                "Arial",
                13
            ),
            wrap="word"
        )

        self.ia_texto.pack(
            fill="x"
        )

        self.ia_texto.configure(
            state="disabled"
        )

    # ============================================================
    # ACTUALIZAR
    # ============================================================

    def actualizar_informacion(self):

        if self.cargando:
            return

        self.cargando = True

        self.btn_actualizar.configure(
            state="disabled",
            text="Actualizando..."
        )

        self.estado_label.configure(
            text=(
                "Recopilando informacion "
                "del equipo. Esto puede "
                "tardar unos segundos..."
            ),
            text_color=self.AZUL
        )

        hilo = threading.Thread(
            target=self._cargar_sistema,
            daemon=True
        )

        hilo.start()

    def _cargar_sistema(self):

        try:
            sistema = (
                obtener_informacion_sistema()
            )

            self.after(
                0,
                lambda: self._mostrar_sistema(
                    sistema
                )
            )

        except Exception as error:

            mensaje = str(
                error
            )

            self.after(
                0,
                lambda: self._mostrar_error(
                    mensaje
                )
            )

    # ============================================================
    # MOSTRAR RESULTADOS
    # ============================================================

    def _mostrar_sistema(
        self,
        sistema
    ):
        # Evitar actualizar una pagina que ya fue destruida
        if not self.winfo_exists():
            return

        self.sistema = sistema
        self.cargando = False

        if self.winfo_exists() and self.btn_actualizar.winfo_exists():
            self.btn_actualizar.configure(
            state="normal",
            text="Actualizar"
        )

        if sistema.errores:

            self.estado_label.configure(
                text=(
                    "Informacion recopilada "
                    "con algunos datos no disponibles."
                ),
                text_color=self.AMARILLO
            )

        else:

            self.estado_label.configure(
                text=(
                    "Informacion del sistema "
                    "actualizada correctamente."
                ),
                text_color=self.VERDE
            )

        self.actualizar_tarjetas()
        self.actualizar_sistema()
        self.actualizar_almacenamiento()
        self.actualizar_red()
        self.actualizar_seguridad()
        self.actualizar_netpro()
        self.actualizar_detalles()

    def _mostrar_error(
        self,
        mensaje
    ):

        self.cargando = False

        self.btn_actualizar.configure(
            state="normal",
            text="Actualizar"
        )

        self.estado_label.configure(
            text=(
                "No fue posible obtener "
                "la informacion del sistema.\n"
                + mensaje
            ),
            text_color=self.ROJO
        )

    # ============================================================
    # TARJETAS
    # ============================================================

    def actualizar_tarjetas(self):

        s = self.sistema

        self.card_cpu[
            "valor"
        ].configure(
            text=s.cpu.nombre
        )

        cpu_detalle = (
            f"{s.cpu.nucleos_fisicos or '-'} nucleos"
            f" / "
            f"{s.cpu.procesadores_logicos or '-'} logicos"
        )

        self.card_cpu[
            "detalle"
        ].configure(
            text=cpu_detalle
        )

        self.card_ram[
            "valor"
        ].configure(
            text=bytes_legibles(
                s.memoria.total_bytes
            )
        )

        ram_uso = (
            f"{s.memoria.uso_porcentaje}% en uso"
            if s.memoria.uso_porcentaje
            is not None
            else "Uso no disponible"
        )

        self.card_ram[
            "detalle"
        ].configure(
            text=ram_uso
        )

        gpu = obtener_gpu_principal(
            s
        )

        if gpu:

            self.card_gpu[
                "valor"
            ].configure(
                text=gpu.nombre
            )

            self.card_gpu[
                "detalle"
            ].configure(
                text=(
                    f"{bytes_legibles(gpu.memoria_bytes)} VRAM"
                )
            )

        else:

            self.card_gpu[
                "valor"
            ].configure(
                text="No disponible"
            )

            self.card_gpu[
                "detalle"
            ].configure(
                text=""
            )

    # ============================================================
    # SISTEMA
    # ============================================================

    def actualizar_sistema(self):

        s = self.sistema

        texto = (
            f"{s.sistema_operativo}\n"
            f"Version: {s.version_sistema}   "
            f"Build: {s.build}\n"
            f"Arquitectura: {s.arquitectura}\n"
            f"Equipo: {s.fabricante_equipo} "
            f"{s.modelo_equipo}"
        )

        self.sistema_label.configure(
            text=texto
        )

    # ============================================================
    # ALMACENAMIENTO
    # ============================================================

    def actualizar_almacenamiento(self):

        for widget in (
            self.discos_contenedor.winfo_children()
        ):
            widget.destroy()

        if not self.sistema.volumenes:

            ctk.CTkLabel(
                self.discos_contenedor,
                text="No disponible",
                text_color=self.TEXTO_2
            ).pack(
                anchor="w"
            )

            return

        for volumen in (
            self.sistema.volumenes
        ):

            fila = ctk.CTkFrame(
                self.discos_contenedor,
                fg_color="transparent"
            )

            fila.pack(
                fill="x",
                pady=7
            )

            etiqueta = (
                volumen.etiqueta
                if volumen.etiqueta
                else "Sin etiqueta"
            )

            superior = ctk.CTkFrame(
                fila,
                fg_color="transparent"
            )

            superior.pack(
                fill="x"
            )

            ctk.CTkLabel(
                superior,
                text=(
                    f"{volumen.unidad} "
                    f"{etiqueta}"
                ),
                font=(
                    "Arial",
                    13,
                    "bold"
                ),
                text_color=self.TEXTO
            ).pack(
                side="left"
            )

            porcentaje = (
                volumen.uso_porcentaje
                if volumen.uso_porcentaje
                is not None
                else 0
            )

            color = self.VERDE

            if porcentaje >= 90:
                color = self.ROJO

            elif porcentaje >= 75:
                color = self.AMARILLO

            ctk.CTkLabel(
                superior,
                text=f"{porcentaje:.2f}%",
                font=(
                    "Arial",
                    12,
                    "bold"
                ),
                text_color=color
            ).pack(
                side="right"
            )

            barra = ctk.CTkProgressBar(
                fila,
                height=8,
                corner_radius=4,
                progress_color=color,
                fg_color=self.PANEL_2
            )

            barra.pack(
                fill="x",
                pady=(6, 4)
            )

            barra.set(
                min(
                    max(
                        porcentaje / 100,
                        0
                    ),
                    1
                )
            )

            ctk.CTkLabel(
                fila,
                text=(
                    f"{bytes_legibles(volumen.libre_bytes)} libres "
                    f"de {bytes_legibles(volumen.total_bytes)}"
                ),
                font=(
                    "Arial",
                    11
                ),
                text_color=self.TEXTO_2
            ).pack(
                anchor="w"
            )

    # ============================================================
    # RED
    # ============================================================

    def actualizar_red(self):

        adaptador = (
            obtener_adaptador_principal(
                self.sistema
            )
        )

        if not adaptador:

            self.red_label.configure(
                text=(
                    "No se encontro una "
                    "conexion principal."
                )
            )

            return

        ipv4 = (
            ", ".join(adaptador.ipv4)
            if adaptador.ipv4
            else "No disponible"
        )

        gateway = (
            ", ".join(adaptador.gateway)
            if adaptador.gateway
            else "No disponible"
        )

        dns = (
            ", ".join(adaptador.dns)
            if adaptador.dns
            else "No disponible"
        )

        velocidad = (
            f"{adaptador.velocidad_mbps} Mbps"
            if adaptador.velocidad_mbps
            is not None
            else "No disponible"
        )

        texto = (
            f"{adaptador.nombre}   "
            f"[{adaptador.estado}]\n"
            f"IPv4: {ipv4}\n"
            f"Gateway: {gateway}\n"
            f"DNS: {dns}\n"
            f"Velocidad: {velocidad}"
        )

        self.red_label.configure(
            text=texto
        )

    # ============================================================
    # SEGURIDAD
    # ============================================================

    def actualizar_seguridad(self):

        s = self.sistema.seguridad

        firewall_activo = any(
            perfil.habilitado is True
            for perfil in s.firewall
        )

        texto = (
            "Microsoft Defender: "
            f"{bool_legible(s.defender_antivirus)}\n"
            "Proteccion en tiempo real: "
            f"{bool_legible(s.defender_tiempo_real)}\n"
            "Firewall: "
            f"{'Si' if firewall_activo else 'No disponible'}\n"
            "Secure Boot: "
            f"{bool_legible(s.secure_boot)}\n"
            "TPM: "
            f"{bool_legible(s.tpm_presente)}"
        )

        self.seguridad_label.configure(
            text=texto
        )

    # ============================================================
    # NETPRO
    # ============================================================

    def actualizar_netpro(self):

        e = self.sistema.entorno

        modelos = (
            ", ".join(e.modelos_ollama)
            if e.modelos_ollama
            else "No disponibles"
        )

        texto = (
            f"Python: {e.python_version}\n"
            f"Entorno virtual: "
            f"{bool_legible(e.entorno_virtual)}\n"
            f"Ollama: "
            f"{bool_legible(e.ollama_disponible)}\n"
            f"Version Ollama: "
            f"{e.ollama_version}\n"
            f"Modelos: {modelos}"
        )

        self.netpro_label.configure(
            text=texto
        )

    # ============================================================
    # DETALLES
    # ============================================================

    def alternar_detalles(self):

        if not self.sistema:
            return

        self.detalles_visibles = (
            not self.detalles_visibles
        )

        if self.detalles_visibles:

            self.detalles_exterior.pack(
                fill="x",
                padx=30,
                pady=(0, 20)
            )

            self.btn_detalles.configure(
                text="Ocultar informacion"
            )

        else:

            self.detalles_exterior.pack_forget()

            self.btn_detalles.configure(
                text="Ver mas informacion"
            )

    def actualizar_detalles(self):

        if not self.sistema:
            return

        s = self.sistema

        lineas = []

        lineas.append(
            "SISTEMA"
        )

        lineas.append(
            "-" * 65
        )

        lineas.append(
            f"Equipo: {s.nombre_equipo}"
        )

        lineas.append(
            f"Usuario: {s.usuario}"
        )

        lineas.append(
            f"Sistema operativo: {s.sistema_operativo}"
        )

        lineas.append(
            f"Version: {s.version_sistema}"
        )

        lineas.append(
            f"Build: {s.build}"
        )

        lineas.append(
            f"Arquitectura: {s.arquitectura}"
        )

        lineas.append(
            f"Fabricante: {s.fabricante_equipo}"
        )

        lineas.append(
            f"Modelo: {s.modelo_equipo}"
        )

        lineas.append(
            ""
        )

        lineas.append(
            "PLACA BASE Y BIOS"
        )

        lineas.append(
            "-" * 65
        )

        lineas.append(
            f"Placa: "
            f"{s.placa_base.fabricante} "
            f"{s.placa_base.producto}"
        )

        lineas.append(
            f"BIOS: {s.bios.version}"
        )

        lineas.append(
            f"Fabricante BIOS: "
            f"{s.bios.fabricante}"
        )

        lineas.append(
            f"Fecha BIOS: {s.bios.fecha}"
        )

        lineas.append(
            f"Firmware: "
            f"{s.bios.modo_firmware}"
        )

        lineas.append(
            ""
        )

        lineas.append(
            "CPU"
        )

        lineas.append(
            "-" * 65
        )

        lineas.append(
            f"Modelo: {s.cpu.nombre}"
        )

        lineas.append(
            f"Socket: {s.cpu.socket}"
        )

        lineas.append(
            f"Nucleos: "
            f"{s.cpu.nucleos_fisicos}"
        )

        lineas.append(
            f"Logicos: "
            f"{s.cpu.procesadores_logicos}"
        )

        lineas.append(
            f"Frecuencia actual: "
            f"{s.cpu.frecuencia_actual_mhz} MHz"
        )

        lineas.append(
            f"Frecuencia maxima: "
            f"{s.cpu.frecuencia_max_mhz} MHz"
        )

        lineas.append(
            f"Carga: "
            f"{s.cpu.carga_porcentaje}%"
        )

        lineas.append(
            ""
        )

        lineas.append(
            "MODULOS RAM"
        )

        lineas.append(
            "-" * 65
        )

        for i, modulo in enumerate(
            s.memoria.modulos,
            start=1
        ):

            lineas.append(
                f"Modulo {i}"
            )

            lineas.append(
                f"  Banco: {modulo.banco}"
            )

            lineas.append(
                "  Capacidad: "
                f"{bytes_legibles(modulo.capacidad_bytes)}"
            )

            lineas.append(
                f"  Tipo: {modulo.tipo_memoria}"
            )

            lineas.append(
                f"  Velocidad: "
                f"{modulo.velocidad_configurada_mhz} MHz"
            )

            lineas.append(
                f"  Part Number: "
                f"{modulo.numero_parte}"
            )

        lineas.append(
            ""
        )

        lineas.append(
            "GPU"
        )

        lineas.append(
            "-" * 65
        )

        for gpu in s.gpus:

            lineas.append(
                f"{gpu.nombre}"
            )

            lineas.append(
                f"  Tipo: {gpu.tipo}"
            )

            lineas.append(
                "  VRAM: "
                f"{bytes_legibles(gpu.memoria_bytes)}"
            )

            lineas.append(
                f"  Driver: {gpu.driver}"
            )

            lineas.append(
                f"  Resolucion: "
                f"{gpu.resolucion}"
            )

            lineas.append(
                f"  Refresco: "
                f"{gpu.frecuencia_refresco_hz} Hz"
            )

        lineas.append(
            ""
        )

        lineas.append(
            "DISCOS FISICOS"
        )

        lineas.append(
            "-" * 65
        )

        for disco in s.discos_fisicos:

            lineas.append(
                f"{disco.nombre}"
            )

            lineas.append(
                f"  Tipo: {disco.tipo_medio}"
            )

            lineas.append(
                f"  Bus: {disco.bus}"
            )

            lineas.append(
                "  Tamano: "
                f"{bytes_legibles(disco.tamano_bytes)}"
            )

            lineas.append(
                f"  Salud: "
                f"{disco.estado_salud}"
            )

        lineas.append(
            ""
        )

        lineas.append(
            "ADAPTADORES DE RED"
        )

        lineas.append(
            "-" * 65
        )

        for red in s.adaptadores_red:

            lineas.append(
                f"{red.nombre} [{red.estado}]"
            )

            lineas.append(
                f"  Tipo: {red.tipo}"
            )

            lineas.append(
                f"  MAC: {red.mac}"
            )

            lineas.append(
                "  IPv4: "
                + (
                    ", ".join(red.ipv4)
                    if red.ipv4
                    else "No disponible"
                )
            )

            lineas.append(
                "  IPv6: "
                + (
                    ", ".join(red.ipv6)
                    if red.ipv6
                    else "No disponible"
                )
            )

            lineas.append(
                "  Gateway: "
                + (
                    ", ".join(red.gateway)
                    if red.gateway
                    else "No disponible"
                )
            )

            lineas.append(
                "  DNS: "
                + (
                    ", ".join(red.dns)
                    if red.dns
                    else "No disponible"
                )
            )

            lineas.append(
                ""
            )

        lineas.append(
            "FIREWALL"
        )

        lineas.append(
            "-" * 65
        )

        for perfil in s.seguridad.firewall:

            lineas.append(
                f"{perfil.nombre}: "
                f"{bool_legible(perfil.habilitado)}"
            )

        lineas.append(
            ""
        )

        lineas.append(
            "ENTORNO NETPRO"
        )

        lineas.append(
            "-" * 65
        )

        lineas.append(
            f"Python: "
            f"{s.entorno.python_version}"
        )

        lineas.append(
            f"Ejecutable: "
            f"{s.entorno.python_executable}"
        )

        lineas.append(
            f"VENV: "
            f"{s.entorno.virtual_env}"
        )

        lineas.append(
            f"Ollama: "
            f"{s.entorno.ollama_version}"
        )

        for modelo in (
            s.entorno.modelos_ollama
        ):

            lineas.append(
                f"  - {modelo}"
            )

        texto = "\n".join(
            lineas
        )

        self.detalles_texto.configure(
            state="normal"
        )

        self.detalles_texto.delete(
            "1.0",
            "end"
        )

        self.detalles_texto.insert(
            "1.0",
            texto
        )

        self.detalles_texto.configure(
            state="disabled"
        )

    # ============================================================
    # NETPRO AI
    # ============================================================

    def analizar_ia(self):

        if not self.sistema:
            return

        if generar_respuesta is None:

            self.mostrar_respuesta_ia(
                "No se encontro la funcion "
                "generar_respuesta en "
                "AI/ollama_client.py."
            )

            return

        self.ia_exterior.pack(
            fill="x",
            padx=30,
            pady=(0, 25)
        )

        self.btn_ia.configure(
            state="disabled",
            text="Analizando..."
        )

        self.mostrar_respuesta_ia(
            "NetPro AI esta analizando "
            "la informacion del equipo..."
        )

        hilo = threading.Thread(
            target=self._ejecutar_ia,
            daemon=True
        )

        hilo.start()

    def _ejecutar_ia(self):

        try:

            s = self.sistema

            adaptador = (
                obtener_adaptador_principal(
                    s
                )
            )

            gpu = obtener_gpu_principal(
                s
            )

            volumenes = []

            for volumen in s.volumenes:

                volumenes.append(
                    f"{volumen.unidad}: "
                    f"{volumen.uso_porcentaje}% usado, "
                    f"{bytes_legibles(volumen.libre_bytes)} libre"
                )

            prompt = f"""
NetPro realizo un analisis local del equipo.

Explica estos resultados en espanol de forma educativa,
tecnica y concisa.

No inventes vulnerabilidades.
No conviertas una observacion en una falla.
No afirmes que un componente esta danado si los datos
no lo demuestran.

SISTEMA:
{s.sistema_operativo}
Version: {s.version_sistema}
Build: {s.build}

CPU:
{s.cpu.nombre}
Nucleos: {s.cpu.nucleos_fisicos}
Logicos: {s.cpu.procesadores_logicos}
Carga: {s.cpu.carga_porcentaje}%

RAM:
Total: {bytes_legibles(s.memoria.total_bytes)}
Usada: {bytes_legibles(s.memoria.usada_bytes)}
Uso: {s.memoria.uso_porcentaje}%

GPU:
{gpu.nombre if gpu else "No disponible"}
VRAM: {bytes_legibles(gpu.memoria_bytes) if gpu else "No disponible"}

ALMACENAMIENTO:
{chr(10).join(volumenes)}

RED:
Adaptador: {adaptador.nombre if adaptador else "No disponible"}
IPv4: {", ".join(adaptador.ipv4) if adaptador else "No disponible"}
Gateway: {", ".join(adaptador.gateway) if adaptador else "No disponible"}
Velocidad: {adaptador.velocidad_mbps if adaptador else "No disponible"} Mbps

SEGURIDAD:
Defender: {s.seguridad.defender_antivirus}
Proteccion en tiempo real: {s.seguridad.defender_tiempo_real}

Indica:
1. Estado general observado.
2. Aspectos que llaman la atencion.
3. Recomendaciones educativas o de mantenimiento.
"""

            respuesta = generar_respuesta(
                prompt
            )

            self.after(
                0,
                lambda: self._finalizar_ia(
                    respuesta
                )
            )

        except Exception as error:

            mensaje = (
                "No fue posible obtener "
                "el analisis de NetPro AI.\n\n"
                + str(error)
            )

            self.after(
                0,
                lambda: self._finalizar_ia(
                    mensaje
                )
            )

    def _finalizar_ia(
        self,
        respuesta
    ):

        self.btn_ia.configure(
            state="normal",
            text="Analizar con NetPro AI"
        )

        self.mostrar_respuesta_ia(
            respuesta
        )

    def mostrar_respuesta_ia(
        self,
        texto
    ):

        self.ia_texto.configure(
            state="normal"
        )

        self.ia_texto.delete(
            "1.0",
            "end"
        )

        self.ia_texto.insert(
            "1.0",
            str(texto)
        )

        self.ia_texto.configure(
            state="disabled"
        )