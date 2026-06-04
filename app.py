import time
import json
from flask import Flask, redirect
from selenium import webdriver
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

def obtener_token_fresco():
    print("[+] El reproductor local pidió señal. Abriendo navegador para espiar...")
    
    options = webdriver.ChromeOptions()
    # MODIFICACIÓN 1: Comentamos el modo headless para ver qué pasa en la pantalla
    # options.add_argument("--headless") 
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    driver = webdriver.Chrome(options=options)
    
    url_objetivo = "https://mitelefe.com/" 
    driver.get(url_objetivo)
    
    # MODIFICACIÓN 2: Subimos el tiempo a 20 segundos para asegurar que el video arranque
    print("[+] Esperando 20 segundos a que cargue el streaming...")
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
    url_viva_con_token = obtener_token_fresco()
    
    if url_viva_con_token:
        print(f"[+] ¡ÉXITO! Redirigiendo VLC a:\n{url_viva_con_token}\n")
        return redirect(url_viva_con_token)
    else:
        # MODIFICACIÓN 3: Controlamos el error de forma elegante
        print("[-] ERROR: El script abrió la web pero no logró capturar ningún .m3u8")
        return "No se pudo cazar el token. Revisa la terminal.", 404

if __name__ == '__main__':
    print("[+] Servidor Proxy IPTV encendido en el puerto 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)