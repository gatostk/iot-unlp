# iot-unlp
Pasos 1- Descarga los archivos
Paso 2-Ejecuta docker compose up -d  -–build para levantar los dockers.
C:\dockers > docker compose up -d  -–build
Paso 3- Edita las variables en el archivo .env
C:\dockers>.env
# Credenciales RTSP
RTSP_USER=agregar usuario rtsp
RTSP_PASS=agregar contraseña
RTSP_IP=agregar ip 
RTSP_PORT=554
RTSP_PATH=Streaming/Channels/101


# MQTT
MQTT_HOST=mosquitto
MQTT_PORT=1883

# Telegram (si lo usás más adelante)
TELEGRAM_BOT_TOKEN=ingresar
TELEGRAM_CHAT_ID=ingresar
Paso 4- Obtener tu Chat_id y el botname,bot token.
Paso 5-Configurar en node-red desde localhost:1880 el nodo Telegram
Agregar los datos de telegram
Paso 6- Configurar en node-red en el nodo Buffer Caption en el JS
Chatid: tu numero de chat
Paso 7- Iniciar el Python y ver los logs
PS C:\dockers> docker logs -f python-app
INFO:rtsp_reader:[RTSP] Cámara conectada correctamente
INFO:publisher:[MQTT] Connected with code 0
INFO:__main__:Starting detection loop...
INFO:publisher:[MQTT] Image published successfully
INFO:__main__:Movement detected! Publishing image...
INFO:publisher:[MQTT] Image published successfully
