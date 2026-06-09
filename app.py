import os
import requests
from flask import Flask, redirect, jsonify

app = Flask(__name__)

HEADERS_TV = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Origin": "https://mitelefe.com",
    "Referer": "https://mitelefe.com/"
}

@app.route("/telefe")
def telefe():
    print("[+] Procesando solicitud de streaming sobre enlace directo...")
    
    # Enlace de distribución directa de Paramount/Telefe libre de bloqueos de DNS NXDOMAIN
    url_directa_ok = "https://telefe.cdn.telefe.com/live/telefetv/master.m3u8"
    
    try:
        # Intentamos consultar la API interna por si nos da un token extra en 1.5 segundos
        respuesta = requests.get(
            "https://server.mitelefe.com/api/v1/channels/telefe/stream", 
            headers=HEADERS_TV, 
            timeout=1.5
        )
        if respuesta.status_code == 200:
            datos = respuesta.json()
            url_dinamica = datos.get("streamUrl") or datos.get("url")
            if url_dinamica and "akamaized" not in url_dinamica:
                print(f"[+] URL Dinámica válida obtenida: {url_dinamica}")
                return redirect(url_dinamica)
                
    except Exception as e:
        print(f"[-] API lenta o protegida: {str(e)}. Derivando a CDN abierto.")
    
    # Retorno inmediato al CDN alternativo que sí resuelve el DNS correctamente
    return redirect(url_directa_ok)

@app.route("/")
def index():
    return jsonify({"status": "online", "service": "patapatatvd-proxy"}), 200

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=False)
