import customtkinter as ctk


class BinaryVisualizer(ctk.CTkToplevel):

    def __init__(self, parent, resultado):
        super().__init__(parent)

        self.resultado = resultado

        self.title("NetPro - Visualizador IPv4")
        self.geometry("1050x760")
        self.minsize(900, 650)

        self.transient(parent.winfo_toplevel())

        self.crear_interfaz()

    def crear_interfaz(self):

        # ========================================================
        # DATOS
        # ========================================================

        ip = self.resultado["ip"]
        cidr = int(
            self.resultado["cidr"].replace("/", "")
        )

        bits_host = 32 - cidr
        total = 2 ** bits_host

        # Convertimos los cuatro octetos a enteros
        octetos = [
            int(x)
            for x in ip.split(".")
        ]

        # Convertimos cada octeto a 8 bits
        octetos_binarios = [
            format(octeto, "08b")
            for octeto in octetos
        ]

        ip_binaria = ".".join(
            octetos_binarios
        )

        # 32 bits sin puntos
        todos_bits = "".join(
            octetos_binarios
        )

        # Separación RED / HOST
        bits_red_texto = todos_bits[:cidr]
        bits_host_texto = todos_bits[cidr:]

        # Máscara binaria
        mascara_bits = (
            "1" * cidr
            +
            "0" * bits_host
        )

        mascara_binaria = ".".join(
            mascara_bits[i:i + 8]
            for i in range(0, 32, 8)
        )

        # ========================================================
        # COLORES
        # ========================================================

        AZUL = "#3B8ED0"
        TEXTO_SECUNDARIO = "#A9A9A9"

        # ========================================================
        # CONTENEDOR CON SCROLL
        # ========================================================

        scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )

        scroll.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # ========================================================
        # CABECERA
        # ========================================================

        ctk.CTkLabel(
            scroll,
            text="Visualizador IPv4",
            font=("Arial", 30, "bold")
        ).pack(
            pady=(15, 4)
        )

        ctk.CTkLabel(
            scroll,
            text=(
                "Observa cómo una dirección IPv4 "
                "se representa y divide a nivel binario."
            ),
            font=("Arial", 14),
            text_color=TEXTO_SECUNDARIO
        ).pack(
            pady=(0, 8)
        )

        ctk.CTkLabel(
            scroll,
            text=f"{ip}/{cidr}",
            font=("Consolas", 18, "bold"),
            text_color=AZUL
        ).pack(
            pady=(0, 25)
        )

        # ========================================================
        # TARJETA PRINCIPAL
        # ========================================================

        principal = ctk.CTkFrame(
            scroll,
            corner_radius=12,
            border_width=1
        )

        principal.pack(
            padx=30,
            pady=(0, 10),
            fill="x"
        )

        ctk.CTkLabel(
            principal,
            text="DIRECCIÓN ANALIZADA",
            font=("Arial", 13, "bold"),
            text_color=AZUL
        ).pack(
            anchor="w",
            padx=25,
            pady=(18, 5)
        )

        ctk.CTkLabel(
            principal,
            text=f"{ip}/{cidr}",
            font=("Consolas", 23, "bold")
        ).pack(
            anchor="w",
            padx=25
        )

        ctk.CTkLabel(
            principal,
            text=(
                f"IPv4 utiliza 32 bits. "
                f"El prefijo /{cidr} utiliza {cidr} bits "
                f"para red y deja {bits_host} bits para host."
            ),
            font=("Arial", 13),
            text_color=TEXTO_SECUNDARIO,
            justify="left",
            wraplength=900
        ).pack(
            anchor="w",
            padx=25,
            pady=(6, 18)
        )

        # ========================================================
        # 01 - CONVERSIÓN DECIMAL → BINARIO
        # ========================================================

        conversion_frame = ctk.CTkFrame(
            scroll,
            corner_radius=12,
            border_width=1
        )

        conversion_frame.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        header_conversion = ctk.CTkFrame(
            conversion_frame,
            fg_color="transparent"
        )

        header_conversion.pack(
            fill="x",
            padx=22,
            pady=(18, 10)
        )

        ctk.CTkLabel(
            header_conversion,
            text="01",
            font=("Arial", 21, "bold"),
            text_color=AZUL
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            header_conversion,
            text="   CONVERSIÓN DECIMAL A BINARIO",
            font=("Arial", 16, "bold")
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            conversion_frame,
            text=(
                "Cada número decimal de la dirección "
                "se representa utilizando exactamente 8 bits."
            ),
            font=("Arial", 13),
            text_color=TEXTO_SECUNDARIO
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 12)
        )

        octetos_frame = ctk.CTkFrame(
            conversion_frame,
            fg_color="transparent"
        )

        octetos_frame.pack(
            fill="x",
            padx=17,
            pady=(0, 18)
        )

        for columna in range(4):

            octetos_frame.grid_columnconfigure(
                columna,
                weight=1,
                uniform="octetos"
            )

        for columna, (
            decimal,
            binario
        ) in enumerate(
            zip(
                octetos,
                octetos_binarios
            )
        ):

            tarjeta = ctk.CTkFrame(
                octetos_frame,
                height=115,
                corner_radius=9
            )

            tarjeta.grid(
                row=0,
                column=columna,
                padx=5,
                sticky="nsew"
            )

            tarjeta.grid_propagate(False)

            ctk.CTkLabel(
                tarjeta,
                text=f"OCTETO {columna + 1}",
                font=("Arial", 10, "bold"),
                text_color=TEXTO_SECUNDARIO
            ).pack(
                pady=(15, 4)
            )

            ctk.CTkLabel(
                tarjeta,
                text=str(decimal),
                font=("Consolas", 21, "bold"),
                text_color=AZUL
            ).pack()

            ctk.CTkLabel(
                tarjeta,
                text=binario,
                font=("Consolas", 14)
            ).pack(
                pady=(4, 10)
            )

        # ========================================================
        # 02 - LOS 32 BITS
        # ========================================================

        bits_frame = ctk.CTkFrame(
            scroll,
            corner_radius=12,
            border_width=1
        )

        bits_frame.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        header_bits = ctk.CTkFrame(
            bits_frame,
            fg_color="transparent"
        )

        header_bits.pack(
            fill="x",
            padx=22,
            pady=(18, 10)
        )

        ctk.CTkLabel(
            header_bits,
            text="02",
            font=("Arial", 21, "bold"),
            text_color=AZUL
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            header_bits,
            text="   LOS 32 BITS DE LA DIRECCIÓN",
            font=("Arial", 16, "bold")
        ).pack(
            side="left"
        )

        binario_box = ctk.CTkFrame(
            bits_frame,
            corner_radius=9
        )

        binario_box.pack(
            fill="x",
            padx=22,
            pady=(5, 18)
        )

        ctk.CTkLabel(
            binario_box,
            text="REPRESENTACIÓN BINARIA",
            font=("Arial", 10, "bold"),
            text_color=TEXTO_SECUNDARIO
        ).pack(
            pady=(14, 5)
        )

        ctk.CTkLabel(
            binario_box,
            text=ip_binaria,
            font=("Consolas", 17, "bold"),
            text_color=AZUL
        ).pack(
            pady=(0, 6)
        )

        ctk.CTkLabel(
            binario_box,
            text=(
                f"{octetos[0]:^10}"
                f"{octetos[1]:^10}"
                f"{octetos[2]:^10}"
                f"{octetos[3]:^10}"
            ),
            font=("Consolas", 13),
            text_color=TEXTO_SECUNDARIO
        ).pack(
            pady=(0, 14)
        )

        # ========================================================
        # 03 - RED VS HOST
        # ========================================================

        division = ctk.CTkFrame(
            scroll,
            corner_radius=12,
            border_width=1
        )

        division.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        header_division = ctk.CTkFrame(
            division,
            fg_color="transparent"
        )

        header_division.pack(
            fill="x",
            padx=22,
            pady=(18, 10)
        )

        ctk.CTkLabel(
            header_division,
            text="03",
            font=("Arial", 21, "bold"),
            text_color=AZUL
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            header_division,
            text="   DIVISIÓN ENTRE RED Y HOST",
            font=("Arial", 16, "bold")
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            division,
            text=(
                f"El prefijo /{cidr} marca exactamente "
                "dónde termina la parte de RED "
                "y comienza la parte de HOST."
            ),
            font=("Arial", 13),
            text_color=TEXTO_SECUNDARIO
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 12)
        )

        red_host_frame = ctk.CTkFrame(
            division,
            fg_color="transparent"
        )

        red_host_frame.pack(
            fill="x",
            padx=17,
            pady=(0, 18)
        )

        red_host_frame.grid_columnconfigure(
            0,
            weight=1,
            uniform="redhost"
        )

        red_host_frame.grid_columnconfigure(
            1,
            weight=1,
            uniform="redhost"
        )

        # RED

        red_frame = ctk.CTkFrame(
            red_host_frame,
            corner_radius=9
        )

        red_frame.grid(
            row=0,
            column=0,
            padx=5,
            sticky="nsew"
        )

        ctk.CTkLabel(
            red_frame,
            text="RED",
            font=("Arial", 12, "bold"),
            text_color=AZUL
        ).pack(
            pady=(15, 4)
        )

        ctk.CTkLabel(
            red_frame,
            text=f"{cidr} bits",
            font=("Consolas", 23, "bold")
        ).pack()

        ctk.CTkLabel(
            red_frame,
            text=(
                bits_red_texto
                if bits_red_texto
                else "—"
            ),
            font=("Consolas", 13),
            wraplength=400
        ).pack(
            padx=15,
            pady=(7, 15)
        )

        # HOST

        host_frame = ctk.CTkFrame(
            red_host_frame,
            corner_radius=9
        )

        host_frame.grid(
            row=0,
            column=1,
            padx=5,
            sticky="nsew"
        )

        ctk.CTkLabel(
            host_frame,
            text="HOST",
            font=("Arial", 12, "bold"),
            text_color=AZUL
        ).pack(
            pady=(15, 4)
        )

        ctk.CTkLabel(
            host_frame,
            text=f"{bits_host} bits",
            font=("Consolas", 23, "bold")
        ).pack()

        ctk.CTkLabel(
            host_frame,
            text=(
                bits_host_texto
                if bits_host_texto
                else "—"
            ),
            font=("Consolas", 13),
            wraplength=400
        ).pack(
            padx=15,
            pady=(7, 15)
        )

        # ========================================================
        # 04 - PUNTO DE CORTE CIDR
        # ========================================================

        corte_frame = ctk.CTkFrame(
            scroll,
            corner_radius=12,
            border_width=1
        )

        corte_frame.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        header_corte = ctk.CTkFrame(
            corte_frame,
            fg_color="transparent"
        )

        header_corte.pack(
            fill="x",
            padx=22,
            pady=(18, 10)
        )

        ctk.CTkLabel(
            header_corte,
            text="04",
            font=("Arial", 21, "bold"),
            text_color=AZUL
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            header_corte,
            text="   PUNTO DE CORTE CIDR",
            font=("Arial", 16, "bold")
        ).pack(
            side="left"
        )

        visual_bits = (
            todos_bits[:cidr]
            +
            " | "
            +
            todos_bits[cidr:]
        )

        corte_box = ctk.CTkFrame(
            corte_frame,
            corner_radius=9
        )

        corte_box.pack(
            fill="x",
            padx=22,
            pady=(5, 12)
        )

        ctk.CTkLabel(
            corte_box,
            text=visual_bits,
            font=("Consolas", 16, "bold"),
            text_color=AZUL,
            wraplength=850
        ).pack(
            padx=15,
            pady=15
        )

        ctk.CTkLabel(
            corte_frame,
            text=(
                f"Los primeros {cidr} bits pertenecen a RED. "
                f"Los {bits_host} bits restantes pertenecen a HOST."
            ),
            font=("Arial", 13),
            text_color=TEXTO_SECUNDARIO
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 18)
        )

        # ========================================================
        # 05 - MÁSCARA DE SUBRED
        # ========================================================

        mascara_frame = ctk.CTkFrame(
            scroll,
            corner_radius=12,
            border_width=1
        )

        mascara_frame.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        header_mascara = ctk.CTkFrame(
            mascara_frame,
            fg_color="transparent"
        )

        header_mascara.pack(
            fill="x",
            padx=22,
            pady=(18, 10)
        )

        ctk.CTkLabel(
            header_mascara,
            text="05",
            font=("Arial", 21, "bold"),
            text_color=AZUL
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            header_mascara,
            text="   MÁSCARA DE SUBRED",
            font=("Arial", 16, "bold")
        ).pack(
            side="left"
        )

        mascara_grid = ctk.CTkFrame(
            mascara_frame,
            fg_color="transparent"
        )

        mascara_grid.pack(
            fill="x",
            padx=17,
            pady=(5, 18)
        )

        mascara_grid.grid_columnconfigure(
            0,
            weight=1,
            uniform="mask"
        )

        mascara_grid.grid_columnconfigure(
            1,
            weight=1,
            uniform="mask"
        )

        mascara_bin_card = ctk.CTkFrame(
            mascara_grid,
            corner_radius=9
        )

        mascara_bin_card.grid(
            row=0,
            column=0,
            padx=5,
            sticky="nsew"
        )

        ctk.CTkLabel(
            mascara_bin_card,
            text="BINARIO",
            font=("Arial", 11, "bold"),
            text_color=TEXTO_SECUNDARIO
        ).pack(
            pady=(15, 7)
        )

        ctk.CTkLabel(
            mascara_bin_card,
            text=mascara_binaria,
            font=("Consolas", 14, "bold"),
            wraplength=400
        ).pack(
            padx=12,
            pady=(0, 15)
        )

        mascara_dec_card = ctk.CTkFrame(
            mascara_grid,
            corner_radius=9
        )

        mascara_dec_card.grid(
            row=0,
            column=1,
            padx=5,
            sticky="nsew"
        )

        ctk.CTkLabel(
            mascara_dec_card,
            text="DECIMAL",
            font=("Arial", 11, "bold"),
            text_color=TEXTO_SECUNDARIO
        ).pack(
            pady=(15, 7)
        )

        ctk.CTkLabel(
            mascara_dec_card,
            text=self.resultado["netmask"],
            font=("Consolas", 20, "bold"),
            text_color=AZUL
        ).pack(
            pady=(0, 15)
        )

        # ========================================================
        # 06 - CAPACIDAD
        # ========================================================

        capacidad = ctk.CTkFrame(
            scroll,
            corner_radius=12,
            border_width=1
        )

        capacidad.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        header_capacidad = ctk.CTkFrame(
            capacidad,
            fg_color="transparent"
        )

        header_capacidad.pack(
            fill="x",
            padx=22,
            pady=(18, 10)
        )

        ctk.CTkLabel(
            header_capacidad,
            text="06",
            font=("Arial", 21, "bold"),
            text_color=AZUL
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            header_capacidad,
            text="   CAPACIDAD DE LA SUBRED",
            font=("Arial", 16, "bold")
        ).pack(
            side="left"
        )

        capacidad_grid = ctk.CTkFrame(
            capacidad,
            fg_color="transparent"
        )

        capacidad_grid.pack(
            fill="x",
            padx=17,
            pady=(5, 18)
        )

        for columna in range(4):

            capacidad_grid.grid_columnconfigure(
                columna,
                weight=1,
                uniform="capacity"
            )

        capacidad_datos = [
            (
                "BITS RED",
                cidr
            ),
            (
                "BITS HOST",
                bits_host
            ),
            (
                "DIRECCIONES",
                total
            ),
            (
                "HOSTS",
                self.resultado["usable_hosts"]
            )
        ]

        for columna, (
            titulo,
            valor
        ) in enumerate(
            capacidad_datos
        ):

            card = ctk.CTkFrame(
                capacidad_grid,
                height=105,
                corner_radius=9
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
                text_color=TEXTO_SECUNDARIO
            ).pack(
                pady=(17, 5)
            )

            ctk.CTkLabel(
                card,
                text=str(valor),
                font=("Consolas", 23, "bold"),
                text_color=AZUL
            ).pack()

        # ========================================================
        # 07 - RESULTADO DE LA SUBRED
        # ========================================================

        resumen = ctk.CTkFrame(
            scroll,
            corner_radius=12,
            border_width=1
        )

        resumen.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        header_resumen = ctk.CTkFrame(
            resumen,
            fg_color="transparent"
        )

        header_resumen.pack(
            fill="x",
            padx=22,
            pady=(18, 10)
        )

        ctk.CTkLabel(
            header_resumen,
            text="07",
            font=("Arial", 21, "bold"),
            text_color=AZUL
        ).pack(
            side="left"
        )

        ctk.CTkLabel(
            header_resumen,
            text="   RESULTADO DE LA SUBRED",
            font=("Arial", 16, "bold")
        ).pack(
            side="left"
        )

        resumen_grid = ctk.CTkFrame(
            resumen,
            fg_color="transparent"
        )

        resumen_grid.pack(
            fill="x",
            padx=17,
            pady=(5, 18)
        )

        for columna in range(5):

            resumen_grid.grid_columnconfigure(
                columna,
                weight=1,
                uniform="summary"
            )

        resumen_datos = [
            (
                "NETWORK",
                self.resultado["network"]
            ),
            (
                "FIRST HOST",
                self.resultado["first_host"]
            ),
            (
                "TU IP",
                self.resultado["ip"]
            ),
            (
                "LAST HOST",
                self.resultado["last_host"]
            ),
            (
                "BROADCAST",
                self.resultado["broadcast"]
            )
        ]

        for columna, (
            titulo,
            valor
        ) in enumerate(
            resumen_datos
        ):

            card = ctk.CTkFrame(
                resumen_grid,
                height=105,
                corner_radius=9
            )

            card.grid(
                row=0,
                column=columna,
                padx=4,
                sticky="nsew"
            )

            card.grid_propagate(False)

            ctk.CTkLabel(
                card,
                text=titulo,
                font=("Arial", 9, "bold"),
                text_color=TEXTO_SECUNDARIO
            ).pack(
                pady=(17, 7)
            )

            ctk.CTkLabel(
                card,
                text=str(valor),
                font=("Consolas", 12, "bold"),
                text_color=(
                    AZUL
                    if titulo == "TU IP"
                    else None
                )
            ).pack()

        # ========================================================
        # ¿QUÉ ESTÁ OCURRIENDO?
        # ========================================================

        explicacion_frame = ctk.CTkFrame(
            scroll,
            corner_radius=12,
            border_width=1
        )

        explicacion_frame.pack(
            padx=30,
            pady=(10, 30),
            fill="x"
        )

        ctk.CTkLabel(
            explicacion_frame,
            text="¿QUÉ ESTÁ OCURRIENDO?",
            font=("Arial", 16, "bold"),
            text_color=AZUL
        ).pack(
            anchor="w",
            padx=22,
            pady=(18, 8)
        )

        if cidr <= 30:

            hosts_texto = (
                f"Con {bits_host} bits de host se obtienen "
                f"{total} direcciones. En una subred IPv4 "
                f"tradicional quedan "
                f"{self.resultado['usable_hosts']} "
                "hosts utilizables."
            )

        elif cidr == 31:

            hosts_texto = (
                "Un /31 contiene 2 direcciones y recibe "
                "un tratamiento especial. Puede utilizarse "
                "en determinados enlaces punto a punto."
            )

        else:

            hosts_texto = (
                "Un /32 representa una única dirección IPv4."
            )

        explicacion = (
            f"La dirección {ip}/{cidr} utiliza {cidr} bits "
            f"para identificar la parte de red y {bits_host} "
            f"bits para la parte de host.\n\n"
            f"{hosts_texto}\n\n"
            f"Máscara: {self.resultado['netmask']}\n"
            f"Network: {self.resultado['network']}\n"
            f"First Host: {self.resultado['first_host']}\n"
            f"Last Host: {self.resultado['last_host']}\n"
            f"Broadcast: {self.resultado['broadcast']}"
        )

        ctk.CTkLabel(
            explicacion_frame,
            text=explicacion,
            font=("Arial", 13),
            text_color=TEXTO_SECUNDARIO,
            justify="left",
            anchor="w",
            wraplength=900
        ).pack(
            fill="x",
            padx=22,
            pady=(0, 18)
        )