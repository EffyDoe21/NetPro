import customtkinter as ctk
import threading

from ui.home import HomeFrame
from ui.analyzer import AnalyzerFrame
from ui.dns_page import DNSFrame
from ui.diagnostic_page import DiagnosticFrame
from ui.ports_page import PortsFrame
from ui.http_page import HTTPFrame
from ui.system_page import SystemFrame
from ui.learn import LearnFrame
from ui.history_page import HistoryFrame

from core.network_status import obtener_estado_red


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class NetProApp(ctk.CTk):

    # ============================================
    # COLORES
    # ============================================

    AZUL = "#3B8ED0"
    VERDE = "#2ECC71"
    ROJO = "#E74C3C"
    GRIS = "#7F8C8D"
    TEXTO_SECUNDARIO = "#A0A0A0"

    def __init__(self):
        super().__init__()

        self.title(
            "NetPro - Network & Security Toolkit"
        )

        self.geometry("1200x750")
        self.minsize(1000, 650)

        # Evita lanzar varias consultas de red
        # al mismo tiempo.
        self.consulta_red_activa = False

        # ========================================
        # SIDEBAR
        # ========================================

        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        # Mantener ancho fijo del sidebar.
        self.sidebar.pack_propagate(False)

        # ========================================
        # LOGO
        # ========================================

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="NETPRO",
            font=("Arial", 30, "bold")
        )

        self.logo.pack(
            pady=(30, 2)
        )

        self.subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Network & Security Toolkit",
            font=("Arial", 11)
        )

        self.subtitle.pack(
            pady=(0, 25)
        )

        # ========================================
        # MENÚ
        # ========================================

        self.create_menu_button(
            "🏠  Inicio",
            self.show_home
        )

        self.create_menu_button(
            "🌐  IP & Subnet",
            self.show_ip
        )

        self.create_menu_button(
            "🔎  DNS",
            self.show_dns
        )

        self.create_menu_button(
            "📡  Diagnóstico",
            self.show_diagnostic
        )

        self.create_menu_button(
            "🔌  Puertos",
            self.show_ports
        )

        self.create_menu_button(
            "🌍  HTTP / HTTPS",
            self.show_http
        )

        self.create_menu_button(
            "🖥  Mi Sistema",
            self.show_system
        )

        self.create_menu_button(
            "🎓  Aprendizaje",
            self.show_learning
        )

        self.create_menu_button(
            "📋  Historial",
            self.show_history
        )

        # ========================================
        # VERSIÓN
        # ========================================

        self.version = ctk.CTkLabel(
            self.sidebar,
            text="NetPro v0.1",
            font=("Arial", 10),
            text_color="#8A8A8A"
        )

        self.version.pack(
            side="bottom",
            pady=(5, 15)
        )

        # ========================================
        # MONITOR DE RED
        # ========================================

        self.network_frame = ctk.CTkFrame(
            self.sidebar,
            corner_radius=10,
            border_width=1
        )

        self.network_frame.pack(
            side="bottom",
            padx=14,
            pady=(5, 5),
            fill="x"
        )

        # ========================================
        # TÍTULO
        # ========================================

        self.network_title = ctk.CTkLabel(
            self.network_frame,
            text="ESTADO DE RED",
            font=("Arial", 10, "bold"),
            text_color=self.AZUL
        )

        self.network_title.pack(
            pady=(9, 7)
        )

        # ========================================
        # ETHERNET
        # ========================================

        ethernet_row = ctk.CTkFrame(
            self.network_frame,
            fg_color="transparent"
        )

        ethernet_row.pack(
            padx=12,
            pady=(0, 5),
            fill="x"
        )

        self.ethernet_led = ctk.CTkLabel(
            ethernet_row,
            text="●",
            font=("Arial", 17, "bold"),
            text_color=self.GRIS,
            width=20
        )

        self.ethernet_led.pack(
            side="left"
        )

        ethernet_info = ctk.CTkFrame(
            ethernet_row,
            fg_color="transparent"
        )

        ethernet_info.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(4, 0)
        )

        self.ethernet_label = ctk.CTkLabel(
            ethernet_info,
            text="ETHERNET",
            font=("Arial", 10, "bold"),
            anchor="w"
        )

        self.ethernet_label.pack(
            anchor="w"
        )

        self.ethernet_estado = ctk.CTkLabel(
            ethernet_info,
            text="Comprobando...",
            font=("Arial", 9),
            text_color=self.GRIS,
            anchor="w"
        )

        self.ethernet_estado.pack(
            anchor="w",
            pady=(1, 0)
        )

        # Se conserva por compatibilidad con la lógica existente,
        # pero no ocupa espacio visual.
        self.ethernet_velocidad = ctk.CTkLabel(
            self.network_frame,
            text="",
            width=0,
            height=0
        )

        # ========================================
        # SEPARADOR
        # ========================================

        self.separador_red = ctk.CTkFrame(
            self.network_frame,
            height=1,
            fg_color="#444444"
        )

        self.separador_red.pack(
            padx=12,
            pady=(2, 6),
            fill="x"
        )

        # ========================================
        # WI-FI
        # ========================================

        wifi_row = ctk.CTkFrame(
            self.network_frame,
            fg_color="transparent"
        )

        wifi_row.pack(
            padx=12,
            pady=(0, 9),
            fill="x"
        )

        self.wifi_led = ctk.CTkLabel(
            wifi_row,
            text="●",
            font=("Arial", 17, "bold"),
            text_color=self.GRIS,
            width=20
        )

        self.wifi_led.pack(
            side="left"
        )

        wifi_info = ctk.CTkFrame(
            wifi_row,
            fg_color="transparent"
        )

        wifi_info.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(4, 0)
        )

        self.wifi_label = ctk.CTkLabel(
            wifi_info,
            text="WI-FI",
            font=("Arial", 10, "bold"),
            anchor="w"
        )

        self.wifi_label.pack(
            anchor="w"
        )

        self.wifi_estado = ctk.CTkLabel(
            wifi_info,
            text="Comprobando...",
            font=("Arial", 9),
            text_color=self.GRIS,
            anchor="w"
        )

        self.wifi_estado.pack(
            anchor="w",
            pady=(1, 0)
        )

        # Se conserva por compatibilidad con la lógica existente,
        # pero no ocupa espacio visual.
        self.wifi_detalle = ctk.CTkLabel(
            self.network_frame,
            text="",
            width=0,
            height=0
        )

        # ========================================
        # CONTENEDOR PRINCIPAL
        # ========================================

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        # ========================================
        # PÁGINA INICIAL
        # ========================================

        self.show_home()

        # ========================================
        # INICIAR MONITOR
        # ========================================

        self.after(
            500,
            self.actualizar_estado_red
        )

    # ============================================
    # CREAR BOTONES
    # ============================================

    def create_menu_button(
        self,
        text,
        command
    ):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=42,
            anchor="w",
            command=command
        )

        button.pack(
            padx=18,
            pady=5,
            fill="x"
        )

    # ============================================
    # MONITOR DE RED
    # ============================================

    def actualizar_estado_red(self):
        """
        Inicia una consulta de Ethernet y Wi-Fi
        sin bloquear la interfaz.
        """

        if not self.consulta_red_activa:

            self.consulta_red_activa = True

            hilo = threading.Thread(
                target=self._consultar_estado_red,
                daemon=True
            )

            hilo.start()

        # Comprobar nuevamente cada 3 segundos.
        self.after(
            3000,
            self.actualizar_estado_red
        )

    def _consultar_estado_red(self):
        """
        Consulta Ethernet y Wi-Fi desde un hilo
        secundario para no bloquear CustomTkinter.
        """

        try:

            resultado = obtener_estado_red()

        except Exception as error:

            resultado_error = {
                "detectado": False,
                "conectado": False,
                "nombre": None,
                "descripcion": None,
                "velocidad": None,
                "estado": "Error",
                "error": str(error)
            }

            wifi_error = resultado_error.copy()

            wifi_error.update({
                "ssid": None,
                "senal": None,
                "recepcion": None,
                "transmision": None
            })

            resultado = {
                "ethernet": resultado_error,
                "wifi": wifi_error
            }

        # Regresar al hilo principal para
        # modificar los widgets.
        self.after(
            0,
            self._mostrar_estado_red,
            resultado
        )

    # ============================================
    # MOSTRAR ESTADO COMPLETO
    # ============================================

    def _mostrar_estado_red(
        self,
        resultado
    ):

        self.consulta_red_activa = False

        ethernet = resultado.get(
            "ethernet",
            {}
        )

        wifi = resultado.get(
            "wifi",
            {}
        )

        self._mostrar_ethernet(
            ethernet
        )

        self._mostrar_wifi(
            wifi
        )

    # ============================================
    # MOSTRAR ETHERNET
    # ============================================

    def _mostrar_ethernet(
        self,
        resultado
    ):

        # ----------------------------------------
        # ERROR
        # ----------------------------------------

        if resultado.get("error"):

            self.ethernet_led.configure(
                text_color=self.GRIS
            )

            self.ethernet_estado.configure(
                text="Error de consulta",
                text_color=self.GRIS
            )

            self.ethernet_velocidad.configure(
                text=""
            )

            return

        # ----------------------------------------
        # NO DETECTADO
        # ----------------------------------------

        if not resultado.get("detectado"):

            self.ethernet_led.configure(
                text_color=self.GRIS
            )

            self.ethernet_estado.configure(
                text="No disponible",
                text_color=self.GRIS
            )

            self.ethernet_velocidad.configure(
                text="Sin adaptador"
            )

            return

        # ----------------------------------------
        # CONECTADO
        # ----------------------------------------

        if resultado.get("conectado"):

            self.ethernet_led.configure(
                text_color=self.VERDE
            )

            velocidad = (
                resultado.get("velocidad")
                or ""
            )

            texto_estado = "Conectado"

            if velocidad:
                texto_estado += f" · {velocidad}"

            self.ethernet_estado.configure(
                text=texto_estado,
                text_color=self.VERDE
            )

            self.ethernet_velocidad.configure(
                text=""
            )

        # ----------------------------------------
        # DESCONECTADO
        # ----------------------------------------

        else:

            self.ethernet_led.configure(
                text_color=self.ROJO
            )

            self.ethernet_estado.configure(
                text="Desconectado · Sin enlace",
                text_color=self.ROJO
            )

            self.ethernet_velocidad.configure(
                text=""
            )

    # ============================================
    # MOSTRAR WI-FI
    # ============================================

    def _mostrar_wifi(
        self,
        resultado
    ):

        # ----------------------------------------
        # ERROR
        # ----------------------------------------

        if resultado.get("error"):

            self.wifi_led.configure(
                text_color=self.GRIS
            )

            self.wifi_estado.configure(
                text="Error de consulta",
                text_color=self.GRIS
            )

            self.wifi_detalle.configure(
                text=""
            )

            return

        # ----------------------------------------
        # NO HAY ADAPTADOR WI-FI
        # ----------------------------------------

        if not resultado.get("detectado"):

            self.wifi_led.configure(
                text_color=self.GRIS
            )

            self.wifi_estado.configure(
                text="No disponible · Sin adaptador",
                text_color=self.GRIS
            )

            self.wifi_detalle.configure(
                text=""
            )

            return

        # ----------------------------------------
        # WI-FI CONECTADO
        # ----------------------------------------

        if resultado.get("conectado"):

            self.wifi_led.configure(
                text_color=self.VERDE
            )



            ssid = resultado.get(
                "ssid"
            )

            senal = resultado.get(
                "senal"
            )

            velocidad = resultado.get(
                "velocidad"
            )

            detalles = []

            if ssid:
                detalles.append(
                    ssid
                )

            if senal:
                detalles.append(
                    f"Señal {senal}"
                )

            if not detalles and velocidad:
                detalles.append(
                    velocidad
                )

            if detalles:

                texto_detalle = " • ".join(
                    detalles
                )

            else:

                texto_detalle = (
                    "Red inalámbrica"
                )

            texto_wifi = "Conectado"

            if texto_detalle:
                texto_wifi += f" · {texto_detalle}"

            self.wifi_estado.configure(
                text=texto_wifi,
                text_color=self.VERDE
            )

            self.wifi_detalle.configure(
                text=""
            )

        # ----------------------------------------
        # WI-FI DESCONECTADO
        # ----------------------------------------

        else:

            self.wifi_led.configure(
                text_color=self.ROJO
            )

            self.wifi_estado.configure(
                text="Desconectado · Sin conexión",
                text_color=self.ROJO
            )

            self.wifi_detalle.configure(
                text=""
            )

    # ============================================
    # CAMBIAR PÁGINAS
    # ============================================

    def show_page(
        self,
        frame_class
    ):

        for widget in self.content.winfo_children():
            widget.destroy()

        page = frame_class(
            self.content
        )

        page.pack(
            fill="both",
            expand=True
        )

    # ============================================
    # NAVEGACIÓN
    # ============================================

    def show_home(self):
        self.show_page(HomeFrame)

    def show_ip(self):
        self.show_page(AnalyzerFrame)

    def show_dns(self):
        self.show_page(DNSFrame)

    def show_diagnostic(self):
        self.show_page(DiagnosticFrame)

    def show_ports(self):
        self.show_page(PortsFrame)

    def show_http(self):
        self.show_page(HTTPFrame)

    def show_system(self):
        self.show_page(SystemFrame)

    def show_learning(self):
        self.show_page(LearnFrame)

    def show_history(self):
        self.show_page(HistoryFrame)


# ============================================================
# INICIAR NETPRO
# ============================================================

if __name__ == "__main__":

    app = NetProApp()

    app.mainloop()