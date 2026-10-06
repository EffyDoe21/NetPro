import json
import urllib.request
import urllib.error
import socket


# ============================================================
# CONFIGURACIÓN DE OLLAMA / NETPRO AI
# ============================================================

OLLAMA_URL = "http://localhost:11434"
MODELO_PREDETERMINADO = "netpro-ai"

TIMEOUT_ESTADO = 3
TIMEOUT_CONEXION = 60


# ============================================================
# EXCEPCIONES
# ============================================================

class OllamaError(Exception):
    """Error general relacionado con NetPro AI."""
    pass


class OllamaNoDisponibleError(OllamaError):
    """Ollama no está ejecutándose o no responde."""
    pass


class ModeloNoDisponibleError(OllamaError):
    """El modelo solicitado no está instalado."""
    pass


# ============================================================
# PETICIÓN HTTP A OLLAMA
# ============================================================

def _peticion_json(
    endpoint,
    metodo="GET",
    datos=None,
    timeout=TIMEOUT_CONEXION
):
    """
    Realiza una petición JSON a la API local de Ollama.
    """

    url = f"{OLLAMA_URL}{endpoint}"

    cuerpo = None

    headers = {
        "Content-Type": "application/json"
    }

    if datos is not None:
        cuerpo = json.dumps(
            datos,
            ensure_ascii=False
        ).encode("utf-8")

    request = urllib.request.Request(
        url=url,
        data=cuerpo,
        headers=headers,
        method=metodo
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=timeout
        ) as respuesta:

            contenido = respuesta.read()

            if not contenido:
                return {}

            return json.loads(
                contenido.decode("utf-8")
            )

    except urllib.error.HTTPError as error:

        try:
            detalle = error.read().decode(
                "utf-8",
                errors="replace"
            )

        except Exception:
            detalle = str(error)

        raise OllamaError(
            f"Ollama respondió con HTTP {error.code}: "
            f"{detalle}"
        ) from error

    except (
        urllib.error.URLError,
        ConnectionRefusedError,
        socket.timeout,
        TimeoutError
    ) as error:

        raise OllamaNoDisponibleError(
            "No fue posible conectar con NetPro AI. "
            "Comprueba que Ollama esté ejecutándose."
        ) from error

    except json.JSONDecodeError as error:

        raise OllamaError(
            "Ollama devolvió una respuesta que NetPro "
            "no pudo interpretar."
        ) from error


# ============================================================
# ESTADO DE OLLAMA
# ============================================================

def ollama_disponible():
    """
    Comprueba si el servidor local de Ollama responde.
    """

    try:

        _peticion_json(
            "/api/tags",
            timeout=TIMEOUT_ESTADO
        )

        return True

    except OllamaError:

        return False


# ============================================================
# MODELOS INSTALADOS
# ============================================================

def obtener_modelos():
    """
    Obtiene la lista de modelos instalados en Ollama.
    """

    respuesta = _peticion_json(
        "/api/tags",
        timeout=5
    )

    modelos = []

    for modelo in respuesta.get("models", []):

        nombre = modelo.get(
            "name",
            ""
        ).strip()

        if nombre:
            modelos.append(nombre)

    return modelos


def modelo_disponible(
    modelo=MODELO_PREDETERMINADO
):
    """
    Comprueba si el modelo indicado está instalado.

    Reconoce tanto:

        netpro-ai

    como:

        netpro-ai:latest
    """

    modelo_base = modelo.split(":")[0]

    for instalado in obtener_modelos():

        instalado_base = instalado.split(":")[0]

        if (
            instalado == modelo
            or instalado_base == modelo_base
        ):
            return True

    return False


# ============================================================
# GENERAR RESPUESTA CON NETPRO AI
# ============================================================

