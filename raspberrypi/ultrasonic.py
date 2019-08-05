# objectification
# 2018.10.12
# BCODE
import RPi.GPIO as gpio
import time

class UltraSonic(object) :
    def __init__(self) :
        gpio.setmode(gpio.BCM)
        self.trig = 17 #trig 핀 번호
        self.echo = 27 #echo 핀 번호

        gpio.setup(self.trig, gpio.OUT)
        gpio.setup(self.echo, gpio.IN)
        #trig 핀은 초음파를 내보내고 echo 핀이 되돌아온 초음파를 인식

    def run(self, server) :
        while(True):
            gpio.output(self.trig, False)
            time.sleep(0.1)
            #일단 처음에는 안 내보냄

            gpio.output(self.trig, True)
            time.sleep(0.00001)
            gpio.output(self.trig, False)
            #0.00001동안 쏜 다음에 다시 닫음

            while gpio.input(self.echo) == 0:
                pulse_start = time.time()
            #안 들어오다가 들어오기 시작한 시간 저장

            while gpio.input(self.echo) == 1:
                pulse_end = time.time()
            #들어오다가 끊긴 시간 저장

            distance = round((pulse_end - pulse_start) * 17000, 2)
            #두 시간의 차이를 이용하여 거리를 계산  
            server.Send_Data(str(int(distance)).encode())
            #거리를 문자열로 저장해서 서버로 전송
    def __del__(self) :
        gpio.cleanup()
        #점유한 리소스를 해제
