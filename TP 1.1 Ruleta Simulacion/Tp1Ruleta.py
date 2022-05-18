import random
import numpy as np
import matplotlib.pyplot as plt

"""
Integrantes del grupo:
    -Luciano Vannelli
    -Manuel Bahamonde
"""

class Ruleta:
    def __init__(self,cantTiradas,numAEvaluar):
        self.cantTiradas = cantTiradas
        self.numAEvaluar = numAEvaluar
        self.listaTirada = []
        self.mediaAritLista = []
        self.frecCeroLista = []
        self.desvioLista = []
        self.desvioNumLista= []
        self.varianzaLista = []
        self.varianzaNumLista = []
        self.medianaLista = []

    def GirarRuleta(self):
        cantNumero = 0
        for _ in range(self.cantTiradas):
            self.listaTirada.append(random.randint(0,36))
            self.mediaAritLista.append(np.mean(self.listaTirada))
            self.medianaLista.append(np.median(self.listaTirada))
            self.desvioLista.append(np.std(self.listaTirada))
            self.desvioNumLista.append(abs(self.numAEvaluar - np.mean(self.listaTirada)))
            self.varianzaLista.append(np.var(self.listaTirada))
            self.varianzaNumLista.append(abs(self.numAEvaluar - np.mean(self.listaTirada)) ** 2)
            if self.listaTirada[-1] == self.numAEvaluar:
                cantNumero += 1
            self.frecCeroLista.append(cantNumero/len(self.listaTirada))
        self.MostrarResultados()

    def RuletaMultiple(self):
        self.MultiplesTiradas()
        self.MultiplesFrecTotales()
        self.MultiplesMedias()
        self.MultiplesMedianas()
        self.MultiplesDesvios()
        self.MultiplesVarianzas()
        self.MultiplesFrecRel()
        self.MultiplesDesviosNum()
        self.MultiplesVarianzasNum()
    
    def MostrarResultados(self):
        self.MostrarTiradas()
        self.MostrarFrecTotales()
        self.MostrarMedia()
        self.MostrarMediana()
        self.MostrarDesvio()
        self.MostrarVarianza()
        self.MostrarFrecRel()
        self.MostrarDesvioNum()
        self.MostrarVarianzaNum()

    def MostrarTiradas(self):
        plt.scatter(range(self.cantTiradas),self.listaTirada, s=3)
        plt.title("Valores de cada repeticion")
        plt.xlabel("n (número de tiradas)")
        plt.ylabel("Resultado")
        plt.show()

    def MultiplesTiradas(self):
        for _ in range(10):
            thisList = []
            for _ in range(self.cantTiradas):
                thisList.append(random.randint(0,36))
            plt.scatter(range(self.cantTiradas),thisList, s=3)
        plt.title("Valores de cada repeticion en 10 réplicas")
        plt.xlabel("n (número de tiradas)")
        plt.ylabel("Resultado")
        plt.show()
    
    def MostrarFrecTotales(self):
        plt.hist(self.listaTirada, bins=37, edgecolor="black", color="skyblue")
        plt.title("Histograma de los valores")
        plt.xlabel("Valor")
        plt.ylabel("Frecuencia absoluta")
        plt.show()
    
    def MultiplesFrecTotales(self):
        for _ in range(10):
            thisList = []
            for _ in range(self.cantTiradas):
                thisList.append(random.randint(0,36))
            plt.hist(thisList, bins=37, edgecolor="black",alpha=0.4)
        plt.title("Histograma de los valores en 10 réplicas")
        plt.xlabel("Valor")
        plt.ylabel("Frecuencia absoluta")
        plt.show()

    def MostrarMedia(self):
        plt.plot(self.mediaAritLista, label = "Valor Obtenido")
        plt.title("Valor promedio de las tiradas")
        plt.xlabel("n (número de tiradas)")
        plt.ylabel("vp (valor promedio de las tiradas)")
        MediaEsperada = [18] * self.cantTiradas
        plt.plot(MediaEsperada, label = "Valor Esperado", lineStyle="--")
        plt.legend(loc = "upper left")  
        plt.grid(True)
        plt.show()
    
    def MultiplesMedias(self):
        for _ in range(10):
            thisList = []
            mediaList = []
            for _ in range(self.cantTiradas):
                thisList.append(random.randint(0,36))
                mediaList.append(np.mean(thisList))
            plt.plot(mediaList)
        plt.title("Valor promedio de las tiradas en 10 réplicas")
        plt.xlabel("n (número de tiradas)")
        plt.ylabel("vp (valor promedio de las tiradas)")
        MediaEsperada = [18] * self.cantTiradas
        plt.plot(MediaEsperada, label = "Valor Esperado", lineStyle="--")
        plt.legend(loc = "upper left")  
        plt.grid(True)
        plt.show()

    def MostrarFrecRel(self):
        plt.plot(self.frecCeroLista, label = "Valor Obtenido")
        plt.title(f"Frecuencia relativa del número {self.numAEvaluar}")
        plt.xlabel("n (número de tiradas)")
        plt.ylabel("fr (frecuencia relativa)")
        FrecEsperada = [0.02702702702] * self.cantTiradas
        plt.plot(FrecEsperada, label = "Valor Esperado", lineStyle="--")
        plt.legend(loc = "upper left")  
        plt.grid(True)
        plt.show()

    def MultiplesFrecRel(self):
        for _ in range(10):
            thisList = []
            frecRelList = []
            cantNumero = 0
            for _ in range(self.cantTiradas):
                thisList.append(random.randint(0,36))
                if thisList[-1] == self.numAEvaluar:
                    cantNumero += 1
                frecRelList.append(cantNumero/len(thisList))
            plt.plot(frecRelList)
        plt.title(f"Frecuencia relativa del número {self.numAEvaluar} en 10 réplicas")
        plt.xlabel("n (número de tiradas)")
        plt.ylabel("fr (frecuencia relativa)")
        FrecEsperada = [0.02702702702] * self.cantTiradas
        plt.plot(FrecEsperada, label = "Valor Esperado", lineStyle="--")
        plt.legend(loc = "upper left")  
        plt.grid(True)
        plt.show()

    def MostrarDesvio(self):
        plt.plot(self.desvioLista, label = "Valor Obtenido")
        plt.title("Valor del desvío")
        plt.xlabel("n (número de tiradas)")
        plt.ylabel("vd (valor del desvío)")
        DesvEsperado = [10.68] * self.cantTiradas
        plt.plot(DesvEsperado, label = "Valor Esperado", lineStyle="--")
        plt.legend(loc = "upper left")  
        plt.grid(True)
        plt.show()    

    def MultiplesDesvios(self):
        for _ in range(10):
            thisList = []
            desviosList = []
            for _ in range(self.cantTiradas):
                thisList.append(random.randint(0,36))
                desviosList.append(np.std(thisList))
            plt.plot(desviosList)
        plt.title("Valor del desvío en 10 réplicas")
        plt.xlabel("n (número de tiradas)")
        plt.ylabel("vd (valor del desvío)")
        DesvEsperado = [10.68] * self.cantTiradas
        plt.plot(DesvEsperado, label = "Valor Esperado", lineStyle="--")
        plt.legend(loc = "upper left")  
        plt.grid(True)
        plt.show()

    def MostrarDesvioNum(self):
        plt.plot(self.desvioNumLista, label = "Valor Obtenido")
        plt.title(f"Valor del Desvio del número {self.numAEvaluar}")
        plt.xlabel("n (número de tiradas)")
        plt.ylabel("vd (valor del desvío)")
        DesvEsperado = [abs(self.numAEvaluar - 18)] * self.cantTiradas
        plt.plot(DesvEsperado, label = "Valor Esperado", lineStyle="--")
        plt.legend(loc = "upper left")  
        plt.grid(True)
        plt.show()

    def MultiplesDesviosNum(self):
        for _ in range(10):
            thisList = []
            desviosNumList = []
            for _ in range(self.cantTiradas):
                thisList.append(random.randint(0,36))
                desviosNumList.append(abs(self.numAEvaluar - np.mean(thisList)))
            plt.plot(desviosNumList)
        plt.title(f"Valor del Desvio del número {self.numAEvaluar} en 10 réplicas")
        plt.xlabel("n (número de tiradas)")
        plt.ylabel("vd (valor del desvío)")
        DesvEsperado = [abs(self.numAEvaluar - 18)] * self.cantTiradas
        plt.plot(DesvEsperado, label = "Valor Esperado", lineStyle="--")
        plt.legend(loc = "upper left")  
        plt.grid(True)
        plt.show()

    def MostrarVarianza(self):
        plt.plot(self.varianzaLista, label = "Valor Obtenido")
        plt.title("Valor de la varianza")
        plt.xlabel("n (número de tiradas)")
        plt.ylabel("vv (valor de la varianza)")
        VarianzaEsperada = [10.68 ** 2] * self.cantTiradas
        plt.plot(VarianzaEsperada, label = "Valor Esperado", lineStyle="--")
        plt.legend(loc = "upper left")  
        plt.grid(True)
        plt.show() 

    def MultiplesVarianzas(self):
        for _ in range(10):
            thisList = []
            varianzasList = []
            for _ in range(self.cantTiradas):
                thisList.append(random.randint(0,36))
                varianzasList.append(np.var(thisList))
            plt.plot(varianzasList)
        plt.title("Valor de la varianza en 10 réplicas")
        plt.xlabel("n (número de tiradas)")
        plt.ylabel("vv (valor de la varianza)")
        VarianzaEsperada = [10.68 ** 2] * self.cantTiradas
        plt.plot(VarianzaEsperada, label = "Valor Esperado", lineStyle="--")
        plt.legend(loc = "upper left")  
        plt.grid(True)
        plt.show()

    def MostrarVarianzaNum(self):
        plt.plot(self.varianzaNumLista, label = "Valor Obtenido")
        plt.title(f"Valor de la Varianza del número {self.numAEvaluar}")
        plt.xlabel("n (número de tiradas)")
        plt.ylabel("vv (valor de la varianza)")
        VarianzaEsperada = [(abs(self.numAEvaluar - 18))** 2] * self.cantTiradas
        plt.plot(VarianzaEsperada, label = "Valor Esperado", lineStyle="--")
        plt.legend(loc = "upper left")  
        plt.grid(True)
        plt.show()

    def MultiplesVarianzasNum(self):
        for _ in range(10):
            thisList = []
            varianzasNumList = []
            for _ in range(self.cantTiradas):
                thisList.append(random.randint(0,36))
                varianzasNumList.append(abs(self.numAEvaluar - np.mean(thisList)) ** 2)
            plt.plot(varianzasNumList)
        plt.title(f"Valor de la Varianza del número {self.numAEvaluar} en 10 réplicas")
        plt.xlabel("n (número de tiradas)")
        plt.ylabel("vv (valor de la varianza)")
        VarianzaEsperada = [(abs(self.numAEvaluar - 18))** 2] * self.cantTiradas
        plt.plot(VarianzaEsperada, label = "Valor Esperado", lineStyle="--")
        plt.legend(loc = "upper left")  
        plt.grid(True)
        plt.show()

    def MostrarMediana(self):
        plt.plot(self.medianaLista, label = "Valor Obtenido")
        plt.title("Valor de la Mediana")
        plt.xlabel("n (número de tiradas)")
        plt.ylabel("vm (valor de la mediana)")
        MedianaEsperada = [18] * self.cantTiradas
        plt.plot(MedianaEsperada, label = "Valor Esperado", lineStyle="--")
        plt.legend(loc = "upper left")  
        plt.grid(True)
        plt.show()
    
    def MultiplesMedianas(self):
        for _ in range(10):
            thisList = []
            medianaList = []
            for _ in range(self.cantTiradas):
                thisList.append(random.randint(0,36))
                medianaList.append(np.median(thisList))
            plt.plot(medianaList)
        plt.title("Valor de la Mediana en 10 réplicas")
        plt.xlabel("n (número de tiradas)")
        plt.ylabel("vm (valor de la mediana)")
        MedianaEsperada = [18] * self.cantTiradas
        plt.plot(MedianaEsperada, label = "Valor Esperado", lineStyle="--")
        plt.legend(loc = "upper left")  
        plt.grid(True)
        plt.show()

def Iniciar():
    cantTiradas = None
    numAEvaluar = None
    print("Bienvenido a la ruleta de 37 números")
    while not ((isinstance(cantTiradas,int)) and (isinstance(numAEvaluar,int) and numAEvaluar>=0 and numAEvaluar<=36)):
        try:
            cantTiradas=int(input("Ingrese cantidad de tiradas a realizar:"))
            numAEvaluar=int(input("Ingrese numero a evaluar (0-36):"))
            if not(numAEvaluar>=0 and numAEvaluar<=36):
                raise Exception()
        except ValueError:
            print("No ingresó un numero entero, intente nuevamente")
        except:
            print("El numero a evaluar debe estar entre 0 y 36")

    ruleta = Ruleta(cantTiradas,numAEvaluar)
    
    ruleta.GirarRuleta()
    ruleta.RuletaMultiple()

Iniciar()



