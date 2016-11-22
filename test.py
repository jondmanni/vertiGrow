def test_method():
    r = 0
    try:
        f = open('text.txt', 'w')
        f.write('Success!')
        f.close()
        r = 1
    except:
        r = 0
    return r
