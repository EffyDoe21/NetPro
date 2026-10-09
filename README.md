# 🌐 NetPro

**NetPro** es una aplicación de escritorio desarrollada en **Python**, orientada al análisis, diagnóstico y aprendizaje de conceptos relacionados con redes de computadores.

El proyecto integra herramientas de diagnóstico de red, análisis HTTP/HTTPS, consultas DNS, análisis de puertos, información del sistema y recursos educativos mediante una interfaz gráfica moderna desarrollada con **CustomTkinter**.

Además, incorpora inteligencia artificial local mediante **Ollama**, permitiendo complementar determinados análisis técnicos con explicaciones en español.

---

## 🚀 Características principales

### 🌐 Análisis de redes

- Análisis de direcciones IPv4 y subredes.
- Cálculo de máscaras de subred.
- Identificación de direcciones de red y broadcast.
- Visualización de direcciones IP en formato binario.
- Herramientas para comprender el direccionamiento IP.

### 📡 Diagnóstico de conectividad

- Pruebas de conectividad mediante Ping.
- Ejecución de Traceroute.
- Consultas DNS.
- Diagnóstico del estado de red.
- Herramientas para identificar posibles problemas de conectividad.

### 🔌 Análisis de puertos

- Análisis de puertos TCP.
- Identificación de servicios asociados a puertos.
- Herramientas para evaluar la disponibilidad de servicios de red.

### 🔍 Análisis HTTP/HTTPS

- Consulta de sitios web mediante HTTP y HTTPS.
- Visualización de códigos de estado HTTP.
- Análisis de encabezados de respuesta.
- Identificación de información del servidor.
- Medición de tiempos de respuesta.
- Evaluación de encabezados básicos de seguridad.
- Consulta de información relacionada con certificados HTTPS.

Entre los encabezados de seguridad evaluados se encuentran:

- Strict-Transport-Security (HSTS).
- Content-Security-Policy (CSP).
- X-Content-Type-Options.
- X-Frame-Options.
- Referrer-Policy.
- Permissions-Policy.

### 💻 Información del sistema

NetPro incorpora un módulo dedicado a visualizar información técnica del equipo.

Permite consultar información relacionada con:

- Sistema operativo.
- Procesador.
- Memoria RAM.
- Tarjeta gráfica.
- Información general del hardware.
- Características del entorno de ejecución.

### 📚 Módulo de aprendizaje

Incluye recursos educativos relacionados con redes de computadores, orientados a facilitar la comprensión de conceptos fundamentales de networking.

### 🤖 Inteligencia artificial local

NetPro integra Ollama para ejecutar modelos de inteligencia artificial localmente.

Esta integración permite ofrecer explicaciones complementarias de determinados resultados de análisis, sin depender necesariamente de servicios comerciales de inteligencia artificial en la nube.

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python 3 | Lenguaje principal |
| CustomTkinter | Interfaz gráfica |
| Tkinter | Componentes de interfaz |
| Requests | Solicitudes HTTP/HTTPS |
| Socket | Operaciones de red |
| Subprocess | Ejecución de herramientas del sistema |
| SQLite | Persistencia de información local |
| Ollama | Inteligencia artificial local |
| Git | Control de versiones |
| GitHub | Repositorio del proyecto |

---

## 📁 Estructura del proyecto

