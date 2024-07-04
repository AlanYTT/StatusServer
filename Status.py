import re
import requests

def obtener_informacion_servidor(ip, puerto, edicion):
    if edicion.lower() == "java":
        url_servidor = f"https://api.mcsrvstat.us/2/{ip}:{puerto}"
    elif edicion.lower() == "bedrock":
        url_servidor = f"https://api.mcsrvstat.us/bedrock/2/{ip}:{puerto}"
    else:
        return "Edición no válida. Por favor, ingresa 'java' o 'bedrock'."

    try:
        response = requests.get(url_servidor)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return f"No se pudo obtener información del servidor. Código de estado: {response.status_code}"
    except Exception as e:
        return f"Ocurrió un error al obtener información del servidor: {str(e)}"

def resaltar_colores_mensaje(mensaje):
    pattern = re.compile("(§[0-9a-fk-or])")
    color_mapping = {
        "§0": "\033[30m",  # Negro
        "§1": "\033[34m",  # Azul oscuro
        "§2": "\033[32m",  # Verde oscuro
        "§3": "\033[36m",  # Azul claro
        "§4": "\033[31m",  # Rojo oscuro
        "§5": "\033[35m",  # Púrpura
        "§6": "\033[33m",  # Amarillo
        "§7": "\033[37m",  # Gris claro
        "§8": "\033[90m",  # Gris oscuro
        "§9": "\033[94m",  # Azul claro
        "§a": "\033[92m",  # Verde claro
        "§b": "\033[96m",  # Azul claro
        "§c": "\033[91m",  # Rojo claro
        "§d": "\033[95m",  # Rosa
        "§e": "\033[93m",  # Amarillo claro
        "§f": "\033[97m",  # Blanco
        "§k": "",           # Texto parpadeante (ignorado)
        "§l": "\033[1m",    # Texto en negrita
        "§m": "\033[9m",    # Texto tachado
        "§n": "\033[4m",    # Texto subrayado
        "§o": "\033[3m",    # Texto en cursiva
        "§r": "\033[0m"     # Restablece el formato del texto al predeterminado
    }
    mensaje_resaltado = pattern.sub(lambda x: color_mapping.get(x.group(0), ""), mensaje)
    mensaje_resaltado += "\033[0m"
    return mensaje_resaltado

def mostrar_informacion_servidor(informacion):
    if not informacion.get("online"):
        print(resaltar_colores_mensaje("§6~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n §cEl Servidor Esta off§6\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"))
        return

    print(resaltar_colores_mensaje("§6~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"))
    print(resaltar_colores_mensaje(f"§aIP numerica:§9 {informacion['ip']}"))
    print(resaltar_colores_mensaje(f"§aPuerto:§9 {informacion['port']}\n"))

    print(resaltar_colores_mensaje("MOTD:"))
    motd = informacion['motd']['raw']
    for line in motd:
        print(resaltar_colores_mensaje(line))
    print()

    print(resaltar_colores_mensaje("§aJugadores:"))
    print(resaltar_colores_mensaje(f"§aEn línea:§e {informacion['players']['online']}"))
    print(resaltar_colores_mensaje(f"§aMáximo:§e {informacion['players']['max']}\n"))

    print(resaltar_colores_mensaje(f"§9Versión:§a {informacion['version']}"))
    print(resaltar_colores_mensaje(f"§9Online:§a {informacion['online']}"))
    print(resaltar_colores_mensaje(f"§9Protocolo:§a {informacion['protocol']}"))
    print(resaltar_colores_mensaje(f"Dominio:§a {informacion['hostname']}"))
    print(resaltar_colores_mensaje(f"§6~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"))

if __name__ == "__main__":
    ip = input(resaltar_colores_mensaje("§eIngrese la dirección IP del servidor: "))
    puerto = input(resaltar_colores_mensaje("§bIngrese el puerto del servidor: "))
    edicion = input(resaltar_colores_mensaje("Ingrese la edición del servidor (java/bedrock): "))
    informacion = obtener_informacion_servidor(ip, puerto, edicion)
    if isinstance(informacion, dict):
        mostrar_informacion_servidor(informacion)
    else:
        print(resaltar_colores_mensaje(f"§c{informacion}"))

print(resaltar_colores_mensaje("§cYouTube: §f@alanYTT"))
