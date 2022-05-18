import random
import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.stats import norm
import scipy.stats 

def uniforme (a,b):
    x=[]
    for _ in range(1000):
        r = round(random.random(), 4)
        x.append(a+(b-a)*r)
    return x
uni=uniforme(1,3)

def TestChiCuadUni(nums):
    print("Test de bondad Chi Cuadrado para distribucion uniforme")
    observado=[]
    esperado=100
    c=1.2
    chiquadesperado = round(scipy.stats.chi2.ppf(1-0.05, 9), 2)
    for _ in range (10):
        x =0
        for num in nums:
            if  (c-0.2) <= float(num) <= c : x+=1
        observado.append(x)
        c+=0.2
    x2 = 0
    for obs in observado:
        x2 += (((obs-esperado)**2)/esperado)
    
    print(f"Valor de X2 obtenido = {str(x2)}")
    if (x2 < chiquadesperado): print(f"Valor obtenido: {str(x2)} menor que {str(chiquadesperado)} ,por lo tanto Paso el test")
    else: print("No paso el test")

def exponencial(media):
    x = []
    for _ in range(1000):
        r = random.random()
        x += [-media*(np.log(r))]
    return x
expo=exponencial(5)

def TestChiCuadExp(nums):
    print("Test de bondad Chi Cuadrado para distribucion exponencial:")
    observado=[]
    esperado=[]
    c=0.3
    chiquadesperado = round(scipy.stats.chi2.ppf(1-0.05, 9), 2)
    for _ in range (9):
        x =0
        for num in nums:
            if  (c-0.3) <= float(num) <= c : x+=1
        observado.append(x)
        esperado.append(1000*((1-(math.e)**(-(1/5)*c))-(1-(math.e)**(-(1/5)*(c-0.3)))))
        c+=0.3
    observado.append(1000-sum(observado))
    esperado.append(1000*((math.e)**(-(1/5)*(c-0.3))))
    x2=0
    for i in range(len(observado)):
        x2 += (((observado[i]-esperado[i])**2)/esperado[i])

    print(f"Valor de X2 obtenido = {str(x2)}")
    if (x2 < chiquadesperado): print(f"Valor obtenido: {str(x2)} menor que {str(chiquadesperado)} ,por lo tanto Paso el test")
    else: print("No paso el test")

def gamma(k,a):
    x=[]
    for _ in range(1, 1000):
        tr=1.0
        for _ in range(1,k):
            r = random.random()
            tr=tr*r
        x.append(-(math.log10(tr))/a)
    return x
gam=gamma(5,20)

def normal(media,desviacion):
    x=[]
    for _ in range(1000):
        sum = 0.0
        for _ in range (12):
            r=random.random()
            sum += r
        x+=[desviacion*(sum-6.0)+media]
    return x
nor=normal(2.35,30)

def TestChiCuadNormal(nums):
    print("Test de bondad Chi Cuadrado para distribucion Normal")
    observado = []
    esperado = []
    a1=0
    a2=0
    chiquadesperado = round(scipy.stats.chi2.ppf(1-0.05, 9), 2)
    c =-80
    for _ in range(10):
        x = 0
        for num in nums:
            if  (c-20) <= float(num) <= c : x+=1
        observado.append(x)
        a1+=(c-10)*x
        a2+=((c-10)**2)*x
        c +=20
    a1=a1/1000
    a2=a2/1000
    desviacion=math.sqrt(a2-a1**2)
    media=a1
    c=-80
    esperado=[]
    for i in range(10):
        esperado.append(1000*(norm.cdf((c-media)/desviacion)-norm.cdf(((c-20)-media)/desviacion)))
        c+=20
    x2 = 0
    for i in range(len(observado)):
        x2 += (((observado[i]-esperado[i])**2)/esperado[i])
        
    print(f"Valor de X2 obtenido = {str(x2)}")
    if (x2 < chiquadesperado): print(f"Valor obtenido: {str(x2)} menor que {str(chiquadesperado)} ,por lo tanto Paso el test")
    else: print("No paso el test")

