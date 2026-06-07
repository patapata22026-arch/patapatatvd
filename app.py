import os
import time
import json
from flask import Flask, redirect
from selenium import webdriver

app = Flask(__name__)

def obtener_token_fresco():
    print("[+] Inicializando Google Chrome con argumentos forzados para Render Free...")
    
    options = webdriver.ChromeOptions()
    
    # Extraer la ruta nativa de Apify
    ruta_chrome = os.environ.get("APIFY_CHROME_EXECUTABLE_PATH", "/usr/bin/google-chrome")
    options.binary_location = r"{}".format(ruta_chrome)
    
    # ARGUMENTOS DE INGENIERÍA CRÍTICOS PARA REDES AISLADAS (EVITA EL EXITED ABNORMALLY):
    options.add_argument("--headless=old")  # Fuerza el headless clásico que no pide permisos de sandbox
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--user-data-dir=/tmp/chrome-user-data") # Fuerza a escribir en la carpeta temporal de Render
    options.add_argument("--remote-debugging-port=9222")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    # Inicialización directa con las opciones inyectadas
    driver = webdriver.Chrome(options=options)
    
    try:
        url_objetivo = "https://mitelefe.com/"
        driver.get(url_objetivo)
        
        print("[+] Pagina cargada. Esperando 20 segundos de trafico de red...")
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
