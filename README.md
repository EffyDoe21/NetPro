# 🌐 NetPro — Network & Security Toolkit

**NetPro** es una aplicación de escritorio desarrollada en **Python**, orientada al análisis, diagnóstico y aprendizaje de redes de computadores.

El proyecto integra herramientas de direccionamiento IPv4 e IPv6, consultas DNS, diagnóstico de conectividad, análisis de puertos, inspección HTTP/HTTPS, información del sistema, historial de análisis e inteligencia artificial local mediante **Ollama**.

Su interfaz gráfica está desarrollada con **CustomTkinter**, ofreciendo un entorno moderno, organizado y accesible para estudiantes, desarrolladores y profesionales interesados en redes y seguridad informática.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?logo=windows)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-3B8ED0)
![AI](https://img.shields.io/badge/AI-Ollama_Local-black)
![Version](https://img.shields.io/badge/Version-0.1-orange)
![Status](https://img.shields.io/badge/Status-En_desarrollo-yellow)
![Rights](https://img.shields.io/badge/Rights-All_Rights_Reserved-red)

---

## 📑 Tabla de contenido

1. [Descripción del proyecto](#-descripción-del-proyecto)
2. [Características principales](#-características-principales)
3. [Tecnologías utilizadas](#-tecnologías-utilizadas)
4. [Estructura del proyecto](#-estructura-del-proyecto)
5. [Requisitos del sistema](#-requisitos-del-sistema)
6. [Instalación](#-instalación)
7. [Ejecución](#-ejecución)
8. [Inteligencia artificial local](#-inteligencia-artificial-local)
9. [Historial y base de datos](#-historial-y-base-de-datos)
10. [Seguridad y uso responsable](#-seguridad-y-uso-responsable)
11. [Objetivos del proyecto](#-objetivos-del-proyecto)
12. [Estado del proyecto](#-estado-del-proyecto)
13. [Derechos de autor](#-derechos-de-autor)
14. [Autora](#-autora)
15. [Repositorio](#-repositorio)

---

## 📖 Descripción del proyecto

NetPro — Network & Security Toolkit es una herramienta de escritorio diseñada para integrar diferentes funcionalidades de análisis de redes en una única aplicación.

El proyecto combina tres áreas fundamentales:

- **Análisis:** interpretación de direcciones IP, subredes, dominios, puertos y protocolos.
- **Diagnóstico:** evaluación de conectividad, servicios de red y respuestas de servidores.
- **Aprendizaje:** comprensión de conceptos de networking mediante herramientas prácticas, recursos educativos e inteligencia artificial local.

NetPro está orientado a estudiantes de ingeniería de software, técnicos de soporte, desarrolladores, administradores de sistemas y personas interesadas en redes de computadores y ciberseguridad.

---

## 🚀 Características principales

### 🌐 1. Analizador IPv4 — IP & Subnet

Módulo dedicado al análisis de direcciones IPv4 y al cálculo de información relacionada con subredes.

**Funciones principales:**

- Validación y análisis de direcciones IPv4.
- Cálculo de máscaras de subred.
- Identificación de direcciones de red.
- Cálculo de direcciones broadcast.
- Identificación de rangos de direcciones.
- Interpretación de prefijos CIDR.
- Análisis de información de subredes.
- Representación binaria de direcciones IP.

**Archivo principal:** `core/subnet.py`

**Interfaz gráfica:** `ui/analyzer.py`

### 🔢 2. Visualizador binario

Herramienta educativa que permite comprender la representación binaria del direccionamiento IP.

**Funciones:**

- Conversión de direcciones IPv4 a formato binario.
- Visualización de octetos.
- Interpretación de bits.
- Apoyo al aprendizaje del direccionamiento IP.

**Archivo:** `ui/binary_visualizer.py`

### 🌍 3. Analizador IPv6

NetPro incorpora un módulo independiente para el análisis de direcciones IPv6, utilizando la biblioteca estándar `ipaddress` de Python.

El módulo permite interpretar la estructura de direccionamiento de 128 bits y realizar cálculos relacionados con prefijos y rangos de direcciones.

**Funciones principales:**

- Validación de direcciones IPv6.
- Compatibilidad con direcciones con o sin prefijo CIDR.
- Compresión de direcciones IPv6.
- Expansión de direcciones IPv6.
- Identificación del prefijo de red.
- Cálculo de bits de red y bits restantes.
- Determinación de la dirección de red.
- Identificación de la primera y última dirección del rango.
- Cálculo de la cantidad total de direcciones.
- Clasificación de direcciones IPv6.
- Representación hexadecimal mediante ocho hextetos.
- Visualización binaria completa de 128 bits.
- Identificación de direcciones IPv4-Mapped.
- Consulta de propiedades de direccionamiento y alcance.
- Registro de análisis en el historial local.

**Clasificaciones contempladas:**

| Tipo | Descripción |
|---|---|
| Global Unicast | Direcciones del espacio unicast global |
| Link-Local | Direcciones del bloque `fe80::/10` |
| Unique Local | Direcciones del bloque `fc00::/7` |
| Multicast | Direcciones del bloque `ff00::/8`, con clasificación de alcance |
| Loopback | Dirección `::1` |
| Unspecified | Dirección `::` |
| IPv4-Mapped | Direcciones IPv4 representadas en IPv6 |
| Documentation | Direcciones del bloque `2001:db8::/32` |
| Especial / Reservada | Direcciones especiales o reservadas |

**Ejemplo de análisis:**

```text
Dirección: 2001:db8:1234:5678::25/64
Prefijo: /64
Red: 2001:db8:1234:5678::/64
Bits de red: 64
Bits restantes: 64
Cantidad de direcciones: 18.446.744.073.709.551.616
Clasificación: Documentation
```

**Archivos principales:**

- `core/ipv6.py`: validación, cálculo, clasificación y representación IPv6.
- `ui/ipv6_page.py`: interfaz gráfica del analizador.

### 🔎 4. Consultas DNS

Módulo dedicado a la resolución de nombres de dominio.

**Funciones principales:**

- Consultas DNS.
- Resolución de nombres de dominio.
- Consulta de registros de direcciones IPv4 e IPv6.
- Visualización de resultados técnicos.

**Archivos principales:**

- `core/dns.py`
- `ui/dns_page.py`

### 📡 5. Diagnóstico de conectividad

NetPro incorpora herramientas para analizar el estado de las conexiones de red.

**Funciones principales:**

- Pruebas Ping.
- Ejecución de Traceroute.
- Diagnóstico básico de conectividad.
- Consulta del estado de red.
- Presentación de resultados técnicos.

**Archivos principales:**

- `core/ping.py`
- `core/traceroute.py`
- `core/network_status.py`
- `ui/diagnostic_page.py`

### 🔌 6. Análisis de puertos

Módulo dedicado a comprobar la conectividad a puertos y analizar servicios de red.

**Funciones principales:**

- Comprobación de conectividad a puertos.
- Consulta de información de servicios asociados.
- Presentación de resultados de análisis.

**Archivos principales:**

- `core/ports.py`
- `ui/ports_page.py`

### 🌐 7. Analizador HTTP/HTTPS

Herramienta para examinar respuestas HTTP y HTTPS y consultar información técnica de servidores web.

**Funciones principales:**

- Solicitudes HTTP/HTTPS.
- Identificación de códigos de estado.
- Visualización de encabezados de respuesta.
- Medición del tiempo de respuesta.
- Consulta de información del servidor.
- Evaluación básica de encabezados de seguridad.
- Consulta de información relacionada con certificados HTTPS.

**Encabezados de seguridad considerados:**

| Encabezado | Propósito |
|---|---|
| Strict-Transport-Security | Política de conexiones HTTPS |
| Content-Security-Policy | Restricciones de carga de contenido |
| X-Content-Type-Options | Control de interpretación de tipos MIME |
| X-Frame-Options | Restricciones de incorporación en marcos |
| Referrer-Policy | Control de información de referencia |
| Permissions-Policy | Restricción de determinadas capacidades del navegador |

La ausencia de un encabezado no demuestra por sí sola la existencia de una vulnerabilidad explotable.

**Archivos principales:**

- `core/http_analyzer.py`
- `ui/http_page.py`

### 🖥️ 8. Información del sistema

Módulo dedicado a visualizar información técnica del equipo.

**Información disponible según el entorno:**

- Sistema operativo.
- Procesador.
- Memoria RAM.
- Tarjeta gráfica.
- Características del hardware.
- Información general del sistema.

**Archivos principales:**

- `core/system_info.py`
- `ui/system_page.py`

### 🎓 9. Aprendizaje

NetPro incorpora un módulo educativo orientado al aprendizaje de redes de computadores.

El proyecto incluye contenidos y recursos multimedia para complementar las herramientas prácticas.

**Recurso multimedia incluido:**

`assets/computacion_datos.mp4`

**Archivos relacionados:**

- `ui/learn.py`
- `data/lesson.py`

### 📋 10. Historial de análisis

NetPro incorpora un sistema de historial que permite conservar localmente registros relacionados con determinados análisis.

El almacenamiento utiliza una base de datos SQLite.

**Componentes principales:**

- `core/history.py`: operaciones de persistencia.
- `ui/history_page.py`: interfaz de consulta del historial.
- `data/netpro.db`: archivo de base de datos local.

### 🤖 11. Inteligencia artificial local

NetPro incorpora integración con Ollama para ejecutar modelos de inteligencia artificial localmente.

Esta funcionalidad permite complementar determinados análisis con explicaciones técnicas y educativas en español.

**Componentes:**

- `AI/ollama_client.py`
- `AI/http_ai.py`
- `modelfile`

La disponibilidad de estas funciones depende de que Ollama esté instalado y ejecutándose en el equipo.

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python 3 | Lenguaje principal |
| CustomTkinter | Interfaz gráfica |
| Tkinter | Componentes de interfaz |
| ipaddress | Análisis de direcciones IP |
| dnspython | Consultas DNS |
| socket | Operaciones de red |
| subprocess | Ejecución de comandos del sistema |
| SQLite | Persistencia local |
| Ollama | Inteligencia artificial local |
| Git | Control de versiones |
| GitHub | Repositorio del proyecto |

### Dependencias Python

El archivo `requirements.txt` declara:

```text
customtkinter==6.0.0
darkdetect==0.8.0
dnspython==2.8.0
packaging==26.3
```

Otras bibliotecas como `ipaddress`, `socket`, `sqlite3` y `subprocess` forman parte de la biblioteca estándar de Python.

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
│   └── computacion_datos.mp4
│
├── core/
│   ├── __init__.py
│   ├── diagnostic_page.py
│   ├── dns.py
│   ├── history.py
│   ├── http_analyzer.py
│   ├── ipv6.py
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
│   ├── ipv6_page.py
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

La carpeta `.venv`, los archivos `__pycache__` y la base de datos SQLite local se excluyen del control de versiones.

---

## 💻 Requisitos del sistema

### Requisitos generales

- Windows 10 o superior como entorno principal.
- Python 3 instalado.
- Git para clonar el repositorio.
- Conexión a internet para instalar dependencias.
- Acceso a la red para las herramientas que lo requieran.

### Requisitos opcionales para inteligencia artificial

- Ollama instalado.
- Modelo de lenguaje compatible.
- Recursos de memoria y procesamiento suficientes para ejecutar el modelo.

El rendimiento dependerá de las características del equipo y del modelo seleccionado.

---

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

```powershell
python -m venv .venv
```

### 4. Activar el entorno virtual

En PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

---

## ▶️ Ejecución

Con el entorno virtual activado:

```powershell
python main.py
```

La aplicación iniciará la interfaz gráfica de NetPro.

Algunas herramientas pueden requerir conectividad, permisos del sistema o servicios adicionales.

---

## 🤖 Inteligencia artificial local

NetPro utiliza Ollama como plataforma para ejecutar modelos de lenguaje localmente.

### 1. Instalar Ollama

Descarga Ollama desde su sitio oficial:

https://ollama.com

### 2. Verificar la instalación

```powershell
ollama --version
```

### 3. Descargar el modelo base

El archivo `modelfile` utiliza `llama3.2:1b` como modelo base.

```powershell
ollama pull llama3.2:1b
```

### 4. Crear el modelo personalizado

Desde la carpeta principal del proyecto:

```powershell
ollama create netpro-ai -f modelfile
```

### 5. Verificar los modelos instalados

```powershell
ollama list
```

### 6. Probar el modelo

```powershell
ollama run netpro-ai
```

NetPro AI está orientado a conceptos de redes, TCP/IP, IPv4, IPv6, DNS, conectividad, puertos, HTTP/HTTPS y seguridad informática.

La ejecución del modelo es local, aunque su descarga inicial requiere conexión a internet.

---

## 🗃️ Historial y base de datos

NetPro utiliza SQLite para almacenar localmente información relacionada con determinados análisis.

**Ubicación:**

```text
data/netpro.db
```

### Protección mediante Git

El archivo `.gitignore` contiene las siguientes reglas:

```gitignore
data/netpro.db
data/*.db
data/*.db-journal
data/*.db-wal
data/*.db-shm
```

Estas reglas permiten excluir del control de versiones la base de datos y sus archivos auxiliares.

Esto facilita mantener separados los datos generados durante la ejecución y el código fuente.

**Importante:** `.gitignore` no constituye un mecanismo de cifrado ni garantiza la confidencialidad frente al acceso local no autorizado.

---

## 🔒 Seguridad y uso responsable

NetPro está diseñado para fines educativos, técnicos y de diagnóstico.

Las herramientas deben utilizarse únicamente sobre sistemas, dispositivos y redes propios o para los cuales exista autorización.

### Recomendaciones

- No almacenar contraseñas ni tokens directamente en el código.
- Evitar publicar información sensible.
- Mantener actualizadas las dependencias.
- Revisar los cambios antes de realizar commits.
- Validar los resultados técnicos.
- Utilizar las herramientas de análisis de forma responsable.

---

## 🎯 Objetivos del proyecto

### Objetivo general

Desarrollar una aplicación de escritorio que integre herramientas de análisis de redes, diagnóstico de conectividad y aprendizaje de conceptos de networking mediante una interfaz gráfica accesible.

### Objetivos específicos

1. Facilitar el análisis de direccionamiento IPv4 e IPv6.
2. Incorporar herramientas para el diagnóstico de conectividad.
3. Permitir consultas DNS y análisis de puertos.
4. Integrar herramientas de análisis HTTP/HTTPS.
5. Presentar información técnica del equipo.
6. Ofrecer contenidos educativos sobre redes de computadores.
7. Integrar inteligencia artificial local como apoyo al aprendizaje.
8. Mantener un historial local de determinados análisis.
9. Mejorar progresivamente la experiencia de usuario y las funcionalidades de la aplicación.

---

## 🚧 Estado del proyecto

**Versión actual mostrada en la aplicación: NetPro v0.1**

NetPro se encuentra en desarrollo y mejora continua.

### Líneas de mejora

- Optimización de la interfaz gráfica.
- Ampliación de herramientas IPv4 e IPv6.
- Mejoras en los módulos de diagnóstico.
- Evolución del sistema de historial.
- Optimización de la integración con Ollama.
- Incorporación de pruebas automatizadas.
- Ampliación de recursos educativos.
- Mejoras en la documentación técnica.

---

## 📄 Derechos de autor

**NetPro — Network & Security Toolkit**

Copyright © 2026 Estefanía Becerra Quintero.

**Todos los derechos reservados.**

NetPro es un proyecto de desarrollo de software orientado al análisis, diagnóstico y aprendizaje de redes de computadores.

El código fuente se encuentra disponible públicamente en GitHub con fines de consulta, demostración y presentación del proyecto.

**Este repositorio no dispone actualmente de una licencia de software de código abierto.**

La publicación del código fuente no implica autorización para copiarlo, modificarlo, redistribuirlo o incorporarlo en otros proyectos sin el permiso correspondiente de la titular de los derechos.

Cualquier solicitud de autorización de uso o colaboración deberá realizarse a través del repositorio oficial.

El software se proporciona en su estado actual, sin que su publicación constituya una garantía de funcionamiento o idoneidad para un propósito específico.

---

## 👩‍💻 Autora

**Estefanía Becerra Quintero**

Desarrollo de software, herramientas de networking y aprendizaje de redes de computadores.

**GitHub:** https://github.com/EffyDoe21

---

## 🔗 Repositorio

**Repositorio oficial:**

https://github.com/EffyDoe21/NetPro

---

**NetPro — Network & Security Toolkit**

*Análisis, diagnóstico y aprendizaje de redes desde una sola aplicación.*

**Python · IPv4 · IPv6 · DNS · Networking · Ollama · Todos los derechos reservados**