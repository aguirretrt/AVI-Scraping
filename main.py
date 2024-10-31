
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

from sys import exit
from time import sleep

from objetos.asistente import *
from objetos.audio_driver import *
from objetos.texto_terminal import *

def main():
    # Aca se crean los objetos y se inicializan los drivers    
    asistente = Asistente()
    asistente.ultima_conversacion()

    audio_driver = AudioDriver()
    texto_terminal = TextoTerminal()

    text = 'Buenas, ya podemos comunicarnos libremente...'
    print(f'{verde}{text}{gris}')    
    audio_driver.thread_texto_a_audio(text)
    print(f'{rojo}{gris}')
    sleep(1)
    
    while True:
            voz = audio_driver.devolver_contenido()
            texto = texto_terminal.user_input
        
            if voz or texto:
                comando = voz if voz else texto
                texto_terminal.user_input = ''

                acciones = {
                    'salir': lambda: None,
                    'finalizar': lambda: None,
                    'to_google': asistente.buscar_texto_en_navegador
                }

                if comando in acciones:
                    if comando == 'salir':
                        break  # Agregar esta línea para romper el bucle
                elif comando:
                    if comando.startswith('to_google'):
                        asistente.buscar_texto_en_navegador(comando)
                    else:
                        print(f'\33[K{amarillo}{comando}{gris}')
                        respuesta = asistente.chatear(comando)
                        print(f'{verde}{respuesta}{gris}')
                        print()
                        # Envia la respuesta de texto a reproducir en audio
                        audio_driver.thread_texto_a_audio(respuesta)

            print(f'{rojo}Escuchando... {gris}')
            cursor_arriba()
            sleep(1)  # Reducir la carga del CPU

    if asistente.uc.virtual_display:
        asistente.uc.Driver.quit()
        asistente.uc.detener()
    else:
        asistente.Driver.quit()

    exit()



if __name__ == '__main__':
    main()