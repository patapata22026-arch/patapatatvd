import os
import re
import requests
from flask import Flask, redirect

app = Flask(__name__)

def obtener_token_directo():
    print("[+] Conectando directamente con el sistema de distribucion de Telefe...")
    
    # URL de la API de streams oficiales o del manifiesto master directo de Akamai
    # Usamos la ruta directa del CDN de Telefe que no requiere carga de interfaz visual
    url_stream = "https://telefe-live-akamai.akamaized.net/hls/live/2034220/telefetv/master.m3u8"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://mitelefe.com/",
        "Origin": "https://mitelefe.com"
    }
    
    try:
        # Validamos si el CDN de Akamai responde correctamente
        session = requests.Session()
        respuesta = session.head(url_stream, headers=headers, timeout=8)
        
        # Si el CDN responde con éxito (200 o 302), devolvemos la URL directa inmediatamente
        if respuesta.status_code in [200, 301, 302]:
            print(f"[+] Canal verificado en CDN de Akamai. Codigo: {respuesta.status_code}")
            return url_stream
            
        # Si requiere cookies de sesion previas, hacemos el apretón de manos (handshake) con el sitio web
        print("[-] CDN directo requiere sesion activa. Realizando apreton de manos...")
        session.get("https://mitelefe.com/", headers=headers, timeout=8)
        
        # Reintentamos la comprobacion con la sesion inyectada
        segundo_intento = session.head(url_stream, headers=headers, timeout=8)
        if segundo_intento.status_code in [200, 302]:
            return url_stream
            
        # Si falla el HEAD pero aun asi el stream esta activo, lo devolvemos para el reproductor IPTV
        return url_stream

    except Exception as e:
        print(f"[-] Caída en la resolución de red: {str(e)}")
        # Retorno de contingencia directa (Hardcoded Stream para reproductores como VLC/IPTV)
        return "https://telefe-live-akamai.akamaized.net/hls/live/2034220/telefetv/master.m3u8"

@app.route("/telefe")
def telefe():
    url_final = obtener_token_directo()
    if url_final:
        print(f"[+] Redireccionando flujo m3u8 directo a destino: {url_final}")
        return redirect(url_final)
    else:
        return "Error: No se pudo enlazar el flujo de la API de Telefe.", 500

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)
