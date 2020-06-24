
#CATC Importamos librerias

import paho.mqtt.client as mqtt
import os
import sys
import logging
    


from brokerData import * #CATC Informacion de la conexion
from globals import * #CATC variables globales
from ClientMqtt import ClientMqtt #MTEZ importamos la clase ClientMqtt 

#CATC Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, #MTEZ configuramos el nivel del logging en INFO 
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )
LOG_FILENAME = 'mqtt.log' #archivo en donde se guardará la info

#CATC Se crea una instancia de la Clase tipo ClientMqtt, con los atributos Topics, definidos en el archivo Globals
cli = ClientMqtt(USER_ID_1,USER_ID_2,USER_ID_3,AUDIO,USUARIOS,SALAS,GRUPO)



#CATC Callback que se ejecuta cuando nos conectamos al broker
def on_connect(client, userdata, rc):
    logging.info("Conectado al broker")

#CATC Callback que se ejecuta cuando llega un mensaje al topic suscrito
def on_message(client, userdata, msg):
     
    ver  =    msg.topic.split('/')
    print(str(ver[0]))
    print(str(msg.topic))
    #CARTC evalua si solo llega a los  topics audio 
    if str(ver[0]) == "audio":
        logging.info('autdio Entrando:')
        cli.entrandoAudio(msg.payload)
        
    else:    
    #CATC Se muestra en pantalla informacion que ha llegado
        logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
        logging.info("El contenido del mensaje es: " + str(msg.payload))

    
    #CATC Y se almacena en el log 
    logCommand = 'echo "(' + str(msg.topic) + ') -> ' + str(msg.payload) + '" >> ' + LOG_FILENAME
    os.system(logCommand)

client = mqtt.Client(clean_session=True) #CATC Nueva instancia de Pahoclient
client.on_connect = on_connect #CATC Se configura la funcion "Handler" cuando suceda la conexion
client.on_message = on_message #CATC Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS) #CATC Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #CATC Conectar al servidor remoto

#CATC definimos cambios al quality of service:
qos = 2
#CATC me  suscribo a mis  topics
client.subscribe([(topic_usuario_1, qos), (topic_sala_0, qos), (topic_sala_1, qos),(topic_sala_2, qos),(topic_Asuario_1, qos),(topic_Asala_0, qos),(topic_Asala_1, qos),(topic_Asala_2, qos)])

