#include <Arduino.h>
#include <WiFi.h>

const char* SSID     = "Sebas"; 
const char* PASSWORD = "SoloMillos";
const char* PC_IP    = "10.14.198.107";
const uint16_t UDP_PORT = 5006;
const uint16_t PC_PORT  = 5007;
     
#define IN1 26
#define IN2 27
#define ENA 33
#define IN3 14  
#define IN4 12
#define ENB 25

#define PWM_FREQ    1000
#define PWM_RES     8
#define CH_ENA      0
#define CH_ENB      1

#define TRIG 5
#define ECHO 18

WiFiUDP udp;
WiFiUDP udpSensor;

void setMotor(float valor, int pinA, int pinB, int pwmChannel);

float medirDistancia() {
    digitalWrite(TRIG, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);
    long duracion = pulseIn(ECHO, HIGH, 15000);
    return duracion * 0.034 / 2.0;
}

void setup() {
    Serial.begin(115200);

    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);

    ledcSetup(CH_ENA, PWM_FREQ, PWM_RES);
    ledcAttachPin(ENA, CH_ENA);
    ledcSetup(CH_ENB, PWM_FREQ, PWM_RES);
    ledcAttachPin(ENB, CH_ENB);

    setMotor(0.0, IN1, IN2, CH_ENA);
    setMotor(0.0, IN3, IN4, CH_ENB);

    WiFi.begin(SSID, PASSWORD);
    Serial.print("Conectando WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println();
    Serial.print("IP del ESP32: ");
    Serial.println(WiFi.localIP());

    udp.begin(UDP_PORT);
    udpSensor.begin(PC_PORT);
}

void loop() {
    // ── Recibir comandos de motores ────────────────────────────
    int packetSize = udp.parsePacket();
    if (packetSize > 0) {
        char buf[64];
        int len = udp.read(buf, sizeof(buf) - 1);
        buf[len] = '\0';
        String mensaje = String(buf);

        int idxIzq = mensaje.indexOf("VMIZ:");
        int idxDer = mensaje.indexOf("VMDE:");

        if (idxIzq != -1 && idxDer != -1) {
            float motor_izq = mensaje.substring(idxIzq + 5, mensaje.indexOf('\n', idxIzq)).toFloat();
            float motor_der = mensaje.substring(idxDer + 5, mensaje.indexOf('\n', idxDer)).toFloat();

            motor_izq = constrain(motor_izq, -1.0f, 1.0f);
            motor_der = constrain(motor_der, -1.0f, 1.0f);

            setMotor(motor_izq, IN1, IN2, CH_ENA);
            setMotor(motor_der, IN3, IN4, CH_ENB);
        }
    }

    // ── Enviar distancia a la PC ───────────────────────────────
    static unsigned long lastSend = 0;
    if (millis() - lastSend > 100) {
        float distancia = medirDistancia();
        char buf[32];
        snprintf(buf, sizeof(buf), "DIST:%.2f\n", distancia);
        udpSensor.beginPacket(PC_IP, PC_PORT);
        udpSensor.print(buf);
        udpSensor.endPacket();
        lastSend = millis();
    }
}

void setMotor(float valor, int pinA, int pinB, int pwmChannel) {
    uint8_t pwm = (uint8_t)(abs(valor) * 255.0f);

    if (valor > 0.0f) {
        digitalWrite(pinA, HIGH);
        digitalWrite(pinB, LOW);
    } else if (valor < 0.0f) {
        digitalWrite(pinA, LOW);
        digitalWrite(pinB, HIGH);
    } else {
        digitalWrite(pinA, LOW);
        digitalWrite(pinB, LOW);
    }

    ledcWrite(pwmChannel, pwm);
}