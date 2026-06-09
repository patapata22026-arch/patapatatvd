
import os
import requests
from flask import Flask, Response

app = Flask(__name__)

# URL del Manifiesto Maestro Oficial de Telefe dentro de la red abierta de Paramount (Pluto TV)
URL_PLUTO_TELEFE = "https://images.pluto.tv/channels/64b036577df0720008b8b39d/featured/master.m3u8"

HEADERS_PARAMOUNT = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

def estructurar_m3u8_absoluto(url_origen):
    try:
        # Railway descarga el archivo maestro limpio de la red de Paramount
        respuesta = requests.get(url_origen, headers=HEADERS_PARAMOUNT, timeout=5)
        if respuesta.status_code != 200:
            return None
        
        lineas = respuesta.text.splitlines()
        lineas_reparadas = []
        
        # Extraemos la ruta base para inyectarla de forma absoluta
        # Ejemplo: https://images.pluto.tv/channels/64b036577df0720008b8b39d/featured
        ruta_base = url_origen.rsplit('/', 1)[0]
        
        for linea in lineas:
            linea_limpia = linea.strip()
            if not linea_limpia:
                continue
            
            if linea_limpia.startswith("#"):
                lineas_reparadas.append(linea_limpia)
            elif linea_limpia.startswith("http"):
                lineas_reparadas.append(linea_limpia)
            else:
                # Corregimos las sub-playlists para que VLC no las busque en Railway
                if linea_limpia.startswith("/"):
                    lineas_reparadas.append(f"https://images.pluto.tv{linea_limpia}")
                else:
                    lineas_reparadas.append(f"{ruta_base}/{linea_limpia}")
                    
        return "\n".join(lineas_reparadas)
    except Exception as e:
        print(f"[-] Error en el procesador: {str(e)}")
        return None

@app.route("/telefe")
def telefe():
    print("[+] Procesando la señal unificada de Telefe en la red de Paramount...")
    
    # Generamos el mapa HLS con rutas absolutas e inmunes
    manifiesto_final = estructurar_m3u8_absoluto(URL_PLUTO_TELEFE)
    
    if manifiesto_final:
        return Response(
            manifiesto_final,
            mimetype="application/vnd.apple.mpegurl",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Content-Disposition": "inline; filename=telefe.m3u8"
            }
        )
    
    # En caso de una lentitud extrema, devolvemos un redireccionamiento crudo de emergencia
    return (
        "#EXTM3U\n"
        "#EXT-X-VERSION:3\n"
        "#EXT-X-STREAM-INF:BANDWIDTH=3000000\n"
        f"{URL_PLUTO_TELEFE}\n"
    ), 200, {"Content-Type": "application/vnd.apple.mpegurl"}

@app.route("/")
def index():
    return "Orquestador HLS Paramount Activo - Modo Estable", 200

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=False)
