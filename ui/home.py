import customtkinter as ctk


class HomeFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        title = ctk.CTkLabel(
            self,
            text="NETPRO",
            font=("Arial", 36, "bold")
        )
        title.pack(pady=(70, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Network & Security Toolkit",
            font=("Arial", 18)
        )
        subtitle.pack(pady=(0, 30))

        description = ctk.CTkLabel(
            self,
            text=(
                "Herramienta educativa para análisis, "
                "diagnóstico y aprendizaje de redes.\n\n"
                "Selecciona una herramienta desde el menú lateral."
            ),
            font=("Arial", 16),
            justify="center"
        )
        description.pack(pady=20)