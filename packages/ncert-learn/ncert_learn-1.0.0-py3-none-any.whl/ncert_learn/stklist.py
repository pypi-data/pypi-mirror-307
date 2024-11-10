def createstacklst():
        return []
def clearstacklst(a):
        a.clear()
def pushstacklst(a,b):
        a.append(b)
        return a
def popstacklst(a):
        if a==[]:
            return -1
        else:
            s=a.pop()
            return(a)
def peekstacklst(a):
        if a==[]:
            return -1
        else:
            return a[-1]
def displaymodestacklst(a):
        s=[]
        for i in range(-1,(len(a)*-1)-1,-1):
            s.append(a[i])
        return s
