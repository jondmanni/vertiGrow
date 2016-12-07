import serial
import time
import array
arduino = serial.Serial('/dev/ttyACM0', 9600)
#arduino = serial.Serial('/dev/tty.usbmodem1421', 9600, timeout=.1)

status = ''
words = ''
onLength = [0, 0, 0]
writeArduino = 0

i = 0

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

    with open('buttonStatus.txt', 'r+') as file:
        i = 0
        writeArduino = 0
        #try:
        lines = file.readlines()
        for line in lines:
            status = ''
            line.strip()
            words = line.split(',')
            print(words)
            if len(words) > 1 and len(words) <= 4:
                if words[2] == '1':
                    onLength[i] = int(words[1])
                    words[2] = '0'
                    status = words[0] + ',' + words[1] + ',' + words[2] + ','
                    #print("i equals" + str(i))
                    #print(len(status))
                    file.seek((len(status)+1)*i, 0)
                    file.write(status)
                    ##print(status)
                    #file.write(status)
                    ##print(words[0])
                    ##print(onLength[i])
                if words[0] == 'ON' and onLength[i] > 0:
                    #print('1')
                    writeArduino = writeArduino + i + 1
                    onLength[i] = onLength[i] - 1
                elif words[0] == 'OFF' or onLength[i] == 0:
                    i = i
                    #print('0')
                    #arduino.write('0')
            elif len(words) == 1:
                i = i
            else:
                if words[1] == '1':
                    onLength[i] = int(words[0])
                    words[1] = '0'
                    status = words[0] + ',' + words[1] + ',' + words[2] + ',' + words[3] + ','
                    file.seek(18, 0)
                    file.write(status)
                    print(status)
                    writeArduino = writeArduino + 4
                    #writeArduino = writeArduino + int(words[2]) * 8
                    #writeArduino = writeArduino + 16
                    #writeArduino = writeArduino + int(words[0]) * 32
            #next(file)
            arduino.write(str(writeArduino))
            data = arduino.readline()
            #if data:
            #    print('Arduino:')
            #    print data.rstrip('\n')
            print(writeArduino)
            #print(status)
            i = i + 1
        #except IndexError:
        #    print('IndexError')
