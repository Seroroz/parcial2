#variables
# ALIVE_PERIOD            = 2            #Período entre envío de tramas ALIVE
# ALIVE_CONTINUOUS        = 0.1      #Período entre envío de tramas ALIVE si no hay respuesta

#COMMANDS
# COMMAND_FTR             = b'\x03'
# COMMAND_ALIVE           = b'\x04'
# COMMAND_ACK             = b'\x05'
# COMMAND_OK              = b'\x06'
# COMMAND_NO              = b'\x07'

#CATC System filenames
USERS_FILENAME          = "usuario.txt"
ROOMS_FILENAME          = "salas.txt"

#CATC System ident b
USER_ID_2                 = "201114651"
USER_ID_1                 = "201701038"
USER_ID_3                 = "201700512"
key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
              #*****

AUDIO       = 'audio'
COMANDOS    = 'comandos'
USUARIOS    = 'usuarios'
SALAS       = 'salas'
GRUPO       = '16'


#CATC Topics 

topic_sala_0 = "salas/16/S00"
topic_sala_1 = "salas/16/S01"
topic_sala_2 = "salas/16/S02"

topic_Asala_0 = "audio/16/S00"
topic_Asala_1 = "audio/16/S01"
topic_Asala_2 = "audio/16/S02"

topic_usuario_3 = "usuarios/16/201700512"
topic_usuario_2 = "usuarios/16/201114651"
topic_usuario_1 = "usuarios/16/"+USER_ID_1  

topic_Asuario_3 = "audio/16/201700512"
topic_Asuario_1 = "audio/16/201701038"
topic_Asuario_2 = "audio/16/201114651"


