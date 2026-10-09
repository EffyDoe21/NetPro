# ============================================================
# NETPRO
# MODULO DE APRENDIZAJE
# data/lesson.py
# ============================================================

COURSES = [

    # ========================================================
    # CURSO 1 - FUNDAMENTOS DE REDES
    # ========================================================

    {
        "id": "fundamentals",
        "title": "Fundamentos de Redes",
        "icon": "🌐",
        "level": "Principiante",
        "description": (
            "Aprende los conceptos esenciales de redes, modelos de "
            "comunicacion, direccionamiento IP y funcionamiento "
            "basico de Internet."
        ),
        "lessons": [

            # ------------------------------------------------
            # LECCION 1
            # ------------------------------------------------

            {
                "id": "que_es_red",
                "title": "¿Que es una red?",
                "icon": "🌐",
                "duration": "8 min",

                "objectives": [
                    "Comprender que es una red de computadores.",
                    "Identificar los componentes basicos de una red.",
                    "Diferenciar LAN, WAN y WLAN.",
                ],

                "content": """
Una red de computadores es un conjunto de dispositivos
conectados entre si con el objetivo de intercambiar
informacion y compartir recursos.

Los dispositivos de una red pueden ser:

• Computadores
• Servidores
• Telefonos
• Impresoras
• Routers
• Switches
• Puntos de acceso
• Dispositivos IoT


Una red permite compartir diferentes recursos.

Por ejemplo:

• Archivos
• Aplicaciones
• Impresoras
• Bases de datos
• Conexion a Internet


TIPOS DE REDES


LAN

Local Area Network.

Es una red que cubre un area relativamente pequena.

Ejemplos:

• Una casa
• Una oficina
• Un laboratorio
• Un edificio


WLAN

Wireless Local Area Network.

Es una red local que utiliza tecnologias inalambricas,
como Wi-Fi.


WAN

Wide Area Network.

Permite conectar redes ubicadas a grandes distancias.

Internet es el ejemplo mas grande de una WAN.


PAN

Personal Area Network.

Es una red de alcance personal.

Por ejemplo:

Un telefono conectado mediante Bluetooth a unos audifonos.
                """,

                "key_concepts": [
                    {
                        "term": "Red",
                        "definition": (
                            "Conjunto de dispositivos conectados "
                            "para intercambiar informacion."
                        ),
                    },
                    {
                        "term": "LAN",
                        "definition": (
                            "Red de area local."
                        ),
                    },
                    {
                        "term": "WAN",
                        "definition": (
                            "Red de area amplia."
                        ),
                    },
                    {
                        "term": "WLAN",
                        "definition": (
                            "Red local inalambrica."
                        ),
                    },
                ],

                "example": """
Ejemplo de una red domestica:

Internet
   |
 Router
   |
   +------ Computador
   |
   +------ Telefono
   |
   +------ Smart TV
   |
   +------ Impresora

Todos estos dispositivos pueden formar parte
de la misma red local.
                """,

                "tip": (
                    "Cuando analices una red, comienza identificando "
                    "los dispositivos, la forma en que estan conectados "
                    "y los servicios que necesitan utilizar."
                ),

                "quiz": [
                    {
                        "question": "¿Que significa LAN?",
                        "options": [
                            "Local Area Network",
                            "Large Access Network",
                            "Logical Area Node",
                            "Local Access Number",
                        ],
                        "answer": "Local Area Network",
                        "explanation": (
                            "LAN significa Local Area Network o red "
                            "de area local."
                        ),
                    },
                    {
                        "question": (
                            "¿Cual es un ejemplo de una WAN?"
                        ),
                        "options": [
                            "Internet",
                            "Bluetooth entre dos dispositivos",
                            "Un cable USB",
                            "Una memoria USB",
                        ],
                        "answer": "Internet",
                        "explanation": (
                            "Internet conecta redes distribuidas "
                            "geograficamente y es un ejemplo de WAN."
                        ),
                    },
                ],
            },

            # ------------------------------------------------
            # LECCION 2
            # ------------------------------------------------

            {
                "id": "dispositivos_red",
                "title": "Dispositivos de red",
                "icon": "📡",
                "duration": "10 min",

                "objectives": [
                    "Reconocer los principales dispositivos de red.",
                    "Comprender la funcion de un router.",
                    "Comprender la funcion de un switch.",
                    "Diferenciar router, switch y access point.",
                ],

                "content": """
Las redes utilizan diferentes dispositivos para permitir
la comunicacion.


ROUTER

Un router conecta diferentes redes.

Una de sus funciones principales es decidir por donde deben
enviarse los paquetes para llegar a otra red.

En una red domestica, el router normalmente conecta la red
local con Internet.


SWITCH

Un switch conecta dispositivos dentro de una red local.

Por ejemplo:

• Computadores
• Servidores
• Impresoras
• Puntos de acceso

Los switches Ethernet trabajan principalmente utilizando
direcciones MAC para reenviar tramas dentro de la LAN.


ACCESS POINT

Un punto de acceso permite que dispositivos inalambricos
se conecten a una red.

Es utilizado normalmente para proporcionar conectividad
Wi-Fi.


MODEM

Dependiendo de la tecnologia del proveedor, un modem puede
realizar la conversion necesaria entre la red del proveedor
y los equipos del cliente.

En muchos hogares, diferentes funciones pueden estar
integradas en un solo dispositivo.


FIREWALL

Un firewall permite aplicar reglas al trafico de red.

Puede permitir o bloquear comunicaciones dependiendo de
criterios definidos.
                """,

                "key_concepts": [
                    {
                        "term": "Router",
                        "definition": (
                            "Dispositivo encargado de interconectar "
                            "redes y enrutar paquetes."
                        ),
                    },
                    {
                        "term": "Switch",
                        "definition": (
                            "Dispositivo utilizado para conectar "
                            "equipos dentro de una red local."
                        ),
                    },
                    {
                        "term": "Access Point",
                        "definition": (
                            "Dispositivo que proporciona acceso "
                            "inalambrico a una red."
                        ),
                    },
                    {
                        "term": "Firewall",
                        "definition": (
                            "Sistema que controla trafico utilizando "
                            "reglas de seguridad."
                        ),
                    },
                ],

                "example": """
Internet
   |
 Router
   |
 Switch
   |
   +---- PC
   +---- Servidor
   +---- Impresora
   |
 Access Point
   |
   +---- Telefono
   +---- Portatil
                """,

                "quiz": [
                    {
                        "question": (
                            "¿Que dispositivo se utiliza principalmente "
                            "para conectar diferentes redes?"
                        ),
                        "options": [
                            "Router",
                            "Teclado",
                            "Monitor",
                            "Impresora",
                        ],
                        "answer": "Router",
                        "explanation": (
                            "El router permite interconectar redes "
                            "y enrutar paquetes."
                        ),
                    },
                    {
                        "question": (
                            "¿Que dispositivo conecta normalmente "
                            "equipos dentro de una LAN Ethernet?"
                        ),
                        "options": [
                            "Switch",
                            "Mouse",
                            "Scanner",
                            "UPS",
                        ],
                        "answer": "Switch",
                        "explanation": (
                            "Un switch conecta dispositivos dentro "
                            "de una red local."
                        ),
                    },
                ],
            },

            # ------------------------------------------------
            # LECCION 3
            # ------------------------------------------------

            {
                "id": "modelo_osi",
                "title": "Modelo OSI",
                "icon": "🧱",
                "duration": "15 min",

                "objectives": [
                    "Comprender el objetivo del modelo OSI.",
                    "Identificar sus siete capas.",
                    "Relacionar protocolos con diferentes capas.",
                ],

                "content": """
El modelo OSI es un modelo conceptual utilizado para
comprender como se produce la comunicacion en una red.

OSI significa:

Open Systems Interconnection


El modelo posee siete capas.


7. APLICACION

Es la capa mas cercana a las aplicaciones del usuario.

Ejemplos de protocolos asociados:

• HTTP
• DNS
• SMTP


6. PRESENTACION

Relacionada conceptualmente con representacion,
transformacion y formato de datos.


5. SESION

Relacionada con el establecimiento y mantenimiento
conceptual de sesiones entre aplicaciones.


4. TRANSPORTE

Proporciona comunicacion extremo a extremo.

Protocolos importantes:

• TCP
• UDP


3. RED

Relacionada con direccionamiento logico y enrutamiento.

Ejemplo:

• IP


2. ENLACE DE DATOS

Relacionada con la comunicacion dentro del enlace.

Ethernet es una tecnologia importante en esta capa.


1. FISICA

Relacionada con la transmision fisica de bits.

Ejemplos:

• Cableado
• Senales
• Interfaces fisicas
                """,

                "key_concepts": [
                    {
                        "term": "OSI",
                        "definition": (
                            "Modelo conceptual de siete capas para "
                            "estudiar comunicaciones de red."
                        ),
                    },
                    {
                        "term": "TCP",
                        "definition": (
                            "Protocolo de transporte orientado a conexion."
                        ),
                    },
                    {
                        "term": "IP",
                        "definition": (
                            "Protocolo relacionado con direccionamiento "
                            "y entrega de paquetes entre redes."
                        ),
                    },
                ],

                "example": """
Modelo OSI

7  Aplicacion
6  Presentacion
5  Sesion
4  Transporte
3  Red
2  Enlace de datos
1  Fisica
                """,

                "tip": (
                    "No memorices solamente los nombres. Intenta "
                    "relacionar cada capa con lo que ocurre durante "
                    "una comunicacion real."
                ),

                "quiz": [
                    {
                        "question": (
                            "¿En que capa del modelo OSI se encuentra "
                            "conceptualmente IP?"
                        ),
                        "options": [
                            "Capa 1",
                            "Capa 2",
                            "Capa 3",
                            "Capa 7",
                        ],
                        "answer": "Capa 3",
                        "explanation": (
                            "IP se relaciona con la capa de red, "
                            "que corresponde a la capa 3."
                        ),
                    },
                    {
                        "question": (
                            "¿Que protocolos pertenecen al nivel "
                            "de transporte?"
                        ),
                        "options": [
                            "TCP y UDP",
                            "HTTP y DNS",
                            "IPv4 e IPv6",
                            "ARP y Ethernet",
                        ],
                        "answer": "TCP y UDP",
                        "explanation": (
                            "TCP y UDP son protocolos de transporte."
                        ),
                    },
                ],
            },

            # ------------------------------------------------
            # LECCION 4
            # ------------------------------------------------

            {
                "id": "tcp_ip",
                "title": "TCP/IP y comunicacion",
                "icon": "🔄",
                "duration": "12 min",

                "objectives": [
                    "Comprender el concepto general de TCP/IP.",
                    "Diferenciar TCP y UDP.",
                    "Relacionar IP, puertos y aplicaciones.",
                ],

                "content": """
TCP/IP es el conjunto de protocolos utilizado como base
de las comunicaciones en Internet.

Dentro de este conjunto encontramos protocolos como:

• IP
• TCP
• UDP
• ICMP


IP

Se encarga del direccionamiento y entrega de paquetes
entre redes.


TCP

Transmission Control Protocol.

Es orientado a conexion y proporciona mecanismos para
entrega confiable y ordenada de datos.


UDP

User Datagram Protocol.

No establece una conexion como TCP y tiene menor
sobrecarga.

Es utilizado en situaciones donde la velocidad y la baja
latencia pueden ser importantes.


PUERTOS

TCP y UDP utilizan numeros de puerto para identificar
servicios o procesos de comunicacion.

Ejemplos conocidos:

HTTP  → TCP 80

HTTPS → TCP 443

DNS   → UDP/TCP 53

SSH   → TCP 22
                """,

                "key_concepts": [
                    {
                        "term": "TCP",
                        "definition": (
                            "Protocolo de transporte orientado "
                            "a conexion."
                        ),
                    },
                    {
                        "term": "UDP",
                        "definition": (
                            "Protocolo de transporte basado "
                            "en datagramas."
                        ),
                    },
                    {
                        "term": "Puerto",
                        "definition": (
                            "Numero utilizado por TCP o UDP para "
                            "identificar puntos de comunicacion."
                        ),
                    },
                ],

                "example": """
Cuando visitas:

https://example.com

puede producirse una comunicacion utilizando:

Protocolo de aplicacion:
HTTPS

Transporte:
TCP

Puerto:
443

Red:
IP
                """,

                "quiz": [
                    {
                        "question": (
                            "¿Que protocolo de transporte es "
                            "orientado a conexion?"
                        ),
                        "options": [
                            "TCP",
                            "UDP",
                            "IP",
                            "DNS",
                        ],
                        "answer": "TCP",
                        "explanation": (
                            "TCP establece una conexion logica y "
                            "proporciona mecanismos de confiabilidad."
                        ),
                    },
                    {
                        "question": (
                            "¿Cual es el puerto TCP normalmente "
                            "asociado con HTTPS?"
                        ),
                        "options": [
                            "21",
                            "22",
                            "80",
                            "443",
                        ],
                        "answer": "443",
                        "explanation": (
                            "HTTPS utiliza normalmente TCP 443."
                        ),
                    },
                ],
            },
        ],
    },

    # ========================================================
    # CURSO 2 - SUBNETTING IPv4
    # ========================================================

    {
        "id": "subnetting",
        "title": "Subnetting IPv4",
        "icon": "🧮",
        "level": "Intermedio",
        "description": (
            "Aprende direccionamiento IPv4, mascaras, CIDR, "
            "direccion de red, broadcast, hosts y division de redes."
        ),
        "lessons": [

            {
                "id": "ipv4_basico",
                "title": "Direccionamiento IPv4",
                "icon": "🌐",
                "duration": "12 min",

                "objectives": [
                    "Comprender la estructura de IPv4.",
                    "Identificar los cuatro octetos.",
                    "Comprender la relacion entre decimal y binario.",
                ],

                "content": """
Una direccion IPv4 tiene una longitud de 32 bits.

Normalmente se representa mediante cuatro numeros
decimales separados por puntos.

Ejemplo:

192.168.1.10


Cada grupo representa un octeto.

192  → primer octeto
168  → segundo octeto
1    → tercer octeto
10   → cuarto octeto


Cada octeto contiene 8 bits.

Por lo tanto:

4 octetos x 8 bits = 32 bits


Cada octeto puede representar valores entre:

0 y 255


Ejemplo en binario:

192 = 11000000

168 = 10101000

1 = 00000001

10 = 00001010


Por lo tanto:

192.168.1.10

tambien puede representarse como:

11000000.10101000.00000001.00001010
                """,

                "key_concepts": [
                    {
                        "term": "IPv4",
                        "definition": (
                            "Version del protocolo IP que utiliza "
                            "direcciones de 32 bits."
                        ),
                    },
                    {
                        "term": "Octeto",
                        "definition": (
                            "Grupo de 8 bits."
                        ),
                    },
                ],

                "example": """
Direccion:

192.168.1.10

Octetos:

192 | 168 | 1 | 10

Bits:

8 + 8 + 8 + 8 = 32 bits
                """,

                "quiz": [
                    {
                        "question": (
                            "¿Cuantos bits tiene una direccion IPv4?"
                        ),
                        "options": [
                            "8",
                            "16",
                            "32",
                            "128",
                        ],
                        "answer": "32",
                        "explanation": (
                            "IPv4 utiliza direcciones de 32 bits."
                        ),
                    },
                    {
                        "question": (
                            "¿Cuantos bits tiene un octeto?"
                        ),
                        "options": [
                            "4",
                            "8",
                            "16",
                            "32",
                        ],
                        "answer": "8",
                        "explanation": (
                            "Un octeto contiene 8 bits."
                        ),
                    },
                ],
            },

            {
                "id": "mascaras",
                "title": "Mascaras de subred",
                "icon": "🎭",
                "duration": "15 min",

                "objectives": [
                    "Comprender para que sirve una mascara.",
                    "Diferenciar bits de red y host.",
                    "Relacionar mascara decimal con CIDR.",
                ],

                "content": """
Una mascara de subred permite identificar que parte de una
direccion IPv4 corresponde al prefijo de red.

Ejemplo:

Direccion:

192.168.1.10

Mascara:

255.255.255.0


En binario:

255.255.255.0

es:

11111111.11111111.11111111.00000000


Los bits 1 representan la parte correspondiente al
prefijo de red.

Los bits 0 quedan disponibles para la parte de host.


Esta mascara posee:

24 bits en 1

por lo tanto tambien puede escribirse:

/24


Ejemplos:

255.0.0.0
→ /8

255.255.0.0
→ /16

255.255.255.0
→ /24

255.255.255.128
→ /25

255.255.255.192
→ /26
                """,

                "key_concepts": [
                    {
                        "term": "Mascara",
                        "definition": (
                            "Valor utilizado para identificar la "
                            "longitud del prefijo IPv4."
                        ),
                    },
                    {
                        "term": "CIDR",
                        "definition": (
                            "Notacion que expresa la longitud del "
                            "prefijo mediante /n."
                        ),
                    },
                ],

                "example": """
192.168.1.10/24

Mascara:

255.255.255.0

Binario:

11111111.11111111.11111111.00000000
                """,

                "quiz": [
                    {
                        "question": (
                            "¿A que prefijo corresponde "
                            "255.255.255.0?"
                        ),
                        "options": [
                            "/8",
                            "/16",
                            "/24",
                            "/32",
                        ],
                        "answer": "/24",
                        "explanation": (
                            "255.255.255.0 contiene 24 bits "
                            "con valor 1."
                        ),
                    },
                ],
            },

            {
                "id": "network_broadcast",
                "title": "Red, broadcast y hosts",
                "icon": "📐",
                "duration": "15 min",

                "objectives": [
                    "Identificar la direccion de red.",
                    "Identificar broadcast en una subred IPv4.",
                    "Calcular hosts utilizables en casos tradicionales.",
                ],

                "content": """
En una subred IPv4 tradicional podemos identificar:

• Direccion de red
• Direcciones de host
• Direccion de broadcast


Ejemplo:

192.168.1.0/24


Direccion de red:

192.168.1.0


Primer host:

192.168.1.1


Ultimo host:

192.168.1.254


Broadcast:

192.168.1.255


En una subred tradicional, si existen h bits disponibles
para host, suele utilizarse:

2^h - 2

para calcular las direcciones de host utilizables.

Para /24:

32 - 24 = 8 bits de host

2^8 = 256 direcciones

256 - 2 = 254 hosts utilizables


La resta tradicional excluye:

• Direccion de red
• Direccion de broadcast
                """,

                "key_concepts": [
                    {
                        "term": "Network Address",
                        "definition": (
                            "Direccion que identifica una subred."
                        ),
                    },
                    {
                        "term": "Broadcast",
                        "definition": (
                            "Direccion IPv4 utilizada para enviar "
                            "trafico a todos los hosts de una subred."
                        ),
                    },
                ],

                "example": """
Red:

192.168.10.0/24

Network:
192.168.10.0

Hosts:
192.168.10.1
hasta
192.168.10.254

Broadcast:
192.168.10.255
                """,

                "quiz": [
                    {
                        "question": (
                            "¿Cual es el broadcast de "
                            "192.168.1.0/24?"
                        ),
                        "options": [
                            "192.168.1.0",
                            "192.168.1.1",
                            "192.168.1.254",
                            "192.168.1.255",
                        ],
                        "answer": "192.168.1.255",
                        "explanation": (
                            "En esta subred /24, .255 corresponde "
                            "a la direccion de broadcast."
                        ),
                    },
                ],
            },

            {
                "id": "subnetting_practico",
                "title": "Subnetting practico",
                "icon": "🧠",
                "duration": "20 min",

                "objectives": [
                    "Calcular subredes a partir de un prefijo.",
                    "Determinar rangos de hosts.",
                    "Aplicar subnetting a casos reales.",
                ],

                "content": """
Veamos:

192.168.1.0/26


Una mascara /26 equivale a:

255.255.255.192


El ultimo octeto tiene:

192


El tamano del bloque puede calcularse como:

256 - 192 = 64


Por lo tanto aparecen bloques como:

192.168.1.0

192.168.1.64

192.168.1.128

192.168.1.192


Primera subred:

Network:
192.168.1.0

Hosts:
192.168.1.1 - 192.168.1.62

Broadcast:
192.168.1.63


Segunda subred:

Network:
192.168.1.64

Hosts:
192.168.1.65 - 192.168.1.126

Broadcast:
192.168.1.127
                """,

                "key_concepts": [
                    {
                        "term": "Block Size",
                        "definition": (
                            "Incremento utilizado para identificar "
                            "los limites de determinadas subredes."
                        ),
                    }
                ],

                "example": """
/26

Mascara:
255.255.255.192

Bloque:
256 - 192 = 64

Subredes:

.0
.64
.128
.192
                """,

                "tip": (
                    "Utiliza el modulo IP & Subnet de NetPro para "
                    "comparar tus calculos manuales."
                ),

                "quiz": [
                    {
                        "question": (
                            "¿Cual es el tamano del bloque para "
                            "255.255.255.192?"
                        ),
                        "options": [
                            "32",
                            "64",
                            "128",
                            "192",
                        ],
                        "answer": "64",
                        "explanation": (
                            "256 - 192 = 64."
                        ),
                    },
                ],
            },
        ],
    },

    # ========================================================
    # CURSO 3 - IPv6
    # ========================================================

    {
        "id": "ipv6",
        "title": "IPv6",
        "icon": "🌍",
        "level": "Intermedio",
        "description": (
            "Aprende la estructura de IPv6, abreviacion, tipos de "
            "direcciones, prefijos, Link-Local, SLAAC y diferencias "
            "fundamentales frente a IPv4."
        ),
        "lessons": [

            {
                "id": "ipv6_intro",
                "title": "Introduccion a IPv6",
                "icon": "🌍",
                "duration": "10 min",

                "objectives": [
                    "Comprender que es IPv6.",
                    "Entender por que fue necesario ampliar el espacio de direcciones IP.",
                    "Identificar el tamano de una direccion IPv6.",
                    "Comparar de forma basica IPv4 e IPv6.",
                ],

                "content": """
IPv6 significa Internet Protocol version 6.

Es una version del protocolo IP disenada para proporcionar
un espacio de direccionamiento mucho mayor que IPv4.

IPv4 utiliza:

32 bits

IPv6 utiliza:

128 bits


IPv4:

192.168.1.10


IPv6:

2001:db8:1234:5678:abcd:ef01:2345:6789


Una direccion IPv6 se representa normalmente utilizando
numeros hexadecimales separados mediante dos puntos (:).


ESPACIO DE DIRECCIONES

IPv4:

2^32 direcciones posibles.


IPv6:

2^128 direcciones posibles.


IPv6 no consiste solamente en tener direcciones mas largas.

Tambien introduce cambios importantes en diferentes
aspectos del funcionamiento de las redes.
                """,

                "key_concepts": [
                    {
                        "term": "IPv6",
                        "definition": (
                            "Version del protocolo IP que utiliza "
                            "direcciones de 128 bits."
                        ),
                    },
                    {
                        "term": "128 bits",
                        "definition": (
                            "Longitud de una direccion IPv6."
                        ),
                    },
                    {
                        "term": "Hexadecimal",
                        "definition": (
                            "Sistema numerico de base 16 utilizado "
                            "para representar direcciones IPv6."
                        ),
                    },
                ],

                "example": """
IPv4:

192.168.1.10

IPv6:

2001:db8:1234:5678:abcd:ef01:2345:6789

IPv4 utiliza 32 bits.

IPv6 utiliza 128 bits.
                """,

                "tip": (
                    "No intentes memorizar direcciones IPv6 completas. "
                    "Primero aprende a reconocer su estructura."
                ),

                "quiz": [
                    {
                        "question": (
                            "¿Cuantos bits contiene una direccion IPv6?"
                        ),
                        "options": [
                            "32 bits",
                            "64 bits",
                            "128 bits",
                            "256 bits",
                        ],
                        "answer": "128 bits",
                        "explanation": (
                            "Una direccion IPv6 tiene una longitud "
                            "de 128 bits."
                        ),
                    },
                    {
                        "question": (
                            "¿Que sistema numerico se utiliza normalmente "
                            "para representar IPv6?"
                        ),
                        "options": [
                            "Decimal",
                            "Hexadecimal",
                            "Octal",
                            "Romano",
                        ],
                        "answer": "Hexadecimal",
                        "explanation": (
                            "IPv6 utiliza representacion hexadecimal."
                        ),
                    },
                ],
            },

            {
                "id": "ipv6_estructura",
                "title": "Estructura de una direccion IPv6",
                "icon": "🧩",
                "duration": "12 min",

                "objectives": [
                    "Identificar los ocho grupos de una direccion IPv6.",
                    "Comprender cuantos bits representa cada grupo.",
                    "Reconocer caracteres hexadecimales validos.",
                ],

                "content": """
Una direccion IPv6 tiene 128 bits.

Normalmente se representa mediante ocho grupos
hexadecimales separados por dos puntos.


Ejemplo:

2001:0db8:1234:5678:abcd:ef01:2345:6789


Podemos dividirla asi:

2001
0db8
1234
5678
abcd
ef01
2345
6789


Cada grupo contiene hasta cuatro digitos hexadecimales.

Cada digito hexadecimal representa 4 bits.

Por lo tanto:

4 digitos x 4 bits = 16 bits por grupo

8 grupos x 16 bits = 128 bits


Los caracteres hexadecimales posibles son:

0 1 2 3 4 5 6 7 8 9
a b c d e f
                """,

                "key_concepts": [
                    {
                        "term": "Hexteto",
                        "definition": (
                            "Nombre utilizado frecuentemente para un "
                            "grupo de 16 bits de una direccion IPv6."
                        ),
                    },
                    {
                        "term": "Hexadecimal",
                        "definition": (
                            "Sistema numerico de base 16."
                        ),
                    },
                ],

                "example": """
2001:0db8:0000:0000:0000:ff00:0042:8329

Grupo 1 → 2001
Grupo 2 → 0db8
Grupo 3 → 0000
Grupo 4 → 0000
Grupo 5 → 0000
Grupo 6 → ff00
Grupo 7 → 0042
Grupo 8 → 8329
                """,

                "quiz": [
                    {
                        "question": (
                            "¿Cuantos grupos tiene la representacion "
                            "completa de una direccion IPv6?"
                        ),
                        "options": [
                            "4",
                            "6",
                            "8",
                            "16",
                        ],
                        "answer": "8",
                        "explanation": (
                            "Una direccion IPv6 completa contiene "
                            "ocho grupos de 16 bits."
                        ),
                    },
                ],
            },

            {
                "id": "ipv6_abreviacion",
                "title": "Abreviacion de direcciones IPv6",
                "icon": "✂",
                "duration": "15 min",

                "objectives": [
                    "Eliminar ceros iniciales correctamente.",
                    "Utilizar la abreviacion ::.",
                    "Expandir una direccion IPv6 abreviada.",
                ],

                "content": """
Las direcciones IPv6 pueden abreviarse.


REGLA 1

Se pueden eliminar ceros ubicados al inicio de cada grupo.

0db8 → db8

0042 → 42

0001 → 1

0000 → 0


REGLA 2

Una secuencia contigua de grupos formados por ceros puede
comprimirse utilizando:

::


Ejemplo:

2001:0db8:0000:0000:0000:ff00:0042:8329


Eliminando ceros iniciales:

2001:db8:0:0:0:ff00:42:8329


Comprimiendo los grupos cero:

2001:db8::ff00:42:8329


IMPORTANTE

El simbolo :: solo puede utilizarse una vez en una misma
direccion IPv6.
                """,

                "key_concepts": [
                    {
                        "term": "::",
                        "definition": (
                            "Abreviacion utilizada para representar "
                            "una secuencia contigua de grupos cero."
                        ),
                    }
                ],

                "example": """
Completa:

2001:0db8:0000:0000:0000:ff00:0042:8329

Abreviada:

2001:db8::ff00:42:8329
                """,

                "quiz": [
                    {
                        "question": (
                            "¿Cual es una abreviacion valida de "
                            "2001:0db8:0000:0000:0000:0000:0000:0001?"
                        ),
                        "options": [
                            "2001:db8::1",
                            "2001::db8::1",
                            "2001-db8-1",
                            "2001:db8:1::1::",
                        ],
                        "answer": "2001:db8::1",
                        "explanation": (
                            "La secuencia de grupos cero puede "
                            "representarse mediante un unico ::."
                        ),
                    },
                ],
            },

            {
                "id": "ipv6_tipos",
                "title": "Tipos de direcciones IPv6",
                "icon": "🏷",
                "duration": "15 min",

                "objectives": [
                    "Reconocer Global Unicast.",
                    "Reconocer Link-Local.",
                    "Comprender Unique Local.",
                    "Identificar Multicast.",
                    "Reconocer Loopback y Unspecified.",
                ],

                "content": """
GLOBAL UNICAST

2000::/3

Este espacio contiene direcciones Global Unicast.


LINK-LOCAL

fe80::/10

Las direcciones Link-Local se utilizan para comunicacion
dentro del enlace local.


UNIQUE LOCAL

fc00::/7

Se utiliza para direccionamiento local.

En la practica es habitual encontrar asignaciones dentro
de fd00::/8.


MULTICAST

ff00::/8

IPv6 utiliza multicast para diferentes funciones.


LOOPBACK

::1

Representa el propio host.


UNSPECIFIED

::

Representa la direccion no especificada.


IPv6 no utiliza direcciones broadcast como IPv4.
                """,

                "key_concepts": [
                    {
                        "term": "Global Unicast",
                        "definition": (
                            "Direcciones unicast con alcance global."
                        ),
                    },
                    {
                        "term": "Link-Local",
                        "definition": (
                            "Direccion utilizada dentro del enlace local."
                        ),
                    },
                    {
                        "term": "Multicast",
                        "definition": (
                            "Comunicacion dirigida a un grupo "
                            "de interfaces."
                        ),
                    },
                ],

                "example": """
::1
→ Loopback

::
→ Unspecified

fe80::1
→ Link-Local

fd12:3456:789a::1
→ Unique Local

ff02::1
→ Multicast
                """,

                "quiz": [
                    {
                        "question": (
                            "¿Que direccion representa loopback en IPv6?"
                        ),
                        "options": [
                            "::1",
                            "::",
                            "fe80::1",
                            "ff00::1",
                        ],
                        "answer": "::1",
                        "explanation": (
                            "::1 es la direccion loopback IPv6."
                        ),
                    },
                    {
                        "question": (
                            "¿Que prefijo identifica Link-Local?"
                        ),
                        "options": [
                            "fe80::/10",
                            "ff00::/8",
                            "2000::/3",
                            "127.0.0.0/8",
                        ],
                        "answer": "fe80::/10",
                        "explanation": (
                            "Las direcciones Link-Local pertenecen "
                            "a fe80::/10."
                        ),
                    },
                ],
            },

            {
                "id": "ipv6_prefijos",
                "title": "Prefijos y subredes IPv6",
                "icon": "📐",
                "duration": "15 min",

                "objectives": [
                    "Comprender la notacion de prefijo IPv6.",
                    "Interpretar /64.",
                    "Comprender la separacion entre prefijo e identificador.",
                ],

                "content": """
IPv6 utiliza notacion de prefijo.

Ejemplo:

2001:db8:1234:5678::/64


/64 indica que los primeros 64 bits pertenecen al prefijo.

IPv6 tiene:

128 bits


Por lo tanto:

128 - 64 = 64 bits restantes


/64 es un tamano de prefijo ampliamente utilizado para
subredes IPv6 de hosts.


Ejemplo:

2001:db8:abcd:1234::/64


Direcciones dentro de este prefijo:

2001:db8:abcd:1234::25

2001:db8:abcd:1234:abcd:1234:5678:9abc


No debemos trasladar automaticamente reglas tradicionales
de IPv4 como 2^h - 2 al direccionamiento IPv6.
                """,

                "key_concepts": [
                    {
                        "term": "Prefijo IPv6",
                        "definition": (
                            "Cantidad inicial de bits utilizada "
                            "para identificar el prefijo de red."
                        ),
                    },
                    {
                        "term": "/64",
                        "definition": (
                            "Longitud de prefijo ampliamente utilizada "
                            "en subredes IPv6 de hosts."
                        ),
                    },
                ],

                "example": """
Direccion:

2001:db8:1234:5678::25/64

Prefijo:

2001:db8:1234:5678::/64
                """,

                "quiz": [
                    {
                        "question": (
                            "En 2001:db8:1234:5678::/64, "
                            "¿cuantos bits forman el prefijo?"
                        ),
                        "options": [
                            "32",
                            "48",
                            "64",
                            "128",
                        ],
                        "answer": "64",
                        "explanation": (
                            "/64 indica un prefijo de 64 bits."
                        ),
                    },
                ],
            },

            {
                "id": "ipv6_linklocal_slaac",
                "title": "Link-Local, SLAAC y Neighbor Discovery",
                "icon": "🔄",
                "duration": "15 min",

                "objectives": [
                    "Comprender el papel de Link-Local.",
                    "Conocer el concepto de SLAAC.",
                    "Introducir Neighbor Discovery.",
                    "Comprender la relacion con ICMPv6.",
                ],

                "content": """
LINK-LOCAL

Las direcciones Link-Local pertenecen a:

fe80::/10

Permiten comunicacion dentro del enlace local.


SLAAC

SLAAC significa:

Stateless Address Autoconfiguration

Permite que un dispositivo configure determinados
parametros IPv6 utilizando informacion anunciada
por la red.


ROUTER ADVERTISEMENT

Los routers IPv6 pueden anunciar informacion relevante
para la configuracion de los hosts.


NEIGHBOR DISCOVERY

IPv6 utiliza Neighbor Discovery Protocol, basado en ICMPv6.

Entre sus funciones se encuentran:

• Descubrimiento de routers
• Descubrimiento de vecinos
• Resolucion de direcciones de enlace


IPv6 no utiliza ARP.

Neighbor Discovery proporciona mecanismos relacionados
con funciones que en IPv4 dependen de ARP.
                """,

                "key_concepts": [
                    {
                        "term": "SLAAC",
                        "definition": (
                            "Stateless Address Autoconfiguration."
                        ),
                    },
                    {
                        "term": "NDP",
                        "definition": (
                            "Neighbor Discovery Protocol."
                        ),
                    },
                    {
                        "term": "ICMPv6",
                        "definition": (
                            "Internet Control Message Protocol for IPv6."
                        ),
                    },
                ],

                "example": """
Host IPv6
   |
   v
Router Advertisement
   |
   v
Informacion de configuracion
   |
   v
SLAAC
                """,

                "quiz": [
                    {
                        "question": "¿Que significa SLAAC?",
                        "options": [
                            "Stateless Address Autoconfiguration",
                            "Secure Local Address Access Control",
                            "Static Link Address Assignment",
                            "System Local Automatic Access Configuration",
                        ],
                        "answer": "Stateless Address Autoconfiguration",
                        "explanation": (
                            "SLAAC significa Stateless Address "
                            "Autoconfiguration."
                        ),
                    },
                    {
                        "question": (
                            "¿IPv6 utiliza ARP para Neighbor Discovery?"
                        ),
                        "options": [
                            "Si",
                            "No",
                        ],
                        "answer": "No",
                        "explanation": (
                            "IPv6 utiliza Neighbor Discovery "
                            "en lugar de ARP."
                        ),
                    },
                ],
            },

            {
                "id": "ipv4_vs_ipv6",
                "title": "IPv4 vs IPv6",
                "icon": "⚖",
                "duration": "12 min",

                "objectives": [
                    "Comparar IPv4 e IPv6.",
                    "Reconocer diferencias de direccionamiento.",
                    "Comprender la coexistencia mediante Dual Stack.",
                ],

                "content": """
IPv4

Longitud:

32 bits

Ejemplo:

192.168.1.10

Representacion:

Decimal con puntos


IPv6

Longitud:

128 bits

Ejemplo:

2001:db8::10

Representacion:

Hexadecimal separada por dos puntos


BROADCAST

IPv4 dispone de broadcast.

IPv6 no utiliza direcciones broadcast.


RESOLUCION DE VECINOS

IPv4 utiliza ARP en redes como Ethernet.

IPv6 utiliza Neighbor Discovery.


CONFIGURACION

IPv4 puede utilizar:

• Configuracion manual
• DHCP


IPv6 puede utilizar:

• Configuracion manual
• SLAAC
• DHCPv6


DUAL STACK

IPv4 e IPv6 pueden funcionar simultaneamente en un
mismo dispositivo o infraestructura.

Esto se conoce como Dual Stack.
                """,

                "key_concepts": [
                    {
                        "term": "Dual Stack",
                        "definition": (
                            "Uso simultaneo de IPv4 e IPv6."
                        ),
                    }
                ],

                "example": """
IPv4:

192.168.1.10
32 bits


IPv6:

2001:db8::10
128 bits
                """,

                "quiz": [
                    {
                        "question": "¿Que significa Dual Stack?",
                        "options": [
                            "Utilizar IPv4 e IPv6 simultaneamente",
                            "Utilizar dos routers",
                            "Tener dos servidores DNS",
                            "Utilizar dos tarjetas de red",
                        ],
                        "answer": "Utilizar IPv4 e IPv6 simultaneamente",
                        "explanation": (
                            "Dual Stack permite operar IPv4 e IPv6 "
                            "simultaneamente."
                        ),
                    },
                ],
            },
        ],
    },

    # ========================================================
    # CURSO 4 - DNS
    # ========================================================

    {
        "id": "dns",
        "title": "DNS",
        "icon": "🔎",
        "level": "Principiante",
        "description": (
            "Comprende como DNS convierte nombres de dominio en "
            "direcciones IP y conoce sus registros principales."
        ),
        "lessons": [

            {
                "id": "dns_intro",
                "title": "¿Que es DNS?",
                "icon": "🔎",
                "duration": "10 min",

                "objectives": [
                    "Comprender la funcion de DNS.",
                    "Relacionar dominios con direcciones IP.",
                    "Comprender una consulta DNS basica.",
                ],

                "content": """
DNS significa:

Domain Name System


Permite relacionar nombres faciles de recordar con
informacion utilizada por los sistemas de red.

Por ejemplo:

example.com

puede resolverse hacia una direccion IP.


Sin DNS, los usuarios tendrian que recordar direcciones IP
para acceder a muchos servicios.


Proceso simplificado:

Usuario escribe un dominio

        ↓

Se realiza una consulta DNS

        ↓

Se obtiene informacion asociada

        ↓

La aplicacion puede continuar la comunicacion
                """,

                "key_concepts": [
                    {
                        "term": "DNS",
                        "definition": (
                            "Sistema de nombres de dominio."
                        ),
                    },
                    {
                        "term": "Resolucion",
                        "definition": (
                            "Proceso de obtener informacion DNS "
                            "asociada a un nombre."
                        ),
                    },
                ],

                "example": """
Dominio:

example.com

Consulta DNS:

example.com → direccion IP
                """,

                "quiz": [
                    {
                        "question": "¿Que significa DNS?",
                        "options": [
                            "Domain Name System",
                            "Digital Network Security",
                            "Data Node Service",
                            "Dynamic Network System",
                        ],
                        "answer": "Domain Name System",
                        "explanation": (
                            "DNS significa Domain Name System."
                        ),
                    },
                ],
            },

            {
                "id": "dns_records",
                "title": "Registros DNS",
                "icon": "📋",
                "duration": "15 min",

                "objectives": [
                    "Reconocer registros A y AAAA.",
                    "Comprender CNAME.",
                    "Conocer MX y TXT.",
                ],

                "content": """
DNS utiliza diferentes tipos de registros.


A

Relaciona un nombre con una direccion IPv4.


AAAA

Relaciona un nombre con una direccion IPv6.


CNAME

Permite definir un nombre canonico o alias.


MX

Indica servidores relacionados con correo electronico.


TXT

Permite almacenar informacion de texto.

Es utilizado para diferentes finalidades, incluyendo
determinados mecanismos de verificacion y seguridad.


NS

Indica servidores de nombres autoritativos para una zona.
                """,

                "key_concepts": [
                    {
                        "term": "A",
                        "definition": "Registro para IPv4.",
                    },
                    {
                        "term": "AAAA",
                        "definition": "Registro para IPv6.",
                    },
                    {
                        "term": "MX",
                        "definition": (
                            "Registro relacionado con servidores "
                            "de correo."
                        ),
                    },
                ],

                "example": """
A
example.com → IPv4

AAAA
example.com → IPv6

MX
example.com → servidor de correo
                """,

                "quiz": [
                    {
                        "question": (
                            "¿Que registro DNS se utiliza para IPv6?"
                        ),
                        "options": [
                            "A",
                            "AAAA",
                            "MX",
                            "TXT",
                        ],
                        "answer": "AAAA",
                        "explanation": (
                            "AAAA relaciona nombres con direcciones IPv6."
                        ),
                    },
                ],
            },

            {
                "id": "dns_diagnostico",
                "title": "Diagnostico DNS",
                "icon": "🛠",
                "duration": "12 min",

                "objectives": [
                    "Comprender fallos basicos de resolucion.",
                    "Conocer herramientas de diagnostico DNS.",
                    "Relacionar DNS con NetPro.",
                ],

                "content": """
Cuando un dominio no puede resolverse, el problema no
necesariamente significa que Internet este completamente
caido.

Puede existir un problema relacionado con DNS.


Herramientas comunes:

nslookup

Resolve-DnsName

dig


Al diagnosticar DNS podemos revisar:

• Si el nombre existe
• Si devuelve registros A
• Si devuelve registros AAAA
• Que servidor DNS responde
• Si existe un error de resolucion


NetPro incorpora un modulo DNS que permite consultar
informacion relacionada con nombres y direcciones.
                """,

                "key_concepts": [
                    {
                        "term": "nslookup",
                        "definition": (
                            "Herramienta utilizada para realizar "
                            "consultas DNS."
                        ),
                    }
                ],

                "example": """
nslookup example.com

Tambien puedes utilizar el modulo:

NetPro → DNS
                """,

                "quiz": [
                    {
                        "question": (
                            "¿Que herramienta puede utilizarse "
                            "para realizar consultas DNS?"
                        ),
                        "options": [
                            "nslookup",
                            "notepad",
                            "paint",
                            "calc",
                        ],
                        "answer": "nslookup",
                        "explanation": (
                            "nslookup es una herramienta de consulta DNS."
                        ),
                    },
                ],
            },
        ],
    },

    # ========================================================
    # CURSO 5 - PUERTOS Y PROTOCOLOS
    # ========================================================

    {
        "id": "ports",
        "title": "Puertos y Protocolos",
        "icon": "🔌",
        "level": "Intermedio",
        "description": (
            "Aprende que son los puertos TCP/UDP, servicios "
            "comunes y como interpretar puertos abiertos."
        ),
        "lessons": [

            {
                "id": "ports_intro",
                "title": "¿Que es un puerto?",
                "icon": "🔌",
                "duration": "10 min",

                "objectives": [
                    "Comprender el concepto de puerto.",
                    "Relacionar puertos con TCP y UDP.",
                    "Interpretar un puerto abierto correctamente.",
                ],

                "content": """
Un puerto es un identificador numerico utilizado por
protocolos de transporte como TCP y UDP.

Permite diferenciar comunicaciones y servicios dentro
de un mismo dispositivo.


Ejemplos conocidos:

22  → SSH

53  → DNS

80  → HTTP

443 → HTTPS


Un puerto abierto puede indicar que existe un servicio
escuchando y accesible desde el punto donde se realiza
la comprobacion.

IMPORTANTE:

Un puerto abierto no significa automaticamente que exista
una vulnerabilidad.
                """,

                "key_concepts": [
                    {
                        "term": "Puerto",
                        "definition": (
                            "Identificador numerico utilizado por "
                            "TCP o UDP."
                        ),
                    },
                    {
                        "term": "Puerto abierto",
                        "definition": (
                            "Estado que puede indicar que un servicio "
                            "esta aceptando comunicaciones."
                        ),
                    },
                ],

                "example": """
Destino:

192.168.1.20

Puerto:

443/TCP

Posible servicio asociado:

HTTPS

Esto no demuestra por si solo una vulnerabilidad.
                """,

                "warning": (
                    "Analiza solamente sistemas propios o aquellos "
                    "para los cuales tengas autorizacion."
                ),

                "quiz": [
                    {
                        "question": (
                            "¿Un puerto abierto significa automaticamente "
                            "que el sistema es vulnerable?"
                        ),
                        "options": [
                            "Si",
                            "No",
                        ],
                        "answer": "No",
                        "explanation": (
                            "Un puerto abierto indica exposicion de un "
                            "servicio, pero no demuestra por si mismo "
                            "una vulnerabilidad."
                        ),
                    },
                ],
            },

            {
                "id": "common_ports",
                "title": "Puertos comunes",
                "icon": "📋",
                "duration": "12 min",

                "objectives": [
                    "Reconocer puertos de servicios frecuentes.",
                    "Relacionar servicios con TCP o UDP.",
                ],

                "content": """
Algunos puertos ampliamente conocidos son:

20/21 TCP
FTP

22 TCP
SSH

23 TCP
Telnet

25 TCP
SMTP

53 UDP/TCP
DNS

67/68 UDP
DHCP

80 TCP
HTTP

110 TCP
POP3

143 TCP
IMAP

443 TCP
HTTPS


Estos valores son asociaciones comunes.

Un servicio puede configurarse para utilizar un puerto
diferente al puerto convencional.
                """,

                "key_concepts": [
                    {
                        "term": "Well-known ports",
                        "definition": (
                            "Rango de puertos ampliamente asociado "
                            "con servicios estandarizados."
                        ),
                    }
                ],

                "example": """
22  → SSH
53  → DNS
80  → HTTP
443 → HTTPS
                """,

                "quiz": [
                    {
                        "question": (
                            "¿Que servicio se asocia normalmente "
                            "con el puerto 22/TCP?"
                        ),
                        "options": [
                            "SSH",
                            "HTTP",
                            "DNS",
                            "HTTPS",
                        ],
                        "answer": "SSH",
                        "explanation": (
                            "SSH utiliza normalmente TCP 22."
                        ),
                    },
                ],
            },

            {
                "id": "port_security",
                "title": "Puertos y seguridad",
                "icon": "🛡",
                "duration": "12 min",

                "objectives": [
                    "Interpretar exposicion de servicios.",
                    "Comprender el principio de minima exposicion.",
                    "Evitar conclusiones incorrectas sobre puertos abiertos.",
                ],

                "content": """
Desde una perspectiva de seguridad, debemos conocer que
servicios se encuentran expuestos.

Una buena practica general consiste en mantener disponibles
solamente los servicios necesarios.

Al encontrar un puerto abierto debemos preguntarnos:

• ¿Que servicio esta escuchando?
• ¿Es necesario?
• ¿Esta actualizado?
• ¿Requiere autenticacion?
• ¿Deberia ser accesible desde esta red?
• ¿Existe un firewall?


No debemos afirmar:

"Puerto abierto = vulnerabilidad"


La interpretacion correcta requiere contexto.
                """,

                "key_concepts": [
                    {
                        "term": "Superficie de exposicion",
                        "definition": (
                            "Conjunto de servicios e interfaces "
                            "potencialmente accesibles."
                        ),
                    }
                ],

                "warning": (
                    "El escaneo de sistemas ajenos sin autorizacion "
                    "puede violar politicas, contratos o leyes. "
                    "Utiliza NetPro con fines educativos y autorizados."
                ),

                "quiz": [
                    {
                        "question": (
                            "¿Que deberias hacer al detectar un "
                            "puerto abierto?"
                        ),
                        "options": [
                            "Analizar el servicio y su contexto",
                            "Declarar inmediatamente que fue hackeado",
                            "Eliminar el sistema operativo",
                            "Asumir que no existe ningun riesgo",
                        ],
                        "answer": "Analizar el servicio y su contexto",
                        "explanation": (
                            "La exposicion debe evaluarse considerando "
                            "el servicio, necesidad y configuracion."
                        ),
                    },
                ],
            },
        ],
    },

    # ========================================================
    # CURSO 6 - HTTP / HTTPS
    # ========================================================

    {
        "id": "http",
        "title": "HTTP y HTTPS",
        "icon": "🌐",
        "level": "Intermedio",
        "description": (
            "Aprende como funciona la Web, codigos HTTP, headers, "
            "HTTPS y conceptos basicos de seguridad web."
        ),
        "lessons": [

            {
                "id": "http_intro",
                "title": "Fundamentos de HTTP",
                "icon": "🌐",
                "duration": "12 min",

                "objectives": [
                    "Comprender el modelo solicitud-respuesta.",
                    "Conocer metodos HTTP basicos.",
                    "Interpretar una respuesta HTTP.",
                ],

                "content": """
HTTP significa:

Hypertext Transfer Protocol


HTTP utiliza un modelo de solicitud y respuesta.


Cliente

        ↓ Solicitud HTTP

Servidor

        ↓ Respuesta HTTP

Cliente


METODOS

Algunos metodos HTTP son:

GET
POST
PUT
DELETE
HEAD
OPTIONS


Una respuesta puede contener:

• Codigo de estado
• Headers
• Cuerpo de respuesta
                """,

                "key_concepts": [
                    {
                        "term": "Request",
                        "definition": "Solicitud HTTP.",
                    },
                    {
                        "term": "Response",
                        "definition": "Respuesta HTTP.",
                    },
                    {
                        "term": "Header",
                        "definition": (
                            "Campo que transporta metadatos "
                            "de una solicitud o respuesta."
                        ),
                    },
                ],

                "example": """
GET / HTTP/1.1
Host: example.com

Respuesta:

HTTP/1.1 200 OK
                """,

                "quiz": [
                    {
                        "question": (
                            "¿Que metodo HTTP se utiliza normalmente "
                            "para solicitar un recurso?"
                        ),
                        "options": [
                            "GET",
                            "DELETE",
                            "DROP",
                            "PING",
                        ],
                        "answer": "GET",
                        "explanation": (
                            "GET se utiliza para solicitar una "
                            "representacion de un recurso."
                        ),
                    },
                ],
            },

            {
                "id": "http_status",
                "title": "Codigos de estado HTTP",
                "icon": "🔢",
                "duration": "12 min",

                "objectives": [
                    "Interpretar familias 2xx, 3xx, 4xx y 5xx.",
                    "Reconocer codigos frecuentes.",
                ],

                "content": """
Los codigos HTTP permiten conocer el resultado general
de una solicitud.


1xx
Informativos


2xx
Exito

Ejemplo:

200 OK


3xx
Redireccion


4xx
Error relacionado con la solicitud del cliente

Ejemplos:

400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found


5xx
Error del servidor

Ejemplos:

500 Internal Server Error
502 Bad Gateway
503 Service Unavailable
                """,

                "key_concepts": [
                    {
                        "term": "200",
                        "definition": "Solicitud procesada correctamente.",
                    },
                    {
                        "term": "404",
                        "definition": "Recurso no encontrado.",
                    },
                    {
                        "term": "500",
                        "definition": "Error interno del servidor.",
                    },
                ],

                "quiz": [
                    {
                        "question": (
                            "¿Que indica generalmente un codigo 2xx?"
                        ),
                        "options": [
                            "Exito",
                            "Redireccion",
                            "Error de cliente",
                            "Error de servidor",
                        ],
                        "answer": "Exito",
                        "explanation": (
                            "La familia 2xx indica resultados exitosos."
                        ),
                    },
                ],
            },

            {
                "id": "https_security",
                "title": "HTTPS y seguridad",
                "icon": "🔒",
                "duration": "15 min",

                "objectives": [
                    "Comprender la funcion general de HTTPS.",
                    "Conocer TLS y certificados.",
                    "Introducir headers de seguridad.",
                ],

                "content": """
HTTPS utiliza HTTP sobre una conexion protegida mediante TLS.

TLS proporciona mecanismos relacionados con:

• Confidencialidad
• Integridad
• Autenticacion del servidor mediante certificados


CERTIFICADO

Un certificado digital permite asociar una identidad con
una clave publica dentro de una infraestructura de confianza.


HEADERS DE SEGURIDAD

Los sitios web pueden utilizar diferentes headers para
reforzar determinadas protecciones.

Ejemplos:

Strict-Transport-Security

Content-Security-Policy

X-Content-Type-Options

X-Frame-Options

Referrer-Policy

Permissions-Policy


La ausencia de un header no demuestra por si sola que
un sitio sea vulnerable.

Debe interpretarse dentro de su contexto.
                """,

                "key_concepts": [
                    {
                        "term": "TLS",
                        "definition": (
                            "Protocolo utilizado para proteger "
                            "comunicaciones de red."
                        ),
                    },
                    {
                        "term": "HSTS",
                        "definition": (
                            "Mecanismo que permite indicar al navegador "
                            "el uso de HTTPS bajo determinadas condiciones."
                        ),
                    },
                ],

                "example": """
https://example.com

Puerto habitual:

443/TCP

Protocolo:

HTTPS

Proteccion de transporte:

TLS
                """,

                "quiz": [
                    {
                        "question": (
                            "¿Que tecnologia protege normalmente "
                            "la comunicacion HTTPS?"
                        ),
                        "options": [
                            "TLS",
                            "ARP",
                            "FTP",
                            "ICMP",
                        ],
                        "answer": "TLS",
                        "explanation": (
                            "HTTPS utiliza TLS para proteger "
                            "la comunicacion."
                        ),
                    },
                ],
            },
        ],
    },

    # ========================================================
    # CURSO 7 - DIAGNOSTICO DE RED
    # ========================================================

    {
        "id": "diagnostics",
        "title": "Diagnostico de Redes",
        "icon": "🛠",
        "level": "Intermedio",
        "description": (
            "Aprende una metodologia ordenada para diagnosticar "
            "problemas de conectividad utilizando herramientas de red."
        ),
        "lessons": [

            {
                "id": "diagnostic_method",
                "title": "Metodologia de diagnostico",
                "icon": "🧭",
                "duration": "12 min",

                "objectives": [
                    "Diagnosticar problemas de forma estructurada.",
                    "Evitar cambiar configuraciones al azar.",
                    "Separar problemas locales, DNS y conectividad.",
                ],

                "content": """
Cuando existe un problema de red, debemos diagnosticarlo
de forma ordenada.

Un posible proceso es:


1. Revisar el estado fisico

¿Existe conexion Ethernet o Wi-Fi?


2. Revisar configuracion IP

¿El equipo tiene direccion IP?

¿Tiene gateway?

¿Tiene DNS?


3. Probar el propio host


4. Probar el gateway


5. Probar conectividad IP externa


6. Probar resolucion DNS


7. Revisar el servicio especifico


Este enfoque ayuda a identificar en que punto falla
la comunicacion.
                """,

                "key_concepts": [
                    {
                        "term": "Diagnostico",
                        "definition": (
                            "Proceso sistematico para identificar "
                            "la causa de un problema."
                        ),
                    }
                ],

                "example": """
Problema:

"No tengo Internet"

No debemos asumir inmediatamente que Internet esta caido.

Podemos revisar:

Adaptador
   ↓
IP
   ↓
Gateway
   ↓
Conectividad externa
   ↓
DNS
   ↓
Aplicacion
                """,

                "quiz": [
                    {
                        "question": (
                            "¿Que es mejor al diagnosticar una red?"
                        ),
                        "options": [
                            "Seguir un proceso ordenado",
                            "Cambiar todas las configuraciones",
                            "Reiniciar indefinidamente",
                            "Asumir que siempre es DNS",
                        ],
                        "answer": "Seguir un proceso ordenado",
                        "explanation": (
                            "Una metodologia sistematica permite "
                            "aislar mejor el problema."
                        ),
                    },
                ],
            },

            {
                "id": "ping",
                "title": "Ping e ICMP",
                "icon": "📡",
                "duration": "12 min",

                "objectives": [
                    "Comprender para que sirve ping.",
                    "Interpretar latencia y perdida.",
                    "Evitar conclusiones incorrectas.",
                ],

                "content": """
Ping es una herramienta utilizada para comprobar
determinados aspectos de conectividad IP.

Normalmente utiliza mensajes ICMP Echo.


Puede ayudarnos a observar:

• Si existe respuesta
• Tiempo aproximado de ida y vuelta
• Perdida de paquetes


Ejemplo:

ping 8.8.8.8


IMPORTANTE

Que un host no responda a ping no significa necesariamente
que este apagado.

ICMP puede estar filtrado por firewalls o politicas
de seguridad.
                """,

                "key_concepts": [
                    {
                        "term": "ICMP",
                        "definition": (
                            "Protocolo utilizado para mensajes "
                            "de control y diagnostico."
                        ),
                    },
                    {
                        "term": "Latencia",
                        "definition": (
                            "Tiempo asociado al desplazamiento "
                            "de informacion entre puntos."
                        ),
                    },
                ],

                "quiz": [
                    {
                        "question": (
                            "¿La ausencia de respuesta a ping demuestra "
                            "que un host esta apagado?"
                        ),
                        "options": [
                            "Si",
                            "No",
                        ],
                        "answer": "No",
                        "explanation": (
                            "ICMP puede estar filtrado aunque el host "
                            "se encuentre funcionando."
                        ),
                    },
                ],
            },

            {
                "id": "traceroute",
                "title": "Traceroute",
                "icon": "🛣",
                "duration": "12 min",

                "objectives": [
                    "Comprender el objetivo de traceroute.",
                    "Interpretar saltos.",
                    "Utilizarlo como herramienta de diagnostico.",
                ],

                "content": """
Traceroute permite observar una aproximacion de los saltos
que sigue el trafico hacia un destino.

En Windows podemos utilizar:

tracert


Ejemplo:

tracert example.com


Cada salto representa normalmente un dispositivo de
enrutamiento que participa en el trayecto observado.


IMPORTANTE

No todos los routers responden a las sondas utilizadas
por traceroute.

Por ello pueden aparecer saltos sin respuesta sin que
necesariamente exista una falla.
                """,

                "key_concepts": [
                    {
                        "term": "Hop",
                        "definition": (
                            "Salto entre dispositivos de enrutamiento."
                        ),
                    },
                    {
                        "term": "Traceroute",
                        "definition": (
                            "Herramienta utilizada para observar "
                            "el trayecto aproximado hacia un destino."
                        ),
                    },
                ],

                "quiz": [
                    {
                        "question": (
                            "¿Como se llama la herramienta equivalente "
                            "a traceroute en Windows?"
                        ),
                        "options": [
                            "tracert",
                            "format",
                            "mkdir",
                            "tasklist",
                        ],
                        "answer": "tracert",
                        "explanation": (
                            "Windows proporciona el comando tracert."
                        ),
                    },
                ],
            },

            {
                "id": "system_network",
                "title": "Configuracion de red del sistema",
                "icon": "💻",
                "duration": "12 min",

                "objectives": [
                    "Identificar IP, gateway y DNS.",
                    "Comprender la importancia del adaptador.",
                    "Relacionar configuracion local con conectividad.",
                ],

                "content": """
Al diagnosticar un computador debemos revisar su
configuracion de red.


DATOS IMPORTANTES

• Direccion IPv4
• Direccion IPv6
• Mascara o prefijo
• Gateway
• Servidores DNS
• Estado del adaptador


En Windows puede utilizarse:

ipconfig

o:

ipconfig /all


NetPro tambien dispone del modulo:

Mi Sistema

que permite visualizar informacion del equipo.
                """,

                "key_concepts": [
                    {
                        "term": "Default Gateway",
                        "definition": (
                            "Dispositivo utilizado normalmente para "
                            "alcanzar redes externas a la subred local."
                        ),
                    }
                ],

                "quiz": [
                    {
                        "question": (
                            "¿Que comando de Windows muestra "
                            "configuracion IP?"
                        ),
                        "options": [
                            "ipconfig",
                            "mkdir",
                            "copy",
                            "tree",
                        ],
                        "answer": "ipconfig",
                        "explanation": (
                            "ipconfig permite consultar configuracion "
                            "IP en Windows."
                        ),
                    },
                ],
            },
        ],
    },

    # ========================================================
    # CURSO 8 - CIBERSEGURIDAD
    # ========================================================

    {
        "id": "security",
        "title": "Fundamentos de Ciberseguridad",
        "icon": "🛡",
        "level": "Principiante",
        "description": (
            "Conoce principios esenciales de seguridad, amenazas, "
            "vulnerabilidades y buenas practicas defensivas."
        ),
        "lessons": [

            {
                "id": "security_basics",
                "title": "Principios de seguridad",
                "icon": "🛡",
                "duration": "12 min",

                "objectives": [
                    "Comprender confidencialidad, integridad y disponibilidad.",
                    "Relacionar controles con riesgos.",
                ],

                "content": """
Tres principios clasicos de seguridad de la informacion son:

CONFIDENCIALIDAD

La informacion debe ser accesible solamente para quienes
tengan autorizacion.


INTEGRIDAD

La informacion debe mantenerse correcta y protegida frente
a modificaciones no autorizadas.


DISPONIBILIDAD

Los sistemas y datos deben estar disponibles cuando sean
necesarios para los usuarios autorizados.


Estos principios suelen conocerse como:

CIA Triad

Confidentiality
Integrity
Availability
                """,

                "key_concepts": [
                    {
                        "term": "Confidencialidad",
                        "definition": (
                            "Proteccion frente al acceso no autorizado."
                        ),
                    },
                    {
                        "term": "Integridad",
                        "definition": (
                            "Proteccion frente a modificaciones "
                            "no autorizadas."
                        ),
                    },
                    {
                        "term": "Disponibilidad",
                        "definition": (
                            "Acceso oportuno a sistemas e informacion."
                        ),
                    },
                ],

                "quiz": [
                    {
                        "question": (
                            "¿Que principio busca evitar modificaciones "
                            "no autorizadas?"
                        ),
                        "options": [
                            "Integridad",
                            "Disponibilidad",
                            "Latencia",
                            "Enrutamiento",
                        ],
                        "answer": "Integridad",
                        "explanation": (
                            "La integridad protege la exactitud y "
                            "consistencia de la informacion."
                        ),
                    },
                ],
            },

            {
                "id": "threat_vulnerability_risk",
                "title": "Amenaza, vulnerabilidad y riesgo",
                "icon": "⚠",
                "duration": "12 min",

                "objectives": [
                    "Diferenciar amenaza y vulnerabilidad.",
                    "Comprender el concepto de riesgo.",
                ],

                "content": """
AMENAZA

Es una circunstancia, actor o evento con potencial para
causar dano.


VULNERABILIDAD

Es una debilidad que podria ser aprovechada.


RIESGO

El riesgo considera la posibilidad de que una amenaza
aproveche una vulnerabilidad y produzca un impacto.


Ejemplo:

Un servidor utiliza software desactualizado.

Software desactualizado:

Puede representar una vulnerabilidad.

Un atacante:

Puede representar una amenaza.

Compromiso del servidor:

Puede ser una consecuencia del riesgo materializado.
                """,

                "key_concepts": [
                    {
                        "term": "Amenaza",
                        "definition": (
                            "Elemento con potencial de causar dano."
                        ),
                    },
                    {
                        "term": "Vulnerabilidad",
                        "definition": (
                            "Debilidad susceptible de ser aprovechada."
                        ),
                    },
                    {
                        "term": "Riesgo",
                        "definition": (
                            "Combinacion de posibilidad e impacto "
                            "asociada a eventos adversos."
                        ),
                    },
                ],

                "quiz": [
                    {
                        "question": (
                            "¿Que es una vulnerabilidad?"
                        ),
                        "options": [
                            "Una debilidad susceptible de ser aprovechada",
                            "Un tipo de direccion IPv6",
                            "Un servidor DNS",
                            "Una mascara de subred",
                        ],
                        "answer": (
                            "Una debilidad susceptible de ser aprovechada"
                        ),
                        "explanation": (
                            "Una vulnerabilidad es una debilidad "
                            "que puede ser aprovechada."
                        ),
                    },
                ],
            },

            {
                "id": "security_practices",
                "title": "Buenas practicas",
                "icon": "✅",
                "duration": "15 min",

                "objectives": [
                    "Conocer practicas defensivas basicas.",
                    "Comprender la importancia de actualizaciones.",
                    "Aplicar minimo privilegio.",
                ],

                "content": """
Algunas buenas practicas generales son:


ACTUALIZACIONES

Mantener sistemas y aplicaciones actualizados.


AUTENTICACION

Utilizar contrasenas robustas y mecanismos adicionales
de autenticacion cuando esten disponibles.


MINIMO PRIVILEGIO

Los usuarios y servicios deben tener solamente los permisos
necesarios para realizar sus funciones.


COPIAS DE SEGURIDAD

Mantener backups adecuados y comprobar su recuperacion.


FIREWALL

Limitar comunicaciones innecesarias.


SERVICIOS

Deshabilitar servicios que no sean necesarios.


MONITOREO

Revisar eventos y comportamientos relevantes.


CAPACITACION

Los usuarios deben conocer riesgos como phishing,
ingenieria social y manejo inadecuado de credenciales.
                """,

                "key_concepts": [
                    {
                        "term": "Minimo privilegio",
                        "definition": (
                            "Asignar solamente los permisos necesarios."
                        ),
                    },
                    {
                        "term": "Backup",
                        "definition": (
                            "Copia de informacion destinada a facilitar "
                            "la recuperacion ante determinados incidentes."
                        ),
                    },
                ],

                "quiz": [
                    {
                        "question": (
                            "¿Que significa el principio de "
                            "minimo privilegio?"
                        ),
                        "options": [
                            "Asignar solamente los permisos necesarios",
                            "Dar permisos de administrador a todos",
                            "Desactivar todas las contrasenas",
                            "Abrir todos los puertos",
                        ],
                        "answer": (
                            "Asignar solamente los permisos necesarios"
                        ),
                        "explanation": (
                            "El minimo privilegio limita permisos "
                            "a los estrictamente necesarios."
                        ),
                    },
                ],
            },

            {
                "id": "ethical_use",
                "title": "Uso etico de herramientas de red",
                "icon": "⚖",
                "duration": "10 min",

                "objectives": [
                    "Comprender la importancia de la autorizacion.",
                    "Utilizar NetPro con fines educativos y defensivos.",
                ],

                "content": """
Las herramientas de diagnostico de red son utiles para:

• Administracion
• Soporte tecnico
• Aprendizaje
• Inventario
• Diagnostico
• Seguridad defensiva


Sin embargo, algunas acciones pueden generar trafico hacia
otros sistemas.

Antes de realizar pruebas debes verificar que:

• El sistema sea tuyo

o

• Tengas autorizacion para analizarlo


El objetivo de NetPro es apoyar el aprendizaje,
diagnostico y comprension de redes.

La informacion obtenida debe interpretarse responsablemente.
                """,

                "warning": (
                    "No utilices las herramientas de NetPro para "
                    "analizar infraestructura ajena sin autorizacion."
                ),

                "key_concepts": [
                    {
                        "term": "Autorizacion",
                        "definition": (
                            "Permiso para realizar una actividad "
                            "sobre un sistema o infraestructura."
                        ),
                    }
                ],

                "quiz": [
                    {
                        "question": (
                            "¿Cuando es apropiado analizar un sistema?"
                        ),
                        "options": [
                            "Cuando es propio o existe autorizacion",
                            "Siempre que tenga Internet",
                            "Cuando conozco su direccion IP",
                            "Siempre que el puerto 443 este abierto",
                        ],
                        "answer": (
                            "Cuando es propio o existe autorizacion"
                        ),
                        "explanation": (
                            "Las pruebas deben realizarse sobre sistemas "
                            "propios o con autorizacion."
                        ),
                    },
                ],
            },
        ],
    },
]


