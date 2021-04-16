# just a file to test some logic
if __name__ == '__main__':
    x = "1"
    y = "2"
    a = set()
    b = set()
    for it in x.split(" "):
        a.add(it)
    for it in y.split(" "):
        b.add(it)
    c = b.union(a)
    print(c)
    nextStr = []
    for x in c:
        nextStr += x
    nextStr.sort()
    nextStr2 = ""
    for x in nextStr:
        nextStr2 += x
        nextStr2 += " "
    nextStr2 = nextStr2[:-1]
    print(nextStr2)


