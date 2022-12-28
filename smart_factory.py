import cv2
import serial
import numpy as np
from keras.models import load_model
import threading
import time

PORT='COM9'
baud=19200
startBit=0xAA #시리얼 통신은 한방향, 시작할 때 신호

ser=serial.Serial(PORT, baud, timeout=1)

cap=cv2.VideoCapture(0)

def start_belt():
    main_command = 0x01
    sub_command = 0x01

    packet = bytearray()
    packet.append(startBit)

    data = [main_command, sub_command]
    length = len(data) + 0x03
    packet.append(length)

    for d in data:
        packet.append(d)

    checksum = ~(length + sum(data)) & 0xFF
    packet.append(checksum)
    ser.write(packet)
    print("start함수 실행")

def stop_belf():
    main_command=0x01
    sub_command=0x00

    packet=bytearray()
    packet.append(startBit)

    data=[main_command, sub_command]
    length=len(data)+0x03
    packet.append(length)

    for d in data:
        packet.append(d)

    checksum= ~(length+sum(data))&0xFF
    packet.append(checksum)
    ser.write(packet)

def class_A():
    main_command = 0x03
    sub_command = 0x01

    packet = bytearray()
    packet.append(startBit)
    data = [main_command, sub_command]
    length = len(data) + 0x03
    packet.append(length)
    for d in data:
        packet.append(d)

    checksum = ~(length + sum(data)) & 0xFF
    packet.append(checksum)
    ser.write(packet)

def class_B():
    main_command = 0x03
    sub_command = 0x02

    packet = bytearray()
    packet.append(startBit)
    data = [main_command, sub_command]
    length = len(data) + 0x03
    packet.append(length)
    for d in data:
        packet.append(d)

    checksum = ~(length + sum(data)) & 0xFF
    packet.append(checksum)
    ser.write(packet)

def class_C():
    main_command = 0x03
    sub_command = 0x03

    packet = bytearray()
    packet.append(startBit)
    data = [main_command, sub_command]
    length = len(data) + 0x03
    packet.append(length)
    for d in data:
        packet.append(d)

    checksum = ~(length + sum(data)) & 0xFF
    packet.append(checksum)
    ser.write(packet)

def speed_up():
    main_command = 0x04
    sub_command = 0x01

    packet = bytearray()
    packet.append(startBit)

    data = [main_command, sub_command]
    length = len(data) + 0x03
    packet.append(length)

    for d in data:
        packet.append(d)

    checksum = ~(length + sum(data)) & 0xFF
    packet.append(checksum)
    ser.write(packet)
    print("speed up 함수 실행")

def speed_down():
    main_command = 0x04
    sub_command = 0x02

    packet = bytearray()
    packet.append(startBit)
    data = [main_command, sub_command]
    length = len(data) + 0x03
    packet.append(length)

    for d in data:
        packet.append(d)

    checksum = ~(length + sum(data)) & 0xFF
    packet.append(checksum)
    ser.write(packet)


def model():
    # Load the model
    model = load_model('C:/Users/7/Desktop/test/converted_keras/keras_model.h5')

    # CAMERA can be 0 or 1 based on default camera of your computer.
    camera = cv2.VideoCapture(0)

    # Grab the labels from the labels.txt file. This will be used later.
    labels = open('C:/Users/7/Desktop/test/converted_keras/labels.txt', 'r').readlines()

    while True:
        # Grab the webcameras image.
        ret, image = camera.read()
        # Resize the raw image into (224-height,224-width) pixels.
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        # Show the image in a window
        cv2.imshow('Webcam Image', image)
        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        # Normalize the image array
        image = (image / 127.5) - 1
        # Have the model predict what the current image is. Model.predict
        # returns an array of percentages. Example:[0.2,0.8] meaning its 20% sure
        # it is the first label and 80% sure its the second label.
        probabilities = model.predict(image)
        # Print what the highest value probabilitie label
        #print(labels[np.argmax(probabilities)])
        if labels[np.argmax(probabilities)][0] != ' ':
            time.sleep(0.5)
            print("판별 대기")

        if labels[np.argmax(probabilities)][0]=='0':
            print("0 circle")
            time.sleep(1)
            class_A()

            time.sleep(3)
        elif labels[np.argmax(probabilities)][0]=='2':
            print("1 Square")
            time.sleep(1.5)
            class_B()

            time.sleep(3)
        elif labels[np.argmax(probabilities)][0]=='1' :

            class_C()
            print("2 triangle")
        else :
            class_C()
            print('물체를 올려주십시오.')
        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)
        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            break

    camera.release()
    cv2.destroyAllWindows()


# def main():
#     start_belt()
#     class_A()
#     time.sleep(10)
#     class_B()
#     time.sleep(10)
#     class_C()
#     time.sleep(10)
#     stop_belf()


def main():
    #  start_belt()
    # speed_up()
    # speed_up()
    #   model()
    #     speed_up()
    #   speed_up()
         stop_belf()

# def main():
#     start_belt()
#     for
main()
#
