def checkprime(a):
    c=0
    for i in range(1,a+1):
        if a%i==0:
            c+=1
    if c==2:
        return True
    else:
        return False
def factors(a):
    c=()
    for i in range(1,a+1):
        if a%i==0:
            c+=(i,)
    return c
def len_fibonacci(a):
    z=()
    c,b,e=-1,1,0
    for i in range(a):
        e=b+c
        c=b
        b=e
        z+=(e,)
    return  z
def checkarmstrong(a):
    z=a
    s=0
    while a>0:
        r=a%10
        a=int(a//10)
        s+=r**3
    if s==z:    return True
    else:   return False
def reverse(a):
    k=str(a)
    k=k[::-1]
    k=int(k)
    return k
def checkpalindrome(a):
    k=str(a)
    k=k[::-1]
    k=int(k)
    if k==a:
        return True
    else:
        return False
def checkstrong(a):
    c=0
    for i in range(1,a+1):
        if a%i==0:
            c+=i
    if c==a:    return True
    else:   return False
def checkniven(a):
    z=a
    s=0
    while a>0:
        r=a%10
        a=int(a//10)
        s+=r
    if z%s==0:  return True
    else:   return True
def prime(z):
    m=()
    for a in range(2,z+1):
        c=0
        for i in range(1,a+1):
            if a%i==0:
                c+=1
        if c==2:
            m+=(a,)
        else:
            pass
    if m==():
        return -1
    else:
        return m
def armstrong(z):
    m=()
    for a in range(1,z+1):
        k=a
        s=0
        while a>0:
            r=a%10
            a=int(a//10)
            s+=r**3
        if s==k:    m+=(s,)
        else:   pass
    if m==():
        return -1
    else:
        return m
def strong(z):
    m=()
    for a in range(2,z+1):
        c=0
        for i in range(1,a+1):
            if a%i==0:
                c+=i
        if c==a:    m+=(c,)
        else:   pass
    if m==():
        return -1
    else:
        return m
def niven(z):
    m=()
    for a in range(2,z+1):
        i=a
        s=0
        while a>0:
            r=a%10
            a=int(a//10)
            s+=r
        if i%s==0:  m+=(i,)
        else:   pass
    if m==():
        return -1
    else:
        return m
def palindrome(z):
    m=()
    for a in range(1,z+1):
        k=str(a)
        k=k[::-1]
        k=int(k)
        if k==a:
            m+=(k,)
        else:
            pass
    if m==():
        return -1
    else:
        return m
def len_prime(yt):
    m=()
    k=2
    while True:
        a=k
        c=0
        for i in range(1,a+1):
            if a%i==0:
                c+=1
        if c==2:
            m+=(a,)
        else:
            pass
        k+=1
        if len(m)==yt:
            break
    if m==():
        return -1
    else:
        return m
def len_armstrong(yt):
    m=()
    re=1
    while True:
        a=re
        k=a
        s=0
        while a>0:
            r=a%10
            a=int(a//10)
            s+=r**3
        if s==k:    m+=(s,)
        else:   pass
        re+=1
        if len(m)==yt:
            break
    if m==():
        return -1
    else:
        return m
def len_strong(yt):
    m=()
    re=2
    while True:
        a=re
        c=0
        for i in range(1,a+1):
            if a%i==0:
                c+=i
        if c==a:    m+=(c,)
        else:   pass
        re+=1
        if len(m)==yt:
            break
    if m==():
        return -1
    else:
        return m
def len_niven(yt):
    m=()
    re=2
    while True:
        a=re
        i=a
        s=0
        while a>0:
            r=a%10
            a=int(a//10)
            s+=r
        if i%s==0:  m+=(i,)
        else:   pass
        re+=1
        if len(m)==yt:
            break
    if m==():
        return -1
    else:
        return m
def len_palindrome(yt):
    m=()
    re=1
    while True:
        a=re
        k=str(a)
        k=k[::-1]
        k=int(k)
        if k==a:
            m+=(k,)
        else:
            pass
        re+=1
        if len(m)==yt:
            break
    if m==():
        return -1
    else:
        return m
def checkeven(a):
    if a%2==0 and a!=0:
        return True
    else:
        return False
def checkodd(a):
    if a%2==1:
        return True
    else:
        return False
def checkzero(a):
    if a==0:
        return True
    else:
        return False
def checknegative(a):
    if a<0:
        return True
    else:
        return True
def checkpositive(a):
    if a>0:
        return True
    else:
        return False
