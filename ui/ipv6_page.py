import customtkinter as ctk

from core.ipv6 import (
    analizar_ipv6,
    comprimir_ipv6,
    expandir_ipv6,
    informacion_prefijo,
) 

from core.history import guardar_ipv6


class IPv6Frame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="#2B2B2B",
            corner_radius=0,
            **kwargs
        )

        # ====================================================
        # COLORES NETPRO
        # ====================================================

        self.bg = "#2B2B2B"
        self.card = "#181818"
        self.card_alt = "#202020"

        self.blue = "#3B8ED0"
        self.blue_hover = "#2478B5"

        self.text = "#f5f5f5"
        self.text_secondary = "#a8a8a8"
        self.border = "#303030"

        self.success = "#36c98f"
        self.warning = "#f0b44d"
        self.error = "#ff5d5d"

        self.resultado_actual = None

        # ====================================================
        # GRID PRINCIPAL
        # ====================================================

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        # ====================================================
        # ENCABEZADO
        # ====================================================

        self.crear_encabezado()

        # ====================================================
        # CONTENIDO SCROLL
        # ====================================================

        
        self.scroll = ctk.CTkScrollableFrame(
        self,
        fg_color="#2B2B2B",
        corner_radius=0,
        scrollbar_button_color="#3B8ED0",
        scrollbar_button_hover_color="#2478B5",
        scrollbar_fg_color="#2B2B2B"
        )


        self.scroll.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=22,
            pady=(0, 22)
        )

        self.scroll.grid_columnconfigure(
            0,
            weight=1
        )

        # ====================================================
        # SECCIONES
        # ====================================================

        self.crear_analizador()
        self.crear_resumen()
        self.crear_informacion()
        self.crear_hextetos()
        self.crear_binario()
        self.crear_herramientas()

        # Estado inicial
        self.limpiar_resultados()


    # ========================================================
    # ENCABEZADO
    # ========================================================

    def crear_encabezado(self):
        # Mismo encabezado que IPv4, sin barras verticales decorativas.
        encabezado = ctk.CTkFrame(self, fg_color="transparent")
        encabezado.grid(row=0, column=0, sticky="ew", padx=28, pady=(22, 15))

        ctk.CTkLabel(
            encabezado,
            text="🌐  Analizador IPv6",
            font=("Arial", 27, "bold"),
            text_color=self.blue,
            anchor="w"
        ).pack(anchor="w")

        ctk.CTkLabel(
            encabezado,
            text="Analiza direcciones IPv6, prefijos, hextetos y estructura de 128 bits.",
            font=("Arial", 13),
            text_color=self.text_secondary,
            anchor="w"
        ).pack(anchor="w", pady=(5, 0))


    # ========================================================
    # ANALIZADOR
    # ========================================================

    def crear_analizador(self):

        card = self.crear_card()

        card.pack(
            fill="x",
            pady=(0, 14)
        )

        ctk.CTkLabel(
            card,
            text="ANALIZADOR IPv6",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=self.blue
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 4)
        )

        ctk.CTkLabel(
            card,
            text=(
                "Introduce una direccion IPv6 "
                "con o sin prefijo."
            ),
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w",
            padx=20
        )

        input_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        input_frame.pack(
            fill="x",
            padx=20,
            pady=(14, 18)
        )

        input_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.entry_ipv6 = ctk.CTkEntry(
            input_frame,
            height=42,
            placeholder_text=(
                "Ejemplo: "
                "2001:db8:1234:5678::25/64"
            ),
            fg_color="#111111",
            border_color=self.border,
            text_color=self.text,
            placeholder_text_color="#707070"
        )

        self.entry_ipv6.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 10)
        )

        self.entry_ipv6.bind(
            "<Return>",
            lambda event: self.analizar()
        )

        ctk.CTkButton(
            input_frame,
            text="ANALIZAR",
            width=130,
            height=42,
            fg_color=self.blue,
            hover_color=self.blue_hover,
            command=self.analizar
        ).grid(
            row=0,
            column=1
        )

        self.label_estado = ctk.CTkLabel(
            card,
            text="",
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=12
            )
        )

        self.label_estado.pack(
            anchor="w",
            padx=20,
            pady=(0, 14)
        )


    # ========================================================
    # RESUMEN
    # ========================================================

    def crear_resumen(self):

        frame = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent"
        )

        frame.pack(
            fill="x",
            pady=(0, 14)
        )

        frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        self.card_tipo = self.crear_mini_card(
            frame,
            0,
            "TIPO"
        )

        self.card_prefijo = self.crear_mini_card(
            frame,
            1,
            "PREFIJO"
        )

        self.card_bits = self.crear_mini_card(
            frame,
            2,
            "LONGITUD"
        )


    def crear_mini_card(
        self,
        parent,
        column,
        title
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.card,
            corner_radius=10,
            border_width=1,
            border_color=self.border
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=(
                0 if column == 0 else 6,
                0 if column == 2 else 6
            )
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=11,
                weight="bold"
            ),
            text_color=self.text_secondary
        ).pack(
            anchor="w",
            padx=16,
            pady=(14, 3)
        )

        value = ctk.CTkLabel(
            card,
            text="--",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color=self.blue
        )

        value.pack(
            anchor="w",
            padx=16,
            pady=(0, 14)
        )

        return value


    # ========================================================
    # INFORMACION IPv6
    # ========================================================

    def crear_informacion(self):

        card = self.crear_card()

        card.pack(
            fill="x",
            pady=(0, 14)
        )

        ctk.CTkLabel(
            card,
            text="INFORMACION IPv6",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=self.blue
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 12)
        )

        self.info_labels = {}

        campos = [
            (
                "direccion_comprimida",
                "Direccion comprimida"
            ),
            (
                "direccion_expandida",
                "Direccion expandida"
            ),
            (
                "red_cidr",
                "Prefijo de red"
            ),
            (
                "primera_direccion",
                "Inicio del rango"
            ),
            (
                "ultima_direccion",
                "Fin del rango"
            ),
            (
                "cantidad_direcciones",
                "Cantidad de direcciones"
            ),
        ]

        for key, nombre in campos:

            row = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=20,
                pady=5
            )

            ctk.CTkLabel(
                row,
                text=nombre,
                width=175,
                anchor="w",
                text_color=self.text_secondary,
                font=ctk.CTkFont(
                    size=12
                )
            ).pack(
                side="left"
            )

            label = ctk.CTkLabel(
                row,
                text="--",
                anchor="w",
                justify="left",
                text_color=self.text,
                font=ctk.CTkFont(
                    size=12,
                    family="Consolas"
                )
            )

            label.pack(
                side="left",
                fill="x",
                expand=True
            )

            self.info_labels[key] = label

        ctk.CTkLabel(
            card,
            text=""
        ).pack(
            pady=3
        )


    # ========================================================
    # HEXTETOS
    # ========================================================

    def crear_hextetos(self):

        card = self.crear_card()

        card.pack(
            fill="x",
            pady=(0, 14)
        )

        ctk.CTkLabel(
            card,
            text="ESTRUCTURA HEXADECIMAL",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=self.blue
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 4)
        )

        ctk.CTkLabel(
            card,
            text=(
                "IPv6 contiene 8 hextetos de 16 bits cada uno."
            ),
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w",
            padx=20
        )

        hextetos_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        hextetos_frame.pack(
            fill="x",
            padx=20,
            pady=18
        )

        for i in range(8):
            hextetos_frame.grid_columnconfigure(
                i,
                weight=1
            )

        self.hexteto_labels = []

        for i in range(8):

            box = ctk.CTkFrame(
                hextetos_frame,
                fg_color=self.card_alt,
                corner_radius=8,
                border_width=1,
                border_color=self.border
            )

            box.grid(
                row=0,
                column=i,
                sticky="ew",
                padx=3
            )

            ctk.CTkLabel(
                box,
                text=f"H{i + 1}",
                text_color=self.text_secondary,
                font=ctk.CTkFont(
                    size=10
                )
            ).pack(
                pady=(8, 1)
            )

            label = ctk.CTkLabel(
                box,
                text="----",
                text_color=self.blue,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold",
                    family="Consolas"
                )
            )

            label.pack(
                pady=(0, 8)
            )

            self.hexteto_labels.append(
                label
            )


    # ========================================================
    # BINARIO
    # ========================================================

    def crear_binario(self):

        card = self.crear_card()

        card.pack(
            fill="x",
            pady=(0, 14)
        )

        ctk.CTkLabel(
            card,
            text="REPRESENTACION BINARIA - 128 BITS",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=self.blue
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 4)
        )

        ctk.CTkLabel(
            card,
            text=(
                "Cada linea representa un hexteto "
                "de 16 bits."
            ),
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w",
            padx=20
        )

        self.binary_text = ctk.CTkTextbox(
            card,
            height=180,
            fg_color="#111111",
            border_width=1,
            border_color=self.border,
            text_color=self.text,
            font=ctk.CTkFont(
                family="Consolas",
                size=12
            )
        )

        self.binary_text.pack(
            fill="x",
            padx=20,
            pady=(14, 20)
        )


    # ========================================================
    # HERRAMIENTAS
    # ========================================================

    def crear_herramientas(self):

        card = self.crear_card()

        card.pack(
            fill="x",
            pady=(0, 20)
        )

        ctk.CTkLabel(
            card,
            text="HERRAMIENTAS IPv6",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            text_color=self.blue
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 4)
        )

        ctk.CTkLabel(
            card,
            text=(
                "Convierte rapidamente una direccion "
                "entre formato comprimido y expandido."
            ),
            text_color=self.text_secondary,
            font=ctk.CTkFont(
                size=12
            )
        ).pack(
            anchor="w",
            padx=20
        )

        tools = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        tools.pack(
            fill="x",
            padx=20,
            pady=16
        )

        tools.grid_columnconfigure(
            0,
            weight=1
        )

        self.entry_tools = ctk.CTkEntry(
            tools,
            height=40,
            placeholder_text=(
                "Ejemplo: "
                "2001:0db8:0000:0000:0000:ff00:0042:8329"
            ),
            fg_color="#111111",
            border_color=self.border,
            text_color=self.text
        )

        self.entry_tools.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, 10)
        )

        ctk.CTkButton(
            tools,
            text="COMPRIMIR",
            height=38,
            fg_color=self.blue,
            hover_color=self.blue_hover,
            command=self.comprimir
        ).grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 5)
        )

        ctk.CTkButton(
            tools,
            text="EXPANDIR",
            height=38,
            fg_color=self.card_alt,
            hover_color="#292929",
            border_width=1,
            border_color=self.blue,
            command=self.expandir
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(5, 0)
        )

        self.label_conversion = ctk.CTkLabel(
            card,
            text="",
            anchor="w",
            justify="left",
            text_color=self.text,
            font=ctk.CTkFont(
                family="Consolas",
                size=12
            )
        )

        self.label_conversion.pack(
            fill="x",
            padx=20,
            pady=(0, 18)
        )

    
    # ========================================================
    # ANALIZAR
    # ========================================================

    def analizar(self):

        direccion = self.entry_ipv6.get().strip()

        if not direccion:

            self.mostrar_error(
                "Introduce una direccion IPv6."
            )

            return

        try:

            # ====================================================
            # ANALIZAR IPv6
            # ====================================================

            resultado = analizar_ipv6(
                direccion
            )

            self.resultado_actual = resultado

            # ====================================================
            # GUARDAR AUTOMATICAMENTE EN HISTORIAL
            # ====================================================

            try:
                guardar_ipv6(resultado)

            except Exception as error_historial:
                print(
                    "[NetPro Historial] "
                    "No se pudo guardar el analisis IPv6:"
                )
                print(error_historial)

            # ====================================================
            # MOSTRAR RESULTADO
            # ====================================================

            self.mostrar_resultado(
                resultado
            )

            self.label_estado.configure(
                text="Direccion IPv6 valida.",
                text_color=self.success
            )

        except ValueError as error:

            self.resultado_actual = None

            self.mostrar_error(
                str(error)
            )

        except Exception as error:

            self.resultado_actual = None

            self.mostrar_error(
                f"Se produjo un error: {error}"
            )


    # ========================================================
    # MOSTRAR RESULTADOS
    # ========================================================

    def mostrar_resultado(
        self,
        resultado
    ):

        self.card_tipo.configure(
            text=resultado["tipo"]
        )

        self.card_prefijo.configure(
            text=f"/{resultado['prefijo']}"
        )

        self.card_bits.configure(
            text=f"{resultado['bits']} bits"
        )

        self.info_labels[
            "direccion_comprimida"
        ].configure(
            text=resultado[
                "direccion_comprimida"
            ]
        )

        self.info_labels[
            "direccion_expandida"
        ].configure(
            text=resultado[
                "direccion_expandida"
            ]
        )

        self.info_labels[
            "red_cidr"
        ].configure(
            text=resultado[
                "red_cidr"
            ]
        )

        self.info_labels[
            "primera_direccion"
        ].configure(
            text=resultado[
                "primera_direccion"
            ]
        )

        self.info_labels[
            "ultima_direccion"
        ].configure(
            text=resultado[
                "ultima_direccion"
            ]
        )

        cantidad = resultado[
            "cantidad_direcciones"
        ]

        self.info_labels[
            "cantidad_direcciones"
        ].configure(
            text=f"{cantidad:,}".replace(
                ",",
                "."
            )
        )

        # Hextetos
        for label, value in zip(
            self.hexteto_labels,
            resultado["hexadecimal"]
        ):

            label.configure(
                text=value
            )

        # Binario
        self.binary_text.configure(
            state="normal"
        )

        self.binary_text.delete(
            "1.0",
            "end"
        )

        for numero, grupo in enumerate(
            resultado["binario"],
            start=1
        ):

            hexteto = resultado[
                "hexadecimal"
            ][numero - 1]

            linea = (
                f"H{numero}  "
                f"{hexteto}  "
                f"{grupo}\n"
            )

            self.binary_text.insert(
                "end",
                linea
            )

        self.binary_text.configure(
            state="disabled"
        )


    # ========================================================
    # ERROR
    # ========================================================

    def mostrar_error(
        self,
        mensaje
    ):

        self.label_estado.configure(
            text=mensaje,
            text_color=self.error
        )


    # ========================================================
    # COMPRIMIR
    # ========================================================

    def comprimir(self):

        direccion = self.entry_tools.get().strip()

        if not direccion:

            self.label_conversion.configure(
                text=(
                    "Introduce una direccion IPv6."
                ),
                text_color=self.error
            )

            return

        try:

            resultado = comprimir_ipv6(
                direccion
            )

            self.label_conversion.configure(
                text=(
                    f"Comprimida:\n{resultado}"
                ),
                text_color=self.success
            )

        except ValueError as error:

            self.label_conversion.configure(
                text=str(error),
                text_color=self.error
            )


    # ========================================================
    # EXPANDIR
    # ========================================================

    def expandir(self):

        direccion = self.entry_tools.get().strip()

        if not direccion:

            self.label_conversion.configure(
                text=(
                    "Introduce una direccion IPv6."
                ),
                text_color=self.error
            )

            return

        try:

            resultado = expandir_ipv6(
                direccion
            )

            self.label_conversion.configure(
                text=(
                    f"Expandida:\n{resultado}"
                ),
                text_color=self.success
            )

        except ValueError as error:

            self.label_conversion.configure(
                text=str(error),
                text_color=self.error
            )


    # ========================================================
    # LIMPIAR RESULTADOS
    # ========================================================

    def limpiar_resultados(self):

        self.card_tipo.configure(
            text="--"
        )

        self.card_prefijo.configure(
            text="--"
        )

        self.card_bits.configure(
            text="128 bits"
        )

        for label in self.info_labels.values():

            label.configure(
                text="--"
            )

        for label in self.hexteto_labels:

            label.configure(
                text="----"
            )

        self.binary_text.configure(
            state="normal"
        )

        self.binary_text.delete(
            "1.0",
            "end"
        )

        self.binary_text.insert(
            "1.0",
            (
                "Introduce una direccion IPv6 "
                "para visualizar sus 128 bits."
            )
        )

        self.binary_text.configure(
            state="disabled"
        )


    # ========================================================
    # CARD GENERICA
    # ========================================================

    def crear_card(self):

        return ctk.CTkFrame(
            self.scroll,
            fg_color=self.card,
            corner_radius=10,
            border_width=1,
            border_color=self.border
        )