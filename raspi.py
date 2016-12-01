import serial
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.OUT)
arduino = serial.Serial('/dev/ttyACM0', 9600)

status = ''
words = ''
onLength = 0

while(True):
    time.sleep(1)
#    file = open('buttonStatus.txt', 'r+')
#    print(status)
#    status = file.readline()
#    status.strip()
#    words = status.split(' ')
#    try:
#        if words[2] == '1':
#            onLength = int(words[1])
#            words[2] = '0'
#            status = words[0] + ' ' + words[1] + ' ' + words[2]
#            file.seek(0)
#            file.write(status)
#    except IndexError, e:
#        print(e)
#    if words[0] == 'ON' and onLength > 0:
#        arduino.write('1')
#        onLength = onLength - 1
#    elif words[0] == 'OFF' or onLength == 0:
#        arduino.write('0')
#    file.close()

    with open('buttonStatus.txt') as file:
        for line in file:
            line.strip()
            words = line.split(' ')
            if line < 3:
                if words[2] == '1':
                    onLength[line] = int(words[1])
                    words[2] = '0'
                    status = words[0] + ' ' + words[1] + ' ' + words[2]
                    file.seek(0)
                    file.write(status)
                if words[0] == 'ON' and onLength[line] > 0:
                    arduino.write('1')
                    onLength[line] = onLength[line] - 1
                elif words[0] == 'OFF' or onLength[line] == 0:
                    arduino.write('0')
            else:
                if words[1] == '1':
                    onLength[line] = int(words[0])
                    words[1] = '0'
                    status = words[0] + ' ' + words[1] + ' ' + words[2] + ' ' + words[3]
                    file.seek(0)
                    file.write(status)
                arduino.write(onLength[line])
                arduino.write(words[2])
                arduino.write(words[3])

