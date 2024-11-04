import network
import socket
from machine import Pin
import time

# Configura el LED en el pin 'LED'
led = Pin('LED', Pin.OUT)

# Credenciales de Wi-Fi
ssid = 'REPLACE_WITH_YOUR_SSID'
password = 'REPLACE_WITH_YOUR_PASSWORD'

# Conectar a Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Espera a que se conecte
while not wlan.isconnected():
    print("Conectando a Wi-Fi...")
    time.sleep(1)

print("Conexión exitosa, IP:", wlan.ifconfig()[0])

# Inicia el servidor
s = socket.socket()
s.bind(('0.0.0.0', 80))
s.listen(1)

# Bucle principal
while True:
    conn, addr = s.accept()
    request = conn.recv(1024).decode()

    if '/on' in request:
        led.value(1)  # Enciende el LED
    elif '/off' in request:
        led.value(0)  # Apaga el LED

    # Responde con un mensaje simple
    response = "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nLED " + ("ON" if led.value() else "OFF")
    conn.send(response)
    conn.close()
