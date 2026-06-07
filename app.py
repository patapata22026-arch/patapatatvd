import os
import time
import json
from flask import Flask, redirect
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

app = Flask(__name__)

def obtener_token_fresco():
    print("[+] Lanzando Chromium con bypass de memoria para Render...")
    
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    
    # ARGUMENTOS MATEMÁTICOS DE FUERZA MAYOR PARA EVITAR EL "DEVSHMPERMISSION":
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-dev-shm-usage") # Desactiva el uso de /dev/shm por completo
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    
    # Forzar a Chrome a usar carpetas temporales de disco en lugar de memoria RAM compartida
    options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    options.add_argument("--data-path=/tmp/chrome-data")
    options.add_argument("--disk-cache-dir=/tmp/chrome-cache")
    
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    # Inicializar apuntando al driver del sistema operativo
    servicio = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=servicio, options=options)
    
    try:
        url_objetivo = "https://mitelefe.com/"
        driver.get(url_objetivo)
        
        print("[+] Pagina cargada exitosamente en aislamiento total. Extrayendo red...")
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
        print(f"[-] Error operativo interno en la instancia de Selenium: {str(e)}")
        return None
    finally:
        driver.quit()

@app.route("/telefe")
def telefe():
    try:
        url_final = obtener_token_fresco()
        if url_final:
            print(f"[+] Token m3u8 interceptado con exito: {url_final}")
            return redirect(url_final)
        else:
            return "Error: No se pudo capturar el flujo dinamico de video.", 500
    except Exception as e:
        return f"Error interno en la pasarela proxy: {str(e)}", 500

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)
