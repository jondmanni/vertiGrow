def test_method():
    r = 0
    try:
        f = open('buttonStatus.txt', 'w')
        f.write('ON 5 1 ')
        f.close()
        r = 1
    except:
        r = 0
    return r

def LED0_update(LED0_time):
    try:
        f = open('buttonStatus.txt', 'r')
        lines = f.readlines()
        f.close()
        f = open('buttonStatus.txt', 'w')
        if (LED0_time != ''):
            f.write('ON,'+LED0_time+',1,\n')
            f.write(lines[1])
            f.write(lines[2])
        else:
            f.write(lines[0])
            f.write(lines[1])
            f.write(lines[2])
        f.close()
        return 1;
    except:
        return 0;

def LED1_update(LED1_time):
    try:
        f = open('buttonStatus.txt', 'r')
        lines = f.readlines()
        f.close()
        f = open('buttonStatus.txt', 'w')
        if (LED1_time != ''):
            f.write(lines[0])
            f.write('ON,'+LED1_time+',1,\n')
            f.write(lines[2])
        else:
            f.write(lines[0])
            f.write(lines[1])
            f.write(lines[2])
        f.close()
        return 1;
    except:
        return 0;

def MOTOR_update(MOTOR_steps):
    try:
        f = open('buttonStatus.txt', 'r')
        lines = f.readlines()
        f.close()
        f = open('buttonStatus.txt', 'w')
        if (MOTOR_steps != ''):
            f.write(lines[0])
            f.write(lines[1])
            f.write(MOTOR_steps+',1,0,1,')
        else:
            f.write(lines[0])
            f.write(lines[1])
            f.write(lines[2])
        f.close()
        return 1;
    except:
        return 0;

#def send_home():
    # This function will use the serial port to communicate with the
    # Arduino to tell the motors to home the X-axis
