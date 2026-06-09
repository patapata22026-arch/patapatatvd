import os
import requests
from flask import Flask, Response, request

app = Flask(__name__)

DOMINIO_ORIGEN = "https://wms.teledifusora.com.ar"
URL_M3U8_PADRE = f"{DOMINIO_ORIGEN}/telefe/telefe.m3u8"

def reescribir_manifiesto(url_objetivo):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": f"{DOMINIO_ORIGEN}/"
    }
    try:
        respuesta = requests.get(url_objetivo, headers=headers, timeout=5)
        if respuesta.status_code != 200:
            return None
        
        lineas = respuesta.text.splitlines()
        lineas_convertidas = []
        
        # Obtenemos la ruta base para resolver archivos relativos
        ruta_base = url_objetivo.rsplit('/', 1)[0]
        
        for linea in lineas:
            linea_limpia = linea.strip()
            if not linea_limpia:
                continue
            
            # Si es una línea de contenido (no un tag de configuración) y no es una URL absoluta
            if not linea_limpia.startswith("#") and not linea_limpia.startswith("http"):
                if linea_limpia.startswith("/"):
                    # Si apunta a la raíz del servidor de origen
                    lineas_convertidas.append(f"{DOMINIO_ORIGEN}{linea_limpia}")
                else:
                    # Si es una ruta relativa al directorio actual
                    lineas_convertidas.append(f"{ruta_base}/{linea_limpia}")
            else:
                lineas_convertidas.append(linea_limpia)
                
        return "\n".join(lineas_convertidas)
    except Exception as e:
        print(f"[-] Error procesando manifiesto: {str(e)}")
        return None

@app.route("/telefe")
def telefe():
    print("[+] Extrayendo y reestructurando segmentos HLS...")
    
    # Pasamos el archivo m3u8 principal por la reescritura de rutas
    manifiesto_final = reescribir_manifiesto(URL_M3U8_PADRE)
    
    if manifiesto_final:
        return Response(
            manifiesto_final,
            mimetype="application/vnd.apple.mpegurl",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Content-Disposition": "inline; filename=telefe.m3u8"
            }
        )
    
    return "Error: No se pudo parsear el mapa de segmentos del stream.", 502

@app.route("/")
def index():
    return "Reescritor de Manifiestos HLS Activo", 200

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=False)
