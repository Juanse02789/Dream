import rclpy

from std_msgs.msg import Float32MultiArray
from std_msgs.msg import String


motor_der1 = 0.0
motor_izq1 = 0.0

audio1 = ""

def callback_motores(msg:Float32MultiArray):
    global motor_izq1
    global motor_der1

    motor_izq1 = msg.data[0]
    motor_der1 = msg.data[1]




def callback_audio(msg:String):

    global audio1

    audio1 = msg.data


def calltime():
    
    global motor_der1
    global motor_izq1
    global audio1

    print ("---------------")

    print ("Estado del motor izquierdo = " + str(motor_izq1))
    print ("Estado del motor derecho = " + str(motor_der1))

    print("----------------")

    if audio1 == "":
        print("No se esta reproduciendo nada")
    else:
        print("El señor de la noche")


def main():
    
    rclpy.init()

    node = rclpy.create_node("Nodo_Monitor")

    node.create_subscription(Float32MultiArray,"/control_motores", callback_motores ,10)
    node.create_subscription(String, "/control_audio", callback_audio, 10)

    node.create_timer(0.1,calltime)

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()