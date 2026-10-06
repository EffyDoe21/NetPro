import customtkinter as ctk


class LearnFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        title = ctk.CTkLabel(
            self,
            text="🎓 Modo Aprendizaje",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=(50, 10))

        subtitle = ctk.CTkLabel(
            self,
            text="Aprende redes y ciberseguridad paso a paso.",
            font=("Arial", 15)
        )
        subtitle.pack(pady=(0, 30))

        mensaje = ctk.CTkLabel(
            self,
            text=(
                "Bienvenida al modo aprendizaje de NetPro.\n\n"
                "Aquí aprenderás conceptos como:\n\n"
                "• Direcciones IPv4\n"
                "• IP pública y privada\n"
                "• Máscaras de subred\n"
                "• CIDR\n"
                "• Network Address\n"
                "• Broadcast\n"
                "• Hosts\n"
                "• Subnetting\n"
                "• DNS\n"
                "• Puertos y protocolos"
            ),
            font=("Arial", 16),
            justify="left"
        )

        mensaje.pack(
            padx=40,
            pady=20
        )