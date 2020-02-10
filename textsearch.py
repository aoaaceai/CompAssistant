def search(string,start="", end=""):
    lstart=len(start)
    lend=len(end)
    startpoint=endpoint=0
    for i in range(len(string)):
        if string[i:i+lstart]==start:
            startpoint=i+lstart
    for i in range(len(string)-lend, startpoint, -1):
        if string[i:i+lend]==end:
            endpoint=i
    return string[startpoint:endpoint]

if __name__=="__main__":
    search("hello", "he", "lo")