import customtkinter as ctk


class HistoryFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        ctk.CTkLabel(
            self,
            text="📋 Historial",
            font=("Arial", 30, "bold")
        ).pack(pady=50)

        ctk.CTkLabel(
            self,
            text="Aquí aparecerán las consultas realizadas en NetPro.",
            font=("Arial", 16)
        ).pack()