```text
NetPro/
│
├── AI/
│   ├── __init__.py
│   ├── http_ai.py
│   └── ollama_client.py
│
├── assets/
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

La base de datos `data/netpro.db` se utiliza localmente y está excluida del control de versiones.

---

## ⚙️ Instalación

### 1. Clonar el repositorio

Abre PowerShell o una terminal y ejecuta:

```bash
git clone https://github.com/EffyDoe21/NetPro.git
```

### 2. Acceder al proyecto

```bash
cd NetPro
```

### 3. Crear un entorno virtual

En Windows:

```powershell
python -m venv .venv
```

### 4. Activar el entorno virtual

En PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

---

## ▶️ Ejecución

Con el entorno virtual activado, ejecuta:

```powershell
python main.py
```

Esto iniciará la interfaz gráfica de NetPro.

Algunas herramientas pueden depender de la disponibilidad de servicios de red, permisos del sistema o componentes instalados en Windows.

---

## 🤖 Configuración de Ollama

NetPro permite utilizar modelos de inteligencia artificial mediante Ollama.

### 1. Instalar Ollama

Descarga Ollama desde su página oficial:

https://ollama.com

### 2. Verificar la instalación

```powershell
ollama --version
```

### 3. Descargar un modelo

Por ejemplo:

```powershell
ollama pull llama3.2:1b
```

También pueden utilizarse otros modelos compatibles con los recursos del equipo.

### 4. Crear el modelo personalizado

El proyecto incluye un archivo `modelfile` que permite configurar el comportamiento del modelo de inteligencia artificial.

Para crear un modelo personalizado:

```powershell
ollama create netpro-ai -f modelfile
```

### 5. Verificar los modelos disponibles

```powershell
ollama list
```

### 6. Ejecutar el modelo

```powershell
ollama run netpro-ai
```

La disponibilidad de las funciones de IA dentro de NetPro depende de que Ollama esté instalado, configurado y accesible desde la aplicación.

---

## 🗃️ Historial local y base de datos SQLite

NetPro incorpora un sistema de historial que permite almacenar localmente información relacionada con determinados análisis realizados desde la aplicación.

### Almacenamiento

La persistencia de datos se realiza mediante SQLite.

**Archivo local:**

```text
data/netpro.db
```

El historial puede consultarse mediante el módulo correspondiente de la interfaz gráfica.

### Protección de datos

Para evitar la publicación accidental de información almacenada localmente, el archivo `.gitignore` incluye:

```gitignore
data/*.db
```

Esta configuración permite:

- Excluir las bases de datos SQLite del control de versiones.
- Mantener separados los datos locales y el código fuente.
- Evitar incorporar accidentalmente registros locales en nuevos commits.
- Facilitar la distribución del proyecto sin incluir el historial personal de análisis.

**Importante:** `.gitignore` no cifra los archivos ni sustituye las medidas de seguridad del sistema operativo.

---

## 🔒 Consideraciones de seguridad

NetPro está diseñado para actividades de aprendizaje, análisis y diagnóstico técnico.

Las herramientas de red deben utilizarse exclusivamente en sistemas, dispositivos y redes propios o para los cuales se cuente con autorización.

Las funciones de análisis HTTP, diagnóstico de puertos y conectividad no deben utilizarse para realizar actividades no autorizadas.

La información generada por las herramientas debe manejarse de acuerdo con las políticas de seguridad y privacidad correspondientes.

---

## 🎯 Objetivo del proyecto

Desarrollar una aplicación de escritorio que integre herramientas prácticas de análisis de redes, diagnóstico de conectividad y aprendizaje de conceptos de networking, proporcionando una experiencia accesible mediante una interfaz gráfica moderna.

NetPro busca facilitar la interpretación de información técnica y contribuir al fortalecimiento de conocimientos relacionados con redes de computadores.

---

## 🚧 Estado del proyecto

**NetPro se encuentra en desarrollo y mejora continua.**

Entre las áreas de evolución del proyecto se encuentran:

- Mejoras en la experiencia de usuario.
- Ampliación de herramientas de diagnóstico.
- Optimización de los módulos de análisis.
- Mejoras en la presentación de información técnica.
- Ampliación del historial de resultados.
- Integración progresiva de inteligencia artificial local.
- Incorporación de nuevos recursos educativos.

---

## 👩‍💻 Autora

**Estefanía Becerra Quintero**

Desarrollo de software y herramientas de análisis de redes.

---

## 📄 Licencia

El proyecto está orientado actualmente a fines académicos y educativos.

No se ha especificado una licencia de software de código abierto.

---

## 🔗 Repositorio oficial

**GitHub:** https://github.com/EffyDoe21/NetPro

---

**NetPro — Análisis, diagnóstico y aprendizaje de redes desde una sola aplicación.**