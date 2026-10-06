import ipaddress


def analizar_subred(ip: str, cidr: int) -> dict:
    """
    Analiza una dirección IPv4 y su prefijo CIDR.
    Devuelve los datos principales de la subred.
    """

    # Creamos la interfaz IPv4.
    # strict=False permite introducir una IP de host,
    # por ejemplo 192.168.10.37/24.
    interfaz = ipaddress.ip_interface(f"{ip}/{cidr}")

    direccion = interfaz.ip
    red = interfaz.network

    # Información principal
    network_address = red.network_address
    broadcast_address = red.broadcast_address
    netmask = red.netmask
    hostmask = red.hostmask

    # Hosts utilizables
    if red.prefixlen <= 30:
        first_host = network_address + 1
        last_host = broadcast_address - 1
        usable_hosts = red.num_addresses - 2

    elif red.prefixlen == 31:
        # /31 tiene un tratamiento especial y se usa,
        # entre otros casos, en enlaces punto a punto.
        first_host = network_address
        last_host = broadcast_address
        usable_hosts = 2

    else:
        # /32 representa una sola dirección.
        first_host = direccion
        last_host = direccion
        usable_hosts = 1

    return {
        "ip": str(direccion),
        "cidr": f"/{red.prefixlen}",
        "network": str(network_address),
        "netmask": str(netmask),
        "wildcard": str(hostmask),
        "broadcast": str(broadcast_address),
        "first_host": str(first_host),
        "last_host": str(last_host),
        "total_addresses": red.num_addresses,
        "usable_hosts": usable_hosts,
        "private": direccion.is_private,
        "version": direccion.version,
    }

if __name__ == "__main__":
    resultado = analizar_subred("192.168.10.37", 24)

    for clave, valor in resultado.items():
        print(f"{clave}: {valor}")