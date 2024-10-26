
from sys import exit
from time import sleep

from objetos.audio_driver import *

def main():
    # Aca se crean los objetos y se inicializan los drivers
    audio_driver = AudioDriver()

    text = 'Buenas, ya podemos comunicarnos libremente...'
    print(f'{verde}{text}{gris}')    
    audio_driver.thread_texto_a_audio(text)
    print(f'{rojo}{gris}')
    sleep(1)
    
    
    text = text = "El diseño del sistema se basó en la metodología XP, que promovió simplicidad y flexibilidad. Se priorizaron las historias de usuario fundamentales para garantizar que el asistente funcionara correctamente desde las primeras interacciones. El enfoque inicial fue construir la estructura básica de interacción, sobre la cual se añadieron funcionalidades más complejas. Se presentó un diagrama de flujo que describió el ciclo de interacción básico del asistente, sirviendo como punto de partida para la implementación de las historias de usuario."
    audio_driver.thread_texto_a_audio(text)
    print(f'{rojo}{gris}')
    
    while True:
        aux = audio_driver.devolver_contenido()
        if aux:
            if 'salir' in aux:
                break
            elif 'finalizar' in aux:
                aux = None
            elif aux:
                print(f'\33[K{amarillo}{aux}{gris}')
                respuesta = aux
                #respuesta = chat.chatear(aux)
                #print(f'{verde}{respuesta}{gris}')
                print()
                # Envia la respuesta de texto a reproducir en audio
                audio_driver.thread_texto_a_audio(respuesta)
                aux = None
        print(f'{rojo}Escuchando...{gris}')
        cursor_arriba()
        sleep(1)
    # if chat.uc.display_virt:
    #     chat.uc.detener()
    # else:
    #     chat.uc.Driver.quit()
    exit()



if __name__ == '__main__':
    main()