import customtkinter as ctk

from ui.home import HomeFrame
from ui.analyzer import AnalyzerFrame
from ui.ipv6_page import IPv6Frame
from ui.dns_page import DNSFrame
from ui.diagnostic_page import DiagnosticFrame
from ui.ports_page import PortsFrame
from ui.http_page import HTTPFrame
from ui.system_page import SystemFrame
from ui.learn import LearnFrame
from ui.history_page import HistoryFrame



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

        # ========================================
        # SIDEBAR
        # ========================================

        
        self.sidebar = ctk.CTkScrollableFrame(
        self,
        width=230,
        corner_radius=0,
        scrollbar_button_color="#2478B5",
        scrollbar_button_hover_color="#3594D0"
        )


        self.sidebar.pack(
            side="left",
            fill="y"
        )

        # Mantener ancho fijo del sidebar.
        #self.sidebar.pack_propagate(False)

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
        "🌐  IPv6",
        self.show_ipv6
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
        # CONTENEDOR PRINCIPAL
        # ========================================

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="#2B2B2B"
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
    # CAMBIAR PAGINAS
    # ============================================

    def show_page(self, frame_class):

        # Eliminar la pagina anterior
        for widget in self.content.winfo_children():
            widget.destroy()

        # Mantener el fondo gris grafito
        self.content.configure(fg_color="#2B2B2B")

        # Modulos que no necesitan scroll externo
        modulos_sin_scroll = (
            SystemFrame,
            IPv6Frame,
            LearnFrame,
            HistoryFrame,
            AnalyzerFrame
        )

        if frame_class in modulos_sin_scroll:

            # Cargar directamente el modulo
            page = frame_class(self.content)

        else:

            # Crear contenedor desplazable
            contenedor = ctk.CTkScrollableFrame(
                self.content,
                corner_radius=0,
                fg_color="#2B2B2B",
                scrollbar_button_color="#2478B5",
                scrollbar_button_hover_color="#3594D0"
            )

            contenedor.pack(
                fill="both",
                expand=True
            )

            page = frame_class(contenedor)

        # Mostrar pagina
        page.pack(
            fill="both",
            expand=True
        )

    # ============================================
    # NAVEGACION
    # ============================================

    def show_home(self):
        self.show_page(HomeFrame)

    def show_ip(self):
        self.show_page(AnalyzerFrame)

    def show_ipv6(self):
        self.show_page(IPv6Frame)

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