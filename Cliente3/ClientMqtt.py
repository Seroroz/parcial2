#Los comentarios completos del código estan en Cliente1.py
import paho.mqtt.client as paho
#import sounddevice as sd
#import soundfile as sf

import threading 
import binascii
import logging
import time
import random
import os 
#import socket
import sys

from brokerData import * #Informacion de la conexion

#from scipy.io.wavfile import write

from globals import *    #variables globales
#Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )

class ClientMqtt():

    def __init__(self,USER_ID_1,USER_ID_2,USER_ID_3,AUDIO,USUARIO,SALAS,GRUPO):
        self.USER_ID_1  = USER_ID_1
        self.USER_ID_2  = USER_ID_2
        self.USER_ID_3  = USER_ID_3
        self.AUDIO = AUDIO
        self.USUARIO = USUARIOS 
        self.SALAS = SALAS
        self.GRUPO = GRUPO
       
        '''
        Config. inicial del cliente MQTT
        '''
        self.client = paho.Client(clean_session=True)                #Nueva instancia de cliente
        # client.on_connect = on_connect                          #Se configura la funcion "Handler" cuando suceda la conexion
        self.client.on_publish = self.on_publish                          #Se configura la funcion "Handler" que se activa al publicar algo
        self.client.on_message = self.on_message                          #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
        self.client.username_pw_set(MQTT_USER, MQTT_PASS)            #Credenciales requeridas por el broker
        self.client.connect(host=MQTT_HOST, port = MQTT_PORT)        #Conectar al servidor remoto
        #self.client.subscribe(('usuarios/16/201114651', 2))             
        self.client.loop_start()
    
    
    #USEOB fucion para indicar que se publicó
    def on_publish(self, client, userdata, mid):                
        publishText = 'Publicación satisfactoria'
        print(publishText)

    #USEOB nos notifica los mensajes entrantes
    def on_message(self, client, userdata, msg):
        os.system('clear')  
        print(str(msg.payload))
        print ('\nPresione cualquier tecla para continuar')

    #USEOB es el menú principal
    def mainMenu(self): 
        os.system('clear') 
        print ('Menú principal')
        print ('\t1 - Enviar texto')
        print ('\t2 - Enviar mensaje de voz')
        print ('\t3 - Reproducir El Ultimo Audio Grabado')
        print ('\t4 - Reproducir El Ultimo Audio Recibido')
        print ('\t5 - Salir')

    
    #USEOB menú de selección
    def typeMenu(self):  
        os.system('clear') 
        print ('Seleccione una opcion')
        print ('\t1 - Enviar a usuario')
        print ('\t2 - Enviar a sala')

    #USEOB menú de usuarios
    def userMenu(self):  
        os.system('clear') 
        print ('Seleccione Seleccione un usuario')
        print ('\t1 -'+ USER_ID_2)
        print ('\t2 -'+ USER_ID_3)
       
    #USEOB menú de salas
    def roomMenu(self):  
        os.system('clear') 
        print ('Seleccione Sala')
        print ('\t0 - S00')
        print ('\t1 - S01')
        print ('\t2 - S02')
        print ('\t3 - S03')

    #USEOB funcion para enviar mensaje a un usuario
    def sendTextUser(self,num):
        #os.system('clear')

        #USEOB se diferencia al usuario destinatario
        self.num = num  
        if num == 1:
            UX = USER_ID_2
        else:
            UX = USER_ID_3 

        a_enviar = input ('Escribe mensaje ->')
        a_enviar = self.USER_ID_1 + ' dice: ' + a_enviar
        self.client.publish((USUARIOS +'/'+ GRUPO +'/' +str(UX)), a_enviar)
        print('...enviado') 
        self.client.loop()

    #USEOB funcion para enviar texto a una sala
    def sendTextRoom(self,num):
        #os.system('clear')
        self.num=num             
        a_enviar = input ('Escribe mensaje ->')
        a_enviar = self.USER_ID_1 + ' dice: ' + a_enviar
        self.client.publish((SALAS+'/'+ GRUPO +"/S0"+ str(num)),  a_enviar )
        print('...enviado') 
        self.client.loop()

    #USEOB funcion para enviar audio a un usuario
    def sendAudioUser(self,num):
        #os.system('clear')
        self.num=num 
        if num == 1:
            UX = USER_ID_2
        else:
            UX = USER_ID_3  
        
        size = (os.stat('output.wav').st_size)
        print(size)
        a_enviar = b'\x03' + bytes("201700512", 'utf-8') + bytes(str(size), 'utf-8')
        self.enviar_audioU(num)
        self.client.publish((AUDIO+'/'+GRUPO+'/'+str(UX)),a_enviar)
        logging.info('...enviado') 

    #USEOB funcion para enviar audio a una sala
    def sendAudioRoom(self,num):
        #os.system('clear')
        self.num=num  

        size = (os.stat('output.wav').st_size)
        print(size)
        a_enviar = b'\x03' + bytes("201700512", 'utf-8') + bytes(str(size), 'utf-8')
        self.client.publish((AUDIO+'/'+GRUPO +"/S0"+ str(num)),a_enviar )
        self.enviar_audioR(num)
        logging.info('...enviado') 

    #USEOB funcion para desconectarse del broker
    def disconnect(self):
        self.client.disconnect()

    #USEOB algoritmo para enviar audio a el usuario seleccionado
    def enviar_audioU(self,num):
            self.num=num 
            if num == 1:
                UX = USER_ID_2
            else:
                UX = USER_ID_3  
            filename = 'output.wav'
            f = open(filename, "rb")
            imagestring = f.read()
            f.close()
            byteArray = bytearray(imagestring)        
            self.client.publish((AUDIO+'/'+GRUPO+'/'+str(UX)), byteArray)

    #USEOB envia el audio a una sala
    def enviar_audioR(self,num):
            self.num=num  
            filename = 'output.wav'
            f = open(filename, "rb")
            imagestring = f.read()
            f.close()
            byteArray = bytearray(imagestring)        
            self.client.publish((AUDIO+'/'+GRUPO +"/S0"+ str(num)), byteArray)

    #USEOB uso de os para reproducir audio enviado
    def reproducir_audio(self):
            print ('Reproduciendo') 
            os.system('aplay output.wav')

    #USEOB uso de os para reproducir audio 
    def reproducir_audio_R(self):
            print ('Reproduciendo') 
            os.system('aplay In_Audio.wav')  

    #USEOB FUNCION QUE INICIALIZA UNA GRABACION
    def audio(self, auidop_seg):
        self.auidop_seg = auidop_seg
        seconds = auidop_seg  # Duration of recording

        logging.info('Comenzando grabacion')
        os.system('arecord -d ' + seconds +' -f U8 -r 8000 output.wav')

        logging.info('Grabacion finalizada, inicia reproduccion')
        os.system('aplay output.wav')    
    
    #USEOB FUNCION PARA GRABAR AUDIO PARA ENVIO 
    def entrandoAudio(self,msg):
        trama = msg
        audio=open('In_Audio.wav','wb')
        audio.write(trama)
        audio.close()
        logging.info('inicia reproduccion de audio:')
        os.system('aplay In_Audio.wav')


    t1 = threading.Thread(name = 'alive' ,
                            target = audio ,
                            daemon = True
                        )
                        
    t2 = threading.Thread(name= 'alive', target= entrandoAudio , daemon= True)

    listaHilos = []
    t1.start()
    t2.start()

    
       
