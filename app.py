import os
from flask import Flask, Response

app = Flask(__name__)

@app.route("/telefe")
def telefe():
    print("[+] Generando enlace de transporte directo libre de tokens...")
    
    # Este enlace apunta directamente al servidor EDGE de streaming crudo de la red de canales públicos.
    # No requiere handshake de JavaScript, cookies web ni validación perimetral.
    enlace_limpio = "https://wms.teledifusora.com.ar/telefe/telefe.m3u8"
    
    manifiesto_m3u8 = (
        "#EXTM3U\n"
        "#EXT-X-VERSION:3\n"
        "#EXT-X-STREAM-INF:BANDWIDTH=2500000,RESOLUTION=1280x720\n"
        f"{enlace_limpio}\n"
    )
    
    return Response(
        manifiesto_m3u8,
        mimetype="application/vnd.apple.mpegurl",
        headers={
            "Content-Disposition": "inline; filename=telefe.m3u8",
            "Access-Control-Allow-Origin": "*"
        }
    )

@app.route("/")
def index():
    return "Distribuidor de Flujo de Video Activo", 200

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=False)
