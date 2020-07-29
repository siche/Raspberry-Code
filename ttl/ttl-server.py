import RPi.GPIO as GPIO
import sys
import time
import socket
import threading

outs = [16,20,21]
ttl_names = ['370 zero','Flip Mirror','399']
SOCK_PORT = 6666
MAX_LISTEN_PORT = 10
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

for i in range(len(outs)):
        GPIO.setup(outs[i],GPIO.OUT)
        GPIO.output(outs[i],False)
state = [False, False, False]
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.1.16',SOCK_PORT))
s.listen(MAX_LISTEN_PORT)

def tcp_link(sock, addr):
        print('Accept new connection from %s:%s...' % addr)
        sock.send(b'CONNECTED to TTL SERVER')
        while True:
                code = sock.recv(1024).decode('utf-8')
                code_contents = code.split(' ')
                num = int(code_contents[0])
                status = code_contents[1]

                if status == 'on':
                        GPIO.output(outs[num],True)
                        state[num] = True
                        print(ttl_names[num] + 'is ON')
                if status == 'off':
                        GPIO.output(outs[num],False)
                        state[num] = False
                        print(ttl_names[num] + 'is OFF')
                
                if status == '?':
                        return state[num]

                reply = ttl_names[num] + ' is ' + status
                sock.send(reply.encode('utf-8'))
        sock.close()
        print('Connection from %s:%s closed' % addr)

while True:
        sock, addr = s.accept()
        t = threading.Thread(target=tcp_link, args=(sock, addr))
        t.setDaemon(True)
        t.start()


