import os
import threading
import cv2
import customtkinter as ctk
from PIL import Image


class HomeFrame(ctk.CTkFrame):
    BG = '#2B2B2B'
    PANEL = '#1A1A1A'
    CARD = '#1A1A1A'
    BORDER = '#414141'
    BLUE = '#3B8ED0'
    CYAN = '#4CBFFF'
    WHITE = '#F4F4F4'
    MUTED = '#A8A8A8'

    def __init__(self, parent):
        super().__init__(parent, fg_color=self.BG, corner_radius=0)
        self.video = None
        self.video_job = None
        self.video_image = None
        self.video_running = False
        self.frame_delay = 33
        self._network_after = None
        self._network_busy = False
        self._network_result = None
        self._closing = False
        self.build_interface()
        self.after(100, self.start_video)

    def build_interface(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=25, pady=(20, 14))
        ctk.CTkLabel(header, text="🏠  Bienvenido a NetPro",
                     font=("Arial", 26, "bold"), text_color=self.BLUE).pack(anchor="w")
        ctk.CTkLabel(header, text="Tu centro de información y actividad de red",
                     font=("Arial", 12), text_color=self.MUTED).pack(anchor="w", pady=(3, 0))

        # Bienvenida: el video original dispone de más espacio horizontal y vertical.
        hero = ctk.CTkFrame(self, fg_color=self.PANEL, corner_radius=12,
                            border_width=1, border_color=self.BORDER, height=260)
        hero.grid(row=1, column=0, sticky="ew", padx=25, pady=(0, 20))
        hero.grid_propagate(False)
        hero.grid_columnconfigure(0, weight=2)
        hero.grid_columnconfigure(1, weight=3)
        hero.grid_rowconfigure(0, weight=1)

        intro = ctk.CTkFrame(hero, fg_color="transparent")
        intro.grid(row=0, column=0, sticky="nsew", padx=(28, 8), pady=28)
        intro.grid_rowconfigure(0, weight=1)
        intro.grid_rowconfigure(4, weight=1)
        ctk.CTkLabel(intro, text="NETWORK INTELLIGENCE",
                     font=("Arial", 12, "bold"), text_color=self.BLUE).grid(
                         row=1, column=0, sticky="w", pady=(0, 15))
        ctk.CTkLabel(intro, text="Explora más allá\nde la red.",
                     font=("Arial", 32, "bold"), text_color=self.WHITE,
                     justify="left").grid(row=2, column=0, sticky="w")
        ctk.CTkLabel(intro, text="Conoce tu entorno digital en un solo lugar.",
                     font=("Arial", 12), text_color=self.MUTED,
                     wraplength=330, justify="left").grid(
                         row=3, column=0, sticky="w", pady=(15, 0))

        self.video_panel = ctk.CTkFrame(hero, fg_color=self.PANEL)
        self.video_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 20), pady=16)
        self.video_label = ctk.CTkLabel(self.video_panel, text="", fg_color=self.PANEL)
        self.video_label.pack(fill="both", expand=True)

        ctk.CTkLabel(self, text="ESTADO DE TU ENTORNO",
                     font=("Arial", 12, "bold"), text_color=self.BLUE).grid(
                         row=2, column=0, sticky="w", padx=27, pady=(0, 12))

        # Cuatro tarjetas en dos filas, con altura suficiente para los datos.
        metrics = ctk.CTkFrame(self, fg_color="transparent")
        metrics.grid(row=3, column=0, sticky="ew", padx=25, pady=(0, 18))
        for col in range(2):
            metrics.grid_columnconfigure(col, weight=1, uniform="metric")
        metrics.grid_rowconfigure(0, minsize=167)
        metrics.grid_rowconfigure(1, minsize=155)
        self.ethernet_value, self.ethernet_dot = self._network_metric(metrics, 0, "ETHERNET", row=0)
        self.wifi_value, self.wifi_dot = self._network_metric(metrics, 1, "WI-FI", row=0)
        self.ip_value = self._metric(metrics, 0, "IP LOCAL", "Consultando...", row=1)
        self.system_value = self._metric(metrics, 1, "SISTEMA", self._system_name(), row=1)

        lower = ctk.CTkFrame(self, fg_color="transparent")
        lower.grid(row=5, column=0, sticky="nsew", padx=25, pady=(0, 22))
        lower.grid_columnconfigure(0, weight=1, uniform="bottom")
        lower.grid_columnconfigure(1, weight=1, uniform="bottom")
        lower.grid_rowconfigure(0, weight=1)
        self._info_card(lower, 0, "◷  Actividad reciente",
                        "Consulta los análisis y registros guardados en NetPro.",
                        "VER HISTORIAL  →", "show_history")
        self._info_card(lower, 1, "🎓  Aprende con NetPro",
                        "IPv6 utiliza direcciones de 128 bits; IPv4 utiliza 32 bits.",
                        "IR A APRENDIZAJE  →", "show_learning")
        self._network_after = self.after(200, self._load_network)

    def _metric(self, parent, column, title, value, row=0):
        card = ctk.CTkFrame(parent, fg_color=self.CARD, border_width=1,
                            border_color=self.BORDER, corner_radius=10, height=105)
        card.grid(row=row, column=column, sticky="nsew",
                  padx=(0, 6) if column == 0 else (6, 0),
                  pady=(0, 12) if row == 0 else (0, 0))
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(0, weight=1)
        card.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(card, text=title, text_color=self.BLUE,
                     font=("Arial", 12, "bold"), anchor="w").grid(
                         row=1, column=0, sticky="w", padx=22, pady=(0, 10))
        label = ctk.CTkLabel(card, text=value, text_color=self.WHITE,
                             font=("Arial", 14, "bold"), anchor="w")
        label.grid(row=2, column=0, sticky="nw", padx=22, pady=(0, 0))
        return label

    def _network_metric(self, parent, column, title, row=0):
        card = ctk.CTkFrame(parent, fg_color=self.CARD, border_width=1,
                            border_color=self.BORDER, corner_radius=10, height=155)
        card.grid(row=row, column=column, sticky="nsew",
                  padx=(0, 6) if column == 0 else (6, 0),
                  pady=(0, 12) if row == 0 else (0, 0))
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(0, weight=1)
        card.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(card, text=title, text_color=self.BLUE,
                     font=("Arial", 12, "bold"), anchor="w").grid(
                         row=1, column=0, sticky="w", padx=22, pady=(0, 10))
        line = ctk.CTkFrame(card, fg_color="transparent")
        line.grid(row=2, column=0, sticky="new", padx=19)
        dot = ctk.CTkLabel(line, text="●", width=20, font=("Arial", 15),
                           text_color="#7F8C8D")
        dot.pack(side="left")
        value = ctk.CTkLabel(line, text="Consultando...", text_color=self.MUTED,
                             font=("Arial", 12), anchor="w", justify="left")
        value.pack(side="left", fill="x", expand=True, padx=(4, 0))
        return value, dot

    def _info_card(self, parent, column, title, description, link, method):
        card = ctk.CTkFrame(parent, fg_color=self.CARD, border_width=1,
                            border_color=self.BORDER, corner_radius=10, height=145)
        card.grid(row=0, column=column, sticky="nsew",
                  padx=(0, 6) if column == 0 else (6, 0))
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(0, weight=1)
        card.grid_rowconfigure(4, weight=1)
        ctk.CTkLabel(card, text=title, font=("Arial", 15, "bold"),
                     text_color=self.WHITE, anchor="w").grid(
                         row=1, column=0, sticky="w", padx=22, pady=(0, 14))
        ctk.CTkLabel(card, text=description, font=("Arial", 12),
                     text_color=self.MUTED, anchor="w", justify="left",
                     wraplength=400).grid(row=2, column=0, sticky="w", padx=22)
        ctk.CTkButton(card, text=link, fg_color="transparent",
                      hover_color="#282828", text_color=self.BLUE,
                      anchor="w", width=185, height=32,
                      font=("Arial", 11, "bold"),
                      command=lambda: getattr(self.winfo_toplevel(), method)()).grid(
                          row=3, column=0, sticky="w", padx=14, pady=(18, 0))

    @staticmethod
    def _system_name():
        import platform
        return platform.system() + " " + platform.release()

    def _load_network(self):
        self._network_after = None
        if self._closing or self._network_busy:
            return
        self._network_busy = True

        def worker():
            import socket
            result = {}
            ip = "No disponible"
            try:
                from core.network_status import obtener_estado_red
                result = obtener_estado_red() or {}
            except Exception:
                result = {}
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                    sock.connect(("192.0.2.1", 80))
                    ip = sock.getsockname()[0]
            except OSError:
                try:
                    ip = socket.gethostbyname(socket.gethostname())
                except OSError:
                    pass
            # No se manipulan widgets Tk desde el hilo secundario.
            self._network_result = (result, ip)

        threading.Thread(target=worker, daemon=True).start()
        self._network_after = self.after(250, self._poll_network)

    def _poll_network(self):
        self._network_after = None
        if self._closing or not self.winfo_exists():
            return
        data = self._network_result
        if data is None:
            self._network_after = self.after(250, self._poll_network)
            return
        self._network_result = None
        self._network_busy = False
        result, ip = data
        self._set_adapter(self.ethernet_value, self.ethernet_dot,
                          result.get("ethernet", {}), "ethernet")
        self._set_adapter(self.wifi_value, self.wifi_dot,
                          result.get("wifi", {}), "wifi")
        self.ip_value.configure(text=ip)
        self._network_after = self.after(10000, self._load_network)

    def _set_adapter(self, label, dot, info, kind):
        if info.get("error"):
            color, text = "#7F8C8D", "Error de consulta"
        elif not info.get("detectado"):
            color, text = "#7F8C8D", "Sin adaptador"
        elif info.get("conectado"):
            color = "#2ECC71"
            speed = info.get("velocidad")
            ssid = info.get("ssid") if kind == "wifi" else None
            parts = ["Conectado"]
            if ssid:
                parts.append(str(ssid))
            if speed:
                parts.append(str(speed))
            text = " · ".join(parts)
        else:
            color, text = "#E74C3C", "Desconectado"
        dot.configure(text_color=color)
        label.configure(text=text, text_color=color)

    def start_video(self):
        if not self.winfo_exists():
            return
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        video_path = os.path.join(base_dir, 'assets', 'computacion_datos.mp4')
        if not os.path.isfile(video_path):
            self.video_label.configure(text='Video no encontrado:\nassets/computacion_datos.mp4')
            return
        self.video = cv2.VideoCapture(video_path)
        if not self.video.isOpened():
            self.video_label.configure(text='No se pudo abrir el video.')
            self.video.release()
            self.video = None
            return
        fps = self.video.get(cv2.CAP_PROP_FPS)
        if not 0 < fps <= 120:
            fps = 30
        self.frame_delay = max(15, int(1000 / fps))
        self.video_running = True
        self.update_video()

    def update_video(self):
        self.video_job = None
        if not self.video_running or not self.winfo_exists() or self.video is None:
            return
        success, frame = self.video.read()
        if not success:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, frame = self.video.read()
        if success:
            panel_w = self.video_panel.winfo_width()
            panel_h = self.video_panel.winfo_height()
            if panel_w > 10 and panel_h > 10:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w = frame.shape[:2]
                ratio = min(panel_w / w, panel_h / h)
                new_w, new_h = max(1, int(w * ratio)), max(1, int(h * ratio))
                frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
                image = Image.fromarray(frame)
                self.video_image = ctk.CTkImage(light_image=image, dark_image=image,
                                                size=(new_w, new_h))
                self.video_label.configure(image=self.video_image, text='')
        self.video_job = self.after(self.frame_delay, self.update_video)

    def destroy(self):
        self._closing = True
        if self._network_after is not None:
            try:
                self.after_cancel(self._network_after)
            except Exception:
                pass
            self._network_after = None
        self.video_running = False
        if self.video_job is not None:
            try:
                self.after_cancel(self.video_job)
            except (ValueError, Exception):
                pass
            self.video_job = None
        if self.video is not None:
            self.video.release()
            self.video = None
        super().destroy()
