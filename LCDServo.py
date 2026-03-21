from machine import Pin, PWM, SoftI2C
from time import sleep
from machine_i2c_lcd import I2cLcd

# ---------------- LCD ----------------
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = SoftI2C(sda=Pin(12), scl=Pin(13), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# ---------------- SERVO ----------------
servo = PWM(Pin(11), freq=50)

# ---------------- LEDS ----------------
ledV = Pin(2, Pin.OUT)
ledA = Pin(7, Pin.OUT)
ledR = Pin(8, Pin.OUT)

# ---------------- BOTON ----------------
pulsador = Pin(6, Pin.IN, Pin.PULL_UP)

# ---------------- ESTADOS ----------------
estados = [
    ("Verde", ledV, 50),
    ("Amarillo", ledA, 75),
    ("Rojo", ledR, 115)
]

estado_actual = 0


def apagar_leds():
    ledV.off()
    ledA.off()
    ledR.off()


def mostrar_estado(nombre, angulo):
    lcd.clear()
    lcd.putstr("Led: " + nombre)
    lcd.move_to(0, 1)
    lcd.putstr("Angulo: " + str(angulo))


while True:

    if pulsador.value() == 0:

        nombre, led, angulo = estados[estado_actual]

        apagar_leds()

        led.on()
        servo.duty(angulo)

        mostrar_estado(nombre, angulo)

        estado_actual += 1
        if estado_actual >= len(estados):
            estado_actual = 0

        sleep(0.3)  # antirrebote
