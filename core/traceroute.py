import subprocess
import platform

from core.ping import validar_destino


# ============================================================
# EJECUTAR TRACEROUTE
# ============================================================

def ejecutar_traceroute(destino: str, max_saltos: int = 30) -> dict:
    """
    Ejecuta un traceroute hacia un dominio o dirección IP.

    Windows:
        utiliza tracert

    Linux / macOS:
        utiliza traceroute

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
    # VALIDAR MÁXIMO DE SALTOS
    # ========================================================

    if max_saltos < 1 or max_saltos > 255:
        raise ValueError(
            "El número máximo de saltos debe estar "
            "entre 1 y 255."
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
    # EJECUTAR TRACEROUTE
    # ========================================================

    try:

        proceso = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            shell=False,
            timeout=60,
            errors="replace"
        )

        # ====================================================
        # OBTENER SALIDA
        # ====================================================

        salida = proceso.stdout.strip()

        if not salida:
            salida = proceso.stderr.strip()

        # ====================================================
        # RESULTADO
        # ====================================================

        return {
            "destino": destino,
            "max_saltos": max_saltos,
            "comando": " ".join(comando),
            "salida": salida,
            "exitoso": proceso.returncode == 0,
            "error": None
        }

    # ========================================================
    # TIMEOUT
    # ========================================================

    except subprocess.TimeoutExpired:

        return {
            "destino": destino,
            "max_saltos": max_saltos,
            "comando": " ".join(comando),
            "salida": "",
            "exitoso": False,
            "error": (
                "El traceroute superó el tiempo máximo "
                "de espera."
            )
        }

    # ========================================================
    # COMANDO NO ENCONTRADO
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