def generar_respuesta(
    mensaje,
    modelo=MODELO_PREDETERMINADO
):
    """
    Envía una consulta al modelo local NetPro AI.

    El modelo personalizado 'netpro-ai' ya contiene
    las instrucciones SYSTEM definidas en el Modelfile.
    """

    if not isinstance(
        mensaje,
        str
    ):
        raise ValueError(
            "El mensaje enviado a NetPro AI debe ser texto."
        )

    mensaje = mensaje.strip()

    if not mensaje:
        raise ValueError(
            "El mensaje enviado a NetPro AI está vacío."
        )

    # --------------------------------------------------------
    # Verificar Ollama
    # --------------------------------------------------------

    if not ollama_disponible():

        raise OllamaNoDisponibleError(
            "Ollama no está disponible."
        )

    # --------------------------------------------------------
    # Verificar modelo
    # --------------------------------------------------------

    if not modelo_disponible(modelo):

        raise ModeloNoDisponibleError(
            f"El modelo '{modelo}' no está instalado. "
            f"Ejecuta: "
            f"ollama create {modelo} -f Modelfile"
        )

    # --------------------------------------------------------
    # Datos enviados a /api/chat
    # --------------------------------------------------------

    datos = {

        "model": modelo,

        "stream": False,

        "messages": [
            {
                "role": "user",
                "content": mensaje
            }
        ]
    }

    # --------------------------------------------------------
    # Consulta
    # --------------------------------------------------------

    respuesta = _peticion_json(
        "/api/chat",
        metodo="POST",
        datos=datos,
        timeout=TIMEOUT_CONEXION
    )

    mensaje_respuesta = respuesta.get(
        "message",
        {}
    )

    contenido = mensaje_respuesta.get(
        "content",
        ""
    )

    if not isinstance(
        contenido,
        str
    ):
        contenido = str(contenido)

    contenido = contenido.strip()

    if not contenido:

        raise OllamaError(
            "NetPro AI no devolvió contenido."
        )

    return contenido


# ============================================================
# EXPLICACIÓN EDUCATIVA DE UN SERVICIO
# ============================================================

def explicar_servicio_con_ia(
    puerto,
    protocolo,
    servicio
):
    """
    Solicita a Ollama únicamente una explicación educativa.

    IMPORTANTE:

    La IA NO determina:
    - estado del puerto
    - vulnerabilidades
    - seguridad
    - servicio confirmado

    Solamente explica el uso habitual del puerto/servicio.
    """

    mensaje = f"""
NetPro proporciona la siguiente asociación educativa:

Puerto: {puerto}
Protocolo: {protocolo}
Servicio habitual asociado: {servicio}

Explica únicamente para qué se utiliza habitualmente
este puerto y el servicio asociado.

REGLAS:

- Responde solamente en español.
- Máximo 60 palabras.
- No determines si el puerto está abierto o cerrado.
- No afirmes que el servicio está realmente ejecutándose.
- No hables de vulnerabilidades.
- No hables de ataques.
- No hables de riesgos.
- No evalúes si el sistema es seguro o inseguro.
- No inventes versiones.
- No inventes configuraciones.
- No inventes resultados.

Explica únicamente el concepto educativo.
""".strip()

    return generar_respuesta(
        mensaje
    )


# ============================================================
# ANÁLISIS IA DE UN PUERTO
# ============================================================

