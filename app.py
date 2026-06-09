import os
import requests
from flask import Flask, redirect

app = Flask(__name__)

@app.route("/telefe")
def telefe():
    print("[+] Petición recibida en /telefe. Ejecutando redirección directa...")
    
    # URL oficial directa del streaming
    url_directa = "https://telefe-live-akamai.akamaized.net/hls/live/2034220/telefetv/master.m3u8"
    
    # Intentamos una ráfaga rápida a la API de Telefe (máximo 2 segundos de espera)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Origin": "https://mitelefe.com",
            "Referer": "https://mitelefe.com/"
        }
        # Hacemos una consulta ultra veloz para validar el estado
        respuesta = requests.get("https://server.mitelefe.com/api/v1/channels/telefe/stream", headers=headers, timeout=2)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            if "streamUrl" in datos:
                print("[+] URL dinámica obtenida con éxito.")
                return redirect(datos["streamUrl"])
    except Exception as e:
        print(f"[-] API lenta o bloqueada: {str(e)}. Usando respaldo inmediato.")
    
    # Si la API tarda más de 2 segundos, redirigimos instantáneamente para evitar el Timeout de Railway
    return redirect(url_directa)

@app.route("/")
def index():
    return "Servidor Proxy Activo. Dirígete a /telefe para el streaming.", 200

if __name__ == "__main__":
    # Railway inyecta el puerto dinámico en la variable PORT, si no existe usa el 5000
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)
