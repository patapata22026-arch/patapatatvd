import os
import requests
from flask import Flask, Response, stream_with_context

app = Flask(__name__)

# Configuración del origen estable (Señal alternativa directa sin tokens complejos)
URL_STREAM_CRUDO = "https://wms.teledifusora.com.ar/telefe/telefe.m3u8"

HEADERS_REQUISITO = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://wms.teledifusora.com.ar/",
    "Origin": "https://wms.teledifusora.com.ar"
}

@app.route("/telefe")
def telefe():
    print("[+] Modo Full-Tunnel Activo. Solicitando flujo de datos al nodo central...")
    
    try:
        # El servidor de Railway realiza la petición manteniendo la conexión abierta (stream=True)
        # e inyectando las credenciales perimetrales correctas.
        respuesta_nodo = requests.get(
            URL_STREAM_CRUDO, 
            headers=HEADERS_REQUISITO, 
            stream=True, 
            timeout=8
        )
        
        # Validamos que el nodo de video responda con éxito
        if respuesta_nodo.status_code == 200:
            print("[+] Conexión establecida con el nodo de origen. Retransmitiendo...")
            
            # Función generadora interna que descarga y escupe los fragmentos binarios al instante
            def transferir_datos():
                # Leemos en bloques pequeños de 8KB para optimizar la latencia y no saturar la RAM de Railway
                for bloque in respuesta_nodo.iter_content(chunk_size=8192):
                    if bloque:
                        yield bloque
            
            # Retornamos el flujo crudo simulando un archivo de transporte continuo MPEG
            return Response(
                stream_with_context(transferir_datos()),
                content_type="video/mp2t", # Forzamos formato binario de transporte multimedia
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Content-Disposition": "inline; filename=stream.ts"
                }
            )
        else:
            print(f"[-] Nodo rechazó la conexión. Código de estado: {respuesta_nodo.status_code}")
            return f"Error de enlace con el nodo de origen: {respuesta_nodo.status_code}", 502
            
    except Exception as e:
        print(f"[-] Colapso en el puente de transmisión: {str(e)}")
        return f"Error crítico en el túnel de infraestructura: {str(e)}", 500

@app.route("/")
def index():
    return "Túnel de Infraestructura Multimedia Activo v3.0", 200

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=False)
