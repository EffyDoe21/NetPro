# 🌐 NetPro

**NetPro** es una aplicación de escritorio desarrollada en Python orientada al análisis, diagnóstico y aprendizaje de conceptos relacionados con redes de computadores.

El proyecto integra herramientas de diagnóstico de red, análisis HTTP/HTTPS, consulta DNS, análisis de puertos, información del sistema y recursos educativos en una interfaz gráfica. Además, incorpora inteligencia artificial local mediante **Ollama** para apoyar la interpretación de determinados resultados.

## 🚀 Características principales

- 🔢 Analizador de redes IPv4 y subredes.
- 🧮 Visualización de direcciones IP en formato binario.
- 🌐 Consultas DNS.
- 📡 Pruebas de conectividad mediante Ping.
- 🛣️ Ejecución de Traceroute.
- 🔌 Análisis de puertos y servicios.
- 🔍 Análisis HTTP/HTTPS.
- 🛡️ Evaluación de encabezados básicos de seguridad HTTP.
- 💻 Visualización de información del sistema.
- 📊 Diagnóstico del estado de red.
- 📚 Módulo educativo para aprendizaje de conceptos de networking.
- 🤖 Integración con inteligencia artificial local mediante Ollama.

## 🧠 Inteligencia artificial local

NetPro utiliza **Ollama** para ejecutar modelos de inteligencia artificial de manera local.

La integración permite complementar determinadas herramientas de análisis con explicaciones comprensibles de los resultados obtenidos.

El proyecto incluye un `modelfile` para la configuración del comportamiento del modelo utilizado por NetPro.

> La disponibilidad de las funciones de inteligencia artificial depende de que Ollama esté instalado y ejecutándose en el equipo.

## 🛠️ Tecnologías utilizadas

- Python 3
- CustomTkinter
- Tkinter
- Requests
- Socket
- Subprocess
- Ollama
- Git
- GitHub

## 📁 Estructura del proyecto

```text
NetPro/
│
├── AI/
│   ├── __init__.py
│   ├── http_ai.py
│   └── ollama_client.py
│
├── core/
│   ├── __init__.py
│   ├── dns.py
│   ├── http_analyzer.py
│   ├── network_status.py
│   ├── ping.py
│   ├── ports.py
│   ├── subnet.py
│   ├── system_info.py
│   └── traceroute.py
│
├── data/
│   ├── __init__.py
│   └── lesson.py
│
├── ui/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── binary_visualizer.py
│   ├── diagnostic_page.py
│   ├── dns_page.py
│   ├── history_page.py
│   ├── home.py
│   ├── http_page.py
│   ├── learn.py
│   ├── ports_page.py
│   ├── system_page.py
│   └── tools_page.py
│
├── .gitignore
├── main.py
├── modelfile
├── README.md
└── requirements.txt
```

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/EffyDoe21/NetPro.git
```

### 2. Acceder al proyecto

```bash
cd NetPro
```

### 3. Crear un entorno virtual

En Windows:

```bash
python -m venv .venv
```

### 4. Activar el entorno virtual

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Instalar las dependencias

```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

Con el entorno virtual activado:

```bash
python main.py
```

## 🤖 Configuración de Ollama

Para utilizar las funcionalidades de inteligencia artificial se requiere tener Ollama instalado y ejecutándose localmente.

El modelo correspondiente puede configurarse utilizando el `modelfile` incluido en el proyecto.

Las demás herramientas de diagnóstico de NetPro pueden utilizarse independientemente de las funciones de IA, según el módulo.

## 🎯 Objetivo del proyecto

NetPro busca integrar herramientas prácticas de diagnóstico de redes con contenidos educativos en una única aplicación de escritorio.

Su propósito es facilitar tanto el análisis técnico como la comprensión de conceptos fundamentales de redes de computadores mediante una interfaz gráfica accesible.

## 🔒 Consideraciones de seguridad

Las herramientas de análisis de red deben utilizarse únicamente sobre sistemas, dispositivos y redes propios o para los cuales se cuente con autorización.

NetPro tiene fines educativos y de diagnóstico.

## 👩‍💻 Autora

**Estefanía Becerra Quintero**

## 📄 Licencia

Este proyecto se encuentra actualmente destinado a fines académicos y educativos.