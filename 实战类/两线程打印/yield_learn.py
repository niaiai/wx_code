
def yield_num():
    while True:
        i = yield
        print("%d%d" % (i*2+1, i*2+2), end="")


def yield_alpha():
    while True:
        i = yield
        print(chr(i+ord('A')), end=" ")


if __name__ == "__main__":
    num = yield_num()
    alpha = yield_alpha()
    num.send(None)
    alpha.send(None)
    for n in range(26):
        num.send(n)
        alpha.send(n)