def analizar_puerto_con_ia(resultado):
    """
    Genera una explicación educativa de un resultado
    previamente obtenido por core/ports.py.

    ARQUITECTURA:

    core/ports.py
          |
          v
    RESULTADO REAL
          |
          +-----------> Python
          |              |
          |              + Estado
          |              + IP
          |              + Puerto
          |              + Seguridad
          |
          +-----------> Ollama
                         |
                         + Explicación educativa

    Ollama NO determina los hechos técnicos.
    """

    # ========================================================
    # OBTENER DATOS
    # ========================================================

    host = getattr(
        resultado,
        "host",
        "No disponible"
    )

    ip = getattr(
        resultado,
        "ip",
        "No disponible"
    )

    puerto = getattr(
        resultado,
        "puerto",
        "No disponible"
    )

    protocolo = getattr(
        resultado,
        "protocolo",
        "TCP"
    )

    estado_original = getattr(
        resultado,
        "estado",
        "DESCONOCIDO"
    )

    servicio_original = getattr(
        resultado,
        "servicio",
        "Desconocido"
    )

    descripcion = getattr(
        resultado,
        "descripcion",
        ""
    )

    tiempo_ms = getattr(
        resultado,
        "tiempo_ms",
        None
    )

    # --------------------------------------------------------
    # Normalización
    # --------------------------------------------------------

    estado = str(
        estado_original
    ).strip().upper()

    servicio_nombre = str(
        servicio_original
    ).strip()

    if not servicio_nombre:
        servicio_nombre = "Desconocido"

    # --------------------------------------------------------
    # Tiempo
    # --------------------------------------------------------

    if tiempo_ms is not None:

        try:

            tiempo = (
                f"{float(tiempo_ms):.1f} ms"
            )

        except (
            TypeError,
            ValueError
        ):

            tiempo = str(
                tiempo_ms
            )

    else:

        tiempo = "No disponible"

    # ========================================================
    # INTERPRETACIÓN CONTROLADA POR PYTHON
    # ========================================================

    if estado == "ABIERTO":

        interpretacion = (
            f"NetPro pudo establecer una conexión "
            f"{protocolo} con el puerto {puerto} "
            f"de {ip} durante la comprobación."
        )

    elif estado == "CERRADO":

        interpretacion = (
            f"El puerto {puerto} de {ip} no estaba "
            f"aceptando conexiones {protocolo} durante "
            f"esta comprobación."
        )

    elif estado == "SIN RESPUESTA":

        interpretacion = (
            f"NetPro no obtuvo una respuesta suficiente "
            f"del puerto {puerto} de {ip} dentro del "
            f"tiempo establecido."
        )

    elif estado == "ERROR":

        interpretacion = (
            f"NetPro encontró un error durante la "
            f"comprobación del puerto {puerto} "
            f"de {ip}."
        )

    else:

        interpretacion = (
            f"NetPro obtuvo el estado "
            f"'{estado_original}' para el puerto "
            f"{puerto} de {ip}."
        )

    # ========================================================
    # SERVICIO HABITUAL CONTROLADO POR PYTHON
    # ========================================================

    servicios_desconocidos = {
        "",
        "desconocido",
        "unknown",
        "no disponible",
        "n/a",
        "none"
    }

    servicio_es_conocido = (
        servicio_nombre.lower()
        not in servicios_desconocidos
    )

    if servicio_es_conocido:

        servicio_texto = (
            f"El puerto {puerto} se asocia habitualmente "
            f"con {servicio_nombre}. "
            f"Esta asociación no confirma que "
            f"{servicio_nombre} sea el servicio realmente "
            f"ejecutado por el objetivo."
        )

    else:

        servicio_texto = (
            f"NetPro no dispone de una asociación habitual "
            f"conocida para el puerto {puerto}. "
            f"El número de puerto por sí solo no permite "
            f"identificar qué servicio se está ejecutando."
        )

    # ========================================================
    # SEGURIDAD CONTROLADA POR PYTHON
    # ========================================================

    seguridad = (
        "El estado de este puerto, por sí solo, no permite "
        "determinar la existencia ni la ausencia de "
        "vulnerabilidades. Tampoco permite determinar si "
        "el sistema es seguro o inseguro. Para establecer "
        "esas conclusiones serían necesarias comprobaciones "
        "adicionales."
    )

    # ========================================================
    # EXPLICACIÓN EDUCATIVA MEDIANTE OLLAMA
    # ========================================================

    if servicio_es_conocido:

        try:

            explicacion_ia = explicar_servicio_con_ia(
                puerto=puerto,
                protocolo=protocolo,
                servicio=servicio_nombre
            )

        except OllamaError:

            explicacion_ia = (
                "NetPro AI no está disponible en este "
                "momento. Los resultados técnicos del "
                "análisis continúan siendo válidos."
            )

    else:

        explicacion_ia = (
            "No existe suficiente información para generar "
            "una explicación específica del servicio. "
            "Sería necesaria una identificación adicional."
        )

    # ========================================================
    # SIGUIENTE PASO CONTROLADO POR PYTHON
    # ========================================================

    siguiente_paso = (
        "No se requiere una comprobación adicional "
        "específica únicamente a partir de este resultado."
    )

    # --------------------------------------------------------
    # Recomendaciones internas de NetPro
    # --------------------------------------------------------

    try:

        puerto_num = int(
            puerto
        )

    except (
        TypeError,
        ValueError
    ):

        puerto_num = None

    # HTTP / HTTPS
    if puerto_num in {
        80,
        443,
        8000,
        8080,
        8443
    }:

        siguiente_paso = (
            "Si el objetivo es propio o está autorizado, "
            "puedes continuar con el módulo HTTP/HTTPS "
            "de NetPro para obtener información adicional "
            "del servicio web."
        )

    # DNS
    elif puerto_num == 53:

        siguiente_paso = (
            "Puedes continuar con el módulo DNS de NetPro "
            "para realizar comprobaciones relacionadas "
            "con resolución de nombres."
        )

    # SSH
    elif puerto_num == 22:

        siguiente_paso = (
            "Puedes consultar el módulo Aprendizaje de "
            "NetPro para estudiar el funcionamiento de SSH "
            "y la administración remota segura."
        )

    # RDP
    elif puerto_num == 3389:

        siguiente_paso = (
            "Puedes consultar el módulo Aprendizaje de "
            "NetPro para estudiar el funcionamiento de "
            "los servicios de escritorio remoto."
        )

    # ========================================================
    # DESCRIPCIÓN LOCAL
    # ========================================================

    descripcion_texto = ""

    if descripcion:

        descripcion_texto = (
            "\n\nDESCRIPCIÓN LOCAL\n\n"
            f"{descripcion}"
        )

    # ========================================================
    # RESPUESTA FINAL
    # ========================================================

    resultado_final = f"""
INTERPRETACIÓN

{interpretacion}

SERVICIO HABITUAL

{servicio_texto}

EXPLICACIÓN EDUCATIVA - NETPRO AI

{explicacion_ia}

SEGURIDAD

{seguridad}

SIGUIENTE PASO

{siguiente_paso}

DATOS DEL ANÁLISIS

Objetivo: {host}
Dirección IP: {ip}
Puerto: {puerto}/{protocolo}
Estado: {estado_original}
Tiempo de respuesta: {tiempo}{descripcion_texto}
""".strip()

    return resultado_final


