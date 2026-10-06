from AI.ollama_client import (
    generar_respuesta,
    OllamaError
)


# ============================================================
# NETPRO AI - MÓDULO HTTP / HTTPS
# ============================================================

def analizar_http_con_ia(resultado):
    """
    Interpreta mediante NetPro AI un análisis HTTP/HTTPS
    previamente realizado por core/http_analyzer.py.

    IMPORTANTE:
    Python obtiene los hechos técnicos.
    Ollama únicamente los interpreta.
    """

    if resultado is None:
        raise ValueError(
            "No existe un resultado HTTP/HTTPS para analizar."
        )

    # ========================================================
    # DATOS GENERALES
    # ========================================================

    url_solicitada = getattr(
        resultado,
        "url_solicitada",
        "No disponible"
    )

    url_final = getattr(
        resultado,
        "url_final",
        "No disponible"
    )

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

    protocolo = getattr(
        resultado,
        "protocolo",
        "No disponible"
    )

    codigo = getattr(
        resultado,
        "codigo_estado",
        None
    )

    razon = getattr(
        resultado,
        "razon_estado",
        ""
    )

    tiempo_ms = getattr(
        resultado,
        "tiempo_ms",
        None
    )

    servidor = getattr(
        resultado,
        "servidor",
        "No informado"
    )

    content_type = getattr(
        resultado,
        "content_type",
        "No informado"
    )

    usa_https = bool(
        getattr(
            resultado,
            "usa_https",
            False
        )
    )

    # ========================================================
    # TIEMPO
    # ========================================================

    if tiempo_ms is not None:

        try:
            tiempo = f"{float(tiempo_ms):.2f} ms"

        except (TypeError, ValueError):
            tiempo = str(tiempo_ms)

    else:
        tiempo = "No disponible"

    # ========================================================
    # ESTADO HTTP
    # ========================================================

    if codigo is None:

        estado_http = "No disponible"

    else:

        estado_http = str(codigo)

        if razon:
            estado_http += f" {razon}"

    # ========================================================
    # TLS
    # ========================================================

    certificado_disponible = getattr(
        resultado,
        "certificado_disponible",
        False
    )

    certificado_valido = getattr(
        resultado,
        "certificado_valido",
        None
    )

    certificado_sujeto = getattr(
        resultado,
        "certificado_sujeto",
        "No disponible"
    )

    certificado_emisor = getattr(
        resultado,
        "certificado_emisor",
        "No disponible"
    )

    certificado_desde = getattr(
        resultado,
        "certificado_desde",
        "No disponible"
    )

    certificado_hasta = getattr(
        resultado,
        "certificado_hasta",
        "No disponible"
    )

    dias_restantes = getattr(
        resultado,
        "dias_restantes_certificado",
        None
    )

    if not usa_https:

        estado_tls = (
            "La URL final utiliza HTTP. "
            "No se realizó validación de certificado TLS."
        )

    elif certificado_valido is True:

        estado_tls = (
            "NetPro validó correctamente el certificado "
            "TLS durante esta conexión."
        )

    elif certificado_valido is False:

        estado_tls = (
            "NetPro no pudo validar correctamente el "
            "certificado TLS durante esta conexión."
        )

    else:

        estado_tls = (
            "No pudo determinarse el estado de validación "
            "del certificado TLS."
        )

    # ========================================================
    # HEADERS DE SEGURIDAD
    # ========================================================

    headers_seguridad = getattr(
        resultado,
        "headers_seguridad",
        {}
    )

    presentes = 0
    no_observados = 0

    lineas_headers = []

    for nombre, datos in headers_seguridad.items():

        presente = bool(
            datos.get(
                "presente",
                False
            )
        )

        valor = datos.get(
            "valor"
        )

        if presente:

            presentes += 1

            linea = (
                f"- {nombre}: PRESENTE"
            )

            if valor:

                linea += (
                    f" | Valor observado: {valor}"
                )

        else:

            no_observados += 1

            linea = (
                f"- {nombre}: NO OBSERVADO"
            )

        lineas_headers.append(
            linea
        )

    if lineas_headers:

        texto_headers = "\n".join(
            lineas_headers
        )

    else:

        texto_headers = (
            "No existen resultados de headers "
            "de seguridad."
        )

    # ========================================================
    # REDIRECCIONES
    # ========================================================

    redirecciones = getattr(
        resultado,
        "redirecciones",
        []
    )

    lineas_redirecciones = []

    for redireccion in redirecciones:

        codigo_redireccion = (
            redireccion.get(
                "codigo",
                "?"
            )
        )

        desde = redireccion.get(
            "desde",
            "No disponible"
        )

        hacia = redireccion.get(
            "hacia",
            "No disponible"
        )

        lineas_redirecciones.append(
            f"- {codigo_redireccion}: "
            f"{desde} -> {hacia}"
        )

    if lineas_redirecciones:

        texto_redirecciones = "\n".join(
            lineas_redirecciones
        )

    else:

        texto_redirecciones = (
            "No se registraron redirecciones."
        )

    # ========================================================
    # DATOS TÉCNICOS
    # ========================================================

    datos_tecnicos = f"""
RESULTADOS TÉCNICOS OBTENIDOS POR NETPRO

URL solicitada: {url_solicitada}
URL final: {url_final}
Host: {host}
Dirección IP observada: {ip}
Protocolo final: {protocolo}
Estado HTTP: {estado_http}
Tiempo de respuesta: {tiempo}
Servidor informado: {servidor}
Content-Type: {content_type}

TLS

HTTPS: {"Sí" if usa_https else "No"}
Certificado disponible: {"Sí" if certificado_disponible else "No"}
Validación: {estado_tls}
Sujeto: {certificado_sujeto}
Emisor: {certificado_emisor}
Válido desde: {certificado_desde}
Válido hasta: {certificado_hasta}
Días restantes: {
    dias_restantes
    if dias_restantes is not None
    else "No disponible"
}

HEADERS DE SEGURIDAD

Total revisados: {len(headers_seguridad)}
Presentes: {presentes}
No observados: {no_observados}

{texto_headers}

REDIRECCIONES

{texto_redirecciones}
""".strip()

    # ========================================================
    # PROMPT NETPRO AI
    # ========================================================

    prompt = f"""
Eres NetPro AI, componente educativo de NetPro -
Network & Security Toolkit.

Python ya realizó el análisis HTTP/HTTPS.

Los siguientes datos constituyen la fuente de verdad:

{datos_tecnicos}

Tu única función es interpretar estos resultados.

REGLAS OBLIGATORIAS:

1. Responde únicamente en español.

2. No cambies ningún dato proporcionado por NetPro.

3. No cambies:
   - URL
   - IP
   - protocolo
   - código HTTP
   - tiempos
   - headers
   - certificado
   - redirecciones

4. No inventes:
   - vulnerabilidades
   - CVE
   - versiones
   - software
   - configuraciones
   - ataques
   - resultados

5. Si Server informa un producto, descríbelo únicamente
   como información declarada por la respuesta HTTP.

6. No utilices Server para afirmar qué tecnología existe
   realmente en toda la infraestructura.

7. Si un header figura como NO OBSERVADO, utiliza la
   expresión "no observado".

8. NO OBSERVADO no significa automáticamente ausente en
   toda la aplicación.

9. La ausencia o no observación de un header NO demuestra
   por sí sola una vulnerabilidad.

10. HTTPS NO significa automáticamente que el sitio sea
    completamente seguro.

11. HTTP NO demuestra por sí solo que una aplicación haya
    sido comprometida.

12. Un certificado TLS validado significa que NetPro pudo
    validar el certificado durante esta conexión.

13. Un certificado válido NO demuestra la seguridad completa
    de la aplicación.

14. Un código HTTP 200 significa que la solicitud fue
    procesada satisfactoriamente dentro del contexto HTTP.
    No representa una calificación de seguridad.

15. Un código 3xx representa redirección.

16. Un código 4xx representa una respuesta relacionada con
    la solicitud del cliente.

17. Un código 5xx representa una respuesta de error del
    servidor.

18. No proporciones instrucciones ofensivas.

19. No expliques cómo comprometer sistemas.

20. No propongas explotación.

21. No muestres razonamiento interno.

22. No muestres cadena de pensamiento.

23. Sé técnico pero comprensible para un estudiante.

24. Mantén la respuesta por debajo de 220 palabras.

FORMATO OBLIGATORIO:

INTERPRETACIÓN

Explica qué ocurrió durante la solicitud.

TLS

Explica solamente las conclusiones respaldadas por los
datos del certificado y HTTPS.

HEADERS DE SEGURIDAD

Explica los resultados observados sin convertir la ausencia
de headers en vulnerabilidades confirmadas.

SEGURIDAD

Explica claramente qué puede y qué NO puede determinarse
con este análisis.

SIGUIENTE PASO

Sugiere como máximo una comprobación educativa o defensiva,
únicamente si aporta información adicional.

Entrega únicamente la respuesta final.
""".strip()

    # ========================================================
    # CONSULTAR OLLAMA
    # ========================================================

    try:

        return generar_respuesta(
            prompt
        )

    except OllamaError:

        return (
            "NetPro AI no está disponible en este momento.\n\n"
            "Los resultados técnicos obtenidos por NetPro "
            "continúan siendo válidos."
        )