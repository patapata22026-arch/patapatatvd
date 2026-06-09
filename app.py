import os
import requests
from flask import Flask, redirect, jsonify

app = Flask(__name__)

# Definimos las cabeceras globales para simular un reproductor autorizado
HEADERS_TV = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; BRAVIA 4K HCD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
    "Origin": "https://mitelefe.com",
    "Referer": "https://mitelefe.com/"
}

@app.route("/telefe")
def telefe():
    print("[+] Procesando solicitud de streaming...")
    url_respaldo = "https://telefe-live-akamai.akamaized.net/hls/live/2034220/telefetv/master.m3u8"
    
    try:
        # Hacemos una consulta ultra veloz con tiempo límite estricto de 1.5 segundos
        respuesta = requests.get(
            "https://server.mitelefe.com/api/v1/channels/telefe/stream", 
            headers=HEADERS_TV, 
            timeout=1.5
        )
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            url_dinamica = datos.get("streamUrl") or datos.get("url")
            if url_dinamica:
                print(f"[+] URL Dinámica obtenida: {url_dinamica}")
                return redirect(url_dinamica)
                
    except Exception as e:
        print(f"[-] API fuera de rango o con demora: {str(e)}. Derivando a CDN directo.")
    
    # Retorno inmediato de contingencia. Evita que Railway mate el contenedor por congelamiento
    return redirect(url_respaldo)

@app.route("/")
def index():
    return jsonify({"status": "online", "service": "patapatatvd-proxy"}), 200

if __name__ == "__main__":
    # Captura el puerto asignado por la infraestructura de Railway de forma nativa
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=False)
