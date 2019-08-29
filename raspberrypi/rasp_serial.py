# Some code has modified.

import wiringpi  # python 표준 모듈. 라즈베리파이의 GPIO 핀을 제어하는 기능 제공
import playmusic

class Serial(object):
    #TODO: CODE MODIFIED, default_speed -> Class Attribute
    default_speed = 120

    def __init__(self):

        self.music = playmusic.MUSIC()
        # default speed
        self.speed = self.default_speed

        # motor
        self.STOP = 0
        self.FORWARD = 1
        self.BACKWARD = 2
        self.DIR = 3

        #motor channel
        self.CH1 = 0
        self.CH2 = 1

        #PIN input & output
        self.OUTPUT = 1
        self.INPUT = 0

        #PIN setting
        self.HIGH = 1
        self.LOW = 0

        #Raspberry GPIO setting
        #PWM
        self.ENA = 4 #front wheel
        self.ENB = 5 #rear wheel

        #GPIO PIN
        self.IN1 = 30
        self.IN2 = 21
        self.IN3 = 22
        self.IN4 = 23

        wiringpi.wiringPiSetup()                            # 초기화(Initialize)

        self.setPinConfig(self.ENA, self.IN1, self.IN2)     # 51번줄 정의 참고)
        self.setPinConfig(self.ENB, self.IN3, self.IN4)

    #PIN setting function
    #   Description: Input GPIO들을 OUTPUT으로 매핑 및 Software PWM을 생성?하는 함수
    #   input:
    #       EN: PWM 단자(모터)
    #       INA, INB: 2개의 GPIO 단자들
    #   output: None
    def setPinConfig(self, EN, INA, INB):
        wiringpi.pinMode(EN, self.OUTPUT)   # 핀들을 OUTPUT으로 매핑
        wiringpi.pinMode(INA, self.OUTPUT)
        wiringpi.pinMode(INB, self.OUTPUT)
        wiringpi.softPwmCreate(EN, 0, 255)  # EN 핀이 0~255 사이의 하나의 값을 가지도록

    #motor control function
    #   Description: 모터의 속도를 조절해주는 함수
    #   input:
    #       PWM: PWM 단자(=EN)
    #       INA, INB: 2개의 GPIO 단자들
    #       speed: 모터의 속도 값
    #   output: None
    def setMotorControl(self, PWM, INA, INB, speed, stat):
        #motor speed control PWM
        wiringpi.softPwmWrite(PWM, speed)   # PWM(모터) 값을 speed 값으로 조정

        #TODO: INA, INB값이 HIGH, LOW로 계속 바뀌는데 정확히 어떤 의미인지?

        #FORWARD
        if stat == self.FORWARD:
            wiringpi.digitalWrite(INA, self.HIGH)
            wiringpi.digitalWrite(INB, self.LOW)

        #BACKWARD
        elif stat == self.BACKWARD:
            wiringpi.digitalWrite(INA, self.LOW)
            wiringpi.digitalWrite(INB, self.HIGH)

        #STOP
        elif stat == self.STOP:
            wiringpi.digitalWrite(INA, self.LOW)
            wiringpi.digitalWrite(INB, self.LOW)

        elif stat == self.DIR:
            wiringpi.digitalWrite(INA, self.HIGH)
            wiringpi.digitalWrite(INB, self.HIGH)

    #motor control function_warp
    #ch1 == front
    #ch2 == back

    #TODO: 채널은 무슨 의미인지?

    def setMotor(self, ch, speed, stat):
        if ch == self.CH1:
            self.setMotorControl(self.ENA, self.IN1, self.IN2, speed, stat)
        else :
            self.setMotorControl(self.ENB, self.IN3, self.IN4, speed, stat)

    def steer(self, data):
        print(data)
        if data == '60' :
            print('limit 60')
            self.speed = 180
            self.music.play_music('./sounds/limit60.mp3')
        elif data == '30' :
            self.speed = self.default_speed
            self.music.play_music('./sounds/limit30.mp3')
        elif (data == 'w') or (data == 'lw') or (data == 'ww') :
            self.setMotor(self.CH1, self.speed, self.DIR)

            self.setMotor(self.CH2, self.speed, self.FORWARD)
            if data == 'lw' :
                self.music.play_music('./sounds/go.mp3')
        elif data == 'x' :
            self.setMotor(self.CH2, self.speed, self.BACKWARD)
        elif data == 'a' :
            self.setMotor(self.CH1, 255, self.FORWARD)
            self.setMotor(self.CH2, self.speed, self.FORWARD)
        elif (data == 'd') or (data == 'td') :
            self.setMotor(self.CH1, 255, self.BACKWARD)
            self.setMotor(self.CH2, self.speed, self.FORWARD)
            if data == 'td' :
                self.music.play_music('./sounds/turn_right.mp3')
        elif (data == 's') or (data == 'us') or (data == 'ls') or (data == 'ss') :
            self.setMotor(self.CH1, self.speed, self.DIR)
            self.setMotor(self.CH2, 0, self.STOP)
            if data == 's' :
                self.music.play_music('./sounds/stop.mp3')
            elif data == 'us' :
                self.music.play_music('./sounds/obs_stop.mp3')
            elif data == 'ls' :
                self.music.play_music('./sounds/light_stop.mp3')
            elif data == 'ss' :
                self.music.play_music('./sounds/wait.mp3')
