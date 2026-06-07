import os
import time
import json
from flask import Flask, Response, redirect
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

app = Flask(__name__)

def obtener_token_fresco():
    print("[+] Iniciando busqueda de token con Chrome en contenedor...")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    # Conecta directo con el Chrome preinstalado de la imagen
    driver = webdriver.Chrome(options=options)
    
    url_objetivo = "https://mitelefe.com/"
    driver.get(url_objetivo)
    
    print("[+] Esperando 20 segundos a que cargue el streaming...")
    time.sleep(20)
    
    logs = driver.get_log("performance")
    enlace_m3u8 = None
    
    for entrada in logs:
        mensaje = json.loads(entrada["message"])["message"]
        if "Network.requestWillBeSent" in mensaje["method"]:
            url_solicitud = mensaje["params"]["request"]["url"]
            if ".m3u8" in url_solicitud and "akamai" in url_solicitud:
                enlace_m3u8 = url_solicitud
                break
                
    driver.quit()
    return enlace_m3u8

@app.route("/telefe")
def telefe():
    try:
        url_final = obtener_token_fresco()
        if url_final:
            print(f"[+] ¡Token capturado con exito!: {url_final}")
            return redirect(url_final)
        else:
            return "Error: No se pudo capturar el token de Telefe.", 500
    except Exception as e:
        return f"Error interno en el servidor: {str(e)}", 500

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)
