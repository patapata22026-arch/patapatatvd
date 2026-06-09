import os
from flask import Flask, redirect, jsonify

app = Flask(__name__)

@app.route("/telefe")
def telefe():
    print("[+] Desviando tráfico al flujo de distribución abierto de TDA...")
    
    # URL directa de la señal alternativa de Telefe de la lista unificada de IPTV de código abierto.
    # Este flujo está optimizado para reproductores directos (VLC, IPTV, etc.) y no se bloquea por DNS.
    url_iptv_estable = "https://televisionlibre.net/tv/telefe.html" 
    
    # Como respaldo directo en formato m3u8 puro para VLC si el reproductor soporta flujos crudos directos de red:
    url_m3u8_directo = "https://live-edge01.telefe.com/live/telefetv/master.m3u8"
    
    # Redirigimos al cliente directamente al flujo optimizado que salta el firewall perimetral
    return redirect(url_m3u8_directo)

@app.route("/")
def index():
    return jsonify({
        "status": "online",
        "canal": "Telefe Proxy",
        "instrucciones": "Conéctate a /telefe desde tu reproductor"
    }), 200

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=False)