# ============================================================
# FUNCIONES DE CONSULTA
# ============================================================


def get_courses():
    """
    Devuelve todos los cursos disponibles.
    """

    return COURSES


def get_course(course_id):
    """
    Busca un curso por su identificador.
    """

    for course in COURSES:

        if course["id"] == course_id:

            return course

    return None


def get_lesson(course_id, lesson_id):
    """
    Busca una leccion dentro de un curso.
    """

    course = get_course(course_id)

    if course is None:

        return None

    for lesson in course.get("lessons", []):

        if lesson["id"] == lesson_id:

            return lesson

    return None


def get_all_lessons():
    """
    Devuelve todas las lecciones en una sola lista.
    """

    lessons = []

    for course in COURSES:

        for lesson in course.get("lessons", []):

            lessons.append(
                {
                    "course_id": course["id"],
                    "course_title": course["title"],
                    **lesson,
                }
            )

    return lessons


def get_learning_stats():
    """
    Devuelve estadisticas generales del contenido educativo.
    """

    total_courses = len(COURSES)

    total_lessons = sum(
        len(course.get("lessons", []))
        for course in COURSES
    )

    total_questions = 0

    for course in COURSES:

        for lesson in course.get("lessons", []):

            total_questions += len(
                lesson.get("quiz", [])
            )

    return {
        "courses": total_courses,
        "lessons": total_lessons,
        "questions": total_questions,
    }


