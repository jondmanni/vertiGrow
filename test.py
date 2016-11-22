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
