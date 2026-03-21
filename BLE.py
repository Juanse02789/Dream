from machine import Pin, PWM
import bluetooth
import struct
import time

ble = bluetooth.BLE()
ble.active(True)

buzzer = PWM(Pin(5))
buzzer.freq(1000)

# UUIDs simples
SERVICE_UUID = bluetooth.UUID(0x180F)
CHAR_UUID = bluetooth.UUID(0x2A19)

service = (
    SERVICE_UUID,
    (
        (CHAR_UUID, bluetooth.FLAG_WRITE),
    ),
)

((char_handle,),) = ble.gatts_register_services((service,))

name = "ESP32-LLAVES"

def advertising_payload(name):
    payload = bytearray()
    payload += struct.pack("BB", len(name) + 1, 0x09)
    payload += name.encode()
    return payload

payload = advertising_payload(name)

ble.gap_advertise(100, payload)

print("BLE listo")

def irq(event, data):
    if event == 3:  # write
        value = ble.gatts_read(char_handle)
        print("Recibido:", value)

        buzzer.duty(512)
        time.sleep(1)
        buzzer.duty(0)

ble.irq(irq)

while True:
    time.sleep(1)
