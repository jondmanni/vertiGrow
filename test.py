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
        f = open('buttonStatus.txt', 'w')
        f.write('ON '+LED0_time+' 1 \n')
        f.write('OFF '+LED0_time+' 0 \n')
        f.close()
        return 1;
    except:
        return 0;
