import os
import requests
from flask import Flask, Response

app = Flask(__name__)

# Nodo central oficial de Telefe para la distribución de señales digitales
URL_MASTER_TELEFE = "https://live-edge01.telefe.com/live/telefetv/master.m3u8"

HEADERS_PROXIES = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://mitelefe.com/",
    "Origin": "https://mitelefe.com"
}

def procesar_y_reparar_m3u8(url_origen):
    try:
        # El servidor de Railway descarga el manifiesto original directo de Telefe
        respuesta = requests.get(url_origen, headers=HEADERS_PROXIES, timeout=6)
        if respuesta.status_code != 200:
            return None
        
        lineas = respuesta.text.splitlines()
        lineas_reparadas = []
        
        # Extraemos la ruta base para convertir las rutas relativas en absolutas
        # Ejemplo de ruta_base: https://live-edge01.telefe.com/live/telefetv
        ruta_base = url_origen.rsplit('/', 1)[0]
        
        for linea in lineas:
            linea_limpia = linea.strip()
            if not linea_limpia:
                continue
            
            # Si es un tag de configuración de HLS, se pasa idéntico
            if linea_limpia.startswith("#"):
                lineas_reparadas.append(linea_limpia)
            # Si ya es una URL absoluta, se deja como está
            elif linea_limpia.startswith("http"):
                lineas_reparadas.append(linea_limpia)
            # ¡Acá está la magia! Si es una ruta relativa, le inyectamos el dominio original al frente
            else:
                if linea_limpia.startswith("/"):
                    # Si viene desde la raíz del servidor
                    lineas_reparadas.append(f"https://live-edge01.telefe.com{linea_limpia}")
                else:
                    # Si es relativa al directorio del stream
                    lineas_reparadas.append(f"{ruta_base}/{linea_limpia}")
                    
        return "\n".join(lineas_reparadas)
    except Exception as e:
        print(f"[-] Error en el motor de parseo: {str(e)}")
        return None

@app.route("/telefe")
def telefe():
    print("[+] Petición recibida. Ejecutando ingeniería inversa sobre el manifiesto de Telefe...")
    
    # Obtenemos la lista de reproducción con todas sus sub-rutas reparadas a nivel absoluto
    manifiesto_arreglado = procesar_y_reparar_m3u8(URL_MASTER_TELEFE)
    
    if manifiesto_arreglado:
        print("[+] Manifiesto reconstruido con éxito. Transmitiendo al reproductor cliente.")
        return Response(
            manifiesto_arreglado,
            mimetype="application/vnd.apple.mpegurl",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Content-Disposition": "inline; filename=telefe.m3u8"
            }
        )
    
    # En caso de una caída masiva del nodo primario, mandamos un archivo M3U8 genérico de escape
    manifiesto_contingencia = (
        "#EXTM3U\n"
        "#EXT-X-VERSION:3\n"
        "#EXT-X-STREAM-INF:BANDWIDTH=2000000\n"
        "https://live-edge01.telefe.com/live/telefetv/master.m3u8\n"
    )
    return Response(manifiesto_contingencia, mimetype="application/vnd.apple.mpegurl")

@app.route("/")
def index():
    return "Orquestador de Video HLS Activo v4.0 - Modo Estable", 200

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=False)
