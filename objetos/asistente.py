
from time import sleep, time as timenow
from tempfile import gettempdir
from pickle import load, dump
from sys import exit
from os import path

from objetos.utils import *
from objetos.audio_driver import *
from objetos.google_driver import *
from objetos.selenium_driver import *

from config import USER, PASS

class Asistente():
    def __init__(self):        
        self.USER = USER
        self.PASSWORD = PASS
        self.url = "https://chat.openai.com"
        self.robots = "https://chat.openai.com/robots.txt"
        self.COOKIES_FILE = f'{gettempdir()}/openai.cookies'
        print(f'{azul}Iniciando Selenium Drivers{gris}')
        # Carga el Driver del Navegador
        self.uc = SeleniumDriver()
        #self.uc.Driver.get("https://chat.openai.com")
        login = self.login_openai() # Login
        print()
        if not login:
            if self.uc.virtual_display:
                self.uc.Driver.quit()
                self.uc.detener()
            exit()

    def login_openai(self):

        print(f'\33[K{azul}Cargando Asistente...{gris}')  
        #Login por Cookies
        if path.isfile(self.COOKIES_FILE):
            print(f'\33[K{azul}VERIFICANDO COOKIES{gris}')
            cookies = load(open(self.COOKIES_FILE, 'rb'))
            self.uc.Driver.get(self.robots)
            for cookie in cookies:
                try:
                    self.uc.Driver.add_cookie(cookie)                    
                except:
                    pass
            self.uc.Driver.get(self.url)
        else:
            #Login desde CERO
            self.uc.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="login-button"]'))).click()
            self.uc.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "social-logo"))).click()
            self.uc.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))).send_keys(self.OPENAI_USER)
            self.uc.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#identifierNext'))).click()
            self.uc.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))).send_keys(self.OPENAI_PASSWORD)
            self.uc.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#passwordNext'))).click()

        login = self.comprobar_login()
        # Verifica si se pudo logear correctamente
        if login:
            print(f'\33[K{azul}COOKIE: {verde}OK{gris}')
            dump(self.uc.Driver.get_cookies(),open(self.COOKIES_FILE,"wb"))
            return login
        else:
            print(f'\33[K{azul}COOKIE: {rojo}FALLIDO{gris}')

    def comprobar_login(self, tmpo=3):

        login = False
        while tmpo > 0:
            try:
                self.uc.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="profile-button"]')))  
                self.uc.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#prompt-textarea'))).click()
                login = True
                break
            except:
                pass
            try:
                if 'session has expired' in self.uc.Driver.find_element("h3.text-lg").text:
                    cursor_arriba()
                    print(f'\33[K{amarillo}LA SESSION HA EXPIRADO{gris}')
                    print()
                    break
            except:
                pass
            cursor_arriba()
            print(f'\33[K{gris}Comprobando Login... {tmpo}{gris}')
            sleep(1)
            tmpo -= 1
        cursor_arriba()
        print('\33[K')
        cursor_arriba(2)
        return login

    def ultima_conversacion(self, tmpo=3):
        try:
            self.uc.Driver.click('a:contains("Historial")',  timeout=tmpo)            
        except:
            print("No se encontro Ultima Conversacion")

        
    def chatear(self, prompt = None):
        if prompt:
            # Intruduce texto en el promp o textbox
            self.uc.Driver.send_keys('#prompt-textarea', prompt + '\n')
            sleep(0.5)
            # Generando las respuestas
            inicio = timenow()
            while True:
                # Obtener el último elemento markdown y su texto
                elementos_markdown = self.uc.Driver.find_elements("div.markdown")
                if elementos_markdown:
                    respuesta = elementos_markdown[-1].text            
                # Verificar si el botón de "Stop generating" todavía está presente
                botones_stop = self.uc.Driver.find_elements('[data-testid="stop-button"]')
                if not botones_stop and respuesta:
                    break  # Salir del bucle si el botón no está presente y ya hay respuesta generada            
                # Calcular el tiempo transcurrido
                segundos = int(timenow() - inicio)
                if segundos > 0:                
                    print(f'\33[K{azul2}Generando respuesta... {gris}{segundos} segundos ({len(respuesta)} caracteres{gris})')
                    sleep(1)
                    # Mantener el cursor en la misma línea
                    cursor_arriba()
            try:
                if segundos:
                    print(f'\33[K{magenta}Respuesta generada en... {blanco}{segundos} {magenta}segundos{gris}')
            except:
                pass
            
            # Esperar antes de devolver la respuesta final
            sleep(2)
            # Devolver la respuesta completa
            return self.uc.Driver.find_elements("div.markdown")[-1].text
        else:
            return None
    
    def buscar_texto_en_navegador(self, texto_a_buscar):
        try: 
            nav = GoogleDriver()
            nav.Driver.get("https://google.com")
            nav.Driver.find_element("textarea").send_keys(texto_a_buscar + "\n")     
              
        except:
            print("Ocurrió un error en la busqueda...")