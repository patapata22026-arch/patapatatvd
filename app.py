import os
import time
import json
from flask import Flask, redirect
from selenium import webdriver
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def obtener_token_fresco():
    print("[+] Servidor en la nube activado. Iniciando Chrome invisible...")
    
    options = webdriver.ChromeOptions()
    # Opciones críticas para que Chrome corra en un servidor en la nube sin errores:
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Esto descarga e instala el Chrome compatible con Linux en milisegundos
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)
    
    # Capturamos Telefe (puedes cambiarlo por el canal que estudies)
    url_objetivo = "https://mitelefe.com/" 
    driver.get(url_objetivo)
    
    # En la nube le damos 20 segundos para asegurar que pesque el tráfico
    time.sleep(20)
    
    logs = driver.get_log('performance')
    url_encontrada = None
    
    for entry in logs:
        log = json.loads(entry['message'])['message']
        if log['method'] == 'Network.responseReceived':
            url_peticion = log['params']['response']['url']
            
            if "jwpltx.com" in url_peticion and "mu=" in url_peticion:
                url_parseada = urlparse(url_peticion)
                parametros = parse_qs(url_parseada.query)
                url_encontrada = parametros['mu'][0]
                break
            elif ".m3u8" in url_peticion and "jwpltx.com" not in url_peticion:
                url_encontrada = url_peticion
                break
                
    driver.quit()
    return url_encontrada

@app.route('/telefe')
def telefe():
    url_viva = obtener_token_fresco()
    if url_viva:
        print(f"[+] Redirección exitosa enviada al reproductor.")
        return redirect(url_viva)
    else:
        return "Error: No se pudo capturar el token en la nube.", 404

if __name__ == '__main__':
    # Render nos asigna un puerto dinámico mediante una variable de entorno
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto)
