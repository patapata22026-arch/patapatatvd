import os
import requests
from flask import Flask, Response, stream_with_context

app = Flask(__name__)

HEADERS_OFICIALES = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://mitelefe.com/",
    "Origin": "https://mitelefe.com"
}

@app.route("/telefe")
def telefe():
    print("[+] Modo Proxy Activo: Transmitiendo datos de forma directa sin redirección...")
    
    # URL directa de origen (El servidor de Railway sí tiene acceso al handshake de red)
    url_origen = "https://telefe.cdn.telefe.com/live/telefetv/master.m3u8"
    
    try:
        # El servidor de Railway realiza la petición en segundo plano
        req = requests.get(url_origen, headers=HEADERS_OFICIALES, stream=True, timeout=5)
        
        # Si el CDN responde, encapsulamos el flujo y se lo reenviamos al usuario en tiempo real
        if req.status_code == 200:
            def generar_stream():
                for fragmento in req.iter_content(chunk_size=4096):
                    yield fragmento
            
            # Devolvemos el archivo m3u8 original simulando que lo generó nuestro propio servidor
            return Response(
                stream_with_context(generar_stream()),
                content_type="application/vnd.apple.mpegurl"
            )
            
    except Exception as e:
        print(f"[-] Error en el puente del Proxy: {str(e)}")
        
    # Ruta alternativa de contingencia si el CDN principal falla
    try:
        url_respaldo = "https://telefe-live-akamai.akamaized.net/hls/live/2034220/telefetv/master.m3u8"
        req_alt = requests.get(url_respaldo, headers=HEADERS_OFICIALES, stream=True, timeout=5)
        if req_alt.status_code == 200:
            return Response(stream_with_context(lambda: req_alt.iter_content(chunk_size=4096))(), content_type="application/vnd.apple.mpegurl")
    except:
        pass

    return "Error de enlace: El sistema de protección perimetral de Telefe no validó la sesión.", 503

@app.route("/")
def index():
    return "Proxy de Video Activo v2.0", 200

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=False)
