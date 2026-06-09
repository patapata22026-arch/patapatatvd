import os
from flask import Flask, Response

app = Flask(__name__)

@app.route("/telefe")
def telefe():
    print("[+] Generando manifiesto HLS dinámico estructurado para el cliente...")
    
    # Usamos las URL de los chunks oficiales que el reproductor de Telefe distribuye.
    # Al estructurarlo de esta manera, el reproductor de IPTV del usuario final (en su casa)
    # será el que le pida el video a Telefe con su IP residencial, burlando el bloqueo perimetral.
    
    manifiesto_m3u8 = (
        "#EXTM3U\n"
        "#EXT-X-VERSION:3\n"
        "#EXT-X-STREAM-INF:BANDWIDTH=3000000,RESOLUTION=1280x720\n"
        "https://telefe-live-akamai.akamaized.net/hls/live/2034220/telefetv/master.m3u8\n"
        "#EXT-X-STREAM-INF:BANDWIDTH=1500000,RESOLUTION=854x480\n"
        "https://telefe.cdn.telefe.com/live/telefetv/master.m3u8\n"
    )
    
    # Devolvemos el texto plano pero con el tipo de contenido (MIME-Type) oficial de Apple HLS Stream
    return Response(
        manifiesto_m3u8,
        mimetype="application/vnd.apple.mpegurl",
        headers={"Content-Disposition": "inline; filename=telefe.m3u8"}
    )

@app.route("/")
def index():
    return "Estructurador M3U8 de Telefe Online", 200

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=False)
