import rclpy
from std_msgs.msg import Float32MultiArray, Float32

distancia = 999.0
motor_izq = 0.0
motor_der = 0.0

pub_motores = None

def callback_distancia(msg: Float32):
    global distancia
    distancia = msg.data

def callback_motores(msg: Float32MultiArray):
    global motor_izq, motor_der
    motor_izq = msg.data[0]
    motor_der = msg.data[1]

def calltime():
    global distancia, motor_izq, motor_der, pub_motores

    izq = motor_izq
    der = motor_der

    # Si hay obstáculo a menos de 15cm, bloquea avance
    if distancia >0.0 and distancia < 15.0:
        if izq > 0: izq = 0.0
        if der > 0: der = 0.0

    msg = Float32MultiArray()
    msg.data = [izq, der]
    pub_motores.publish(msg)

def main():
    global pub_motores

    rclpy.init()
    node = rclpy.create_node("nodo_decision")

    node.create_subscription(Float32MultiArray, "/control_motores", callback_motores, 1)
    node.create_subscription(Float32, "/distancia", callback_distancia, 1)

    pub_motores = node.create_publisher(Float32MultiArray, "/motores_final", 10)

    node.create_timer(0.01, calltime)

    print("Nodo decision iniciado")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()