# ============================================================
# ANÁLISIS DE VARIOS PUERTOS
# ============================================================

def analizar_resultados_con_ia(
    resultados
):
    """
    Genera un resumen de varios resultados de puertos.

    Los conteos son realizados por Python.
    Ollama únicamente explica conceptos educativos.
    """

    if not resultados:

        raise ValueError(
            "No existen resultados para analizar."
        )

    # ========================================================
    # CLASIFICACIÓN REALIZADA POR PYTHON
    # ========================================================

    abiertos = []

    cerrados = []

    sin_respuesta = []

    errores = []

    otros = []

    for resultado in resultados:

        estado = str(
            getattr(
                resultado,
                "estado",
                ""
            )
        ).strip().upper()

        if estado == "ABIERTO":
            abiertos.append(resultado)

        elif estado == "CERRADO":
            cerrados.append(resultado)

        elif estado == "SIN RESPUESTA":
            sin_respuesta.append(resultado)

        elif estado == "ERROR":
            errores.append(resultado)

        else:
            otros.append(resultado)

    # ========================================================
    # LISTADO DE PUERTOS ABIERTOS
    # ========================================================

    if abiertos:

        lineas_abiertos = []

        for resultado in abiertos:

            puerto = getattr(
                resultado,
                "puerto",
                "?"
            )

            protocolo = getattr(
                resultado,
                "protocolo",
                "TCP"
            )

            servicio = getattr(
                resultado,
                "servicio",
                "Desconocido"
            )

            lineas_abiertos.append(
                (
                    f"- {puerto}/{protocolo} | "
                    f"Servicio habitual asociado: "
                    f"{servicio}"
                )
            )

        texto_abiertos = "\n".join(
            lineas_abiertos
        )

    else:

        texto_abiertos = (
            "No se detectaron puertos abiertos "
            "durante esta comprobación."
        )

    # ========================================================
    # INTERPRETACIÓN CONTROLADA
    # ========================================================

    if abiertos:

        interpretacion = (
            f"NetPro detectó {len(abiertos)} puerto(s) "
            f"que aceptaron conexiones durante la "
            f"comprobación."
        )

    else:

        interpretacion = (
            "NetPro no detectó puertos que aceptaran "
            "conexiones durante esta comprobación."
        )

    # ========================================================
    # SEGURIDAD CONTROLADA
    # ========================================================

    seguridad = (
        "La cantidad de puertos abiertos o cerrados no "
        "determina por sí sola el nivel de seguridad del "
        "objetivo. Un puerto abierto tampoco demuestra "
        "automáticamente la existencia de una "
        "vulnerabilidad."
    )

    # ========================================================
    # EXPLICACIÓN EDUCATIVA CON IA
    # ========================================================

    if abiertos:

        datos_educativos = []

        for resultado in abiertos[:10]:

            puerto = getattr(
                resultado,
                "puerto",
                "?"
            )

            protocolo = getattr(
                resultado,
                "protocolo",
                "TCP"
            )

            servicio = getattr(
                resultado,
                "servicio",
                "Desconocido"
            )

            datos_educativos.append(
                (
                    f"- {puerto}/{protocolo}: "
                    f"{servicio}"
                )
            )

        servicios_texto = "\n".join(
            datos_educativos
        )

        mensaje = f"""
NetPro encontró las siguientes asociaciones educativas
de puertos y servicios:

{servicios_texto}

Explica brevemente para qué se utilizan habitualmente
estos servicios.

REGLAS:

- Español.
- Máximo 100 palabras.
- No determines vulnerabilidades.
- No hables de ataques.
- No afirmes que los servicios estén confirmados.
- No evalúes la seguridad del sistema.
- No cambies los números de puerto.
- No inventes versiones.
""".strip()

        try:

            explicacion_ia = generar_respuesta(
                mensaje
            )

        except OllamaError:

            explicacion_ia = (
                "NetPro AI no está disponible en este "
                "momento."
            )

    else:

        explicacion_ia = (
            "No hay puertos abiertos que requieran una "
            "explicación educativa adicional."
        )

    # ========================================================
    # RESPUESTA FINAL
    # ========================================================

    return f"""
RESUMEN DEL ANÁLISIS

Total analizado: {len(resultados)}
Abiertos: {len(abiertos)}
Cerrados: {len(cerrados)}
Sin respuesta: {len(sin_respuesta)}
Errores: {len(errores)}
Otros estados: {len(otros)}

INTERPRETACIÓN

{interpretacion}

PUERTOS ABIERTOS

{texto_abiertos}

EXPLICACIÓN EDUCATIVA - NETPRO AI

{explicacion_ia}

SEGURIDAD

{seguridad}
""".strip()