#CATC Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
client.loop_start()
#configurado como acción bloqueante
#CATC muestra el menu  par  enviar  datos  de  audio o texto
try:
    i=1
    while i<6: 
        cli.mainMenu()    #CATC aparece el menu principarl                                       
        opcionMenu = input('\n\tDigite opción -> ')

        if opcionMenu == '1':
            cli.typeMenu() #CATC aparece el menu de topics para  enviar texto
            opcionMenu = input('\n\tDigite tipo -> ')    

            if opcionMenu == '1':
                cli.userMenu() #CATC aparece el menu principal de  mis  contactos
                opcionMenu = input('\n\tDigite Usuario -> ') 

                if opcionMenu == '1':
                    #CATC se  seleciona e primer  usuario 
                    print('va  enviar un mensaje a '+USER_ID_1+':')
                    cli.sendTextUser(1)  #CATC invoca  la funcion enviar texto al usuario
                elif opcionMenu == '2':
                    #CATC se  seleciona al segundo  usuario 
                    print('va  enviar un mensaje a '+USER_ID_2+':')
                    cli.sendTextUser(2) #CATC invoca  la funcion enviar texto al usuario
            elif opcionMenu == '2':
                cli.roomMenu() #CATC aparece  el menu de las  salas
                opcionMenu = input('\n\tDigite Sala -> ') 

                if opcionMenu == '0':
                    print("Has seleccionado enviar un mensaje a la sala: S0"  + str(opcionMenu))
                    cli.sendTextRoom(0) #CATC se  se invoca  a la  funcion enviar  texto a una sala

                elif opcionMenu == '1':
                    print("Has seleccionado enviar un mensaje a la sala: S0"  + str(opcionMenu))
                    cli.sendTextRoom(1)#CATC se  se invoca  a la  funcion enviar  texto a una sala

                elif opcionMenu == '2':
                    print("Has seleccionado enviar un mensaje a la sala: S0"  + str(opcionMenu))
                    cli.sendTextRoom(2)#CATC se  se invoca  a la  funcion enviar  texto a una sala

                elif opcionMenu == '3':
                    print("Has seleccionado enviar un mensaje a la sala: S0"  + str(opcionMenu))
                    cli.sendTextRoom(3)  #CATC se  se invoca  a la  funcion enviar  texto a una sala

        elif opcionMenu == '2':
            cli.typeMenu() #CATC se muestra  el menu principal
            opcionMenu = input('\n\tDigite tipo -> ')  

            if opcionMenu == '1':
                cli.userMenu()#CATC se  se invoca al menu de usuarios 
                opcionMenu = input('\n\tDigite Usuario -> ') 

                if opcionMenu == '1':
                    print("indique el tiempo de grabación >> ")
                    audio_t = str(input())
                    cli.audio(audio_t) #CATC se  realiza  la grabacion de  audio 
                    cli.sendAudioUser(1)  #CATC se  realiza el envio de audio  audio

                if opcionMenu == '2':
                    print("indique el tiempo de grabación >> ")
                    audio_t = str(input())
                    cli.audio(audio_t)#CATC se  realiza  la grabacion de  audio 
                    cli.sendAudioUser(2) #CATC se  realiza el envio de audio  audio    

            elif opcionMenu == '2':
                cli.roomMenu()#CATC despliega  el menu de salas
                opcionMenu = input('\n\tDigite Sala -> ') 

                if opcionMenu == '0':
                    print("Has seleccionado enviar un Audio a la sala: S0"  + str(opcionMenu))
                    audio_t = str(input("indique el tiempo de grabación >> "))
                    cli.audio(audio_t)#CATC se  realiza  la grabacion de  audio 
                    cli.sendAudioRoom(0) #CATC se  realiza el envio de audio  audio

                elif opcionMenu == '1':
                    print("Has seleccionado enviar un Audio a la sala: S0"  + str(opcionMenu))
                    audio_t = str(input("indique el tiempo de grabación >> "))
                    cli.audio(audio_t)#CATC se  realiza  la grabacion de  audio 
                    cli.sendAudioRoom(1) #CATC se  realiza el envio de audio  audio

                elif opcionMenu == '2':
                    print("Has seleccionado enviar un Audio a la sala: S0"  + str(opcionMenu))
                    audio_t = str(input("indique el tiempo de grabación >> "))
                    cli.audio(audio_t)#CATC se  realiza  la grabacion de  audio 
                    cli.sendAudioRoom(2) #CATC se  realiza el envio de audio  audio

                elif opcionMenu == '3':
                    print("Has seleccionado enviar un Audio a la sala: S0"  + str(opcionMenu))
                    audio_t = str(input("indique el tiempo de grabación >> "))
                    cli.audio(audio_t)#CATC se  realiza  la grabacion de  audio 
                    cli.sendAudioRoom(3) #CATC se  realiza el envio de audio  audio
                
        elif opcionMenu == '3':    
             cli.reproducir_audio()  #CATC se  reproduce el  ultimo audio enviado 

        elif opcionMenu == '4':    
             cli.reproducir_audio_R()  #CATC se  reproduce el  ultimo audio enviado 
             
        
        elif opcionMenu == '5':  
             i=7 # hace   que el loop del  menu no  siga  
             logging.info('Desconectando del broker MQTT...')  #CATC se desconecta  el usuario 
             cli.disconnect()
             


#MTEZ excepción para desconectar el brocker
except KeyboardInterrupt:
    logging.info('Desconectando del broker MQTT...')
    cli.disconnect()

# finally:
#     cli.disconnect() 
#     print('Se ha desconectado del broker. Saliendo...')