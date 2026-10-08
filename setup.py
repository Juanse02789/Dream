import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'hand_gesture_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Registra archivos .urdf y .launch.py
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='juan-lopez',
    maintainer_email='jclopezdecastro0201@gmail.com',
    description='Control de brazo robotico por gestos en ROS2',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'gesture_detector = hand_gesture_control.gesture_detector_node:main',
            'hand_controller = hand_gesture_control.hand_controller_node:main',
        ],
    },
)