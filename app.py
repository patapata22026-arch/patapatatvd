import os
import requests
from flask import Flask, redirect

app = Flask(__name__)

def obtener_streaming_vivo():
    print("[+] Consultando API de distribución de Telefe...")
    
    # Endpoint oficial de la API de Telefe para transmisiones en vivo
    url_api = "https://server.mitelefe.com/api/v1/channels/telefe/stream"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Smart TV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Origin": "https://mitelefe.com",
        "Referer": "https://mitelefe.com/"
    }
    
    try:
        # Petición GET directa a la API (devuelve JSON, consume 0 RAM y responde en milisegundos)
        respuesta = requests.get(url_api, headers=headers, timeout=5)
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            # La API entrega la URL limpia del m3u8 dentro de la estructura de datos
            if "streamUrl" in datos:
                url_m3u8 = datos["streamUrl"]
                print(f"[+] Enlace obtenido con éxito de la API: {url_m3u8}")
                return url_m3u8
            elif "url" in datos:
                return datos["url"]
                
        # En caso de que la API principal esté saturada, usamos el endpoint alternativo de Paramount
        print("[-] API principal no retornó JSON esperado. Usando ruta de respaldo...")
        return "https://telefe-live-akamai.akamaized.net/hls/live/2034220/telefetv/master.m3u8"
        
    except Exception as e:
        print(f"[-] Error al consultar la API: {str(e)}")
        # URL cruda de contingencia para evitar que el script se rompa
        return "https://telefe-live-akamai.akamaized.net/hls/live/2034220/telefetv/master.m3u8"

@app.route("/telefe")
def telefe():
    url_final = obtener_streaming_vivo()
    print(f"[+] Redirigiendo cliente a: {url_final}")
    return redirect(url_final)

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)
