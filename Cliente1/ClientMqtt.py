
#MTEZ importamos librerías
import paho.mqtt.client as paho
import threading 
import binascii
import logging
import time
import random
import os 
#import socket
import sys


#MTEZ importamos los datos de conexión y variables globales
from prueba_encriptar import Encryptor              #*****
from brokerData import * #MTEZ Informacion de la conexion
from globals import *    #MTEZ variables globales
#MTEZ Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, #MTEZ Configuramos el loggin en nivel INFO 
    format = '[%(levelname)s] (%(threadName)-10s) %(message)s'
    )

class ClientMqtt(): #MTEZ se crea la clase ClientMqtt 

   #MTEZ el constructor, con atributos los topcis 
    def __init__(self,USER_ID_1,USER_ID_2,USER_ID_3,AUDIO,USUARIO,SALAS,GRUPO):
        self.USER_ID_1  = USER_ID_1
        self.USER_ID_2  = USER_ID_2
        self.USER_ID_3  = USER_ID_3
        self.AUDIO = AUDIO
        self.USUARIO = USUARIOS 
        self.SALAS = SALAS
        self.GRUPO = GRUPO
       
        '''
        USEOB Config. inicial del cliente MQTT
        '''
        self.client = paho.Client(clean_session=True)                #USEOB Nueva instancia de cliente
        #self.client.on_connect = on_connect                          #USEOB Se configura la funcion "Handler" cuando suceda la conexion
        self.client.on_publish = self.on_publish                          #USEOB Se configura la funcion "Handler" que se activa al publicar algo
        self.client.on_message = self.on_message                          #USEOB Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
        self.client.username_pw_set(MQTT_USER, MQTT_PASS)            #USEOB Credenciales requeridas por el broker
        self.client.connect(host=MQTT_HOST, port = MQTT_PORT)        #USEOB Conectar al servidor remoto
        #self.client.subscribe(('usuarios/16/201114651', 2))         #USEOB CONFIGURADO COMO ACCIÓN BLOQUEANTE    
        self.client.loop_start()
        self.enc = Encryptor(key)              #*****
    #def encriptar (self):
    def texto (self, text):              #*****
        self.text = text
        f = open ('Texto_a_encriptar.txt','w')
        f.write(self.text)
        f.close()
    def encrip_texto(self):              #*****
        f2 = open('Texto_a_encriptar.txt','r')
        f2_a    = f2.read()
        f2.close()
        f3 = open('Texto_encriptado.txt','w')
        f3.write(f2_a)
        f3.close()
        self.enc.encrypt_file('Texto_encriptado.txt')

    def encrip_audio(self):
        aud = open('output.wav','rb')
        audi = aud.read()
        aud.close()
        audio_copia = open('Audio_encriptado.wav','wb')
        audio_copia.write(audi)
        audio_copia.close()
        self.enc.encrypt_file('Audio_encriptado.wav')
    
    def descrip_texto(self):
        des = open('In_texto.txt.enc','rb')
        info    = des.read()
        des.close()
        des2 =open('In_tex_decrypt.txt.enc','wb')
        des2.write(info)
        des2.close()
        self.enc.decrypt_file('In_tex_decrypt.txt.enc')

    def descrypt_wav(self):
        des = open('In_Audio_encriptado.wav.enc','rb')
        info    = des.read()
        des.close()
        des2 =open('In_Audio_decryp.wav.enc','wb')
        des2.write(info)
        des2.close()
        #descrypr = open('In_Audio_decryp.wav.enc','wb')
        #descrypt.write(wavdata)
        #descrypr.close()
        self.enc.decrypt_file('In_Audio_decryp.wav.enc')
        #self.enc.decrypt_file('In_Audio_encriptado.wav.enc')
        print('termino de hacer el decrypt')
        ogging.info('inicia reproduccion de audio:') #USEOB COLOCAMOS LA INFO EN EL LOG
        #os.system('aplay In_Audio_decryp.wav') #USEOB REPRODUCIMOS

    

    def on_publish(self, client, userdata, mid): #USEOB METODO PARA PUBLICACION SATISFACTORIA 
        publishText = 'Publicación satisfactoria'
        print(publishText)

    def on_message(self, client, userdata, msg): #USEOB METODO PARA MANEJO DE FUNCION ON_MESSAGE
        os.system('clear')  
        print(str(msg.payload))
        print ('\nPresione cualquier tecla para continuar')

    def mainMenu(self): #USEOB MÉTODO DE MANEJO DEL MENU PRINCIPAL
        os.system('clear') 
        print ('Menú principal')
        print ('\t1 - Enviar texto')
        print ('\t2 - Enviar mensaje de voz')
        print ('\t3 - Reproducir El Ultimo Audio Grabado')
        print ('\t4 - Reproducir El Ultimo Audio Recibido')
        print ('\t5 - Salir')

    

    def typeMenu(self):  #USEOB METODO PARA EL MENU SELECTOR DE USUARIO O SALA
        os.system('clear') 
        print ('Seleccione Usuario')
        print ('\t1 - Enviar a usuario')
        print ('\t2 - Enviar a sala')

    def userMenu(self):  #USEOBMETODO PARA EL SELECTOR DE USUARIO
        os.system('clear') 
        print ('Seleccione Sala')
        print ('\t1 -'+ USER_ID_2)
        print ('\t2 -'+ USER_ID_3)
       
    
    def roomMenu(self):  #USEOB METODO PARA EL SELECTOR DE SALA
        os.system('clear') 
        print ('Seleccione Sala')
        print ('\t0 - S00')
        print ('\t1 - S01')
        print ('\t2 - S02')
        print ('\t3 - S03')

    def sendTextUser(self,num): #MTEZ método para enviar texto a usuario
        #os.system('clear'
        self.num = num  #MTEZ SE RECIBE EL NUMERO SELECTOR DE USUARIO
        if num == 1:
            UX = USER_ID_2
        else:
            UX = USER_ID_3 

        a_enviar = input ('Escribe mensaje ->') #MTEZ SE RECIBE EL TEXTO A ENVIAR
        a_enviar = self.USER_ID_1 + ' dice: ' + a_enviar #MTEZ se concatena el mensaje a enviar
        self.texto(a_enviar)              #*****
        self.encrip_texto()              #*****
        texto = open('Texto_encriptado.txt.enc','rb')              #*****
        datos_tex = texto.read()              #*****
        texto.close()              #*****
        a_enviar    = bytearray(datos_tex)              #*****
        self.client.publish((USUARIOS +'/'+ GRUPO +'/' +str(UX)), a_enviar) #MTEZ se publca en el topic respectivo, la variable a_enviar
        print('...enviado') 
       
        self.client.loop() 
        

    def sendTextRoom(self,num): #MTEZ METODO PARA EL ENVIO DE TEXTO A SALA
        #os.system('clear')
        self.num=num  
                   
        a_enviar = input ('Escribe mensaje ->') #MTEZ SE RECIBE EL TEXTO A ENVIAR
        a_enviar = self.USER_ID_1 + ' dice: ' + a_enviar #MTEZ se concatena el mensaje a enviar
        self.client.publish((SALAS+'/'+ GRUPO +"/S0"+ str(num)),  a_enviar ) #MTEZ se publca en el topic respectivo, la variable a_enviar
        print('...enviado') 
        self.client.loop()

    def sendAudioUser(self,num): #USEOB METODO PARA EL ENVIO DE AUDIO ........
        #os.system('clear')
        self.num=num 
        if num == 1:
            UX = USER_ID_2
        else:
            UX = USER_ID_3  
        
        #size = (os.stat('Audio_encriptado.wav.enc').st_size) #USEOB SE RECIBE EL TAMAÑO DEL ARCHIVO
       # print(size) 
        #a_enviar = b'\x03' + bytes("201700512", 'utf-8') + bytes(str(size), 'utf-8') #USEOB SE CONCATENA EL MENSAJE A ENVIAR
        self.enviar_audioU(num) #USEOB SE LLAMA AL METODO ENVIAR AUDIO
        #self.client.publish((AUDIO+'/'+GRUPO+'/'+str(UX)),a_enviar) #USEOB SE HACE LA PUBLICACION EN EL TOPIC
        logging.info('...enviado') 

    def sendAudioRoom(self,num): #USEOB METODO PARA EL ENVÍO DE AUDIO A SALAS
        #os.system('clear')
        self.num=num  

        size = (os.stat('output.wav').st_size) #USEOB SE OBTIENE EL TAMAÑO DEL ARCHIVO
        print(size)
        a_enviar = b'\x03' + bytes("201700512", 'utf-8') + bytes(str(size), 'utf-8') #USEOB SE CONCATENA EL MENSAJE A ENVIAR
        self.client.publish((AUDIO+'/'+GRUPO +"/S0"+ str(num)),a_enviar ) #USEOB SE CONCATENA EL MENSAJE A ENVIAR
        self.enviar_audioR(num) #USEOB SE LLAMA AL METODO ENVIAR AUDIO
        logging.info('...enviado') 

    def disconnect(self): #USEOB METODO PARA DESCONEXIÓN DEL BROKER
        self.client.disconnect()


    def enviar_audioU(self,num): #MTEZ METODO PARA EL ENVIO DE AUDIO
            self.num=num    #MTEZ SELECCION DE USUARIO
            if num == 1:
                UX = USER_ID_2
            else:
                UX = USER_ID_3  
            self.encrip_audio()
            filename = 'Audio_encriptado.wav.enc' #MTEZ SELECION DEL ARCHIVO Y SE GUARDA EN FILENAME
            f = open(filename, "rb") #MTEZ SE ABRE EL ARCHIVO EN MODO BINARIO Y CON PERMISOS DE REESCRITURA
            imagestring = f.read() #MTEZ LECTURA DEL ARCHIVO Y SE GUARDA COMO ARREGLO BINARIO
            f.close() #MTEZ CERRAMOS EL ARCHIVO
            #encriptar audio
            byteArray = bytearray(imagestring) #MTEZGUARDAMOS LA CADENA DE DATOS EN UNA VARIABLE DE TIPO BYTEARRAY       
            self.client.publish((AUDIO+'/'+GRUPO+'/'+str(UX)), byteArray) #MTEZ SE PUBLICA EN EL USUARIO

    def enviar_audioR(self,num): #MTEZ METODO PARA EL ENVIO DE AUDIO A SALAS, EL MANEJO DE ARCHIVOS ES IGUAL
            self.num=num  
            filename = 'output.wav'
            f = open(filename, "rb")
            imagestring = f.read()
            f.close()
            byteArray = bytearray(imagestring)        
            self.client.publish((AUDIO+'/'+GRUPO +"/S0"+ str(num)), byteArray) #SE PUBLICA EN LA SALA INDICADA

    def reproducir_audio(self): #MTEZ METODO PARA REPRODUCIR AUDIO ATRAVEZ DE ESCRIBIR EN SISTEMA
            print ('Reproduciendo') 
            os.system('aplay output.wav')

    def reproducir_audio_R(self): #MTEZ METODO PARA REPRODUCIR AUDIO DE NUEVO
            print ('Reproduciendo') 
            os.system('aplay In_Audio.wav')        
    
    def audio(self, auidop_seg): #MTEZ METODO PARA LA OBTENER LA GRABACION
        self.auidop_seg = auidop_seg 
        seconds = auidop_seg  # Duration of recording

        logging.info('Comenzando grabacion') #MTEZ DURACION DE LA GRABACION
        os.system('arecord -d ' + seconds +' -f U8 -r 8000 output.wav') #MTEZ GRABANDO CON LA DURACION ESPECIFICADA

        logging.info('Grabacion finalizada, inicia reproduccion')
        os.system('aplay output.wav')    #MTEZ REPRODUCIENDO AL FINAL DE GRABAR

    def entradaTexto(self, msg):              #*****
        trama   =   msg              #*****
        t    = open('In_texto.txt.enc','wb')              #*****
        t.write(trama)              #*****
        t.close()
        logging.info('llego un texto encriptado')   
        print('se creo el archivo encriptado')           #*****
    
    def entrandoAudio(self, msg): #USEOB MANEJO DE METODO PARA LA ENTRADA DE UN AUDIO 
        trama = msg #USEOB SE RECIBE LA PAYLOAD
        audio=open('In_Audio_encriptado.wav.enc','wb') #USEOB ABRIMOS EL ARCHIVO DE AUDIO
        audio.write(trama) #USEOB ESCRIBIMOS EN EL ARCHIVO DE AUDIO
        audio.close() #USEOB CERRAMOS EL ARCHIVO



    t1 = threading.Thread(name = 'alive' , #MTEZ MANEJO DE HILO AUDIO
                            target = audio , #MTEZ SE INDICA LA FUNCIÓN OBJETIVO
                            daemon = True #LEVANTA EL HILO COMO DEMONIO PARA QUE MUERA CUANDO FINALICE EL PROCES
                        )
                        
    t2 = threading.Thread(name= 'alive', target= entrandoAudio , daemon= True) #MTEZ MANEJO DE HILO ENTRANDOAUDIO

    listaHilos = [] #MTEZ SE DEFINE LA LISTA DE HILOS 
    t1.start() #MTEZ MANEJO DE HILO AUDIO ARRIBA
    t2.start() #MTEZ MANEJO DE HILO ENTRANDOAUDIO ARRIBA

    
       