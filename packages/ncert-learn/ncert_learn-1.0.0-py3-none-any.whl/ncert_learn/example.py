import intfncs
def exampleusage():
    print('Welcome!')
    print('This is Your Example!')
    print('Please Choose One:')
    print('------------------------------------------------------')
    count_ds=0
    while True:
        if count_ds!=0: print('+----------------------------------------------------+')
        count_ds+=1
        print('1.Check A Number Is Prime Or Not\n2.Check A Number Is Armstrong Or Not\n3.Print Febinocii Series With a Limit\n4.Print Factors Of A Number\n5.Reverse A Number\n0.Exit')
        try:
            a=int(input('Entry :'))
            if a>-1 and a<6:    pass
            else:   print('Plese Enter A Valid Number')
        except ValueError:  print('Please Enter A Valid Integer')

        if a==1:
            while True:
                try:
                    a=int(input('Enter Number To Check :'))
                    if intfncs.checkprime(a):   print('The Number You Entered Is A Prime')
                    else:   print('The Number You Entered Is Not A Prime')
                except ValueError:
                    print('Please Enter A Integer')
                    b=input('Do You Wanna Renter Your Integer Value(Default Is Yes) :')
                    c=b.lower()
                    if c.startswith('y') or c=='' or c==' ':   pass
                    else:   break
                else:   break
        if a==2:
            while True:
                try:
                    a=int(input('Enter Number To Check :'))
                    if intfncs.checkarmstrong(a):   print('The Number You Entered Is Armstrong')
                    else:   print('The Number You Entered Is Not Armstrong')
                except ValueError:
                    print('Please Enter A Integer')
                    b=input('Do You Wanna Renter Your Integer Value(Default Is Yes) :')
                    c=b.lower()
                    if c.startswith('y') or c=='' or c==' ':    pass
                    else:   break
                else:   break
        if a==3:
            while True:
                try:
                    a=int(input('Enter The Limit Of Febinocii Series :'))
                    n=len(intfncs.len_fibonacci(a))
                    s=intfncs.len_fibonacci(a)
                    print(f'This Is A Febinocii Series With {a} Elements ')
                    for i in range(n):
                        if i==n-1:  print(str(s[i])+'.')
                        else:   print(str(s[i]),end=',')
                except ValueError:
                    print('Please Enter A Integer')
                    b=input('Do You Wanna Renter Your Integer Value(Default Is Yes) :')
                    c=b.lower()
                    if c.startswith('y') or c=='' or c==' ':    pass
                    else:   break
                else:   break
        if a==4:
            while True:
                try:
                    a=int(input('Enter The Number To Print Factors :'))
                    n=len(intfncs.factors(a))
                    s=intfncs.factors((a))
                    print(f'This Are Factors Of {a}')
                    for i in range(n):
                        if i==n-1:  print(str(s[i])+'.')
                        else:   print(str(s[i]),end=',')
                except ValueError:
                    print('Please Enter A Integer')
                    b=input('Do You Wanna Renter Your Integer Value(Default Is Yes) :')
                    c=b.lower()
                    if c.startswith('y') or c=='' or c==' ':   pass
                    else:   break
                else:   break
        if a==0:
            print('Exiting.')
            break
        if a==5:
            while True:
                try:
                    a=int(input('Enter Number To Reverse :'))
                    print(f'{intfncs.reverse(a)} Is Reverse Of Number You Entered')
                except ValueError:
                    print('Please Enter A Integer')
                    b=input('Do You Wanna Renter Your Integer Value(Default Is Yes) :')
                    c=b.lower()
                    if c.startswith('y') or c=='' or c==' ':   pass
                    else:   break
                else:   break