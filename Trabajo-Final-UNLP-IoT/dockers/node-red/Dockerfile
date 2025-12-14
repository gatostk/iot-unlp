FROM nodered/node-red:latest

# Activar Project Mode por defecto
ENV NODE_RED_ENABLE_PROJECTS=true

# Instalar nodos adicionales globalmente
RUN npm install --unsafe-perm --no-update-notifier --no-fund \
    node-red-contrib-telegrambot

# Instalar herramientas de debug MQTT dentro del contenedor (Alpine usa apk)
USER root
RUN apk update && apk add --no-cache mosquitto-clients curl

# Volver al usuario de Node-RED
USER node-red