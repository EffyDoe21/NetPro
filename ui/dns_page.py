import customtkinter as ctk
import threading
from tkinter import messagebox
from urllib.parse import urlparse

from core.dns import resolver_dominio


class DNSFrame(ctk.CTkFrame):

    AZUL = "#3B8ED0"
    AZUL_HOVER = "#367EB8"
    PANEL_COLOR = "#1A1A1A"
    PANEL_BORDER = "#343638"

    def __init__(self, parent):
        super().__init__(parent)

        self.ultimo_resultado = None

        # ========================================================
        # TÍTULO
        # ========================================================

        title = ctk.CTkLabel (
            self,
            text="🔎 DNS Lookup",
            font=("Arial", 30, "bold"),
            text_color=self.AZUL
        )
        title.pack(pady=(30, 5))

        subtitle = ctk.CTkLabel(
            self,
            text=(
                "Consulta registros DNS y aprende "
                "qué significa cada resultado."
            ),
            font=("Arial", 14)
        )
        subtitle.pack(pady=(0, 20))

        # ========================================================
        # DOMINIO
        # ========================================================

        self.domain_entry = ctk.CTkEntry(
            self,
            width=560,
            height=42,
            placeholder_text=(
                "Ejemplo: example.com o "
                "https://www.example.com"
            )
        )
        self.domain_entry.pack(pady=(5, 15))

        self.domain_entry.bind(
            "<Return>",
            lambda event: self.iniciar_busqueda()
        )

        # ========================================================
        # SELECTOR DE REGISTRO
        # ========================================================

        ctk.CTkLabel(
            self,
            text="Tipo de registro",
            font=("Arial", 13, "bold")
        ).pack(pady=(0, 5))

        self.tipo_registro = ctk.CTkSegmentedButton(
            self,
            values=[
                "TODOS",
                "A",
                "AAAA",
                "CNAME",
                "MX",
                "NS",
                "TXT"
            ],
            command=self.cambiar_tipo_registro
        )

        self.tipo_registro.set("TODOS")
        self.tipo_registro.pack(pady=(0, 15))

        # ========================================================
        # BOTONES
        # ========================================================

        acciones = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        acciones.pack(pady=(0, 10))

        self.search_button = ctk.CTkButton(
            acciones,
            text="RESOLVER DNS",
            width=220,
            height=42,
            command=self.iniciar_busqueda
        )
        self.search_button.grid(
            row=0,
            column=0,
            padx=8
        )

        self.base_button = ctk.CTkButton(
            acciones,
            text="🌐 DOMINIO BASE",
            width=180,
            height=42,
            command=self.consultar_dominio_base
        )
        self.base_button.grid(
            row=0,
            column=1,
            padx=8
        )

        # ========================================================
        # RESULTADOS
        # ========================================================

        self.resultado = ctk.CTkTextbox(
            self,
            width=800,
            height=430,
            font=("Consolas", 14),
            wrap="word",
            fg_color=self.PANEL_COLOR,
            border_width=1,
            border_color=self.PANEL_BORDER,
            corner_radius=12
        )

        self.resultado.pack(
            padx=30,
            pady=(10, 10),
            fill="both",
            expand=True
        )

        self.mostrar_texto(
            "Introduce un dominio o una URL para comenzar.\n\n"
            "Ejemplos:\n"
            "google.com\n"
            "www.instagram.com\n"
            "https://www.instagram.com/"
        )

        # ========================================================
        # BOTONES EDUCATIVOS
        # ========================================================

        botones = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        botones.pack(pady=(5, 20))

        self.btn_significado = ctk.CTkButton(
            botones,
            text="¿QUÉ SIGNIFICA?",
            width=220,
            height=40,
            command=self.mostrar_significados
        )
        self.btn_significado.grid(
            row=0,
            column=0,
            padx=10
        )

        self.btn_funcionamiento = ctk.CTkButton(
            botones,
            text="🧠 ¿CÓMO FUNCIONA DNS?",
            width=220,
            height=40,
            command=self.mostrar_funcionamiento
        )
        self.btn_funcionamiento.grid(
            row=0,
            column=1,
            padx=10
        )

    # ============================================================
    # MOSTRAR TEXTO
    # ============================================================

    def mostrar_texto(self, texto):

        self.resultado.configure(state="normal")
        self.resultado.delete("1.0", "end")
        self.resultado.insert("1.0", texto)
        self.resultado.configure(state="disabled")

    # ============================================================
    # INICIAR CONSULTA
    # ============================================================

    def iniciar_busqueda(self):

        dominio = self.domain_entry.get().strip()

        if not dominio:

            self.mostrar_texto(
                "⚠ Debes introducir un dominio.\n\n"
                "Ejemplo:\n"
                "example.com"
            )
            return

        self.search_button.configure(
            state="disabled",
            text="CONSULTANDO..."
        )

        self.mostrar_texto(
            f"Consultando registros DNS para:\n\n"
            f"{dominio}\n\n"
            "Espera un momento..."
        )

        hilo = threading.Thread(
            target=self.buscar_dns,
            args=(dominio,),
            daemon=True
        )

        hilo.start()

    # ============================================================
    # CONSULTA DNS
    # ============================================================

    def buscar_dns(self, dominio):

        try:

            resultado = resolver_dominio(dominio)

            self.ultimo_resultado = resultado

            self.after(
                0,
                self.actualizar_resultado
            )

        except ValueError as error:

            self.ultimo_resultado = None
            mensaje = str(error)

            self.after(
                0,
                lambda: self.finalizar_busqueda(
                    f"⚠ {mensaje}"
                )
            )

        except Exception as error:

            self.ultimo_resultado = None
            mensaje = str(error)

            self.after(
                0,
                lambda: self.finalizar_busqueda(
                    f"⚠ Error inesperado:\n\n{mensaje}"
                )
            )

    # ============================================================
    # CAMBIAR REGISTRO
    # ============================================================

    def cambiar_tipo_registro(self, valor=None):

        if self.ultimo_resultado is not None:
            self.actualizar_resultado()

    # ============================================================
    # ACTUALIZAR RESULTADO
    # ============================================================

    def actualizar_resultado(self):

        if self.ultimo_resultado is None:
            return

        tipo = self.tipo_registro.get()

        if tipo == "TODOS":

            texto = self.construir_resultado_completo(
                self.ultimo_resultado
            )

        else:

            texto = self.construir_resultado_individual(
                self.ultimo_resultado,
                tipo
            )

        self.finalizar_busqueda(texto)

    # ============================================================
    # RESULTADO COMPLETO
    # ============================================================

    def construir_resultado_completo(self, resultado):

        registros_a = self.formatear_lista(
            resultado["A"]
        )

        registros_aaaa = self.formatear_lista(
            resultado["AAAA"]
        )

        registros_cname = self.formatear_lista(
            resultado["CNAME"]
        )

        registros_mx = self.formatear_mx(
            resultado["MX"]
        )

        registros_ns = self.formatear_lista(
            resultado["NS"]
        )

        registros_txt = self.formatear_lista(
            resultado["TXT"]
        )

        texto = f"""
DNS LOOKUP
────────────────────────────────────────────

DOMINIO

{resultado['domain']}


A — IPv4
────────────────────────────────────────────

{registros_a}


AAAA — IPv6
────────────────────────────────────────────

{registros_aaaa}


CNAME — ALIAS
────────────────────────────────────────────

{registros_cname}


MX — SERVIDORES DE CORREO
────────────────────────────────────────────

{registros_mx}


NS — SERVIDORES DE NOMBRES
────────────────────────────────────────────

{registros_ns}


TXT — REGISTROS DE TEXTO
────────────────────────────────────────────

{registros_txt}
"""

        # ========================================================
        # ANÁLISIS TXT AUTOMÁTICO
        # ========================================================

        if resultado["TXT"]:

            interpretaciones = []

            for registro in resultado["TXT"]:

                interpretacion = self.interpretar_txt(
                    str(registro)
                )

                if interpretacion:
                    interpretaciones.append(
                        interpretacion
                    )

            if interpretaciones:

                texto += """

ANÁLISIS AUTOMÁTICO DE TXT
────────────────────────────────────────────

"""

                texto += "\n\n".join(
                    interpretaciones
                )

        return texto

    # ============================================================
    # RESULTADO INDIVIDUAL
    # ============================================================

    def construir_resultado_individual(
        self,
        resultado,
        tipo
    ):

        dominio = resultado["domain"]

        titulos = {
            "A": "A — DIRECCIÓN IPv4",
            "AAAA": "AAAA — DIRECCIÓN IPv6",
            "CNAME": "CNAME — ALIAS",
            "MX": "MX — SERVIDORES DE CORREO",
            "NS": "NS — SERVIDORES DE NOMBRES",
            "TXT": "TXT — REGISTROS DE TEXTO"
        }

        if tipo == "MX":

            registros = self.formatear_mx(
                resultado["MX"]
            )

        else:

            registros = self.formatear_lista(
                resultado[tipo]
            )

        texto = f"""
DNS LOOKUP
────────────────────────────────────────────

DOMINIO

{dominio}


{titulos[tipo]}
────────────────────────────────────────────

{registros}


¿QUÉ SIGNIFICA?
────────────────────────────────────────────

{self.explicar_tipo(tipo)}
"""

        if tipo == "TXT" and resultado["TXT"]:

            interpretaciones = []

            for registro in resultado["TXT"]:

                interpretacion = self.interpretar_txt(
                    str(registro)
                )

                if interpretacion:
                    interpretaciones.append(
                        interpretacion
                    )

            if interpretaciones:

                texto += """

ANÁLISIS AUTOMÁTICO
────────────────────────────────────────────

"""

                texto += "\n\n".join(
                    interpretaciones
                )

        return texto

    # ============================================================
    # EXPLICAR TIPO
    # ============================================================

    def explicar_tipo(self, tipo):

        explicaciones = {

            "A":
                "El registro A relaciona un nombre DNS "
                "con una dirección IPv4.",

            "AAAA":
                "El registro AAAA relaciona un nombre DNS "
                "con una dirección IPv6.",

            "CNAME":
                "CNAME significa Canonical Name.\n\n"
                "Indica que un nombre DNS funciona como "
                "alias de otro nombre.",

            "MX":
                "MX significa Mail Exchange.\n\n"
                "Indica servidores publicados para recibir "
                "correo electrónico para un dominio.",

            "NS":
                "NS significa Name Server.\n\n"
                "Indica servidores de nombres publicados "
                "para una zona DNS.",

            "TXT":
                "Los registros TXT permiten publicar "
                "información textual dentro de DNS.\n\n"
                "Pueden contener configuraciones, "
                "verificaciones y políticas."
        }

        return explicaciones.get(
            tipo,
            "Tipo de registro DNS."
        )

    # ============================================================
    # INTERPRETAR TXT
    # ============================================================

    def interpretar_txt(self, valor):

        valor_limpio = valor.strip().strip('"')
        valor_minusculas = valor_limpio.lower()

        # ========================================================
        # SPF
        # ========================================================

        if valor_minusculas.startswith("v=spf1"):

            partes = valor_limpio.split()
            detalles = []

            for parte in partes:

                parte_lower = parte.lower()

                # Versión
                if parte_lower == "v=spf1":

                    detalles.append(
                        "v=spf1\n"
                        "→ Versión 1 de SPF."
                    )

                    continue

                # Calificador SPF
                calificador = "+"
                mecanismo = parte

                if parte.startswith(("+", "-", "~", "?")):

                    calificador = parte[0]
                    mecanismo = parte[1:]

                mecanismo_lower = mecanismo.lower()

                # INCLUDE
                if mecanismo_lower.startswith("include:"):

                    dominio_include = mecanismo.split(
                        ":",
                        1
                    )[1]

                    detalles.append(
                        f"{parte}\n"
                        "→ Incluye la política SPF publicada "
                        f"por {dominio_include}."
                    )

                # IPv4
                elif mecanismo_lower.startswith("ip4:"):

                    red_ipv4 = mecanismo.split(
                        ":",
                        1
                    )[1]

                    detalles.append(
                        f"{parte}\n"
                        "→ Autoriza la dirección o red IPv4 "
                        f"{red_ipv4}."
                    )

                # IPv6
                elif mecanismo_lower.startswith("ip6:"):

                    red_ipv6 = mecanismo.split(
                        ":",
                        1
                    )[1]

                    detalles.append(
                        f"{parte}\n"
                        "→ Autoriza la dirección o red IPv6 "
                        f"{red_ipv6}."
                    )

                # A
                elif (
                    mecanismo_lower == "a"
                    or mecanismo_lower.startswith("a:")
                    or mecanismo_lower.startswith("a/")
                ):

                    detalles.append(
                        f"{parte}\n"
                        "→ Utiliza direcciones obtenidas "
                        "mediante el mecanismo A de SPF."
                    )

                # MX
                elif (
                    mecanismo_lower == "mx"
                    or mecanismo_lower.startswith("mx:")
                    or mecanismo_lower.startswith("mx/")
                ):

                    detalles.append(
                        f"{parte}\n"
                        "→ Utiliza hosts relacionados con "
                        "los registros MX."
                    )

                # EXISTS
                elif mecanismo_lower.startswith("exists:"):

                    objetivo = mecanismo.split(
                        ":",
                        1
                    )[1]

                    detalles.append(
                        f"{parte}\n"
                        "→ Evalúa la existencia DNS de "
                        f"{objetivo}."
                    )

                # REDIRECT
                elif mecanismo_lower.startswith("redirect="):

                    destino = mecanismo.split(
                        "=",
                        1
                    )[1]

                    detalles.append(
                        f"{parte}\n"
                        "→ Redirige la evaluación SPF hacia "
                        f"{destino}."
                    )

                # ALL
                elif mecanismo_lower == "all":

                    significados = {

                        "+":
                            "Pass: coincide con este mecanismo.",

                        "-":
                            "Fail: los orígenes que lleguen a "
                            "este punto no están autorizados "
                            "por esta política SPF.",

                        "~":
                            "SoftFail: el origen probablemente "
                            "no está autorizado.",

                        "?":
                            "Neutral: la política no establece "
                            "una afirmación positiva o negativa."
                    }

                    detalles.append(
                        f"{parte}\n"
                        f"→ {significados.get(calificador)}"
                    )

                else:

                    detalles.append(
                        f"{parte}\n"
                        "→ Mecanismo SPF detectado, pero "
                        "NetPro todavía no dispone de una "
                        "explicación específica."
                    )

            return (
                "🔎 NetPro detectó: SPF\n"
                "Sender Policy Framework\n\n"

                "REGISTRO ORIGINAL\n"
                "────────────────────────────────────\n"
                f"{valor_limpio}\n\n"

                "INTERPRETACIÓN\n"
                "────────────────────────────────────\n\n"

                + "\n\n".join(detalles)
            )

        # ========================================================
        # DMARC
        # ========================================================

        if valor_minusculas.startswith("v=dmarc1"):

            partes = valor_limpio.split(";")
            detalles = []

            for parte in partes:

                parte = parte.strip()

                if not parte:
                    continue

                parte_lower = parte.lower()

                if parte_lower == "v=dmarc1":

                    detalles.append(
                        "v=DMARC1\n"
                        "→ Versión del protocolo DMARC."
                    )

                elif parte_lower.startswith("p="):

                    politica = parte.split(
                        "=",
                        1
                    )[1].lower()

                    politicas = {

                        "none":
                            "Monitorización. No solicita "
                            "cuarentena ni rechazo.",

                        "quarantine":
                            "Solicita tratar como sospechosos "
                            "los mensajes que fallen DMARC.",

                        "reject":
                            "Solicita rechazar los mensajes "
                            "que fallen DMARC."
                    }

                    detalles.append(
                        f"{parte}\n"
                        f"→ {politicas.get(politica, politica)}"
                    )

                elif parte_lower.startswith("sp="):

                    politica = parte.split(
                        "=",
                        1
                    )[1]

                    detalles.append(
                        f"{parte}\n"
                        "→ Política publicada para "
                        f"subdominios: {politica}."
                    )

                elif parte_lower.startswith("pct="):

                    porcentaje = parte.split(
                        "=",
                        1
                    )[1]

                    detalles.append(
                        f"{parte}\n"
                        "→ Porcentaje de mensajes al que "
                        f"se aplica: {porcentaje}%."
                    )

                elif parte_lower.startswith("rua="):

                    destino = parte.split(
                        "=",
                        1
                    )[1]

                    detalles.append(
                        f"{parte}\n"
                        "→ Destino publicado para reportes "
                        f"agregados:\n{destino}"
                    )

                elif parte_lower.startswith("ruf="):

                    destino = parte.split(
                        "=",
                        1
                    )[1]

                    detalles.append(
                        f"{parte}\n"
                        "→ Destino publicado para determinados "
                        f"reportes:\n{destino}"
                    )

                else:

                    detalles.append(
                        f"{parte}\n"
                        "→ Parámetro DMARC."
                    )

            return (
                "🔎 NetPro detectó: DMARC\n\n"

                "REGISTRO ORIGINAL\n"
                "────────────────────────────────────\n"
                f"{valor_limpio}\n\n"

                "INTERPRETACIÓN\n"
                "────────────────────────────────────\n\n"

                + "\n\n".join(detalles)
            )

        # ========================================================
        # GOOGLE
        # ========================================================

        if valor_minusculas.startswith(
            "google-site-verification="
        ):

            return (
                "🔎 NetPro detectó: "
                "Google Site Verification\n\n"

                "Este registro contiene un token publicado "
                "en DNS para procesos de verificación de "
                "control del dominio utilizados por "
                "determinados servicios de Google."
            )

        # ========================================================
        # META / FACEBOOK
        # ========================================================

        if valor_minusculas.startswith(
            "facebook-domain-verification="
        ):

            return (
                "🔎 NetPro detectó: "
                "Facebook / Meta Domain Verification\n\n"

                "Este registro contiene un token publicado "
                "para procesos de verificación de dominio "
                "asociados con servicios de Meta."
            )

        # ========================================================
        # SLACK
        # ========================================================

        if valor_minusculas.startswith(
            "slack-domain-verification="
        ):

            return (
                "🔎 NetPro detectó: "
                "Slack Domain Verification\n\n"

                "Este registro contiene un token utilizado "
                "para procesos de verificación de dominio "
                "con Slack."
            )

        # ========================================================
        # ADOBE
        # ========================================================

        if valor_minusculas.startswith(
            "adobe-idp-site-verification="
        ):

            return (
                "🔎 NetPro detectó: Adobe Verification\n\n"

                "Este registro contiene información "
                "publicada para procesos de verificación "
                "de dominio relacionados con Adobe."
            )

        # ========================================================
        # MICROSOFT
        # ========================================================

        if valor_minusculas.startswith("ms="):

            return (
                "🔎 NetPro detectó: "
                "Microsoft Verification\n\n"

                "Este registro tiene el formato de un token "
                "de verificación de dominio utilizado por "
                "servicios de Microsoft."
            )

        return None

    # ============================================================
    # DOMINIO BASE
    # ============================================================

    def consultar_dominio_base(self):

        entrada = self.domain_entry.get().strip()

        if not entrada:

            messagebox.showinfo(
                "NetPro",
                "Primero introduce o consulta un dominio."
            )
            return

        dominio = self.extraer_hostname(entrada)

        if not dominio:

            messagebox.showerror(
                "NetPro",
                "No se pudo identificar el dominio."
            )
            return

        partes = dominio.split(".")

        if len(partes) < 2:

            messagebox.showinfo(
                "NetPro",
                "No se pudo determinar un dominio base."
            )
            return

        dominio_base = ".".join(
            partes[-2:]
        )

        if dominio_base == dominio:

            messagebox.showinfo(
                "NetPro",
                "Ya estás consultando el dominio base:\n\n"
                f"{dominio_base}"
            )
            return

        self.domain_entry.delete(
            0,
            "end"
        )

        self.domain_entry.insert(
            0,
            dominio_base
        )

        self.iniciar_busqueda()

    # ============================================================
    # EXTRAER HOSTNAME
    # ============================================================

    def extraer_hostname(self, entrada):

        entrada = entrada.strip()

        if not entrada:
            return None

        if "://" not in entrada:
            entrada = "https://" + entrada

        try:

            parsed = urlparse(entrada)

            return parsed.hostname

        except Exception:

            return None

    # ============================================================
    # FORMATEAR LISTA
    # ============================================================

    def formatear_lista(self, registros):

        if not registros:
            return "No encontrado"

        return "\n".join(
            str(registro)
            for registro in registros
        )

    # ============================================================
    # FORMATEAR MX
    # ============================================================

    def formatear_mx(self, registros):

        if not registros:
            return "No encontrado"

        lineas = []

        for registro in registros:

            if isinstance(registro, dict):

                prioridad = registro.get(
                    "priority",
                    "?"
                )

                servidor = registro.get(
                    "server",
                    "?"
                )

                lineas.append(
                    f"Prioridad {prioridad} → {servidor}"
                )

            else:

                lineas.append(
                    str(registro)
                )

        return "\n".join(lineas)

    # ============================================================
    # FINALIZAR
    # ============================================================

    def finalizar_busqueda(self, texto):

        self.mostrar_texto(texto)

        self.search_button.configure(
            state="normal",
            text="RESOLVER DNS"
        )

    # ============================================================
    # ¿QUÉ SIGNIFICA CADA RESULTADO?
    # ============================================================

    def mostrar_significados(self):

        # ========================================================
        # VALIDAR QUE EXISTA UNA CONSULTA
        # ========================================================

        if self.ultimo_resultado is None:

            messagebox.showinfo(
                "NetPro",
                "Primero realiza una consulta DNS."
            )
            return

        resultado = self.ultimo_resultado
        dominio = resultado["domain"]

        # ========================================================
        # VENTANA
        # ========================================================

        ventana = ctk.CTkToplevel(self)

        ventana.title(
            f"NetPro - DNS de {dominio}"
        )

        ventana.geometry("1050x760")
        ventana.minsize(900, 650)

        ventana.transient(
            self.winfo_toplevel()
        )

        # ========================================================
        # CONTENEDOR PRINCIPAL CON SCROLL
        # ========================================================

        scroll = ctk.CTkScrollableFrame(
            ventana,
            fg_color="#181818",
            corner_radius=0
        )

        scroll.pack(
            fill="both",
            expand=True
        )

        # ========================================================
        # CABECERA
        # ========================================================

        header = ctk.CTkFrame(
            scroll,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=40,
            pady=(30, 20)
        )

        ctk.CTkLabel(
            header,
            text="¿Qué significa cada resultado?",
            font=("Arial", 30, "bold")
        ).pack()

        ctk.CTkLabel(
            header,
            text="Aprende a interpretar la información obtenida en la consulta DNS.",
            font=("Arial", 14),
            text_color="#B8B8B8"
        ).pack(
            pady=(6, 8)
        )

        ctk.CTkLabel(
            header,
            text=f"Dominio analizado:  {dominio}",
            font=("Consolas", 15)
        ).pack()

        # ========================================================
        # TARJETA DEL DOMINIO
        # ========================================================

        dominio_frame = ctk.CTkFrame(
            scroll,
            corner_radius=12
        )

        dominio_frame.pack(
            fill="x",
            padx=40,
            pady=(0, 10)
        )

        ctk.CTkLabel(
            dominio_frame,
            text="🌐  DOMINIO CONSULTADO",
            font=("Arial", 15, "bold"),
            text_color="#3B8ED0"
        ).pack(
            anchor="w",
            padx=25,
            pady=(18, 5)
        )

        ctk.CTkLabel(
            dominio_frame,
            text=dominio,
            font=("Consolas", 20, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(4, 5)
        )

        ctk.CTkLabel(
            dominio_frame,
            text=(
                "Este es el nombre que NetPro consultó mediante DNS."
            ),
            font=("Arial", 13),
            text_color="#AAAAAA"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 18)
        )

        # ========================================================
        # FUNCIÓN INTERNA PARA CREAR TARJETAS
        # ========================================================

        def crear_tarjeta(
            parent,
            tipo,
            nombre,
            datos,
            descripcion
        ):

            tarjeta = ctk.CTkFrame(
                parent,
                corner_radius=12
            )

            # ----------------------------------------------------
            # CABECERA
            # ----------------------------------------------------

            cabecera = ctk.CTkFrame(
                tarjeta,
                fg_color="transparent"
            )

            cabecera.pack(
                fill="x",
                padx=20,
                pady=(18, 5)
            )

            ctk.CTkLabel(
                cabecera,
                text=tipo,
                font=("Consolas", 21, "bold"),
                text_color="#3B8ED0"
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                cabecera,
                text=f"   {nombre}",
                font=("Arial", 13, "bold")
            ).pack(
                side="left"
            )

            # ----------------------------------------------------
            # ESTADO
            # ----------------------------------------------------

            encontrado = bool(datos)

            estado = (
                "✓ ENCONTRADO"
                if encontrado
                else "NO ENCONTRADO"
            )

            color_estado = (
                "#4CAF50"
                if encontrado
                else "#888888"
            )

            ctk.CTkLabel(
                cabecera,
                text=estado,
                font=("Arial", 11, "bold"),
                text_color=color_estado
            ).pack(
                side="right"
            )

            # ----------------------------------------------------
            # RESULTADO
            # ----------------------------------------------------

            ctk.CTkLabel(
                tarjeta,
                text="RESULTADO",
                font=("Arial", 10, "bold"),
                text_color="#888888"
            ).pack(
                anchor="w",
                padx=20,
                pady=(10, 3)
            )

            if encontrado:

                if tipo == "MX":
                    valor = self.formatear_mx(
                        datos
                    )
                else:
                    valor = self.formatear_lista(
                        datos
                    )

            else:
                valor = "No se encontró este tipo de registro."

            resultado_box = ctk.CTkFrame(
                tarjeta,
                fg_color="#202020",
                corner_radius=8
            )

            resultado_box.pack(
                fill="x",
                padx=20,
                pady=(3, 12)
            )

            ctk.CTkLabel(
                resultado_box,
                text=valor,
                font=("Consolas", 13),
                justify="left",
                anchor="w",
                wraplength=390
            ).pack(
                fill="x",
                padx=15,
                pady=12
            )

            # ----------------------------------------------------
            # EXPLICACIÓN
            # ----------------------------------------------------

            ctk.CTkLabel(
                tarjeta,
                text=descripcion,
                font=("Arial", 12),
                text_color="#B8B8B8",
                justify="left",
                anchor="w",
                wraplength=390
            ).pack(
                fill="x",
                padx=20,
                pady=(0, 18)
            )

            return tarjeta

        # ========================================================
        # CONTENEDOR DE REGISTROS
        # ========================================================

        registros_frame = ctk.CTkFrame(
            scroll,
            fg_color="transparent"
        )

        registros_frame.pack(
            fill="x",
            padx=32,
            pady=5
        )

        registros_frame.grid_columnconfigure(
            0,
            weight=1,
            uniform="dns_cards"
        )

        registros_frame.grid_columnconfigure(
            1,
            weight=1,
            uniform="dns_cards"
        )

        # ========================================================
        # A
        # ========================================================

        tarjeta_a = crear_tarjeta(
            registros_frame,
            "A",
            "DIRECCIÓN IPv4",
            resultado["A"],
            (
                "Relaciona un nombre DNS con una dirección IPv4. "
                "IPv4 utiliza direcciones de 32 bits."
            )
        )

        tarjeta_a.grid(
            row=0,
            column=0,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        # ========================================================
        # AAAA
        # ========================================================

        tarjeta_aaaa = crear_tarjeta(
            registros_frame,
            "AAAA",
            "DIRECCIÓN IPv6",
            resultado["AAAA"],
            (
                "Relaciona un nombre DNS con una dirección IPv6. "
                "IPv6 utiliza direcciones de 128 bits."
            )
        )

        tarjeta_aaaa.grid(
            row=0,
            column=1,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        # ========================================================
        # CNAME
        # ========================================================

        tarjeta_cname = crear_tarjeta(
            registros_frame,
            "CNAME",
            "ALIAS",
            resultado["CNAME"],
            (
                "CNAME significa Canonical Name. Permite que un "
                "nombre DNS funcione como alias de otro nombre."
            )
        )

        tarjeta_cname.grid(
            row=1,
            column=0,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        # ========================================================
        # MX
        # ========================================================

        tarjeta_mx = crear_tarjeta(
            registros_frame,
            "MX",
            "MAIL EXCHANGE",
            resultado["MX"],
            (
                "Publica los servidores relacionados con la "
                "recepción de correo electrónico para el dominio."
            )
        )

        tarjeta_mx.grid(
            row=1,
            column=1,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        # ========================================================
        # NS
        # ========================================================

        tarjeta_ns = crear_tarjeta(
            registros_frame,
            "NS",
            "NAME SERVER",
            resultado["NS"],
            (
                "Publica los servidores de nombres asociados "
                "con una zona DNS."
            )
        )

        tarjeta_ns.grid(
            row=2,
            column=0,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        # ========================================================
        # TXT
        # ========================================================

        tarjeta_txt = crear_tarjeta(
            registros_frame,
            "TXT",
            "TEXT RECORD",
            resultado["TXT"],
            (
                "Permite publicar información textual dentro de "
                "DNS. Puede contener políticas de correo, "
                "verificaciones de dominio y otros datos."
            )
        )

        tarjeta_txt.grid(
            row=2,
            column=1,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        # ========================================================
        # RESUMEN DE LA CONSULTA
        # ========================================================

        resumen = ctk.CTkFrame(
            scroll,
            corner_radius=12
        )

        resumen.pack(
            fill="x",
            padx=40,
            pady=(15, 10)
        )

        ctk.CTkLabel(
            resumen,
            text="📊  RESUMEN DE LA CONSULTA",
            font=("Arial", 17, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            resumen,
            text=(
                "Vista rápida de los tipos de registro "
                "encontrados para este dominio."
            ),
            font=("Arial", 13),
            text_color="#AAAAAA"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )

        estados_frame = ctk.CTkFrame(
            resumen,
            fg_color="transparent"
        )

        estados_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        registros_resumen = [
            ("A", resultado["A"]),
            ("AAAA", resultado["AAAA"]),
            ("CNAME", resultado["CNAME"]),
            ("MX", resultado["MX"]),
            ("NS", resultado["NS"]),
            ("TXT", resultado["TXT"])
        ]

        for columna in range(6):

            estados_frame.grid_columnconfigure(
                columna,
                weight=1,
                uniform="summary"
            )

        for columna, (
            tipo,
            datos
        ) in enumerate(registros_resumen):

            encontrado = bool(datos)

            estado_card = ctk.CTkFrame(
                estados_frame,
                height=85,
                corner_radius=8
            )

            estado_card.grid(
                row=0,
                column=columna,
                padx=4,
                sticky="nsew"
            )

            estado_card.grid_propagate(False)

            ctk.CTkLabel(
                estado_card,
                text=tipo,
                font=("Consolas", 15, "bold")
            ).pack(
                pady=(14, 3)
            )

            ctk.CTkLabel(
                estado_card,
                text=(
                    "✓ Encontrado"
                    if encontrado
                    else "No encontrado"
                ),
                font=("Arial", 10, "bold"),
                text_color=(
                    "#4CAF50"
                    if encontrado
                    else "#888888"
                )
            ).pack()

        # ========================================================
        # NOTA EDUCATIVA
        # ========================================================

        nota = ctk.CTkFrame(
            scroll,
            corner_radius=12
        )

        nota.pack(
            fill="x",
            padx=40,
            pady=(0, 35)
        )

        ctk.CTkLabel(
            nota,
            text="💡  IMPORTANTE",
            font=("Arial", 15, "bold"),
            text_color="#3B8ED0"
        ).pack(
            anchor="w",
            padx=25,
            pady=(18, 8)
        )

        ctk.CTkLabel(
            nota,
            text=(
                "Que un registro aparezca como «No encontrado» "
                "no significa necesariamente que exista un problema.\n\n"
                "Cada dominio publica los registros DNS que necesita. "
                "Por ejemplo, un dominio puede tener registros A y AAAA "
                "sin publicar un CNAME para el nombre consultado."
            ),
            font=("Arial", 13),
            text_color="#B8B8B8",
            justify="left",
            anchor="w",
            wraplength=900
        ).pack(
            fill="x",
            padx=25,
            pady=(0, 18)
        )
    
      # ============================================================
    # ¿CÓMO FUNCIONA DNS? 
    # ============================================================

    def mostrar_funcionamiento(self):

        ventana = ctk.CTkToplevel(self)

        ventana.title("NetPro - Aprender DNS")
        ventana.geometry("1050x760")
        ventana.minsize(900, 650)

        ventana.transient(
            self.winfo_toplevel()
        )

        # ========================================================
        # CONTENEDOR CON SCROLL
        # ========================================================

        scroll = ctk.CTkScrollableFrame(
            ventana,
            fg_color="#181818",
            corner_radius=0
        )

        scroll.pack(
            fill="both",
            expand=True
        )

        # ========================================================
        # CABECERA
        # ========================================================

        header = ctk.CTkFrame(
            scroll,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=40,
            pady=(30, 20)
        )

        ctk.CTkLabel(
            header,
            text="¿Cómo funciona DNS?",
            font=("Arial", 30, "bold")
        ).pack()

        ctk.CTkLabel(
            header,
            text=(
                "Aprende qué ocurre cuando consultas un dominio "
                "y qué significa cada tipo de registro."
            ),
            font=("Arial", 14),
            text_color="#B8B8B8"
        ).pack(
            pady=(6, 0)
        )

        # ========================================================
        # ¿QUÉ ES DNS?
        # ========================================================

        intro = ctk.CTkFrame(
            scroll,
            corner_radius=12
        )

        intro.pack(
            fill="x",
            padx=40,
            pady=10
        )

        ctk.CTkLabel(
            intro,
            text="🌐  ¿QUÉ ES DNS?",
            font=("Arial", 17, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 8)
        )

        ctk.CTkLabel(
            intro,
            text=(
                "DNS significa Domain Name System.\n\n"
                "Permite relacionar nombres como www.example.com "
                "con información publicada dentro del sistema DNS. "
                "Esa información puede incluir direcciones IP, "
                "servidores de correo, servidores de nombres, "
                "alias y otros registros."
            ),
            font=("Arial", 14),
            justify="left",
            anchor="w",
            wraplength=880
        ).pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        # ========================================================
        # PROCESO DE CONSULTA
        # ========================================================

        proceso = ctk.CTkFrame(
            scroll,
            corner_radius=12
        )

        proceso.pack(
            fill="x",
            padx=40,
            pady=10
        )

        ctk.CTkLabel(
            proceso,
            text="🔎  PROCESO DE UNA CONSULTA DNS",
            font=("Arial", 17, "bold")
        ).pack(
            pady=(20, 5)
        )

        ctk.CTkLabel(
            proceso,
            text="Ejemplo: www.example.com",
            font=("Consolas", 14),
            text_color="#B8B8B8"
        ).pack(
            pady=(0, 18)
        )

        pasos_frame = ctk.CTkFrame(
            proceso,
            fg_color="transparent"
        )

        pasos_frame.pack(
            fill="x",
            padx=20,
            pady=(5, 25)
        )

        # Cuatro columnas exactamente del mismo tamaño
        for columna in range(4):

            pasos_frame.grid_columnconfigure(
                columna,
                weight=1,
                uniform="dns_steps"
            )

        pasos = [
            (
                "01",
                "USUARIO",
                "Escribes un dominio",
                "www.example.com"
            ),
            (
                "02",
                "RESOLVER DNS",
                "Recibe la consulta",
                "Busca información DNS"
            ),
            (
                "03",
                "SISTEMA DNS",
                "Localiza registros",
                "A, AAAA, CNAME..."
            ),
            (
                "04",
                "RESPUESTA",
                "Recibes información",
                "IP u otros registros"
            )
        ]

        for columna, (
            numero,
            titulo,
            descripcion,
            ejemplo
        ) in enumerate(pasos):

            tarjeta = ctk.CTkFrame(
                pasos_frame,
                height=165,
                corner_radius=10
            )

            tarjeta.grid(
                row=0,
                column=columna,
                padx=6,
                sticky="nsew"
            )

            tarjeta.grid_propagate(False)

            ctk.CTkLabel(
                tarjeta,
                text=numero,
                font=("Arial", 24, "bold"),
                text_color="#3B8ED0"
            ).pack(
                pady=(18, 5)
            )

            ctk.CTkLabel(
                tarjeta,
                text=titulo,
                font=("Arial", 13, "bold")
            ).pack(
                pady=(0, 8)
            )

            ctk.CTkLabel(
                tarjeta,
                text=descripcion,
                font=("Arial", 12),
                text_color="#D0D0D0"
            ).pack(
                pady=(0, 5)
            )

            ctk.CTkLabel(
                tarjeta,
                text=ejemplo,
                font=("Consolas", 11),
                text_color="#999999",
                wraplength=180,
                justify="center"
            ).pack(
                padx=8,
                pady=(2, 12)
            )

        # ========================================================
        # REGISTROS PRINCIPALES
        # ========================================================

        registros_frame = ctk.CTkFrame(
            scroll,
            corner_radius=12
        )

        registros_frame.pack(
            fill="x",
            padx=40,
            pady=10
        )

        ctk.CTkLabel(
            registros_frame,
            text="📚  REGISTROS DNS PRINCIPALES",
            font=("Arial", 17, "bold")
        ).pack(
            pady=(20, 5)
        )

        ctk.CTkLabel(
            registros_frame,
            text=(
                "Un dominio puede publicar diferentes tipos "
                "de información."
            ),
            font=("Arial", 13),
            text_color="#AAAAAA"
        ).pack(
            pady=(0, 15)
        )

        registros_grid = ctk.CTkFrame(
            registros_frame,
            fg_color="transparent"
        )

        registros_grid.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        registros_grid.grid_columnconfigure(
            0,
            weight=1,
            uniform="dns_records"
        )

        registros_grid.grid_columnconfigure(
            1,
            weight=1,
            uniform="dns_records"
        )

        registros = [
            (
                "A",
                "IPv4",
                "Relaciona un nombre DNS con una dirección IPv4.",
                "192.0.2.10"
            ),
            (
                "AAAA",
                "IPv6",
                "Relaciona un nombre DNS con una dirección IPv6.",
                "2001:db8::10"
            ),
            (
                "CNAME",
                "Alias",
                "Indica que un nombre funciona como alias de otro.",
                "Alias: servidor.example.com"
            ),
            (
                "MX",
                "Correo",
                "Publica servidores relacionados con la "
                "recepción de correo.",
                "Servidor: mail.example.com"
            ),
            (
                "NS",
                "Name Server",
                "Publica servidores de nombres asociados "
                "con una zona DNS.",
                "Servidor: ns1.example.com"
            ),
            (
                "TXT",
                "Texto",
                "Permite publicar políticas, verificaciones "
                "y otra información textual.",
                "Ejemplo: v=spf1 ..."
            )
        ]

        for indice, (
            tipo,
            nombre,
            descripcion,
            ejemplo
        ) in enumerate(registros):

            fila = indice // 2
            columna = indice % 2

            tarjeta = ctk.CTkFrame(
                registros_grid,
                corner_radius=10
            )

            tarjeta.grid(
                row=fila,
                column=columna,
                padx=8,
                pady=8,
                sticky="nsew"
            )

            cabecera = ctk.CTkFrame(
                tarjeta,
                fg_color="transparent"
            )

            cabecera.pack(
                fill="x",
                padx=18,
                pady=(15, 5)
            )

            ctk.CTkLabel(
                cabecera,
                text=tipo,
                font=("Consolas", 20, "bold"),
                text_color="#3B8ED0"
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                cabecera,
                text=f"   {nombre}",
                font=("Arial", 14, "bold")
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                tarjeta,
                text=descripcion,
                font=("Arial", 13),
                justify="left",
                anchor="w",
                wraplength=390
            ).pack(
                fill="x",
                padx=18,
                pady=(5, 6)
            )

            ctk.CTkLabel(
                tarjeta,
                text=ejemplo,
                font=("Consolas", 12),
                text_color="#999999",
                anchor="w"
            ).pack(
                fill="x",
                padx=18,
                pady=(3, 15)
            )

        # ========================================================
        # URL VS HOSTNAME
        # ========================================================

        url_frame = ctk.CTkFrame(
            scroll,
            corner_radius=12
        )

        url_frame.pack(
            fill="x",
            padx=40,
            pady=10
        )

        ctk.CTkLabel(
            url_frame,
            text="🔗  URL Y HOSTNAME",
            font=("Arial", 17, "bold")
        ).pack(
            pady=(20, 5)
        )

        ctk.CTkLabel(
            url_frame,
            text=(
                "Una URL contiene varias partes. "
                "DNS trabaja principalmente con el hostname."
            ),
            font=("Arial", 13),
            text_color="#AAAAAA"
        ).pack(
            pady=(0, 15)
        )

        ctk.CTkLabel(
            url_frame,
            text="https://www.example.com/productos?id=20",
            font=("Consolas", 16)
        ).pack(
            pady=(5, 18)
        )

        partes_frame = ctk.CTkFrame(
            url_frame,
            fg_color="transparent"
        )

        partes_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        for columna in range(4):

            partes_frame.grid_columnconfigure(
                columna,
                weight=1,
                uniform="url_parts"
            )

        partes = [
            ("PROTOCOLO", "https"),
            ("HOSTNAME", "www.example.com"),
            ("RUTA", "/productos"),
            ("QUERY", "?id=20")
        ]

        for columna, (titulo, valor) in enumerate(partes):

            tarjeta = ctk.CTkFrame(
                partes_frame,
                height=90,
                corner_radius=8
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
                text=titulo,
                font=("Arial", 11, "bold"),
                text_color="#3B8ED0"
            ).pack(
                pady=(15, 5)
            )

            ctk.CTkLabel(
                tarjeta,
                text=valor,
                font=("Consolas", 12),
                wraplength=190
            ).pack()

        hostname_box = ctk.CTkFrame(
            url_frame,
            corner_radius=8
        )

        hostname_box.pack(
            padx=20,
            pady=(5, 20)
        )

        ctk.CTkLabel(
            hostname_box,
            text="HOSTNAME CONSULTADO POR DNS",
            font=("Arial", 11, "bold"),
            text_color="#3B8ED0"
        ).pack(
            padx=25,
            pady=(12, 3)
        )

        ctk.CTkLabel(
            hostname_box,
            text="www.example.com",
            font=("Consolas", 15, "bold")
        ).pack(
            padx=25,
            pady=(0, 12)
        )

        # ========================================================
        # SPF Y DMARC
        # ========================================================

        correo_frame = ctk.CTkFrame(
            scroll,
            corner_radius=12
        )

        correo_frame.pack(
            fill="x",
            padx=40,
            pady=10
        )

        ctk.CTkLabel(
            correo_frame,
            text="🛡️  DNS Y SEGURIDAD DEL CORREO",
            font=("Arial", 17, "bold")
        ).pack(
            pady=(20, 5)
        )

        ctk.CTkLabel(
            correo_frame,
            text=(
                "Algunos registros DNS publican políticas "
                "relacionadas con correo electrónico."
            ),
            font=("Arial", 13),
            text_color="#AAAAAA"
        ).pack(
            pady=(0, 15)
        )

        correo_grid = ctk.CTkFrame(
            correo_frame,
            fg_color="transparent"
        )

        correo_grid.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        correo_grid.grid_columnconfigure(
            0,
            weight=1,
            uniform="mail_security"
        )

        correo_grid.grid_columnconfigure(
            1,
            weight=1,
            uniform="mail_security"
        )

        # SPF
        spf = ctk.CTkFrame(
            correo_grid,
            corner_radius=10
        )

        spf.grid(
            row=0,
            column=0,
            padx=8,
            sticky="nsew"
        )

        ctk.CTkLabel(
            spf,
            text="SPF",
            font=("Arial", 20, "bold"),
            text_color="#3B8ED0"
        ).pack(
            pady=(18, 3)
        )

        ctk.CTkLabel(
            spf,
            text="Sender Policy Framework",
            font=("Arial", 12, "bold")
        ).pack()

        ctk.CTkLabel(
            spf,
            text=(
                "Publica una política relacionada con qué "
                "sistemas pueden enviar correo utilizando "
                "un dominio."
            ),
            font=("Arial", 13),
            wraplength=380,
            justify="left"
        ).pack(
            padx=20,
            pady=(12, 10)
        )

        ctk.CTkLabel(
            spf,
            text="v=spf1 include:_spf.example.com -all",
            font=("Consolas", 12),
            text_color="#999999",
            wraplength=380
        ).pack(
            padx=20,
            pady=(0, 18)
        )

        # DMARC
        dmarc = ctk.CTkFrame(
            correo_grid,
            corner_radius=10
        )

        dmarc.grid(
            row=0,
            column=1,
            padx=8,
            sticky="nsew"
        )

        ctk.CTkLabel(
            dmarc,
            text="DMARC",
            font=("Arial", 20, "bold"),
            text_color="#3B8ED0"
        ).pack(
            pady=(18, 3)
        )

        ctk.CTkLabel(
            dmarc,
            text="Autenticación y políticas de correo",
            font=("Arial", 12, "bold")
        ).pack()

        ctk.CTkLabel(
            dmarc,
            text=(
                "Publica políticas relacionadas con la "
                "autenticación y el tratamiento del "
                "correo electrónico."
            ),
            font=("Arial", 13),
            wraplength=380,
            justify="left"
        ).pack(
            padx=20,
            pady=(12, 10)
        )

        ctk.CTkLabel(
            dmarc,
            text="_dmarc.example.com",
            font=("Consolas", 12),
            text_color="#999999"
        ).pack(
            padx=20,
            pady=(0, 18)
        )

        # ========================================================
        # RESUMEN
        # ========================================================

        resumen = ctk.CTkFrame(
            scroll,
            corner_radius=12
        )

        resumen.pack(
            fill="x",
            padx=40,
            pady=(10, 35)
        )

        ctk.CTkLabel(
            resumen,
            text="💡  QUÉ DEBES RECORDAR",
            font=("Arial", 17, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 15)
        )

        conceptos = [
            (
                "01",
                "DNS no es solamente dominio e IP.",
                "También publica otros tipos de información."
            ),
            (
                "02",
                "A y AAAA son registros diferentes.",
                "A se relaciona con IPv4 y AAAA con IPv6."
            ),
            (
                "03",
                "CNAME representa un alias.",
                "Un nombre puede estar asociado con otro nombre DNS."
            ),
            (
                "04",
                "MX está relacionado con correo.",
                "Publica servidores relacionados con la recepción "
                "de correo electrónico."
            ),
            (
                "05",
                "TXT puede contener políticas y verificaciones.",
                "SPF es uno de los ejemplos que NetPro puede interpretar."
            ),
            (
                "06",
                "www.example.com y example.com son nombres distintos.",
                "Por eso pueden devolver registros DNS diferentes."
            )
        ]

        for numero, titulo, descripcion in conceptos:

            concepto = ctk.CTkFrame(
                resumen,
                fg_color="transparent"
            )

            concepto.pack(
                fill="x",
                padx=25,
                pady=7
            )

            ctk.CTkLabel(
                concepto,
                text=numero,
                width=45,
                font=("Arial", 16, "bold"),
                text_color="#3B8ED0"
            ).pack(
                side="left",
                anchor="n"
            )

            contenido = ctk.CTkFrame(
                concepto,
                fg_color="transparent"
            )

            contenido.pack(
                side="left",
                fill="x",
                expand=True
            )

            ctk.CTkLabel(
                contenido,
                text=titulo,
                font=("Arial", 13, "bold"),
                anchor="w"
            ).pack(
                fill="x"
            )

            ctk.CTkLabel(
                contenido,
                text=descripcion,
                font=("Arial", 12),
                text_color="#AAAAAA",
                justify="left",
                anchor="w",
                wraplength=800
            ).pack(
                fill="x",
                pady=(2, 0)
            )

        # Espacio inferior
        ctk.CTkLabel(
            resumen,
            text=""
        ).pack(
            pady=8
        )  