# ============================================================
# INFORMACIÓN DE NETPRO AI
# ============================================================

def obtener_estado_ia():
    """
    Devuelve información del estado actual de NetPro AI.

    Esta función podrá utilizarse posteriormente en:
    - Puertos
    - Mi Sistema
    - Configuración
    """

    estado = {

        "ollama": False,

        "modelo": (
            MODELO_PREDETERMINADO
        ),

        "modelo_disponible": False,

        "modelos_instalados": []
    }

    # --------------------------------------------------------
    # Ollama
    # --------------------------------------------------------

    if not ollama_disponible():
        return estado

    estado["ollama"] = True

    # --------------------------------------------------------
    # Modelos
    # --------------------------------------------------------

    try:

        modelos = obtener_modelos()

        estado[
            "modelos_instalados"
        ] = modelos

        estado[
            "modelo_disponible"
        ] = modelo_disponible(
            MODELO_PREDETERMINADO
        )

    except OllamaError:

        pass

    return estado


# ============================================================
# PRUEBA GENERAL
# ============================================================

def probar_netpro_ai():
    """
    Realiza una prueba sencilla de conexión con NetPro AI.
    """

    print("=" * 60)

    print(
        "NETPRO AI - PRUEBA DE OLLAMA"
    )

    print("=" * 60)

    print()

    print(
        f"Modelo configurado: "
        f"{MODELO_PREDETERMINADO}"
    )

    print()

    # --------------------------------------------------------
    # Ollama
    # --------------------------------------------------------

    if not ollama_disponible():

        print(
            "❌ Ollama no está disponible."
        )

        return

    print(
        "✅ Ollama está funcionando."
    )

    print()

    # --------------------------------------------------------
    # Modelos
    # --------------------------------------------------------

    try:

        modelos = obtener_modelos()

        print(
            "Modelos instalados:"
        )

        for modelo in modelos:

            print(
                f"  • {modelo}"
            )

        print()

        # ----------------------------------------------------
        # netpro-ai
        # ----------------------------------------------------

        if not modelo_disponible():

            print(
                "❌ netpro-ai no está disponible."
            )

            print()

            print(
                "Ejecuta:"
            )

            print(
                "ollama create netpro-ai -f Modelfile"
            )

            return

        print(
            "✅ netpro-ai está disponible."
        )

        print()

        # ----------------------------------------------------
        # Prueba educativa
        # ----------------------------------------------------

        print(
            "Probando explicación educativa..."
        )

        print()

        respuesta = explicar_servicio_con_ia(
            puerto=443,
            protocolo="TCP",
            servicio="HTTPS"
        )

        print(
            "Respuesta de NetPro AI:"
        )

        print()

        print(
            respuesta
        )

    except OllamaError as error:

        print(
            f"❌ {error}"
        )


# ============================================================
# EJECUCIÓN DIRECTA
# ============================================================

if __name__ == "__main__":

    probar_netpro_ai()