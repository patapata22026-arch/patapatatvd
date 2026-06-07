import os
import time
import json
from flask import Flask, redirect
from selenium import webdriver

app = Flask(__name__)

def obtener_token_fresco():
    print("[+] Inicializando Google Chrome Oficial en modo servidor...")
    
    options = webdriver.ChromeOptions()
    # Ruta exacta del binario de Google Chrome en Ubuntu
    options.binary_location = "/usr/bin/google-chrome"
    
    # Parámetros obligatorios para el aislamiento en la nube
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    # Dejamos que Selenium detecte el driver nativo de la instalación
    driver = webdriver.Chrome(options=options)
    
    try:
        url_objetivo = "https://mitelefe.com/"
        driver.get(url_objetivo)
        
        print("[+] Navegador abierto. Esperando 20 segundos para recolectar tráfico de red...")
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
                    
        return enlace_m3u8
    except Exception as e:
        print(f"[-] Error en el proceso de Selenium: {str(e)}")
        return None
    finally:
        driver.quit()

@app.route("/telefe")
def telefe():
    try:
        url_final = obtener_token_fresco()
        if url_final:
            print(f"[+] Token localizado con éxito: {url_final}")
            return redirect(url_final)
        else:
            return "Error: No se pudo interceptar el flujo de video dinámico.", 500
    except Exception as e:
        return f"Error interno en la pasarela proxy: {str(e)}", 500

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)
