import customtkinter as ctk

from core.dns import resolver_dominio
from core.ping import ejecutar_ping


class ToolsFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        # =========================
        # TÍTULO
        # =========================

        title = ctk.CTkLabel(
            self,
            text="🛠 Herramientas de Red",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=(30, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Utilidades para diagnóstico y aprendizaje de redes.",
            font=("Arial", 14)
        )
        subtitle.pack(pady=(0, 20))

        # =========================
        # DNS LOOKUP
        # =========================

        dns_title = ctk.CTkLabel(
            self,
            text="DNS Lookup",
            font=("Arial", 22, "bold")
        )
        dns_title.pack(pady=(5, 5))

        dns_description = ctk.CTkLabel(
            self,
            text="Introduce un dominio para consultar sus direcciones IP."
        )
        dns_description.pack(pady=(0, 10))

        # Campo dominio
        self.domain_entry = ctk.CTkEntry(
            self,
            width=400,
            height=40,
            placeholder_text="Ejemplo: example.com"
        )
        self.domain_entry.pack(pady=5)

        # Botón DNS
        dns_button = ctk.CTkButton(
            self,
            text="RESOLVER DNS",
            width=200,
            height=40,
            command=self.buscar_dns
        )
        dns_button.pack(pady=10)

        # =========================
        # PING
        # =========================

        ping_title = ctk.CTkLabel(
            self,
            text="Ping",
            font=("Arial", 22, "bold")
        )
        ping_title.pack(pady=(15, 5))

        ping_description = ctk.CTkLabel(
            self,
            text="Comprueba la conectividad y mide la latencia hacia un destino."
        )
        ping_description.pack(pady=(0, 10))

        # Campo destino
        self.ping_entry = ctk.CTkEntry(
            self,
            width=400,
            height=40,
            placeholder_text="Ejemplo: example.com o 192.168.1.1"
        )
        self.ping_entry.pack(pady=5)

        # Botón Ping
        ping_button = ctk.CTkButton(
            self,
            text="HACER PING",
            width=200,
            height=40,
            command=self.hacer_ping
        )
        ping_button.pack(pady=10)

        # =========================
        # RESULTADOS
        # =========================

        self.resultado = ctk.CTkTextbox(
            self,
            width=650,
            height=230,
            font=("Consolas", 14)
        )

        self.resultado.pack(
            padx=30,
            pady=15
        )

        self.resultado.insert(
            "1.0",
            "Selecciona una herramienta para comenzar."
        )

    # =========================
    # BUSCAR DNS
    # =========================

    def buscar_dns(self):

        dominio = self.domain_entry.get().strip()

        try:
            resultado = resolver_dominio(dominio)

            ipv4 = "\n".join(resultado["ipv4"])
            ipv6 = "\n".join(resultado["ipv6"])

            if not ipv4:
                ipv4 = "No encontrada"

            if not ipv6:
                ipv6 = "No encontrada"

            texto = f"""
DNS LOOKUP
────────────────────────────────────

Dominio:
{resultado['domain']}

IPv4 (registro A):
{ipv4}

IPv6 (registro AAAA):
{ipv6}
"""

            self.resultado.delete(
                "1.0",
                "end"
            )

            self.resultado.insert(
                "1.0",
                texto
            )

        except ValueError as error:

            self.resultado.delete(
                "1.0",
                "end"
            )

            self.resultado.insert(
                "1.0",
                f"⚠ {error}"
            )

    # =========================
    # HACER PING
    # =========================

    def hacer_ping(self):

        destino = self.ping_entry.get().strip()

        try:
            resultado = ejecutar_ping(destino)

            # Estado del destino
            if resultado["respuesta"]:
                estado = "Responde"
            else:
                estado = "Sin respuesta"

            # =========================
            # LATENCIAS
            # =========================

            minimo = (
                f'{resultado["minimo"]} ms'
                if resultado["minimo"] is not None
                else "N/D"
            )

            maximo = (
                f'{resultado["maximo"]} ms'
                if resultado["maximo"] is not None
                else "N/D"
            )

            promedio = (
                f'{resultado["promedio"]} ms'
                if resultado["promedio"] is not None
                else "N/D"
            )

            # =========================
            # TEXTO RESULTADO
            # =========================

            texto = f"""
PING
────────────────────────────────────

Destino:          {resultado['destino']}
IP resuelta:      {resultado['ip']}
Estado:           {estado}

PAQUETES
────────────────────────────────────

Enviados:         {resultado['enviados']}
Recibidos:        {resultado['recibidos']}
Perdidos:         {resultado['perdidos']}
Pérdida:          {resultado['perdida']} %

LATENCIA
────────────────────────────────────

Mínima:           {minimo}
Máxima:           {maximo}
Promedio:         {promedio}
"""

            self.resultado.delete(
                "1.0",
                "end"
            )

            self.resultado.insert(
                "1.0",
                texto
            )

        except ValueError as error:

            self.resultado.delete(
                "1.0",
                "end"
            )

            self.resultado.insert(
                "1.0",
                f"⚠ {error}"
            )