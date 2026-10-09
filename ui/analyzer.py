import customtkinter as ctk
from tkinter import messagebox

from core.subnet import analizar_subred
from core.history import guardar_ipv4
from ui.binary_visualizer import BinaryVisualizer


class AnalyzerFrame(ctk.CTkFrame):
    AZUL = "#3B8ED0"
    AZUL_HOVER = "#367EB8"
    PANEL_COLOR = "#1A1A1A"
    PANEL_BORDER = "#414141"
    FONDO = "#2B2B2B"
    TEXTO = "#f5f5f5"
    SECUNDARIO = "#a8a8a8"

    def __init__(self, parent):
        super().__init__(parent, fg_color=self.FONDO, corner_radius=0)
        self.ultimo_resultado = None
        self.valores = {}
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        encabezado = ctk.CTkFrame(self, fg_color="transparent")
        encabezado.grid(row=0, column=0, sticky="ew", padx=28, pady=(22, 15))
        encabezado.grid_columnconfigure(0, weight=1)
        titulo = ctk.CTkFrame(encabezado, fg_color="transparent")
        titulo.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(titulo, text="🌐  Analizador IPv4",
                     font=("Arial", 27, "bold"), text_color=self.AZUL).pack(anchor="w")
        ctk.CTkLabel(titulo,
                     text="Analiza direcciones IPv4, subredes, hosts y estructura de 32 bits.",
                     font=("Arial", 13), text_color=self.SECUNDARIO).pack(anchor="w", pady=(5, 0))

        accesos = ctk.CTkFrame(encabezado, fg_color="transparent")
        accesos.grid(row=0, column=1, sticky="e", padx=(15, 0))
        for texto, funcion in [
            ("¿Qué significa?", self.mostrar_significados),
            ("¿Cómo se calculó?", self.mostrar_calculo),
            ("Visualizar bits", self.mostrar_visualizador),
        ]:
            ctk.CTkButton(accesos, text=texto, height=34, width=145,
                          fg_color="#343434", hover_color="#414141",
                          border_width=1, border_color="#505050",
                          command=funcion).pack(side="left", padx=(7, 0))

        self.scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0,
            scrollbar_button_color="#2879B1",
            scrollbar_button_hover_color="#3B8ED0")
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=22, pady=(0, 12))
        self.scroll.grid_columnconfigure(0, weight=1)

        entrada = self.crear_panel("ANALIZADOR IPv4")
        ctk.CTkLabel(entrada, text="Introduce una dirección IPv4 y un prefijo CIDR.",
                     font=("Arial", 12), text_color=self.SECUNDARIO).pack(
                         anchor="w", padx=20, pady=(0, 12))
        formulario = ctk.CTkFrame(entrada, fg_color="transparent")
        formulario.pack(fill="x", padx=20, pady=(0, 20))
        formulario.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(formulario, text="Dirección IPv4", text_color=self.SECUNDARIO,
                     font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=(0, 5))
        ctk.CTkLabel(formulario, text="CIDR", text_color=self.SECUNDARIO,
                     font=("Arial", 11)).grid(row=0, column=1, sticky="w", padx=(10, 0), pady=(0, 5))
        self.ip_entry = ctk.CTkEntry(formulario, height=38,
                                    placeholder_text="Ejemplo: 192.168.10.37")
        self.ip_entry.grid(row=1, column=0, sticky="ew")
        self.cidr_entry = ctk.CTkEntry(formulario, width=105, height=38,
                                      placeholder_text="24")
        self.cidr_entry.grid(row=1, column=1, padx=(10, 12))
        self.ip_entry.bind("<Return>", lambda _: self.analizar())
        self.cidr_entry.bind("<Return>", lambda _: self.analizar())
        ctk.CTkButton(formulario, text="ANALIZAR", width=125, height=38,
                      fg_color=self.AZUL, hover_color=self.AZUL_HOVER,
                      command=self.analizar).grid(row=1, column=2)

        resumen = ctk.CTkFrame(self.scroll, fg_color="transparent")
        resumen.pack(fill="x", pady=(0, 12))
        for i in range(3):
            resumen.grid_columnconfigure(i, weight=1, uniform="resumen")
        for i, (titulo, clave) in enumerate([
            ("DIRECCIÓN DE RED", "network"), ("PREFIJO", "cidr"),
            ("HOSTS UTILIZABLES", "usable_hosts")
        ]):
            tarjeta = ctk.CTkFrame(resumen, fg_color=self.PANEL_COLOR,
                                   border_width=1, border_color=self.PANEL_BORDER,
                                   corner_radius=10, height=105)
            tarjeta.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 5, 0 if i == 2 else 5))
            tarjeta.grid_propagate(False)
            ctk.CTkLabel(tarjeta, text=titulo, font=("Arial", 11, "bold"),
                         text_color=self.SECUNDARIO).pack(anchor="w", padx=16, pady=(13, 5))
            valor = ctk.CTkLabel(tarjeta, text="--", font=("Arial", 19, "bold"),
                                 text_color=self.AZUL)
            valor.pack(anchor="w", padx=16)
            self.valores[clave] = valor

        info = self.crear_panel("INFORMACIÓN IPv4")
        filas = [
            ("Dirección IP", "ip"), ("Máscara de subred", "netmask"),
            ("Wildcard", "wildcard"), ("Broadcast", "broadcast"),
            ("Primer host", "first_host"), ("Último host", "last_host"),
            ("Total de direcciones", "total_addresses"),
            ("IP privada", "private"), ("Versión", "version")
        ]
        tabla = ctk.CTkFrame(info, fg_color="transparent")
        tabla.pack(fill="x", padx=20, pady=(0, 18))
        tabla.grid_columnconfigure(1, weight=1)
        for fila, (nombre, clave) in enumerate(filas):
            ctk.CTkLabel(tabla, text=nombre, font=("Arial", 12),
                         text_color=self.SECUNDARIO, width=175, anchor="w").grid(
                             row=fila, column=0, sticky="w", pady=6)
            valor = ctk.CTkLabel(tabla, text="--", font=("Consolas", 12),
                                 text_color=self.TEXTO, anchor="w")
            valor.grid(row=fila, column=1, sticky="w", pady=6)
            self.valores[clave] = valor

        estado = self.crear_panel("DETALLE DEL ANÁLISIS")
        self.resultado = ctk.CTkTextbox(estado, height=145, font=("Consolas", 12),
                                        wrap="word", fg_color="#202020",
                                        border_width=1, border_color=self.PANEL_BORDER,
                                        corner_radius=7)
        self.resultado.pack(fill="x", padx=20, pady=(0, 18))
        self.escribir_resultado("Introduce una dirección IPv4 y un CIDR para comenzar.\n"
                               "Ejemplo: 192.168.10.37 / 24")

    def crear_panel(self, titulo):
        panel = ctk.CTkFrame(self.scroll, fg_color=self.PANEL_COLOR,
                             border_width=1, border_color=self.PANEL_BORDER,
                             corner_radius=10)
        panel.pack(fill="x", pady=(0, 13))
        ctk.CTkLabel(panel, text=titulo, font=("Arial", 13, "bold"),
                     text_color=self.AZUL).pack(anchor="w", padx=20, pady=(18, 12))
        return panel

    def escribir_resultado(self, texto):
        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("1.0", texto)
        self.resultado.configure(state="disabled")
        r = self.ultimo_resultado
        for clave, etiqueta in self.valores.items():
            if r is None:
                etiqueta.configure(text="--")
            elif clave == "private":
                etiqueta.configure(text="Sí" if r["private"] else "No")
            elif clave == "version":
                etiqueta.configure(text=f"IPv{r['version']}")
            else:
                etiqueta.configure(text=str(r.get(clave, "--")))

    # ============================================================
    # ANALIZAR
    # ============================================================

        # ============================================================
    # ANALIZAR
    # ============================================================

    def analizar(self):

        ip = self.ip_entry.get().strip()
        cidr_texto = self.cidr_entry.get().strip()

        try:

            # ====================================================
            # VALIDAR IP
            # ====================================================

            if not ip:
                raise ValueError

            # ====================================================
            # VALIDAR CIDR
            # ====================================================

            cidr = int(cidr_texto)

            if cidr < 0 or cidr > 32:
                raise ValueError

            # ====================================================
            # ANALIZAR SUBRED
            # ====================================================

            resultado = analizar_subred(
                ip,
                cidr
            )

            self.ultimo_resultado = resultado

            # ====================================================
            # GUARDAR AUTOMATICAMENTE EN HISTORIAL
            # ====================================================

            try:

                guardar_ipv4(
                    resultado
                )

            except Exception as error_historial:

                # El historial nunca debe impedir que
                # el analizador principal funcione.
                print(
                    "[NetPro Historial] "
                    "No se pudo guardar el analisis IPv4:"
                )

                print(
                    error_historial
                )

            # ====================================================
            # PREPARAR RESULTADO
            # ====================================================

            privado = (
                "Sí"
                if resultado["private"]
                else "No"
            )

            texto = f"""
INFORMACIÓN DE RED
────────────────────────────────────────

IP                  {resultado['ip']}
CIDR                {resultado['cidr']}

Network             {resultado['network']}
Netmask             {resultado['netmask']}
Wildcard            {resultado['wildcard']}
Broadcast           {resultado['broadcast']}

First Host          {resultado['first_host']}
Last Host           {resultado['last_host']}

Total Addresses     {resultado['total_addresses']}
Usable Hosts        {resultado['usable_hosts']}

IP privada          {privado}
Versión             IPv{resultado['version']}
"""

            self.escribir_resultado(
                texto
            )

        except ValueError:

            self.ultimo_resultado = None

            self.escribir_resultado(
                "⚠ DIRECCIÓN IPv4 O CIDR INVÁLIDO\n\n"
                "Introduce valores válidos.\n\n"
                "Ejemplo:\n"
                "IP:   192.168.10.37\n"
                "CIDR: 24\n\n"
                "El CIDR debe estar entre 0 y 32."
            )

        except Exception as error:

            self.ultimo_resultado = None

            self.escribir_resultado(
                f"⚠ Se produjo un error:\n\n{error}"
            )

    # ============================================================
    # VENTANA EDUCATIVA
    # ============================================================

    def _crear_ventana_educativa(
        self,
        titulo,
        subtitulo
    ):

        ventana = ctk.CTkToplevel(self)

        ventana.title(
            f"NetPro - {titulo}"
        )

        ventana.geometry("920x760")
        ventana.minsize(780, 620)

        ventana.transient(
            self.winfo_toplevel()
        )

        ctk.CTkLabel(
            ventana,
            text=titulo,
            font=("Arial", 27, "bold"),
            text_color=self.AZUL
        ).pack(
            pady=(24, 4)
        )

        ctk.CTkLabel(
            ventana,
            text=subtitulo,
            font=("Consolas", 15, "bold"),
            text_color=self.AZUL
        ).pack(
            pady=(0, 16)
        )

        scroll = ctk.CTkScrollableFrame(
            ventana,
            width=840,
            height=620,
            corner_radius=12
        )

        scroll.pack(
            padx=25,
            pady=(0, 25),
            fill="both",
            expand=True
        )

        return ventana, scroll

    # ============================================================
    # CREAR TARJETA
    # ============================================================

    def _crear_tarjeta(
        self,
        parent,
        titulo,
        valor="",
        descripcion="",
        detalle="",
        columnas=1
    ):

        tarjeta = ctk.CTkFrame(
            parent,
            corner_radius=12,
            border_width=1
        )

        tarjeta.pack(
            padx=12,
            pady=8,
            fill="x"
        )

        encabezado = ctk.CTkFrame(
            tarjeta,
            fg_color="transparent"
        )

        encabezado.pack(
            padx=18,
            pady=(15, 5),
            fill="x"
        )

        ctk.CTkLabel(
            encabezado,
            text=titulo,
            font=("Arial", 15, "bold"),
            text_color=self.AZUL,
            anchor="w"
        ).pack(
            side="left"
        )

        if valor:

            ctk.CTkLabel(
                encabezado,
                text=str(valor),
                font=("Consolas", 15, "bold"),
                text_color=self.AZUL,
                anchor="e"
            ).pack(
                side="right"
            )

        if descripcion:

            ctk.CTkLabel(
                tarjeta,
                text=descripcion,
                font=("Arial", 13),
                justify="left",
                anchor="w",
                wraplength=760
            ).pack(
                padx=18,
                pady=(4, 6),
                fill="x"
            )

        if detalle:

            detalle_frame = ctk.CTkFrame(
                tarjeta,
                corner_radius=8
            )

            detalle_frame.pack(
                padx=18,
                pady=(5, 15),
                fill="x"
            )

            ctk.CTkLabel(
                detalle_frame,
                text=detalle,
                font=("Consolas", 13),
                justify="left",
                anchor="w",
                wraplength=735
            ).pack(
                padx=14,
                pady=12,
                fill="x"
            )

        else:

            ctk.CTkFrame(
                tarjeta,
                height=4,
                fg_color="transparent"
            ).pack()

        return tarjeta

    # ============================================================
    # ¿QUÉ SIGNIFICA?
    # ============================================================

    def mostrar_significados(self):

        if self.ultimo_resultado is None:

            messagebox.showinfo(
                "NetPro",
                "Primero analiza una dirección IPv4."
            )

            return

        resultado = self.ultimo_resultado

        ip = resultado["ip"]

        cidr = int(
            resultado["cidr"].replace("/", "")
        )

        network = resultado["network"]
        netmask = resultado["netmask"]
        wildcard = resultado["wildcard"]
        broadcast = resultado["broadcast"]

        first_host = resultado["first_host"]
        last_host = resultado["last_host"]

        total_addresses = resultado["total_addresses"]
        usable_hosts = resultado["usable_hosts"]

        private = resultado["private"]
        version = resultado["version"]

        bits_red = cidr
        bits_host = 32 - cidr

        tipo_ip = (
            "Privada"
            if private
            else "No privada"
        )

        _, contenido = (
            self._crear_ventana_educativa(
                "¿Qué significa cada resultado?",
                f"Analizando {ip}/{cidr}"
            )
        )

        self._crear_tarjeta(
            contenido,
            "DIRECCIÓN IP",
            ip,
            "Es la dirección IPv4 que estás analizando.",
            (
                "IPv4 utiliza 32 bits divididos "
                "en cuatro octetos.\n"
                f"Dirección completa: {ip}/{cidr}"
            )
        )

        self._crear_tarjeta(
            contenido,
            "CIDR",
            f"/{cidr}",
            (
                "Indica cuántos bits de la dirección "
                "pertenecen al prefijo de red."
            ),
            (
                f"Bits de red:  {bits_red}\n"
                f"Bits de host: {bits_host}\n"
                f"32 - {cidr} = {bits_host}"
            )
        )

        self._crear_tarjeta(
            contenido,
            "NETWORK",
            network,
            (
                "Es la dirección que identifica la subred "
                "a la que pertenece la IP analizada."
            ),
            (
                f"IP analizada: {ip}\n"
                f"Red obtenida: {network}"
            )
        )

        self._crear_tarjeta(
            contenido,
            "NETMASK",
            netmask,
            (
                "La máscara permite distinguir la parte "
                "de red y la parte destinada a hosts."
            ),
            f"/{cidr} = {netmask}"
        )

        self._crear_tarjeta(
            contenido,
            "WILDCARD MASK",
            wildcard,
            "Es el complemento de la máscara de subred.",
            (
                f"Netmask:  {netmask}\n"
                f"Wildcard: {wildcard}"
            )
        )

        self._crear_tarjeta(
            contenido,
            "BROADCAST",
            broadcast,
            (
                "En una subred IPv4 tradicional representa "
                "la dirección destinada a todos los hosts "
                "de esa subred."
            ),
            (
                f"Network:   {network}\n"
                f"Broadcast: {broadcast}"
            )
        )

        self._crear_tarjeta(
            contenido,
            "RANGO DE HOSTS",
            f"{first_host}  —  {last_host}",
            (
                "Muestra la primera y la última dirección "
                "normalmente utilizables por hosts."
            ),
            (
                f"First Host: {first_host}\n"
                f"Tu IP:      {ip}\n"
                f"Last Host:  {last_host}"
            )
        )

        self._crear_tarjeta(
            contenido,
            "CAPACIDAD DE LA SUBRED",
            f"{total_addresses} direcciones",
            (
                "La cantidad total depende del número "
                "de bits disponibles para host."
            ),
            (
                f"Bits de host:       {bits_host}\n"
                f"Total Addresses:    {total_addresses}\n"
                f"Usable Hosts:       {usable_hosts}"
            )
        )

        self._crear_tarjeta(
            contenido,
            "TIPO DE DIRECCIÓN",
            tipo_ip,
            (
                "Indica si la dirección pertenece a uno "
                "de los rangos IPv4 privados habituales."
            ),
            (
                f"IP: {ip}\n"
                f"Versión: IPv{version}"
            )
        )

        self._crear_tarjeta(
            contenido,
            "RESUMEN DE LA SUBRED",
            f"{ip}/{cidr}",
            (
                "Vista compacta de los resultados "
                "obtenidos por NetPro."
            ),
            (
                f"Network:            {network}\n"
                f"Netmask:            {netmask}\n"
                f"Wildcard:           {wildcard}\n"
                f"Broadcast:          {broadcast}\n"
                f"First Host:         {first_host}\n"
                f"Last Host:          {last_host}\n"
                f"Total Addresses:    {total_addresses}\n"
                f"Usable Hosts:       {usable_hosts}"
            )
        )

    # ============================================================
    # ¿CÓMO SE CALCULÓ?
    # ============================================================

    def mostrar_calculo(self):

        if self.ultimo_resultado is None:

            messagebox.showinfo(
                "NetPro",
                "Primero analiza una dirección IP."
            )

            return

        resultado = self.ultimo_resultado

        ip = resultado["ip"]

        cidr = int(
            resultado["cidr"].replace("/", "")
        )

        bits_red = cidr
        bits_host = 32 - cidr

        total = 2 ** bits_host

        octetos = ip.split(".")

        binario_ip = ".".join(
            format(
                int(octeto),
                "08b"
            )
            for octeto in octetos
        )

        mascara_bits = (
            "1" * cidr
            +
            "0" * bits_host
        )

        mascara_binaria = ".".join(
            mascara_bits[i:i + 8]
            for i in range(
                0,
                32,
                8
            )
        )

        if cidr <= 30:

            explicacion_hosts = (
                f"2^{bits_host} = {total} direcciones\n"
                f"{total} - 2 = "
                f"{resultado['usable_hosts']} "
                "hosts utilizables\n\n"
                "Se descuentan tradicionalmente:\n"
                "• Dirección Network\n"
                "• Dirección Broadcast"
            )

        elif cidr == 31:

            explicacion_hosts = (
                "Un /31 contiene 2 direcciones.\n"
                "Es un caso especial utilizado, "
                "entre otros usos,\n"
                "en enlaces punto a punto."
            )

        else:

            explicacion_hosts = (
                "Un /32 identifica una única "
                "dirección IPv4."
            )

        _, contenido = (
            self._crear_ventana_educativa(
                "¿Cómo se calculó?",
                f"{ip}/{cidr}"
            )
        )

        self._crear_tarjeta(
            contenido,
            "PASO 1 · IPv4 UTILIZA 32 BITS",
            "32 bits",
            (
                "Cada dirección IPv4 está formada "
                "por cuatro octetos de 8 bits."
            ),
            (
                "8 + 8 + 8 + 8 = 32 bits\n\n"
                f"IP decimal:  {ip}\n"
                f"IP binaria:  {binario_ip}"
            )
        )

        self._crear_tarjeta(
            contenido,
            "PASO 2 · CIDR",
            f"/{cidr}",
            (
                "El CIDR determina cuántos bits "
                "corresponden a la red y cuántos "
                "quedan para hosts."
            ),
            (
                f"Bits de red:   {bits_red}\n"
                f"Bits de host:  32 - {cidr} = "
                f"{bits_host}"
            )
        )

        self._crear_tarjeta(
            contenido,
            "PASO 3 · MÁSCARA DE SUBRED",
            resultado["netmask"],
            (
                f"Los primeros {cidr} bits son 1 "
                f"y los {bits_host} bits restantes "
                "son 0."
            ),
            (
                f"Binario:  {mascara_binaria}\n"
                f"Decimal:  {resultado['netmask']}"
            )
        )

        self._crear_tarjeta(
            contenido,
            "PASO 4 · CANTIDAD DE DIRECCIONES",
            str(total),
            (
                "La cantidad total de direcciones "
                "depende de los bits disponibles "
                "para host."
            ),
            (
                f"Bits de host: {bits_host}\n"
                f"2^{bits_host} = {total}"
            )
        )

        self._crear_tarjeta(
            contenido,
            "PASO 5 · HOSTS UTILIZABLES",
            str(resultado["usable_hosts"]),
            (
                "NetPro aplica el tratamiento "
                "correspondiente al prefijo analizado."
            ),
            explicacion_hosts
        )

        self._crear_tarjeta(
            contenido,
            "PASO 6 · RESULTADO DE LA SUBRED",
            resultado["network"],
            (
                "Estos son los límites y valores "
                "obtenidos para la subred."
            ),
            (
                f"Network:      {resultado['network']}\n"
                f"First Host:   {resultado['first_host']}\n"
                f"Tu IP:        {resultado['ip']}\n"
                f"Last Host:    {resultado['last_host']}\n"
                f"Broadcast:    {resultado['broadcast']}"
            )
        )

        self._crear_tarjeta(
            contenido,
            "RESUMEN",
            f"{ip}/{cidr}",
            (
                "Vista final sin flechas para mantener "
                "una lectura limpia y alineada."
            ),
            (
                f"NETWORK       {resultado['network']}\n"
                f"FIRST HOST    {resultado['first_host']}\n"
                f"TU IP         {resultado['ip']}\n"
                f"LAST HOST     {resultado['last_host']}\n"
                f"BROADCAST     {resultado['broadcast']}"
            )
        )

    # ============================================================
    # VISUALIZADOR BINARIO
    # ============================================================

    def mostrar_visualizador(self):
        """Abre el visualizador binario de la IPv4 analizada."""

        if self.ultimo_resultado is None:

            messagebox.showinfo(
                "NetPro",
                "Primero analiza una dirección IPv4."
            )

            return

        BinaryVisualizer(
            self,
            self.ultimo_resultado
        )