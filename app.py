import os
import time
import json
from flask import Flask, redirect
from selenium import webdriver

app = Flask(__name__)

def obtener_token_fresco():
    print("[+] Inicializando Google Chrome mediante detección nativa de Apify...")
    
    options = webdriver.ChromeOptions()
    
    # TRUCO EXPERTO: Apify guarda la ruta exacta en la variable de entorno 'APIFY_CHROME_EXECUTABLE_PATH'
    # Si no existe, recurre por defecto a las rutas estándar de Linux de forma segura.
    ruta_chrome = os.environ.get("APIFY_CHROME_EXECUTABLE_PATH", "/usr/bin/google-chrome")
    print(f"[+] Usando el binario de Chrome en la ruta: {ruta_chrome}")
    options.binary_location = ruta_chrome
    
    # Parámetros mandatorios de aislamiento en la nube para evitar consumo excesivo de RAM
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    # Inicialización directa del navegador
    driver = webdriver.Chrome(options=options)
    
    try:
        url_objetivo = "https://mitelefe.com/"
        driver.get(url_objetivo)
        
        print("[+] Conexión establecida con MiTelefe. Extrayendo telemetría de red por 20 segundos...")
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
        # Cierre absoluto del proceso del navegador para liberar memoria inmediatamente
        driver.quit()

@app.route("/telefe")
def telefe():
    try:
        url_final = obtener_token_fresco()
        if url_final:
            print(f"[+] Token m3u8 interceptado con éxito: {url_final}")
            return redirect(url_final)
        else:
            return "Error: No se pudo capturar el flujo dinámico de video.", 500
    except Exception as e:
        return f"Error interno en la pasarela proxy: {str(e)}", 500

if __name__ == "__main__":
    # Render asigna el puerto mediante la variable de entorno PORT
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)
