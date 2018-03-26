import multiprocessing, sys, time

def f(icount, _sleepTime = 1):
    for i in range(icount):
        time.sleep(_sleepTime)
        print(_sleepTime)

def main(args):
    m = multiprocessing.Process(target = f, args=(4, ))
    m.start()
    # f should be sleeping for 1 second so this print statement should come first
    print(m.is_alive())
    m.join()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
