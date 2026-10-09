

import subprocess
import platform

from core.ping import validar_destino


# ============================================================
# EJECUTAR TRACEROUTE
# ============================================================

def ejecutar_traceroute(destino: str, max_saltos: int = 30) -> dict:
    """
    Ejecuta Traceroute sin mostrar ventanas de consola.

    Windows:
        tracert

    Linux / macOS:
        traceroute

    Devuelve:
        destino
        max_saltos
        comando
        salida
        exitoso
        error
    """

    # ========================================================
    # VALIDAR DESTINO
    # ========================================================

    destino = validar_destino(destino)

    # ========================================================
    # VALIDAR NUMERO MAXIMO DE SALTOS
    # ========================================================

    if not isinstance(max_saltos, int) or not 1 <= max_saltos <= 255:
        raise ValueError(
            "El número máximo de saltos debe estar entre 1 y 255."
        )

    # ========================================================
    # DETECTAR SISTEMA OPERATIVO
    # ========================================================

    sistema = platform.system().lower()

    # ========================================================
    # CONSTRUIR COMANDO
    # ========================================================

    if sistema == "windows":

        comando = [
            "tracert",
            "-d",
            "-h",
            str(max_saltos),
            destino
        ]

    else:

        comando = [
            "traceroute",
            "-n",
            "-m",
            str(max_saltos),
            destino
        ]

    # ========================================================
    # CONFIGURAR EJECUCION INVISIBLE
    # ========================================================

    flags = 0

    if sistema == "windows":
        flags = subprocess.CREATE_NO_WINDOW

    # ========================================================
    # EJECUTAR TRACEROUTE
    # ========================================================

    try:

        proceso = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            shell=False,
            timeout=120,
            errors="replace",
            creationflags=flags
        )

        # ====================================================
        # OBTENER SALIDA
        # ====================================================

        salida = proceso.stdout.strip()

        if not salida:
            salida = proceso.stderr.strip()

        # ====================================================
        # EVALUAR RESULTADO
        # ====================================================

        exitoso = proceso.returncode == 0

        error = None

        if not exitoso:
            error = (
                proceso.stderr.strip()
                or "Traceroute finalizó con un error."
            )

        # ====================================================
        # RESULTADO
        # ====================================================

        return {
            "destino": destino,
            "max_saltos": max_saltos,
            "comando": " ".join(comando),
            "salida": salida,
            "exitoso": exitoso,
            "error": error
        }

    # ========================================================
    # TIEMPO MAXIMO SUPERADO
    # ========================================================

    except subprocess.TimeoutExpired:

        return {
            "destino": destino,
            "max_saltos": max_saltos,
            "comando": " ".join(comando),
            "salida": "",
            "exitoso": False,
            "error": (
                "Traceroute superó el tiempo máximo "
                "de espera de 120 segundos."
            )
        }

    # ========================================================
    # COMANDO NO DISPONIBLE
    # ========================================================

    except FileNotFoundError:

        return {
            "destino": destino,
            "max_saltos": max_saltos,
            "comando": " ".join(comando),
            "salida": "",
            "exitoso": False,
            "error": (
                "La herramienta traceroute/tracert "
                "no está disponible en el sistema."
            )
        }

    # ========================================================
    # OTROS ERRORES
    # ========================================================

    except Exception as error:

        return {
            "destino": destino,
            "max_saltos": max_saltos,
            "comando": " ".join(comando),
            "salida": "",
            "exitoso": False,
            "error": str(error)
        }


# ============================================================
# PRUEBA
# ============================================================

if __name__ == "__main__":

    resultado = ejecutar_traceroute(
        "example.com"
    )

    print("Destino:")
    print(resultado["destino"])

    print("\nComando:")
    print(resultado["comando"])

    print("\nResultado:")
    print(resultado["salida"])

    if resultado["error"]:
        print("\nError:")
        print(resultado["error"])
