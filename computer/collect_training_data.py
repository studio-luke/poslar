#-*-coding:utf-8 -*-
import numpy as np
import cv2
# import serial
import pygame
from pygame.locals import *
import socket
import time
import os

class CollectTrainingData(object):

    def __init__(self, host, port, input_size):

        #self.server_socket = socket.socket()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)

        # accept a single connection
        #self.connection = self.server_socket.accept()[0].makefile('rb')
        self.connection = self.server_socket.accept()[0]
        self.send_inst = True

        self.input_size = input_size

        # create labels
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1

        pygame.init()
        pygame.display.set_mode((250, 250))
        pygame.key.set_repeat(True)

    def collect(self):

        saved_frame = 0
        total_frame = 0

        # collect images for training
        print("Start collecting images...")
        print("Press 'q' or 'x' to finish...")
        start = cv2.getTickCount()

        # //////////////////////////////////////////////////// #
        # //////////////////////////////////////////////////// #

        X = np.empty((0, self.input_size))
        y = np.empty((0, 4))

        # stream video frames one by one
        try:
            stream_bytes = b' '
            frame = 1
            cnt = 0
            while self.send_inst:
                #stream_bytes += self.connection.read(1024)
                stream_bytes += self.connection.recv(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]

                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

                    # select lower half of the image
                    height, width = image.shape
                    #roi = image[int(height/2):height, :]
                    roi = image[120:240, :]

                    cv2.imshow('roi', roi)
                    cv2.imshow('origin', image)

                    # reshape the roi image into a vector
                    temp_array = roi.reshape(1, int(height/2) * width).astype(np.float32)


                    frame += 1
                    total_frame += 1

                    # get input from human driver
                    for event in pygame.event.get():

                        if event.type == KEYDOWN:
                            key_input = pygame.key.get_pressed()

                            # complex orders
                            # 서버 컴퓨터에서 에서 화살표 키 입력 시 그에 해당하는 알파벳 문자?를
                            # 인코드 해서 라즈베리 파이에 보냄!
                            # 그럼 라즈베리 파이가 그걸 인식하고 모터를 돌리겠지??
                            if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                               print("Forward Right")
                               X = np.vstack((X, temp_array))
                               y = np.vstack((y, self.k[1]))
                               saved_frame += 1
                               self.connection.send('d'.encode())

                            elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                               print("Forward Left")
                               X = np.vstack((X, temp_array))
                               y = np.vstack((y, self.k[0]))
                               saved_frame += 1
                               self.connection.send('a'.encode())

                            elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
                               print("Reverse Right")
                               self.connection.send('c'.encode())

                            elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
                               print("Reverse Left")
                               self.connection.send('z'.encode())

                            # simple orders
                            if key_input[pygame.K_UP]:
                                print("Forward")
                                saved_frame += 1
                                X = np.vstack((X, temp_array))
                                y = np.vstack((y, self.k[2]))
                                self.connection.send('w'.encode())

                            elif key_input[pygame.K_DOWN]:
                                print("Reverse")
                                saved_frame += 1
                                self.connection.send('x'.encode())
                                #X = np.vstack((X, temp_array))
                                #y = np.vstack((y, self.k[3]))

                            elif key_input[pygame.K_RIGHT]:
                                print("Right")
                                X = np.vstack((X, temp_array))
                                y = np.vstack((y, self.k[1]))
                                saved_frame += 1
                                self.connection.send('d'.encode())

                            elif key_input[pygame.K_LEFT]:
                                print("Left")
                                X = np.vstack((X, temp_array))
                                y = np.vstack((y, self.k[0]))
                                saved_frame += 1
                                self.connection.send('a'.encode())

                            elif key_input[pygame.K_q]:
                                print("exit")
                                self.send_inst = False
                                self.connection.send('q'.encode())
                                self.connection.close()
                                break

                            elif key_input[pygame.K_s]:
                                print("stop")
                                self.connection.send('s'.encode())

                            elif key_input[pygame.K_f]:
                                print("reset")
                                X = np.empty((0, self.input_size))
                                y = np.empty((0, 4))

                        else : # key up
                            self.connection.send('s'.encode())

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            # save data as a numpy file
            file_name = str(int(time.time()))
            directory = "training_data"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                np.savez(directory + '/' + file_name + '.npz', train=X, train_labels=y)
            except IOError as e:
                print(e)

            end = cv2.getTickCount()
            # calculate streaming duration
            print("Streaming duration: , %.2fs" % ((end - start) / cv2.getTickFrequency()))

            print(X.shape)
            print(y.shape)
            print("Total frame: ", total_frame)
            print("Saved frame: ", saved_frame)
            print("Dropped frame: ", total_frame - saved_frame)

        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    # host, port

    h, p = "141.223.163.207", 5557

    # serial port
    #sp = "/dev/tty.usbmodem1421"

    # vector size, half of the image
    s = 120 * 320

    ctd = CollectTrainingData(h, p, s)
    ctd.collect()
