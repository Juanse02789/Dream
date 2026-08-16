import rclpy
from std_msgs.msg import String
import pygame

pygame.mixer.init()

SONIDOS = {
    "ElSEÑORDELANOCHE": "/home/juan-lopez/Descargas/else.mp3"
}

def callback(msg: String):
    comando = msg.data
    if comando in SONIDOS:
        print(f"Reproduciendo: {comando}")
        pygame.mixer.music.load(SONIDOS[comando])
        pygame.mixer.music.play()

def main():
    rclpy.init()
    node = rclpy.create_node("nodo_audio")
    node.create_subscription(String, "/control_audio", callback, 1)
    print("Nodo audio iniciado")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()