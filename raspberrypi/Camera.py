import io #file input/output
import struct #C에서의 struct랑 같음
import time #여러 시간과 관련된 function
import picamera #pi camera 관련 function

class Camera(object):
    def __init__(self, server):
        #wb: binary mode로 write한다
        self.server = server.makefile('wb')

    #run function
    #   Description: 카메라를 실행하여 영상정보를 사진정보로 받아옴
    def run(self):
        with picamera.PiCamera() as camera :
            #camera의 resolution
            #   input: wideth, height
            camera.resolution = (320, 240) 
            #camera가 초당 전송하는 frame 개수
            camera.framerate = 20
            #일시정지 함수
            #   input: 일시정지할 시간
            time.sleep(2)
            #현재시간 return function
            start = time.time()
            #byte 배열을 이진 배열로 사용할 수 있도록 해줌
            stream = io.BytesIO()
            #capture function
            #   input: 위치, 파일형식, 이미지 캡쳐 여부에 사용이 된다
            #   output: infinity iterator
            for _ in camera.capture_continuous(stream, 'jpeg', use_video_port = True) :
                #pack function
                #   Description: 원하는 format으로 값을 변환해줌 
                #   input: format, 현재 stream 위치 //여기서 format에 <을 써주면 주소를 little-endian으로 정렬(하위->상위)
                #   output: 해당 format으로의 변환값을 return
                #write function 
                #   Description: ()속 형태의 문자열을 파일에(서버에) 쓴다
                self.server.write(struct.pack('<L', stream.tell()))
                #flush function
                #   Description: 버퍼가 다 채워지지 않아도 내부 버퍼 내용을 파일에 보냄
                self.server.flush()
                #seek function
                #   Description: stream 위치를 주어진 byteoffset으로 변경 -> 0이면 stream의 시작. 기본값
                stream.seek(0)
                #read function
                #   Description: ()속만큼 파일을 읽어온다. 비어있거나 -1이면 전체를 읽어옴.
                #write function: 위 Description 참고
                self.server.write(stream.read())
                if time.time() - start > 600 :
                    break
                stream.seek(0)
                #truncate function
                #   Description: stream의 크기를 지정된 크기로 조절. 지정되지 않을 경우 현재 크기로 변경.
                stream.truncate()
        self.server.write(struct.pack('<L', 0))
