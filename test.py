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
        else:
            f.write(lines[0])
            f.write(lines[1])
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
            f.write('ON,'+LED1_time+',1,')
        else:
            f.write(lines[0])
            f.write(lines[1])
        f.close()
        return 1;
    except:
        return 0;