def pascal(k,q):
    nx = []
    for _ in range(1000):
        tr = 1
        qr = math.log10(q)
        for _ in range(k):
            r = random.random()
            tr *= r
        x = int(math.log10(tr)//qr)
        nx.append(x)
    return nx
pas=pascal(5,0.4)

def binomial (n,p):
    x=[]
    for _ in range(1000):
        y=0.0
        for _ in range(1,n):
            r = random.random()
            if (r-p) <0:
                y+=1.0
        x.append(y)
    return x
bino=binomial(1000,0.4)

def TestChiCuadBinomial(nums):
    print("Test de bondad Chi Cuadrado para distribucion Binomial")
    observado = []
    esperado = []
    X=scipy.stats.binom(1000,0.4)
    c =354
    chiquadesperado = round(scipy.stats.chi2.ppf(1-0.05, 9), 2)
    for _ in range(10):
        x = 0
        for num in nums:
            if  (c-14) <= float(num) <= c : x+=1
        observado.append(x)
        total=sum(X.pmf(k) for k in range (c)) - sum(X.pmf(m) for m in range (c-14))
        esperado.append(1000*total)
        c +=14   
    x2 = 0
    for i in range(len(observado)):
        x2 += (((observado[i]-esperado[i])**2)/esperado[i])

    print(f"Valor de X2 obtenido = {str(x2)}")
    if (x2 < chiquadesperado): print(f"Valor obtenido: {str(x2)} menor que {str(chiquadesperado)} ,por lo tanto Paso el test")
    else: print("No paso el test")

def hipergeometrica(tn,ns,p):
    x=[]
    for _ in range(1000):
        tn1=tn
        ns1=ns
        p1=p
        y=0.0
        for _ in range(1, ns1):
            r = random.random()
            if(r-p1) > 0:
                s=0.0
            else:
                s=1.0
                y+=1.0
            p1 = (tn1*p1-s)/(tn1-1.0)
            tn1 -= 1.0
        x.append(y)
    return x
hipergeo=hipergeometrica(5000000,500,0.4)

def poisson (lamb):
    x = []
    for _ in range(1000):
        cont=0
        tr=1
        b=0
        while(tr-b >= 0):
            b = math.exp(-lamb)
            r = random.random()
            tr=tr*r
            if(tr-b >= 0):
                cont+=1
        x.append(cont)
    return x
poi=poisson(50)

def TestChiCuadPoisson(nums):
    print("Test de bondad Chi Cuadrado para distribucion Poisson")
    observado = []
    esperado = []
    X=scipy.stats.poisson(50)
    chiquadesperado = round(scipy.stats.chi2.ppf(1-0.05, 9), 2)
    c =26
    for _ in range(10):
        x = 0
        for j in range(len(nums)):
            if (c-6) <= float(nums[j]) < c:
                x += 1
        observado.append(x)
        total=sum(X.pmf(k) for k in range (c)) -sum(X.pmf(m) for m in range (c-6))
        esperado.append(1000*total)
        c +=6 
    x2 = 0
    for i in range(len(observado)):
        x2 += (((observado[i]-esperado[i])**2)/esperado[i])

    print(f"Valor de X2 obtenido = {str(x2)}")
    if (x2 < chiquadesperado): print(f"Valor obtenido: {str(x2)} menor que {str(chiquadesperado)} ,por lo tanto Paso el test")
    else: print("No paso el test")

def empirica():
    x=[]
    p=[0.273,0.037,0.195,0.009,0.124,0.058,0.062,0.151,0.047,0.044]
    for _ in range(1000):
        r=random.random()
        a=0
        z=1
        for j in p:
            a+=j
            if (r<=a):
                break
            else:
                z+=1
        x.append(z)
    return x
empi=empirica()

def TestChiCuadEmpirica(nums):
    print("Test de bondad Chi Cuadrado para distribucion Empirica")
    observado = []
    esperado = []
    chiquadesperado = round(scipy.stats.chi2.ppf(1-0.05, 9),2)
    p = [0.273, 0.037, 0.195, 0.009, 0.124, 0.058, 0.062, 0.151, 0.047, 0.044]
    for i in range(10):
        x = 0
        for num in nums:
            if num==i+1:
                x += 1
        observado.append(x)
        esperado.append(1000 * p[i]) 
    x2 = 0
    for i in range(len(observado)):
        x1 = (((observado[i]-esperado[i])**2)/esperado[i])
        x2 += x1

    print(f"Valor de X2 obtenido = {str(x2)}")
    if (x2 < chiquadesperado): print(f"Valor obtenido: {str(x2)} menor que {str(chiquadesperado)} ,por lo tanto Paso el test")
    else: print("No paso el test")

# GRÁFICOS
def graficar(uni, expo, gam, nor, pas, bino, hipergeo, poi, empi):
    plt.figure(1)
    plt.title("uniforme")
    plt.hist(uni, alpha=.7, edgecolor="black")
    plt.savefig("Uniforme3.png")
    plt.show()

    plt.figure(2)
    plt.title("exponencial")
    plt.hist(expo, 25, alpha=.7, color='g', edgecolor="black")
    plt.savefig("Exponencial3.png")
    plt.show()

    plt.figure(3)
    plt.title("gamma")
    plt.hist(gam,25, alpha=.7, color='r', edgecolor="black")
    plt.savefig("Gamma3.png")
    plt.show()

    plt.figure(4)
    plt.title("normal")
    plt.hist(nor, 25, alpha=.7, color='y', edgecolor="black")
    plt.savefig("Normal3.png")
    plt.show()

    plt.figure(5)
    plt.title("pascal")
    plt.hist(pas, alpha=.7, edgecolor="black", color='cyan')
    plt.savefig("Pascal3.png")
    plt.show()

    plt.figure(6)
    plt.title("binomial")
    plt.hist(bino, 25, alpha=.7, edgecolor="cyan", color='black')
    plt.savefig("Binomial3.png")
    plt.show()

    plt.figure(7)
    plt.title("hipergeometrica")
    plt.hist(hipergeo, 25, alpha=.7, edgecolor="black", color='chocolate')
    plt.savefig("HiperGeometrica3.png")
    plt.show()

    plt.figure(8)
    plt.title("poisson")
    plt.hist(poi, 25, alpha=.7, edgecolor="black", color='orange')
    plt.savefig("Poisson3.png")
    plt.show()

    plt.figure(9)
    plt.title("empirica")
    plt.hist(empi,color='violet', alpha=.7, edgecolor="black",)
    plt.savefig("Empirica3.png")
    plt.show()
 
#graficar(uni, expo, gam, nor, pas, bino, hipergeo, poi, empi)
# TestChiCuadUni(uni)
# print()
# TestChiCuadExp(expo)
# print()
# TestChiCuadNormal(nor)
# print()
# TestChiCuadBinomial(bino)
# print()
#TestChiCuadPoisson(poi)
# print()
TestChiCuadEmpirica(empi)