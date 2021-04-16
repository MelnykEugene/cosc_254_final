# just a file to test some logic
if __name__ == '__main__':
    x = "1"
    y = "2"
    a = {x}
    b = {y}
    b = b.union(a).sort()
    nextStr = ""
    for x in b:
        nextStr += x + " ";
    print(a)
    print(nextStr)
    print(nextStr.split(" "))


