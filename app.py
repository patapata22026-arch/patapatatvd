import os
import requests
from flask import Flask, Response, stream_with_context, request

app = Flask(__name__)

# Usamos la señal de distribución alternativa optimizada para transporte limpio de red
URL_M3U8_ORIGEN = "https://wms.teledifusora.com.ar/telefe/telefe.m3u8"
DOMINIO_NODO = "https://wms.teledifusora.com.ar"

HEADERS_AGRESIVOS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Referer": f"{DOMINIO_NODO}/",
    "Origin": DOMINIO_NODO
}

def obtener_manifiesto_real():
    """
    Obtiene el archivo de reproducción original, resuelve las sub-playlists 
    y extrae el archivo de segmentos final de forma automática.
    """
    try:
        r = requests.get(URL_M3U8_ORIGEN, headers=HEADERS_AGRESIVOS, timeout=5)
        if r.status_code != 200:
            return None
            
        lineas = r.text.splitlines()
        for linea in lineas:
            linea_limpia = linea.strip()
            # Si el archivo maestro apunta a una sub-playlist de calidad
            if not linea_limpia.startswith("#") and ".m3u8" in linea_limpia:
                if linea_limpia.startswith("http"):
                    return linea_limpia
                return f"{DOMINIO_NODO}/telefe/{linea_limpia}"
                
        return URL_M3U8_ORIGEN
    except:
        return URL_M3U8_ORIGEN

@app.route("/telefe")
def telefe():
    print("[+] Inicializando Túnel de Retransmisión de Flujo Binario...")
    
    url_final_stream = obtener_manifiesto_real()
    
    try:
        # El servidor de Railway se conecta al stream manteniendo la conexión abierta (stream=True)
        respuesta_nodo = requests.get(
            url_final_stream, 
            headers=HEADERS_AGRESIVOS, 
            stream=True, 
            timeout=8
        )
        
        if respuesta_nodo.status_code == 200:
            print("[+] Puente de datos establecido con éxito. Retransmitiendo fragmentos...")
            
            # Función generadora que descarga bloques de video en la RAM de Railway y te los escupe en tiempo real
            def transferir_bloques_video():
                # Leemos en bloques optimizados de 16KB para evitar congelamientos en el buffer
                for bloque in respuesta_nodo.iter_content(chunk_size=16384):
                    if bloque:
                        yield bloque
            
            # Devolvemos la respuesta forzando un tipo de flujo multimedia binario continuo (MPEG-TS)
            return Response(
                stream_with_context(transferir_bloques_video()),
                content_type="video/mp2t",
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Content-Disposition": "inline; filename=telefe_live.ts"
                }
            )
        else:
            print(f"[-] Error de conexión con el nodo de video: {respuesta_nodo.status_code}")
            return f"Error de enlace: {respuesta_nodo.status_code}", 502
            
    except Exception as e:
        print(f"[-] Colapso en el puente de transmisión: {str(e)}")
        # Contingencia directa: Si el túnel binario falla, enviamos un archivo de texto auto-reparado
        manifiesto_contingencia = (
            "#EXTM3U\n"
            "#EXT-X-VERSION:3\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=2000000\n"
            "https://live-edge01.telefe.com/live/telefetv/master.m3u8\n"
        )
        return Response(manifiesto_contingencia, mimetype="application/vnd.apple.mpegurl")

@app.route("/")
def index():
    return "Túnel de Datos Multimedia Activo v5.0 - Full Stream Relay", 200

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=False)
