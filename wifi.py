import rclpy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float32
import socket

ESP32_IP   = "10.14.198.23"
ESP32_PORT = 5006
PC_PORT    = 5007

pe = 0.0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock_sensor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_sensor.bind(("0.0.0.0", PC_PORT))
sock_sensor.setblocking(False)

pub_distancia = None


def callback(msg: Float32MultiArray):
    izq = msg.data[0]
    der = msg.data[1]
    mensaje = f"VMIZ:{izq}\nVMDE:{der}\n"
    print(f"Enviando: {mensaje.strip()}")
    sock.sendto(mensaje.encode(), (ESP32_IP, ESP32_PORT))
    print("Enviado OK")
    
def calltime():
    global pe
    global pub_distancia

    # Traigo la distancia del ESP32
    try:
        data, _ = sock_sensor.recvfrom(64)
        mensaje = data.decode()
        if "DIST:" in mensaje:
            pe = float(mensaje.split("DIST:")[1].strip())
    except BlockingIOError:
        pass

    # Publico
    msg = Float32()
    msg.data = pe
    pub_distancia.publish(msg)
    
def main():
    global pub_distancia

    rclpy.init()
    node = rclpy.create_node("wifi_node")
    node.create_subscription(Float32MultiArray, "/motores_final",callback,1)
        
    pub_distancia = node.create_publisher(Float32, "/distancia", 10)
        
    node.create_timer(0.01, calltime)
    
    print(f"Nodo iniciado, enviando a {ESP32_IP}:{ESP32_PORT}")
    print(f"Escuchando distancia en puerto {PC_PORT}")
    
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()