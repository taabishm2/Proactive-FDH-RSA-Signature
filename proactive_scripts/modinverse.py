import math
import matplotlib.pyplot as plt
import time
import nextprime
import random

global c

def modular_inverse(a, m):  
    m0 = m 
    y = 0
    x = 1
  
    if (m == 1) : 
        return 0
  
    while (a > 1) : 
        q = a // m 
        t = m 
        m = a % m 
        a = t 
        t = y 
        y = x - q * y 
        x = t
        #print("\na:",a,"m:",m,"\nx:",x,"y:",y)
  
    if (x < 0) : 
        x = x + m0 
  
    return x

xx=[]
yy=[]
zz=[]

for x in range(1,500):
    for y in range(1,500):
        if x%y != 0 and x/(x%y) != 1:
            xx.append(x)
            yy.append(y)
            zz.append(math.ceil(math.log((x*y),(x/(x%y)))))   
            
plt.scatter(xx, yy, c=zz, s=2, cmap='viridis')
plt.xlabel("value of x in f(x,y)")
plt.ylabel("value of y in f(x,y)")
plt.title("Complexity Analysis")
plt.show()

##
##mx = []
##my = []
##mz = []
##
##for i in range(500):
##    for j in range(500):
##        if math.gcd(i,j) != 1:
##            continue
##        mx.append(i)
##        my.append(j)
##        t1 = time.time()
##        modular_inverse(i,j)
##        t2 = time.time()
##        mz.append(t2-t1)
##
##for i in range(len(mz)):
##    if mz[i] > 0.0000035:
##        mz[i] = 0.0000035
##
##plt.scatter(mx, my, c=mz, s=2, cmap='viridis')
##plt.xlabel("value of x in mod_inverse(x,m)")
##plt.ylabel("value of m in mod_inverse(x,m)")
##plt.title("Modular Inverse Analysis")
##plt.show()
##        


def gcdExtended(a, b, x=1, y=1): 
    # Base Case 
    if a == 0 :  
        x = 0
        y = 1
        return b 
          
    x1 = 1
    y1 = 1 # To store results of recursive call 
    gcd = gcdExtended(b%a, a, x1, y1) 
  
    # Update x and y using results of recursive 
    # call 
    x = y1 - (b/a) * x1 
    y = x1 
  
    return gcd




fib = [0,1]

while fib[-1] <= 500:
    fib.append(fib[-1]+fib[-2])

print(fib)

def isFib(x,y):
    x,y = min(x,y),max(x,y)

    if x in fib and y in fib:
        if fib.index(y)-1 == fib.index(x):
            return True
        else:
            return False

rrr=[0 for i in range(250000)]



for i in range(1,50):
    a = []
    b = []
    z = []
    print("Iteration:",i)
    for x in range(0,500,):
        for y in range(0,500):
            t1 = time.time()
            gcdExtended(x,y)
            t2 = time.time()
            a.append(x)
            b.append(y)
            z.append(t2-t1)
    rrr = [a+b for a,b in zip(z,rrr)]

z = [i/50 for i in rrr]

for i in range(len(z)):
    if z[i] > 0.000003:
        z[i] = 0.000003
print(len(z))      
plt.scatter(a, b, c=z, s=2, cmap='viridis')
plt.title("Analysis of Extended Euclid Algorithm gcd(a,b)")
plt.xlabel("value of a (in gcd(a,b))")
plt.ylabel("value of b (in gcd(a,b))")
#plt.plot(z)

phi = (math.sqrt(5) + 1) / 2
x = []
y = []
z = []
for i in range(500):
    for j in range(500):
        if isFib(i,j):
            x.append(i)
            y.append(j)
            z.append(100)




l1  = []
xl1 = []
for i in range(500):
 if phi*i <= 500:
     xl1.append(i)
     l1.append(phi*i)

l2  = []
xl2 = []
for i in range(500):
 if (1/phi)*i <= 500:
     xl2.append(i)
     l2.append((1/phi)*i)

phi = (math.sqrt(5) + 1) / 2
plt.plot(xl1,l1,color="red")
plt.plot(xl2,l2,color="red")
plt.scatter(x,y,c=z,s=10,cmap="viridis")


plt.show()
        
        
        

##if __name__ == "__main__":
##
##    xres = []
##    res = []
##
##    al = [103,1009,10007,100003,1000003]
##    for a in al:
##        y = []
##        x = []
##        for m in range(500, pow(10,617),333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333331):
##            if math.gcd(a,m) != 1:
##                continue
##
##            x.append(m)
##
##            t1 = time.time()
##            ans = modular_inverse(a,m)
##            t2 = time.time()
##
##            y.append(t2-t1)
##
##        y = [i*pow(10,6) for i in y]
##        plt.plot([c//pow(10,500) for c in x],y)
##
##    plt.plot([100])
##    plt.ylabel("Time Taken to generate inverse in microseconds")
##    plt.legend(['a=103','a=1009','a=10007','a=100003','a=1000003'])
##    plt.show()
    
    
            
