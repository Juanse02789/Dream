import rclpy

from std_msgs.msg import String
from std_msgs.msg import Float32MultiArray

from sensor_msgs.msg import Joy

from rclpy.node import Node 


#Defino variables
motor_izq = 0.0
motor_der = 0.0

Audio = ""

def calltime():
    global pub_motores
    global pub_audio
    global motor_izq
    global motor_der
    global Audio

    #Publico los datos de los motores
    motores_msg = Float32MultiArray()
    motores_msg.data = [motor_izq,motor_der]
    pub_motores.publish(motores_msg)

    #Publico el mensaje de audio
    if Audio != "":
        audio_msg = String()
        audio_msg.data = Audio
        pub_audio.publish(audio_msg)



def callback(msg: Joy):

    global motor_izq
    global motor_der
    global Audio
    
    #Defino los controles que usaracontrol_motores
   
    Velocidad = msg.axes[1]
    Direccion = msg.axes[0]
    Boton_audio = msg.buttons[3]

    
    #Para mejor funcionamiento defino una zona muerta
    if abs(Velocidad) < 0.1:
        Velocidad = 0.0

    if abs(Direccion) < 0.1:
        Direccion = 0.0

    #Hago formuolas para comportamiento diferencial

    motor_der = Velocidad - Direccion
    motor_izq = Velocidad + Direccion

    #Limto los valores de motores a 1 o -1
    if motor_izq > 1: 
        motor_izq = 1
    if motor_izq < -1:
        motor_izq = -1

    if motor_der > 1:
        motor_der = 1
    if motor_der < -1:
        motor_der = -1
    
    #Hago que cuando presione cuadrado mande comando de audio

    if Boton_audio == 1:
        Audio = "ElSEÑORDELANOCHE"
    else:
        Audio = ""

    
def main():
    global pub_motores
    global pub_audio
    
    rclpy.init()

    #creo nodo
   
    node = rclpy.create_node("Nodo_joy")

    #creo subscripcion a Joy, nodo predefinido de ROS2 para traer los datos del control
    node.create_subscription(Joy, "/joy", callback, 10)

    #Creo publicadores
    pub_motores = node.create_publisher(Float32MultiArray, "control_motores", 10)
    pub_audio = node.create_publisher(String, "control_audio",10)

    #Hago el timer
    node.create_timer(0.01, calltime)

    #Spin
    rclpy.spin(node)

    #Destruccion del nodo
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()