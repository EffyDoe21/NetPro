import customtkinter as ctk

from data.lesson import (
    get_courses,
    get_learning_stats,
)


class LearnFrame(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        # ====================================================
        # COLORES NETPRO
        # ====================================================

        self.COLOR_FONDO = "#2B2B2B"
        self.COLOR_PANEL = "#1A1A1A"
        self.COLOR_PANEL_SECUNDARIO = "#242424"

        self.COLOR_AZUL = "#3B8ED0"
        self.COLOR_AZUL_HOVER = "#36719F"

        self.COLOR_VERDE = "#2ECC71"
        self.COLOR_ROJO = "#E74C3C"
        self.COLOR_AMARILLO = "#F1C40F"

        self.COLOR_TEXTO = "#FFFFFF"
        self.COLOR_SECUNDARIO = "#FFFFFF"

        # ====================================================
        # ESTADO
        # ====================================================

        self.curso_actual = None
        self.leccion_actual = None

        # Posteriormente estos datos se guardaran
        # en un archivo JSON.

        self.lecciones_completadas = set()

        # ====================================================
        # GRID PRINCIPAL
        # ====================================================

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

        # ====================================================
        # ENCABEZADO
        # ====================================================

        self.encabezado = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.encabezado.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(20, 5)
        )

        self.encabezado.grid_columnconfigure(
            0,
            weight=1
        )

        self.titulo_principal = ctk.CTkLabel(
            self.encabezado,
            text="🎓 Aprendizaje",
            font=("Arial", 28, "bold"),
            text_color=self.COLOR_AZUL
        )

        self.titulo_principal.grid(
            row=0,
            column=0,
            pady=(0, 4)
        )

        self.subtitulo_principal = ctk.CTkLabel(
            self.encabezado,
            text=(
                "Aprende redes y ciberseguridad "
                "paso a paso."
            ),
            font=("Arial", 13),
            text_color=self.COLOR_TEXTO
        )

        self.subtitulo_principal.grid(
            row=1,
            column=0
        )

        # ====================================================
        # CONTENEDOR DE PAGINAS
        # ====================================================

        self.contenedor = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.contenedor.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(10, 20)
        )

        self.contenedor.grid_columnconfigure(
            0,
            weight=1
        )

        self.contenedor.grid_rowconfigure(
            0,
            weight=1
        )

        # ====================================================
        # MOSTRAR INICIO
        # ====================================================

        self.mostrar_inicio()

    # ========================================================
    # LIMPIAR CONTENEDOR
    # ========================================================

    def limpiar_contenedor(self):

        for widget in self.contenedor.winfo_children():

            widget.destroy()

    # ========================================================
    # MOSTRAR INICIO
    # ========================================================

    def mostrar_inicio(self):

        self.curso_actual = None
        self.leccion_actual = None

        self.limpiar_contenedor()

        self.titulo_principal.configure(
            text="🎓 Aprendizaje"
        )

        self.subtitulo_principal.configure(
            text=(
                "Aprende redes y ciberseguridad "
                "paso a paso."
            )
        )

        # ====================================================
        # SCROLL PRINCIPAL
        # ====================================================

        scroll = ctk.CTkScrollableFrame(
            self.contenedor,
            fg_color="transparent"
        )

        scroll.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scroll.grid_columnconfigure(
            0,
            weight=1
        )

        scroll.grid_columnconfigure(
            1,
            weight=1
        )

        # ====================================================
        # RESUMEN GENERAL
        # ====================================================

        stats = get_learning_stats()

        resumen = ctk.CTkFrame(
            scroll,
            fg_color=self.COLOR_PANEL,
            corner_radius=8
        )

        resumen.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=(0, 15)
        )

        for columna in range(3):

            resumen.grid_columnconfigure(
                columna,
                weight=1
            )

        self.crear_estadistica(
            resumen,
            0,
            "Cursos",
            str(stats["courses"])
        )

        self.crear_estadistica(
            resumen,
            1,
            "Lecciones",
            str(stats["lessons"])
        )

        self.crear_estadistica(
            resumen,
            2,
            "Completadas",
            str(
                len(
                    self.lecciones_completadas
                )
            )
        )

        # ====================================================
        # TITULO CURSOS
        # ====================================================

        ctk.CTkLabel(
            scroll,
            text="Rutas de aprendizaje",
            font=("Arial", 18, "bold"),
            text_color=self.COLOR_TEXTO,
            anchor="w"
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="w",
            padx=5,
            pady=(0, 10)
        )

        # ====================================================
        # CURSOS
        # ====================================================

        cursos = get_courses()

        fila = 2
        columna = 0

        for curso in cursos:

            self.crear_tarjeta_curso(
                scroll,
                curso,
                fila,
                columna
            )

            columna += 1

            if columna > 1:

                columna = 0
                fila += 1

    # ========================================================
    # CREAR ESTADISTICA
    # ========================================================

    def crear_estadistica(
        self,
        parent,
        columna,
        titulo,
        valor
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        frame.grid(
            row=0,
            column=columna,
            sticky="ew",
            padx=10,
            pady=12
        )

        ctk.CTkLabel(
            frame,
            text=titulo,
            font=("Arial", 10),
            text_color=self.COLOR_SECUNDARIO
        ).pack()

        ctk.CTkLabel(
            frame,
            text=valor,
            font=("Arial", 22, "bold"),
            text_color=self.COLOR_AZUL
        ).pack(
            pady=(2, 0)
        )

    # ========================================================
    # CREAR TARJETA DE CURSO
    # ========================================================

    def crear_tarjeta_curso(
        self,
        parent,
        curso,
        fila,
        columna
    ):

        tarjeta = ctk.CTkFrame(
            parent,
            fg_color=self.COLOR_PANEL,
            corner_radius=8
        )

        tarjeta.grid(
            row=fila,
            column=columna,
            sticky="nsew",
            padx=5,
            pady=5
        )

        tarjeta.grid_columnconfigure(
            0,
            weight=1
        )

        # ====================================================
        # CABECERA
        # ====================================================

        cabecera = ctk.CTkFrame(
            tarjeta,
            fg_color="transparent"
        )

        cabecera.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=18,
            pady=(16, 5)
        )

        cabecera.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            cabecera,
            text=(
                f"{curso['icon']}  "
                f"{curso['title']}"
            ),
            font=("Arial", 17, "bold"),
            text_color=self.COLOR_TEXTO,
            anchor="w"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            cabecera,
            text=curso.get(
                "level",
                ""
            ).upper(),
            font=("Arial", 9, "bold"),
            text_color=self.COLOR_AZUL
        ).grid(
            row=0,
            column=1,
            sticky="e"
        )

        # ====================================================
        # DESCRIPCION
        # ====================================================

        descripcion = ctk.CTkLabel(
            tarjeta,
            text=curso.get(
                "description",
                ""
            ),
            font=("Arial", 11),
            text_color=self.COLOR_SECUNDARIO,
            justify="left",
            anchor="w",
            wraplength=370
        )

        descripcion.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=18,
            pady=(5, 12)
        )

        # ====================================================
        # INFORMACION
        # ====================================================

        total_lecciones = len(
            curso.get(
                "lessons",
                []
            )
        )

        completadas = self.obtener_completadas_curso(
            curso
        )

        info = ctk.CTkFrame(
            tarjeta,
            fg_color="transparent"
        )

        info.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=18
        )

        info.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            info,
            text=(
                f"{total_lecciones} lecciones"
            ),
            font=("Arial", 10),
            text_color=self.COLOR_SECUNDARIO
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            info,
            text=(
                f"{completadas}/"
                f"{total_lecciones}"
            ),
            font=("Arial", 10, "bold"),
            text_color=(
                self.COLOR_VERDE
                if completadas == total_lecciones
                and total_lecciones > 0
                else self.COLOR_AZUL
            )
        ).grid(
            row=0,
            column=1,
            sticky="e"
        )

        # ====================================================
        # PROGRESO
        # ====================================================

        progreso = 0

        if total_lecciones > 0:

            progreso = (
                completadas
                / total_lecciones
            )

        barra = ctk.CTkProgressBar(
            tarjeta,
            height=8,
            progress_color=self.COLOR_AZUL
        )

        barra.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=18,
            pady=(8, 12)
        )

        barra.set(
            progreso
        )

        # ====================================================
        # BOTON
        # ====================================================

        texto_boton = "COMENZAR →"

        if completadas > 0:

            texto_boton = "CONTINUAR →"

        if (
            total_lecciones > 0
            and completadas == total_lecciones
        ):

            texto_boton = "REPASAR →"

        ctk.CTkButton(
            tarjeta,
            text=texto_boton,
            height=34,
            font=("Arial", 11, "bold"),
            fg_color=self.COLOR_AZUL,
            hover_color=self.COLOR_AZUL_HOVER,
            command=lambda c=curso: (
                self.mostrar_curso(c)
            )
        ).grid(
            row=4,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 16)
        )

    # ========================================================
    # OBTENER LECCIONES COMPLETADAS DE UN CURSO
    # ========================================================

    def obtener_completadas_curso(
        self,
        curso
    ):

        total = 0

        for leccion in curso.get(
            "lessons",
            []
        ):

            clave = (
                curso["id"],
                leccion["id"]
            )

            if clave in self.lecciones_completadas:

                total += 1

        return total

    # ========================================================
    # MOSTRAR CURSO
    # ========================================================

    def mostrar_curso(
        self,
        curso
    ):

        self.curso_actual = curso

        self.limpiar_contenedor()

        self.titulo_principal.configure(
            text=(
                f"{curso['icon']} "
                f"{curso['title']}"
            )
        )

        self.subtitulo_principal.configure(
            text=curso.get(
                "description",
                ""
            )
        )

        # ====================================================
        # CONTENIDO
        # ====================================================

        scroll = ctk.CTkScrollableFrame(
            self.contenedor,
            fg_color="transparent"
        )

        scroll.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scroll.grid_columnconfigure(
            0,
            weight=1
        )

        # ====================================================
        # BOTON VOLVER
        # ====================================================

        ctk.CTkButton(
            scroll,
            text="← VOLVER A CURSOS",
            width=160,
            height=32,
            font=("Arial", 10, "bold"),
            fg_color=self.COLOR_PANEL_SECUNDARIO,
            hover_color=self.COLOR_AZUL_HOVER,
            command=self.mostrar_inicio
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=(0, 12)
        )

        # ====================================================
        # INFORMACION DEL CURSO
        # ====================================================

        total = len(
            curso.get(
                "lessons",
                []
            )
        )

        completadas = self.obtener_completadas_curso(
            curso
        )

        panel_progreso = ctk.CTkFrame(
            scroll,
            fg_color=self.COLOR_PANEL,
            corner_radius=8
        )

        panel_progreso.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=5,
            pady=(0, 15)
        )

        panel_progreso.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            panel_progreso,
            text="Progreso del curso",
            font=("Arial", 12, "bold"),
            text_color=self.COLOR_TEXTO
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=18,
            pady=(12, 2)
        )

        ctk.CTkLabel(
            panel_progreso,
            text=(
                f"{completadas} de "
                f"{total} lecciones completadas"
            ),
            font=("Arial", 10),
            text_color=self.COLOR_SECUNDARIO
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=18
        )

        progreso = 0

        if total:

            progreso = (
                completadas / total
            )

        barra = ctk.CTkProgressBar(
            panel_progreso,
            height=8,
            progress_color=self.COLOR_AZUL
        )

        barra.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=18,
            pady=(8, 14)
        )

        barra.set(
            progreso
        )

        # ====================================================
        # TITULO LECCIONES
        # ====================================================

        ctk.CTkLabel(
            scroll,
            text="Lecciones",
            font=("Arial", 18, "bold"),
            text_color=self.COLOR_TEXTO
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=5,
            pady=(0, 8)
        )

        # ====================================================
        # LISTA DE LECCIONES
        # ====================================================

        for indice, leccion in enumerate(
            curso.get(
                "lessons",
                []
            )
        ):

            self.crear_fila_leccion(
                scroll,
                curso,
                leccion,
                indice + 3,
                indice + 1
            )

    # ========================================================
    # CREAR FILA DE LECCION
    # ========================================================

    def crear_fila_leccion(
        self,
        parent,
        curso,
        leccion,
        fila,
        numero
    ):

        completada = (
            curso["id"],
            leccion["id"]
        ) in self.lecciones_completadas

        frame = ctk.CTkFrame(
            parent,
            fg_color=self.COLOR_PANEL,
            corner_radius=8
        )

        frame.grid(
            row=fila,
            column=0,
            sticky="ew",
            padx=5,
            pady=4
        )

        frame.grid_columnconfigure(
            1,
            weight=1
        )

        # Numero

        numero_frame = ctk.CTkFrame(
            frame,
            width=40,
            height=40,
            corner_radius=20,
            fg_color=(
                self.COLOR_VERDE
                if completada
                else self.COLOR_AZUL
            )
        )

        numero_frame.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(15, 12),
            pady=12
        )

        numero_frame.grid_propagate(
            False
        )

        ctk.CTkLabel(
            numero_frame,
            text=(
                "✓"
                if completada
                else str(numero)
            ),
            font=("Arial", 14, "bold"),
            text_color=self.COLOR_TEXTO
        ).place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # Titulo

        ctk.CTkLabel(
            frame,
            text=(
                f"{leccion.get('icon', '📘')}  "
                f"{leccion['title']}"
            ),
            font=("Arial", 14, "bold"),
            text_color=self.COLOR_TEXTO,
            anchor="w"
        ).grid(
            row=0,
            column=1,
            sticky="sw",
            pady=(12, 0)
        )

        # Duracion

        ctk.CTkLabel(
            frame,
            text=leccion.get(
                "duration",
                ""
            ),
            font=("Arial", 10),
            text_color=self.COLOR_SECUNDARIO,
            anchor="w"
        ).grid(
            row=1,
            column=1,
            sticky="nw",
            pady=(2, 12)
        )

        # Boton

        ctk.CTkButton(
            frame,
            text=(
                "REPASAR"
                if completada
                else "ABRIR"
            ),
            width=90,
            height=30,
            font=("Arial", 10, "bold"),
            fg_color=self.COLOR_AZUL,
            hover_color=self.COLOR_AZUL_HOVER,
            command=lambda l=leccion: (
                self.mostrar_leccion(
                    curso,
                    l
                )
            )
        ).grid(
            row=0,
            column=2,
            rowspan=2,
            padx=15,
            pady=12
        )

    # ========================================================
    # MOSTRAR LECCION
    # ========================================================

    def mostrar_leccion(
        self,
        curso,
        leccion
    ):

        self.curso_actual = curso
        self.leccion_actual = leccion

        self.limpiar_contenedor()

        self.titulo_principal.configure(
            text=(
                f"{leccion.get('icon', '📘')} "
                f"{leccion['title']}"
            )
        )

        self.subtitulo_principal.configure(
            text=(
                f"{curso['title']}  •  "
                f"{leccion.get('duration', '')}"
            )
        )

        scroll = ctk.CTkScrollableFrame(
            self.contenedor,
            fg_color="transparent"
        )

        scroll.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scroll.grid_columnconfigure(
            0,
            weight=1
        )

        # ====================================================
        # VOLVER
        # ====================================================

        ctk.CTkButton(
            scroll,
            text="← VOLVER AL CURSO",
            width=160,
            height=32,
            font=("Arial", 10, "bold"),
            fg_color=self.COLOR_PANEL_SECUNDARIO,
            hover_color=self.COLOR_AZUL_HOVER,
            command=lambda: (
                self.mostrar_curso(curso)
            )
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=(0, 12)
        )

        fila = 1

        # ====================================================
        # OBJETIVOS
        # ====================================================

        objetivos = leccion.get(
            "objectives",
            []
        )

        if objetivos:

            panel_objetivos = ctk.CTkFrame(
                scroll,
                fg_color=self.COLOR_PANEL,
                corner_radius=8
            )

            panel_objetivos.grid(
                row=fila,
                column=0,
                sticky="ew",
                padx=5,
                pady=5
            )

            panel_objetivos.grid_columnconfigure(
                0,
                weight=1
            )

            ctk.CTkLabel(
                panel_objetivos,
                text="🎯 Objetivos de aprendizaje",
                font=("Arial", 15, "bold"),
                text_color=self.COLOR_AZUL,
                anchor="w"
            ).grid(
                row=0,
                column=0,
                sticky="w",
                padx=18,
                pady=(15, 8)
            )

            texto_objetivos = "\n".join(
                f"• {objetivo}"
                for objetivo in objetivos
            )

            ctk.CTkLabel(
                panel_objetivos,
                text=texto_objetivos,
                font=("Arial", 11),
                text_color=self.COLOR_TEXTO,
                justify="left",
                anchor="w",
                wraplength=800
            ).grid(
                row=1,
                column=0,
                sticky="ew",
                padx=18,
                pady=(0, 15)
            )

            fila += 1

        # ====================================================
        # CONTENIDO
        # ====================================================

        panel_contenido = ctk.CTkFrame(
            scroll,
            fg_color=self.COLOR_PANEL,
            corner_radius=8
        )

        panel_contenido.grid(
            row=fila,
            column=0,
            sticky="ew",
            padx=5,
            pady=5
        )

        panel_contenido.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            panel_contenido,
            text="📖 Contenido",
            font=("Arial", 15, "bold"),
            text_color=self.COLOR_AZUL,
            anchor="w"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=18,
            pady=(15, 8)
        )

        ctk.CTkLabel(
            panel_contenido,
            text=leccion.get(
                "content",
                ""
            ).strip(),
            font=("Arial", 12),
            text_color=self.COLOR_TEXTO,
            justify="left",
            anchor="w",
            wraplength=850
        ).grid(
            row=1,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 18)
        )

        fila += 1

        # ====================================================
        # CONCEPTOS CLAVE
        # ====================================================

        conceptos = leccion.get(
            "key_concepts",
            []
        )

        if conceptos:

            panel_conceptos = ctk.CTkFrame(
                scroll,
                fg_color=self.COLOR_PANEL_SECUNDARIO,
                corner_radius=8
            )

            panel_conceptos.grid(
                row=fila,
                column=0,
                sticky="ew",
                padx=5,
                pady=5
            )

            panel_conceptos.grid_columnconfigure(
                0,
                weight=1
            )

            ctk.CTkLabel(
                panel_conceptos,
                text="💡 Conceptos clave",
                font=("Arial", 15, "bold"),
                text_color=self.COLOR_AZUL,
                anchor="w"
            ).grid(
                row=0,
                column=0,
                sticky="w",
                padx=18,
                pady=(15, 8)
            )

            for indice, concepto in enumerate(
                conceptos
            ):

                texto = (
                    f"{concepto['term']}\n"
                    f"{concepto['definition']}"
                )

                ctk.CTkLabel(
                    panel_conceptos,
                    text=texto,
                    font=("Arial", 11),
                    text_color=self.COLOR_TEXTO,
                    justify="left",
                    anchor="w",
                    wraplength=820
                ).grid(
                    row=indice + 1,
                    column=0,
                    sticky="ew",
                    padx=18,
                    pady=(2, 10)
                )

            fila += 1

        # ====================================================
        # EJEMPLO
        # ====================================================

        ejemplo = leccion.get(
            "example"
        )

        if ejemplo:

            panel_ejemplo = ctk.CTkFrame(
                scroll,
                fg_color=self.COLOR_PANEL,
                corner_radius=8
            )

            panel_ejemplo.grid(
                row=fila,
                column=0,
                sticky="ew",
                padx=5,
                pady=5
            )

            panel_ejemplo.grid_columnconfigure(
                0,
                weight=1
            )

            ctk.CTkLabel(
                panel_ejemplo,
                text="🧪 Ejemplo",
                font=("Arial", 15, "bold"),
                text_color=self.COLOR_AZUL,
                anchor="w"
            ).grid(
                row=0,
                column=0,
                sticky="w",
                padx=18,
                pady=(15, 8)
            )

            ctk.CTkLabel(
                panel_ejemplo,
                text=ejemplo.strip(),
                font=("Consolas", 11),
                text_color=self.COLOR_TEXTO,
                justify="left",
                anchor="w",
                wraplength=820
            ).grid(
                row=1,
                column=0,
                sticky="ew",
                padx=18,
                pady=(0, 15)
            )

            fila += 1

        # ====================================================
        # CONSEJO
        # ====================================================

        consejo = leccion.get(
            "tip"
        )

        if consejo:

            panel_tip = ctk.CTkFrame(
                scroll,
                fg_color=self.COLOR_PANEL_SECUNDARIO,
                corner_radius=8
            )

            panel_tip.grid(
                row=fila,
                column=0,
                sticky="ew",
                padx=5,
                pady=5
            )

            ctk.CTkLabel(
                panel_tip,
                text=(
                    f"💡 Consejo\n\n"
                    f"{consejo}"
                ),
                font=("Arial", 11),
                text_color=self.COLOR_TEXTO,
                justify="left",
                anchor="w",
                wraplength=820
            ).pack(
                fill="x",
                padx=18,
                pady=15
            )

            fila += 1

        # ====================================================
        # ADVERTENCIA
        # ====================================================

        advertencia = leccion.get(
            "warning"
        )

        if advertencia:

            panel_warning = ctk.CTkFrame(
                scroll,
                fg_color=self.COLOR_PANEL_SECUNDARIO,
                corner_radius=8
            )

            panel_warning.grid(
                row=fila,
                column=0,
                sticky="ew",
                padx=5,
                pady=5
            )

            ctk.CTkLabel(
                panel_warning,
                text=(
                    f"⚠ Uso responsable\n\n"
                    f"{advertencia}"
                ),
                font=("Arial", 11),
                text_color=self.COLOR_AMARILLO,
                justify="left",
                anchor="w",
                wraplength=820
            ).pack(
                fill="x",
                padx=18,
                pady=15
            )

            fila += 1

        # ====================================================
        # BOTON COMPLETAR
        # ====================================================

        clave = (
            curso["id"],
            leccion["id"]
        )

        completada = (
            clave
            in self.lecciones_completadas
        )

        self.btn_completar = ctk.CTkButton(
            scroll,
            text=(
                "✓ LECCION COMPLETADA"
                if completada
                else "✓ MARCAR COMO COMPLETADA"
            ),
            height=38,
            font=("Arial", 11, "bold"),
            fg_color=(
                self.COLOR_VERDE
                if completada
                else self.COLOR_AZUL
            ),
            hover_color=self.COLOR_AZUL_HOVER,
            command=lambda: (
                self.marcar_completada(
                    curso,
                    leccion
                )
            )
        )

        self.btn_completar.grid(
            row=fila,
            column=0,
            sticky="ew",
            padx=5,
            pady=(15, 5)
        )

    # ========================================================
    # MARCAR LECCION COMPLETADA
    # ========================================================

    def marcar_completada(
        self,
        curso,
        leccion
    ):

        clave = (
            curso["id"],
            leccion["id"]
        )

        self.lecciones_completadas.add(
            clave
        )

        self.btn_completar.configure(
            text="✓ LECCION COMPLETADA",
            fg_color=self.COLOR_VERDE
        )