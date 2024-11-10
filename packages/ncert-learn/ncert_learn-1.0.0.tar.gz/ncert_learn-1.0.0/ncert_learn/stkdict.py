def createstackdict():
        return {}
def clearstackdict(a):
        a.clear()
def pushstackdict(a,b):
        a.update(b)
        return a
def popstackdict(a):
        if a=={}:
            return -1
        else:
            s=a.pop()
            return(a)
def peekstackdict(a):
    s=a.keys()
    if a=={}:
        return -1
    else:
        return a[s[-1]]
def displaymodestackdict(a):
        s=[]
        for k,v in a:
            s.append((k,v))
        return s
