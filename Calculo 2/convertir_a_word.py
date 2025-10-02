import subprocess
import os

# --- Configuración ---
# Nombre del archivo LaTeX de entrada (el esqueleto que creamos)
archivo_latex_entrada = 'Tarea_3_esqueleto.tex'

# Nombre del archivo Word de salida (el nombre del entregable final)
archivo_word_salida = 'Anexo 2 - Ejercicios Tarea 3 (4).docx'

# Ruta completa a los archivos
ruta_entrada = os.path.join(os.getcwd(), 'Calculo 2', archivo_latex_entrada)
ruta_salida = os.path.join(os.getcwd(), 'Calculo 2', archivo_word_salida)

def instalar_dependencias():
    """
    Instala pandoc y pandoc-eqnos.
    Pandoc es necesario para la conversión de documentos.
    Pandoc-eqnos ayuda a numerar las ecuaciones correctamente.
    """
    print(">>> Intentando instalar dependencias (pandoc)...")
    try:
        # Usamos subprocess para tener más control y capturar errores
        # Se necesita sudo, pero el entorno puede no permitirlo. Intentamos sin él.
        subprocess.run(['apt-get', 'update'], check=True, capture_output=True, text=True)
        subprocess.run(['apt-get', 'install', '-y', 'pandoc'], check=True, capture_output=True, text=True)
        print(">>> Pandoc instalado correctamente.")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"*** No se pudo instalar pandoc con apt-get: {e}")
        print("*** Esto puede ser normal en un entorno de sandboxing.")
        print("*** Se asumirá que pandoc ya está disponible en el sistema.")

def convertir_latex_a_word():
    """
    Convierte el archivo .tex especificado a un archivo .docx usando pandoc.
    """
    print(f"\n>>> Iniciando la conversión de '{archivo_latex_entrada}' a '{archivo_word_salida}'...")

    # Verificar si el archivo de entrada existe
    if not os.path.exists(ruta_entrada):
        print(f"*** ERROR: El archivo de entrada no se encuentra en '{ruta_entrada}'")
        return

    # Comando de Pandoc
    # Usamos el filtro 'pandoc-eqnos' para asegurar que las ecuaciones se numeren bien,
    # aunque no se instaló, puede estar presente. Si no, la conversión igual funciona.
    # El comando es: pandoc <entrada.tex> -o <salida.docx>
    comando = [
        'pandoc',
        ruta_entrada,
        '-o',
        ruta_salida
    ]

    print(f">>> Ejecutando comando: {' '.join(comando)}")

    try:
        # Ejecutar el comando pandoc
        resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
        print(">>> ¡Conversión completada con éxito!")
        print(f">>> Archivo Word generado en: '{ruta_salida}'")
        if resultado.stdout:
            print("Salida de Pandoc:\n", resultado.stdout)
        if resultado.stderr:
            print("Errores de Pandoc:\n", resultado.stderr)

    except FileNotFoundError:
        print("\n*** ERROR CRÍTICO: El comando 'pandoc' no se encontró.")
        print("*** La conversión no puede continuar. Asegúrese de que pandoc esté instalado y en el PATH del sistema.")
    except subprocess.CalledProcessError as e:
        print("\n*** ERROR CRÍTICO: Pandoc falló durante la conversión.")
        print(f"*** Código de error: {e.returncode}")
        print(f"*** Salida de error:\n{e.stderr}")

if __name__ == '__main__':
    # Aunque la instalación falló antes, es buena práctica incluirla en el script
    # por si el entorno cambia o si se ejecuta en otro lugar.
    instalar_dependencias()

    # Proceder con la conversión
    convertir_latex_a_word()