def search_lessons(text):
    """
    Busca lecciones por titulo o contenido.
    """

    text = text.lower().strip()

    if not text:

        return []

    results = []

    for course in COURSES:

        for lesson in course.get("lessons", []):

            title = lesson.get(
                "title",
                ""
            ).lower()

            content = lesson.get(
                "content",
                ""
            ).lower()

            if (
                text in title
                or text in content
            ):

                results.append(
                    {
                        "course_id": course["id"],
                        "course_title": course["title"],
                        "lesson": lesson,
                    }
                )

    return results


# ============================================================
# PRUEBA DEL ARCHIVO
# ============================================================

if __name__ == "__main__":

    stats = get_learning_stats()

    print()
    print("=" * 60)
    print("NETPRO - MODULO DE APRENDIZAJE")
    print("=" * 60)

    print(
        f"Cursos: {stats['courses']}"
    )

    print(
        f"Lecciones: {stats['lessons']}"
    )

    print(
        f"Preguntas: {stats['questions']}"
    )

    print()

    for course in COURSES:

        print(
            f"{course['icon']} "
            f"{course['title']} "
            f"- {course['level']}"
        )

        for number, lesson in enumerate(
            course.get(
                "lessons",
                []
            ),
            start=1
        ):

            print(
                f"   {number}. "
                f"{lesson.get('icon', '📘')} "
                f"{lesson['title']} "
                f"({lesson.get('duration', '')})"
            )

        print()

    print("=" * 60)