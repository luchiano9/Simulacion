import numpy as np
import matplotlib.pyplot as plt

INFINITE = 10**50 # Simular numero arbitrariamente grande para este caso

class ModeloInventario:
    def __init__(self, corridas):
        self.amountOfMonths = 120 # Meses de la simulacion
        self.meanInterDemands = 0.1 # Promedio en meses del tiempo entre demandas
        self.maximumDemandsSize = 4 # Tamaño maximo de las demandas 1,2,3,4
        self.setupCost = 32 # Costo inicial de una orden
        self.incrementalCost = 3 # Costo extra por item ordenado
        self.deliveryLagMinimum = 0.5 # Tiempo minimo para una entrega
        self.deliveryLagMaximum = 1 # Tiempo maximo para una entrega
        self.initialInventorylevel = 60 # Valor inicial de stock en inventario
        self.holdingCost = 1 # Costo mensual por item en inventario $
        self.shortageCost = 5 # Costo mensual de tener un producto en el backlog sin stock $
        self.policyMinimumAmount = [20,20,20,20,40,40,40,60,60]
        self.policyMaximumAmount = [40,60,80,100,60,80,100,80,100]
        self.amountEvents = 4 # Arrival / Demand / End of Simulation / Inventory evaluation
        self.demandSizeProbabilities = [1/6, 0.5, 5/6, 1]
        self.corridas = corridas
        self.main()

    def initializationRoutine(self, minPol, maxPol):
        self.clock = 0
        self.inventorylevel = self.initialInventorylevel
        self.orderCosts = 0
        self.areaHolding = 0
        self.areaShortage = 0
        self.amountOfProductsNeeded = 0
        self.minimumPolicy = minPol
        self.maximumPolicy = maxPol

        self.lastEventTime = 0
        self.nextEventType = 0 
        self.nextEventTime = [0] * self.amountEvents
        self.nextEventTime[0] = INFINITE   # Next Order Arrival
        self.nextEventTime[1] = self.clock + np.random.exponential(self.meanInterDemands)
        self.nextEventTime[2] = self.amountOfMonths
        self.nextEventTime[3] = 0
        
    def initializeTotalEstadistics(self):
        self.totalAverageOrdersCost = []
        self.totalAverageHoldingsCost = []
        self.totalAverageShortageCost = []
        self.totalTotalCost = []

    def timingRoutine(self):
        self.clock = min(self.nextEventTime)
        self.nextEventType = np.argmin(self.nextEventTime)

    def timeAndAverageStadistics(self):
        # Calcula el tiempo desde el último evento y actualiza el marcador del ultimo evento
        self.timeSincelastEvent = self.clock - self.lastEventTime
        self.lastEventTime = self.clock

        if self.inventorylevel < 0:
            # Actualiza el area debajo de la función de productos en Shortage
            self.areaShortage -= self.inventorylevel * self.timeSincelastEvent
        elif self.inventorylevel > 0:
            # Actualiza el area debajo de la función de productos en Shortage
            self.areaHolding += self.inventorylevel * self.timeSincelastEvent

    def arrival(self):
        self.inventorylevel += self.amountOfProductsNeeded
        self.nextEventTime[0] = INFINITE

    def demand(self):
        self.currentDemandAmount = self.getDemandAmount()
        self.inventorylevel -= self.currentDemandAmount
        self.nextEventTime[1] = self.clock + np.random.exponential(self.meanInterDemands)

    def getDemandAmount(self):
        amount = 1
        num = np.random.uniform(0,1)
        for i in range(self.maximumDemandsSize-1):
            if num > self.demandSizeProbabilities[i]:
                amount += 1
        return amount

    def inventoryEvaluation(self, invMin, invMax):
        if self.inventorylevel < invMin:
            self.amountOfProductsNeeded = invMax - self.inventorylevel
            self.orderCosts += self.setupCost + self.incrementalCost * self.amountOfProductsNeeded
            self.nextEventTime[0] = self.clock + self.getNextArrivalTime()
        self.nextEventTime[3] = self.clock + 1

    def getNextArrivalTime(self):
        return (np.random.uniform(self.deliveryLagMinimum,self.deliveryLagMaximum))

    def saveRunData(self):
        runAverageOrdersCost = self.orderCosts/self.amountOfMonths
        runAverageHoldingsCost = self.holdingCost * self.areaHolding /self.amountOfMonths
        runAverageShortageCost = self.shortageCost * self.areaShortage /self.amountOfMonths
        totalCostThisRun = runAverageOrdersCost + runAverageHoldingsCost + runAverageShortageCost
        self.totalAverageOrdersCost.append(runAverageOrdersCost)
        self.totalAverageHoldingsCost.append(runAverageHoldingsCost)
        self.totalAverageShortageCost.append(runAverageShortageCost)
        self.totalTotalCost.append(totalCostThisRun)

    def reportDefaultData(self):
        print(f"Nivel inicial de inventario:            {self.initialInventorylevel}")
        print(f"Tamaño maximo de la demanda:            {self.maximumDemandsSize}")
        print(f"Funcion de distribucion de demandas:    {self.demandSizeProbabilities}")
        print(f"Tiempo medio entre demanda:             {self.meanInterDemands}")
        print(f"Tiempo de entrega: entre                {self.deliveryLagMinimum} y {self.deliveryLagMaximum} meses")
        print(f"Duracion de la simulacion:              {self.amountOfMonths} meses")
        print(f"K = {self.setupCost}  i = {self.incrementalCost}  h = {self.holdingCost}  PI = {self.shortageCost}")
        print(f"Estrategia:  |  Costo Total Mensual:  |  Costo Pedido Mensual:  |  Costo Mantenimiento Mensual: |  Costo Faltantes Mensual  | (Todos son promedios)")

    def reportFinalData(self):
        averageOrdersCost = np.mean(self.totalAverageOrdersCost)
        averageHoldingsCost = np.mean(self.totalAverageHoldingsCost)
        averageShortageCost = np.mean(self.totalAverageShortageCost)
        total = np.mean(self.totalTotalCost)
        print(f"[{self.minimumPolicy},{self.maximumPolicy}] \t {round(total,2)} \t\t\t {round(averageOrdersCost,2)} \t\t\t\t {round(averageHoldingsCost,2)} \t\t\t\t {round(averageShortageCost,2)}")
        
        self.plot(self.totalAverageOrdersCost, "Costo de Orden Promedio", "Dinero ($)",
        self.totalAverageHoldingsCost, "Costo de Almacenamiento Promedio", "Dinero ($)",
        self.totalAverageShortageCost, "Costo de Faltante Promedio", "Dinero ($)",
        self.totalTotalCost, "Costo Total Promedio", "Dinero ($)",
        f"Minimo Estrategia: {self.minimumPolicy}  Maximo Estrategia: {self.maximumPolicy}"
        )

    def plot(self, a1, t1, l1, a2, t2, l2, a3, t3, l3, a4, t4, l4, titulo):
        fig, axs = plt.subplots(2, 2, constrained_layout=True)
        axs[0, 0].set_title(t1)
        axs[0, 0].set_xlabel("Cantidad de Corridas")
        axs[0, 0].set_ylabel(l1)
        axs[0, 0].grid(True)
        axs[0, 0].plot(a1)

        axs[1, 0].set_title(t2)
        axs[1, 0].set_xlabel("Cantidad de Corridas")
        axs[1, 0].set_ylabel(l2)
        axs[1, 0].grid(True)
        axs[1, 0].plot(a2)

        axs[0, 1].set_title(t3)
        axs[0, 1].set_xlabel("Cantidad de Corridas")
        axs[0, 1].set_ylabel(l3)
        axs[0, 1].grid(True)
        axs[0, 1].plot(a3)

        axs[1, 1].set_title(t4)
        axs[1, 1].set_xlabel("Cantidad de Corridas")
        axs[1, 1].set_ylabel(l4)
        axs[1, 1].grid(True)
        axs[1, 1].plot(a4)

        fig.suptitle(titulo)
        plt.savefig(f'GraficosInv/tableroInv-min-{self.minimumPolicy}-max-{self.maximumPolicy}.png')
        #plt.show()

    def main(self):
        self.reportDefaultData()
        for i in range(len(self.policyMinimumAmount)):
            self.initializeTotalEstadistics()
            for _ in range(self.corridas):
                self.initializationRoutine(self.policyMinimumAmount[i], self.policyMaximumAmount[i])
                while (self.nextEventType != 2):
                    self.timingRoutine()
                    self.timeAndAverageStadistics()
                    if (self.nextEventType == 0):
                        self.arrival()
                    elif (self.nextEventType == 1):
                        self.demand()
                    elif (self.nextEventType == 2):
                        self.saveRunData()
                    elif (self.nextEventType == 3):
                        self.inventoryEvaluation(self.policyMinimumAmount[i],self.policyMaximumAmount[i])
            self.reportFinalData()

ModeloInventario(100)